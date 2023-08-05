# -*-coding:utf-8-*-
import logging
import regex
import fitz
import time
import itertools

from collections import defaultdict
from itertools import chain
from pdfminer.converter import PDFPageAggregator
from multiprocessing import Pool
from decimal import Decimal
from math import ceil
from PyPDF3 import PdfFileReader
from pdfplumber.page import Page
#from pdfminer import settings
from pdfplumber import PDF
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfplumber.utils import DEFAULT_X_TOLERANCE, DEFAULT_Y_TOLERANCE, cluster_objects, itemgetter, \
    line_to_edge, resolve_and_decode
from pdfminer.pdfpage import PDFPage, dict_value, PDFObjectNotFound, LITERAL_PAGES, LITERAL_PAGE, list_value
from pdfminer.pdfinterp import PDFPageInterpreter, PDFContentParser, PDFInterpreterError
from pdfplumber.table import TableFinder, Table, DEFAULT_TABLE_SETTINGS, edges_to_intersections, \
    intersections_to_cells, cells_to_tables, Row
from pdfminer.psparser import PSEOF, PSKeyword, keyword_name
from cache_file_view.bsjc_import_conf import process_num, part_page_num
from cache_file_view.bsjc_import_utils import rect_area, bbox_to_str

logger = logging.getLogger(__file__)


class MyPDFPage(PDFPage):
    @classmethod
    def create_pages(cls, document, start, end):
        def search(obj, parent):
            if isinstance(obj, int):
                objid = obj
                tree = dict_value(document.getobj(objid)).copy()
            else:
                objid = obj.objid
                tree = dict_value(obj).copy()
            for (k, v) in parent.items():
                if k in cls.INHERITABLE_ATTRS and k not in tree:
                    tree[k] = v

            tree_type = tree.get('Type')
            #if tree_type is None and not settings.STRICT:  # See #64
            #    tree_type = tree.get('type')

            if tree_type is LITERAL_PAGES and 'Kids' in tree:
                #log.info('Pages: Kids=%r', tree['Kids'])
                for c in list_value(tree['Kids']):
                    yield from search(c, tree)
            elif tree_type is LITERAL_PAGE:
                #log.info('Page: %r', tree)
                yield (objid, tree)
        pages = False
        i = 0
        if 'Pages' in document.catalog:
            objects = search(document.catalog['Pages'], document.catalog)
            for (objid, tree) in objects:
                i += 1
                if i - 1 < start:
                    continue
                yield cls(document, objid, tree)
                pages = True
                if i >= end:
                    break
        if not pages:
            i = 0
            # fallback when /Pages is missing.
            for xref in document.xrefs:
                for objid in xref.get_objids():
                    try:
                        obj = document.getobj(objid)
                        if isinstance(obj, dict) \
                                and obj.get('Type') is LITERAL_PAGE:
                            i += 1
                            if i - 1 < start:
                                continue
                            yield cls(document, objid, obj)
                    except PDFObjectNotFound:
                        pass
                    if i >= end:
                        break
        return


class MyPDF(PDF):
    # 取需要的字段用来入库
    # fields = ('fontname', 'text')
    int_fields = ('x0', 'top', 'width', 'height', 'page_number')
    ceil_fields = ('x1', 'bottom')

    def __init__(self,
                 stream,
                 start=0,
                 end=10000,
                 pages=None,
                 laparams=None,
                 precision=0.001,
                 password="",
                 strict_metadata=False
                 ):
        self.laparams = None if laparams == None else LAParams(**laparams)
        self.stream = stream
        self.pages_to_parse = pages
        # 要取页面的区间,使用这个时上面的self.pages_to_parse失效
        self.start = start
        self.end = end
        self.precision = precision
        self.rsrcmgr = PDFResourceManager()
        self.doc = PDFDocument(PDFParser(stream), password=password)
        self.metadata = {}
        for info in self.doc.info:
            self.metadata.update(info)
        for k, v in self.metadata.items():
            try:
                self.metadata[k] = resolve_and_decode(v)
            except Exception as e:
                if strict_metadata:
                    # Raise an exception since unable to resolve the metadata value.
                    raise
                # This metadata value could not be parsed. Instead of failing the PDF
                # read, treat it as a warning only if `strict_metadata=False`.
                logger.warning(
                    f'[WARNING] Metadata key "{k}" could not be parsed due to '
                    f"exception: {str(e)}"
                )
        # 自定义的pdf总页数
        self.page_len = 0
        # 页眉的原文和数量，满足页眉的判断条件时才加入，最多2个，用于判断页眉是否异常,超过1个就视为异常
        self.page_heads = None

    @property
    def pages(self):
        if hasattr(self, "_pages"):
            return self._pages

        doctop = 0
        self._pages = []
        for i, page in enumerate(MyPDFPage.create_pages(self.doc, self.start, self.end)):
            page_number = self.start + i + 1
            p = PageExt(self, page, page_number=page_number, initial_doctop=doctop)
            self._pages.append(p)
            doctop += p.height
        return self._pages

    # 目录
    @staticmethod
    def outlines(path):
        outlines = []

        def format_outline(v):
            if isinstance(v, list):
                for sub_v in v:
                    format_outline(sub_v)
            else:
                outlines.append({'title': v.title, 'page_number': pdf.getDestinationPageNumber(v) + 1})
        try:
            # 报错 (self[NameObject("/Left")], self[NameObject("/Top")], ValueError: not enough values to unpack (expected 3, got 2)
            with open(path, 'rb') as f:
                pdf = PdfFileReader(f)
                for v in pdf.getOutlines():
                    format_outline(v)
        except Exception as e:
            return []

        return outlines

    # 删除页眉
    @staticmethod
    def skip_page_head_foot(pages):
        page_heads = []
        head_cnt = {}

        def add_to_head_cnt(head, page_number):
            if head in head_cnt:
                cur = head_cnt[head]
                if page_number - cur[1] == 1:
                    cur[2] += 1
                    if cur[2] > cur[3]:
                        cur[3] = cur[2]
                cur[1] = page_number
            else:
                head_cnt[head] = [head, page_number, 1, 1]

        page_signs = []
        for page in pages:
            page.page_foot
            if not page.head_n_lines:
                page_signs.append([])
                continue
            tmp = []
            # 第1行 、第1行+第2行 两种页眉都存起来
            head_2 = page.head_n_lines
            add_to_head_cnt(head_2[0], page.page_number)
            tmp.append(head_2[0])
            if len(head_2) > 1:
                head = (head_2[0], head_2[1])
                add_to_head_cnt(head, page.page_number)
                tmp.append(head)
            page_signs.append(tmp)
        if not head_cnt:
            return page_heads
        head_2_final = []
        # 根据下面的条件过滤页眉,对于多个进程交界处并且只有几个值的页眉，可以在主进程额外检查;连续相同2页以上的为页眉
        for item in head_cnt.values():
            if item[3] > 2:
                head_2_final.append((item[0], item[3]))
        single_heads = [x for x in head_2_final if not isinstance(x[0], tuple)]
        multi_heads = [x for x in head_2_final if isinstance(x[0], tuple)]
        for s in single_heads:  # 单行页眉
            for m in multi_heads:  # 双行页眉
                if m[0][0] == s[0]:
                    # 删除双行页眉包含了的单行页眉,每个s只能删除一次，否则可能报错
                    head_2_final.remove(s)
                    break
        for head, cnt in head_2_final:
            if isinstance(head, tuple):  # 双行页眉
                for i, lines in enumerate(page_signs):
                    if len(lines) == 2 and lines[1] == head:
                        pages[i].line_chars.pop(0)
                        pages[i].line_chars.pop(0)
            else:  # 单行页眉
                for i, lines in enumerate(page_signs):
                    if lines and lines[0] == head:
                        pages[i].line_chars.pop(0)
            page_heads.append(head)  # 把当前循环的页眉存入heads
        return page_heads

    @classmethod
    def make_frag_format(cls, fragment, ori_texts, need_chars=True):
        def slim_dic(dic):
            slim = {'text': dic['text']}
            # slim['fontname'] = decode_text(dic['fontname'])
            if isinstance(dic['fontname'], bytes):
                slim['fontname'] = dic['fontname'].decode('gbk')
            else:
                slim['fontname'] = dic['fontname']
            for k in cls.int_fields:
                slim[k] = int(dic[k])
            for k in cls.ceil_fields:
                slim[k] = ceil(dic[k])
            return slim
        dic = {'text': ''.join(map(lambda x: x['text'], fragment)), 'page_number': fragment[0]['page_number']}
        if need_chars:
            dic['chars'] = [slim_dic(char) for char in fragment]
        ori_texts.append(dic)
        return {'text': dic['text'], 'index': len(ori_texts) - 1}

    # 表格文本格式化
    @classmethod
    def table_text_idx(cls, table, result):
        for row in table['table_info']:
            for cell in row:
                if not cell:
                    continue
                for j in range(len(cell['cell'])):
                    if 'index' not in cell['cell'][j]:
                        cell['cell'][j] = cls.make_frag_format(cell['cell'][j], result)

    # 连接被页分开的段
    def concat_fragment_on_pages(self, ori_texts):
        if len(self.pages) == 1:
            return
        for i in range(1, len(self.pages)):
            pre_page = self.pages[i - 1]
            page = self.pages[i]
            # 上一页无文本或者都是短文本
            if pre_page.max_w is None:
                continue
            # 本页无文本
            if not page.fragments:
                continue
            # 上一页无文本
            if not pre_page.fragments:
                continue
            cur_line = page.line_chars[0]
            # 只要有项目编号标记就视为新段
            if 'head' in cur_line[0]:
                continue
            # 本页第一行距离页顶超过150就视为新段
            if cur_line[0]['top'] > 150:
                continue
            # 上一页只有一行且距离底部大于150视为独立的段
            if pre_page.max_w == 1:
                if pre_page.height - pre_page.line_chars[-1][0]['bottom'] > 150:
                    continue
                else:
                    pre_page.max_w = pre_page.line_chars[-1][-1]['x1']
            # 段落编号不连续就认为是独立的段
            if page.fragments[0]['index'] - pre_page.fragments[-1]['index'] != 1:
                continue
            pre_line = pre_page.line_chars[-1]
            # 上一行剩余的位置不足以放下一个字就认为满行了,没满行就把当前行视为新段
            if 2 * pre_line[-1]['x1'] - pre_line[-1]['x0'] <= pre_page.max_w:
                continue
            # 上一行是满行的情况下，当前行默认为段落的一部分，以下都是例外的情况
            # 字高不同
            if pre_line[-1]['height'] != page.line_chars[0][-1]['height']:
                continue
            # 当前行开头在上一行的右面
            if cur_line[0]['x0'] > pre_line[0]['x1']:
                continue
            # 需要合并，把当前页的第一段并到上一页最后一段
            head_frag = page.fragments.pop(0)
            pre_page.fragments[-1]['text'] += head_frag['text']
            ori_texts[head_frag['index'] - 1]['chars'].extend(ori_texts[head_frag['index']]['chars'])
            ori_texts[head_frag['index'] - 1]['text'] += head_frag['text']
            ori_texts[head_frag['index']] = None

    # 把数据组装成单个文件的返回结果
    def get_text_from_pages(self):
        self.skip_page_head_foot(self.pages)
        ori_texts = []
        # fragments和ori_text
        for page in self.pages:
            # 表格以起始高度参与所有的段落排序
            table_signs = []
            for table in page.table_arr:
                table_signs.append(Decimal(table['bbox'][1]))
            if table_signs:
                i = 0
                for idx in range(len(page.fragments)):
                    if i < len(table_signs) and page.fragments[idx][0]['top'] > table_signs[i]:
                        self.table_text_idx(page.table_arr[i], ori_texts)
                        i += 1
                    page.fragments[idx] = self.make_frag_format(page.fragments[idx], ori_texts)
                # 补上页面底部的表格
                if i < len(table_signs):
                    for table in page.table_arr[i:]:
                        self.table_text_idx(table, ori_texts)
            else:
                page._fragments = [self.make_frag_format(v, ori_texts) for v in page.fragments]
        self.concat_fragment_on_pages(ori_texts)
        return ori_texts


class MultipleProcessMyPDF:
    def __init__(self, file_path, pages, ori_texts):
        self.file_path = file_path
        self.pages = pages
        self.ori_texts = ori_texts

    # 多进程无法提供全局index，出来后表格idx加上base
    @staticmethod
    def table_idx_plus(table, base):
        for row in table['table_info']:
            for cell in row:
                if not cell:
                    continue
                for j in range(len(cell['cell'])):
                    if cell['cell'][j]['index'] != -1:
                        cell['cell'][j]['index'] += base

    # 表格和文本的idx
    @classmethod
    def resume_index(cls, pages, base):
        for page in pages:
            for frag in page['fragments']:
                frag['index'] += base
            for table in page['tables']:
                cls.table_idx_plus(table, base)

    # 连接多个进程首尾页的段
    @staticmethod
    def check_concat_fragment_on_pages(pre_page, page):
        if not pre_page:
            return
        pre_lines, pre_sign = pre_page
        cur_lines, cur_sign = page
        if not pre_sign or not cur_sign:
            return
        pre_line = pre_lines[0]
        cur_line = cur_lines[0]
        # 上一行是满行的情况下，当前行默认为段落的一部分，以下都是例外的情况
        # 字高不同
        if pre_line[-1]['height'] != cur_line[-1]['height']:
            return
        # 当前行开头在上一行的右面
        if cur_line[0]['x0'] > pre_line[0]['x1']:
            return
        return True

    @staticmethod
    def concat_fragments(pre_pages, pre_texts, back_pages, back_texts):
        # 需要合并，把当前页的第一段并到上一页最后一段
        head_frag = back_pages[0]['fragments'].pop(0)
        pre_pages[-1]['fragments'][-1]['text'] += head_frag['text']
        pre_texts[-1]['chars'].extend(back_texts[0]['chars'])
        pre_texts[-1]['text'] += back_texts[0]['text']
        back_texts[0] = None

    # 检查首页是否需要与上一页拼接段落
    @staticmethod
    def is_need_top_for_frag(page):
        # 上一页无文本或者都是短文本
        if page.max_w is None:
            return False
        if page.fragments[0]['index'] != 0:
            return False
        pre_line = page.line_chars[-1]
        # 上一页只有一行且距离底部大于150视为独立的段
        if page.max_w == 1:
            if page.height - pre_line[0]['bottom'] > 150:
                return False
            else:
                page.max_w = pre_line[-1]['x1']
        # 上一行剩余的位置不足以放下一个字就认为满行了,没满行就把当前行视为新段
        if 2 * pre_line[-1]['x1'] - pre_line[-1]['x0'] <= page.max_w:
            return False
        return True

    # 检查尾页是否需要与下一页拼接段落
    @staticmethod
    def is_need_bottom_for_frag(page, max_idx):
        # 本页无文本
        if not page.fragments:
            return False
        cur_line = page.line_chars[-1]
        # 只要有项目编号标记就视为新段
        if 'head' in cur_line[0]:
            return False
        # 本页第一行距离页顶超过150就视为新段
        if cur_line[0]['top'] > 150:
            return False
        if page.fragments[-1]['index'] != max_idx:
            return False
        return True

    # 单个子进程，加载一部分页面
    @classmethod
    def sub_init(cls, file_path, start, end, **kwargs):
        fp = open(file_path, "rb")
        inst = MyPDF(fp, start, end, **kwargs)
        inst.close_file = fp.close
        ori_texts = inst.get_text_from_pages()
        # 把第一页和最后一页连接段落需要的内容传出去,首行/尾行，最大行宽，后面/前面无表
        top_page = (inst.pages[0].line_chars[:1], cls.is_need_top_for_frag(inst.pages[0]))
        bottom_page = (inst.pages[-1].line_chars[-1:], cls.is_need_bottom_for_frag(inst.pages[-1], len(ori_texts) - 1))
        return ([page.to_dict() for page in inst.pages], ori_texts, top_page, bottom_page)

    @classmethod
    def read_info(cls, path):
        with fitz.Document(path) as pdf:
            page_len = pdf.page_count
        if page_len > process_num * 3:
            step = page_len // process_num
            intervals = [[step * i, step * (i + 1)] for i in (range(process_num))]
            intervals[-1][1] = page_len
            with Pool(process_num) as pool:
                res = pool.starmap(cls.sub_init, [(path, *v) for v in intervals])
            pages = []
            ori_texts = []
            base = 0
            pre = None
            for v in res:
                if cls.check_concat_fragment_on_pages(pre, v[2]):
                    cls.concat_fragments(pages, ori_texts, v[0], v[1])
                cls.resume_index(v[0], base)
                pages.extend(v[0])
                ori_texts.extend(v[1])
                base = len(ori_texts)
                pre = v[3]
        else:
            pages, ori_texts, _, _ = cls.sub_init(path, 0, page_len)
        res = cls(path, pages, ori_texts)
        # if cat:
        #     outlines = make_outlines(line_text_from_pages(res.pages), cat)
        # else:
        #     outlines = []
        dic = {'pages': res.pages, 'ori_texts': res.ori_texts, 'file_path': path, 'outlines': MyPDF.outlines(path)}
        return dic

    @classmethod
    def split_file(cls, path, process_pool):
        try:
            with fitz.Document(path) as pdf:
                part_num = ceil(pdf.page_count / part_page_num)
                intervals = [i * part_page_num for i in range(part_num)]
                intervals.append(pdf.page_count)
            return [process_pool.apply_async(cls.sub_init, (path, intervals[i], intervals[i + 1]))
                    for i in range(part_num)]
        except Exception as e:
            logger.exception(e)
            return []

    @classmethod
    def merge_parts(cls, res):
        pages = []
        ori_texts = []
        base = 0
        pre = None
        for v in res:
            if cls.check_concat_fragment_on_pages(pre, v[2]):
                cls.concat_fragments(pages, ori_texts, v[0], v[1])
            cls.resume_index(v[0], base)
            pages.extend(v[0])
            ori_texts.extend(v[1])
            base = len(ori_texts)
            pre = v[3]
        # # 去掉多余的字段
        # for page in pages:
        #     page.pop('head_n_lines')
        dic = {'pages': pages, 'ori_texts': ori_texts}
        return dic


class MyPDFPageAggregator(PDFPageAggregator):
    def handle_undefined_char(self, font, cid):
        raise LackCid('lack cid')


class LackCid(Exception):
    pass


class MyPDFPageInterpreter(PDFPageInterpreter):
    def execute(self, streams):
        try:
            parser = PDFContentParser(streams)
        except PSEOF:
            # empty page
            return
        try:
            start = time.time()
            i = 0
            while 1:
                # 如果缺少后面的字或者元素，可能是页上的总数量超过下面的值了
                if i % 3000 == 0 and time.time() - start > 1:
                    self.argstack = []
                    return
                i += 1
                try:
                    (_, obj) = parser.nextobject()
                except PSEOF:
                    break
                if isinstance(obj, PSKeyword):
                    name = keyword_name(obj)
                    method = 'do_%s' % name.replace('*', '_a').replace('"', '_w') \
                        .replace("'", '_q')
                    if hasattr(self, method):
                        func = getattr(self, method)
                        nargs = func.__code__.co_argcount-1
                        if nargs:
                            args = self.pop(nargs)
                            logger.debug('exec: %s %r', name, args)
                            if len(args) == nargs:
                                func(*args)
                        else:
                            logger.debug('exec: %s', name)
                            func()
                    #else:
                    #    if settings.STRICT:
                    #        error_msg = 'Unknown operator: %r' % name
                    #        raise PDFInterpreterError(error_msg)
                else:
                    self.push(obj)
        except Exception as e:
            self.argstack = []
            logger.exception(e)
        return


class PageExt(Page):
    """
    有的标书的页面是整个包含在表格中的，这种不应该视为表格；还有表格界限超出页面的情况；导致不好判断该不该作为表格。
    目前暂不区分表格中的字，只是把字符分为3种：chars:全部字符；_table_chars：表中的字符；_no_table_chars：表外的字符
    现在的_line_chars是直接在chars中取得的
    页面上的坐标系统有两种，y0,y1的原点在左下角，top,bottom的原点在左上角,通常点、线的坐标是左下角原点，框的是左上角原点

    self._d_chars = self.chars 导致pdf.pages比原来的包慢很多，但是在这个任务里，取字是必须的过程，所以不忽略
    """
    # 项目序号的表达式
    project_order = regex.compile(r'[\(（]?[一二三四五六七八九十\d]+[)）、.]')

    # # 第 2 页
    # foot_pattern = r'\s*第?\s*\d+(\s*/\s*\d+)?\s*页?\s*'
    # 1 / 3和11、~ 1 ~
    foot_pattern = regex.compile(r'\d+/\d+|\d+|~\d+~|第\d+页共\d+页')

    def __init__(self, *args, **kwargs):
        super(PageExt, self).__init__(*args, **kwargs)
        # 按行划分的字的列表
        self._line_chars = None
        # pdf从页面上提取的带位置的表格
        self._tables = None
        # 表格内的字
        self._table_chars = None
        # 组合好的表格
        self._table_arr = None
        # 动态的所有字符集，可以删除其中用掉的词,
        self._d_chars = self.chars
        # 按段落汇总的文本
        self._fragments = None
        # 页脚，通常是页码
        self._page_foot = None
        self._head_n_lines = None
        # 最后一行是否分段的标记，[段是否结束：True:结束，False:待定, 当前页的max_w, 最后一行line_chars]
        self.max_w = None

    @property
    def layout(self):
        if hasattr(self, "_layout"):
            return self._layout
        device = MyPDFPageAggregator(
            self.pdf.rsrcmgr,
            pageno=self.page_number,
            laparams=self.pdf.laparams,
        )
        interpreter = MyPDFPageInterpreter(self.pdf.rsrcmgr, device)
        interpreter.process_page(self.page_obj)
        self._layout = device.get_result()
        return self._layout

    # 把curves中的线也加入计算
    @property
    def edges(self):
        if hasattr(self, "_edges"):
            return self._edges
        line_edges = list(map(line_to_edge, chain(self.lines, self.curves)))
        self._edges = self.rect_edges + line_edges
        return self._edges

    # 把传入的字符分行并排序
    @staticmethod
    def make_line(chars):
        # 修改高度完全被前面的字包含的小字的bottom，使后面分行的时候分到同一行
        cur = [chars[0]['bottom'], chars[0]['top']]
        doc_top = chars[0]['bottom']
        for char in chars:
            if char['bottom'] < cur[0] and char['top'] > cur[1]:
                char['bottom'] = doc_top
            else:
                cur = [char['bottom'], char['top']]
                doc_top = char['bottom']
        lines = [sorted(line, key=itemgetter("x0")) for line in cluster_objects(chars, "bottom", DEFAULT_Y_TOLERANCE)]

        # 删除行右侧的空格
        def remove_r_space(line):
            while line and (not line[-1]['text'] or line[-1]['text'].isspace()):
                line.pop()
            return line

        lines = map(remove_r_space, lines)
        return [line for line in lines if line]

    @property
    def line_chars(self):
        if self._line_chars is None:
            if not self._d_chars:
                self._line_chars = []
                return self._line_chars
            # 先提取表格中的内容
            self.table_arr
            if not self._d_chars:
                self._line_chars = []
                return self._line_chars
            # 文本中可以删除全是空格的行
            self._line_chars = []
            for line in self.make_line(self._d_chars):
                for i in range(len(line)):
                    if not line[i]['text'].isspace():
                        # 在项目编号开头的行首做标记，用于分段
                        text = ''.join(map(lambda x: x['text'], line[i:i + 6]))
                        if self.project_order.match(text):
                            line[0]['head'] = True
                        self._line_chars.append(line)
                        break

        return self._line_chars

    @property
    def head_n_lines(self):
        if self._head_n_lines is not None:
            return self._head_n_lines
        n = 2
        if not self.tables:
            self._head_n_lines = [''.join(map(lambda x: x['text'], line)).strip() for line in self.line_chars[:n]]
            return self._head_n_lines
        limit = self.tables[0].bbox[1]
        self._head_n_lines = [''.join(map(lambda x: x['text'], line)).strip()
                              for line in self.line_chars[:n] if line[0]['bottom'] < limit]
        return self._head_n_lines

    def find_tables(self, table_settings={}):
        # 简单按顺序排除了一下，通常是够了，如果出现不行的情况就改成全部检查
        def skip_duplicate(tables):
            tables = sorted(tables, key=lambda x: x[0].bbox[1])
            if len(tables) < 2:
                return tables
            new_tables = [tables[0]]
            for i in range(1, len(tables)):
                table = tables[i]
                tab = table[0]
                pre = new_tables[-1][0]
                if tab.bbox[1] >= pre.bbox[1] - DEFAULT_Y_TOLERANCE and \
                        tab.bbox[3] <= pre.bbox[3] + DEFAULT_Y_TOLERANCE and \
                        tab.bbox[0] >= pre.bbox[0] - DEFAULT_Y_TOLERANCE and \
                        tab.bbox[2] <= pre.bbox[2] + DEFAULT_Y_TOLERANCE:
                    # 重叠的表格，暂时改成取面积最大的表格，pdfplumber的最终计算结果也会取到最多的那个表
                    if (tab.bbox[2] - tab.bbox[0]) * (tab.bbox[3] - tab.bbox[1]) > \
                            (pre.bbox[2] - pre.bbox[0]) * (pre.bbox[3] - pre.bbox[1]):
                        new_tables[-1] = table
                    continue
                new_tables.append(table)
            return new_tables

        def _worker(lines, level, side, o_side):
            top = []
            bottom = []
            for line in lines:
                if line['x0'] == level:
                    if line['bottom'] > side and side - line['top'] > DEFAULT_Y_TOLERANCE:
                        top.append(line)
                    if line['top'] < o_side and line['bottom'] - o_side > DEFAULT_Y_TOLERANCE:
                        bottom.append(line)
            return top, bottom

        def collect_h_line(lines, table, finder):
            # 把补充的线多出来的点加入finder
            def add_up_intersection(cells, y):
                cells = [cell for cell in cells if cell]
                if not cells:
                    return
                h_lines = [{'x0': cells[0][0], 'y0': y, 'x1': cells[0][1], 'y1': y}]
                finder.intersections[(cells[0][0], y)] = {
                    'v': [{'x0': cells[0][0], 'y0': y, 'x1': cells[0][0], 'y1': cells[0][1]}], 'h': h_lines}
                for cell in cells:
                    finder.intersections[(cell[2], y)] = {
                        'v': [{'x0': cell[2], 'y0': y, 'x1': cell[2], 'y1': cell[1]}], 'h': h_lines}

            def add_bottom_intersection(cells, y):
                cells = [cell for cell in cells if cell]
                if not cells:
                    return
                h_lines = [{'x0': cells[0][0], 'y0': y, 'x1': cells[0][1], 'y1': y}]
                finder.intersections[(cells[0][0], y)] = {
                    'v': [{'x0': cells[0][0], 'y0': cells[0][3], 'x1': cells[0][0], 'y1': y}], 'h': h_lines}
                for cell in cells:
                    finder.intersections[(cell[2], y)] = {
                        'v': [{'x0': cell[2], 'y0': cell[3], 'x1': cell[2], 'y1': y}], 'h': h_lines}

            top1, bottom1 = _worker(lines, table.bbox[0], table.bbox[1], table.bbox[3])
            top2, bottom2 = _worker(lines, table.bbox[2], table.bbox[1], table.bbox[3])
            # 顶部
            if top1 and top2 and top1[0]['top'] == top2[0]['top']:
                table.rows.insert(0, Row(list(map(lambda x: x if x is None else (x[0], top1[0]['top'], x[2], x[1]),
                                                  table.rows[0].cells))))
                add_up_intersection(table.rows[0].cells, top1[0]['top'])
                table.bbox = (table.bbox[0], top1[0]['top'], table.bbox[2], table.bbox[3])
            # 底部
            if bottom1 and bottom2 and bottom1[0]['bottom'] == bottom2[0]['bottom']:
                table.rows.append(Row(list(map(lambda x: x if x is None else (x[0], x[3], x[2], bottom1[0]['bottom']),
                                               table.rows[-1].cells))))
                add_bottom_intersection(table.rows[-1].cells, bottom1[0]['bottom'])
                table.bbox = (table.bbox[0], table.bbox[1], table.bbox[2], bottom1[0]['bottom'])

        # 左侧上下缺横线和左角有缺口
        def complete_table_left_by_v(lines, tabs, t_finder, tab_i):
            tab = tabs[tab_i]
            if tab_i > 0 and tabs[tab_i - 1].bbox[2] < tab.bbox[0]:
                border = tabs[tab_i - 1].bbox[2] + 3
            else:
                border = 0
            result = []
            for line in lines:
                if border < line['x0'] < tab.bbox[0] and abs(tab.bbox[1] - line['top']) < 3 and \
                        abs(tab.bbox[3] - line['bottom']) < 3:
                    result.append(line['x0'])

            if result:
                result.reverse()
                sign = -1
                for i, row in enumerate(tab.rows):
                    line = t_finder.intersections[(row.bbox[0], row.bbox[1])]['h'][0]
                    if abs(line['x0'] - row.bbox[0]) < 3:
                        row.cells = [None] * len(result) + row.cells
                    else:
                        if sign > -1:
                            for j in range(len(result)):
                                ori_cell = tab.rows[sign].cells[j]
                                tab.rows[sign].cells[j] = (*ori_cell[:3], row.bbox[1])
                            tab.rows[sign].bbox = (*tab.rows[sign].bbox[:3], row.bbox[1])
                            sign = -1
                        for x in result:
                            row.cells.insert(0, (x, row.bbox[1], row.bbox[0], row.bbox[3]))
                            row.bbox = (x, *row.bbox[1:])
                        sign = i
                if sign > -1:
                    for i in range(len(result)):
                        ori_cell = tab.rows[sign].cells[i]
                        tab.rows[sign].cells[i] = (*ori_cell[:3], tab.bbox[3])
                    tab.rows[sign].bbox = (*tab.rows[sign].bbox[:3], tab.bbox[3])
                tab.bbox = [result[-1], *tab.bbox[1:]]

            # 取需要补的单元格数量
            def get_row_len(tab, finder, direction):
                def top_sign(rows, table_left):
                    def judge_h(line, bbox):
                        return abs(line['top'] - bbox[1]) < 3

                    for i in range(len(rows)):
                        if rows[i].bbox[0] == table_left:
                            return i, 0, rows[0].bbox, judge_h
                    return -1, -1, rows[0].bbox, judge_h

                def bottom_sign(rows, table_left):
                    def judge_h(line, bbox):
                        return abs(line['bottom'] - bbox[3]) < 3

                    base = -1
                    sign = -1
                    for i in range(1, len(rows) + 1):
                        if rows[len(rows) - i].bbox[0] == table_left:
                            base = len(rows) - i
                            base_bottom = rows[base].bbox[3]
                            for j in range(base + 1, len(rows)):
                                if abs(rows[j].bbox[1] - base_bottom) < 3:
                                    sign = j
                                    return base, sign, rows[-1].bbox, judge_h
                            break
                    return base, sign, rows[-1].bbox, judge_h

                base, sign, row_1_bbox, judge = bottom_sign(tab.rows, tab.bbox[0]) if direction \
                    else top_sign(tab.rows, tab.bbox[0])
                if sign == -1:
                    return base, sign, []
                arr = []
                for line in filter(lambda x: x['orientation'] == 'v', finder.edges):
                    if line['x0'] + 3 < row_1_bbox[0] and judge(line, row_1_bbox):
                        arr.append(line)
                return base, sign, arr

            def complete(direction):
                base, sign, lines = get_row_len(tab, t_finder, direction)
                if lines:
                    base_y = tab.bbox[3] if direction else tab.rows[base].bbox[1]
                    sign_row = tab.rows[sign]
                    lines.append({'x0': sign_row.bbox[0], 'top': sign_row.bbox[1]})
                    for i in range(len(lines) - 1):
                        try:
                            sign_row.cells[i] = (lines[i]['x0'], sign_row.bbox[1], lines[i + 1]['x0'], base_y)
                        except:
                            continue
                    sign_row.bbox = (tab.bbox[0], sign_row.bbox[1], sign_row.bbox[2], base_y)

            # 左上缺口
            if tab.bbox[0] + 3 < tab.rows[0].bbox[0]:
                complete(0)
            # 左下缺口
            if tab.bbox[0] + 3 < tab.rows[-1].bbox[0]:
                complete(1)

        def edge_sign(edge):
            signs = []
            if isinstance(edge['stroking_color'], (list, tuple)):
                signs.extend(edge['stroking_color'])
            else:
                signs.append(edge['stroking_color'])
            signs.append('-')
            if isinstance(edge['non_stroking_color'], (list, tuple)):
                signs.extend(edge['non_stroking_color'])
            else:
                signs.append(edge['non_stroking_color'])
            return tuple(signs)

        # non_stroking_color表示线的颜色，颜色不的线分别组成表格;0是黑，1是白
        dic = defaultdict(list)
        for edge in self.edges:
            # 只把线按颜色分组
            dic[edge_sign(edge)].append(edge)
        arr = []
        # 如果想要完整的边信息，可以在执行完下面操作后把dic的全部值重新放回self._edges中
        for v in dic.values():
            self._edges = v
            finder = MyTableFinder(self, table_settings)
            for table in finder.tables:
                arr.append((table, finder))

        # 去除空，并且有的表位置是左上和右下，统一改成左下右上
        for table, _ in arr:
            table.bbox = [min(table.bbox[0], table.bbox[2]), min(table.bbox[1], table.bbox[3]),
                          max(table.bbox[0], table.bbox[2]), max(table.bbox[1], table.bbox[3])]
        arr = skip_duplicate(arr)
        target = [v[0] for v in arr]

        for i in range(len(arr)):
            # 使用finder已经合并过的线
            finder = arr[i][1]
            v_edges = [edge for edge in finder.edges if edge['orientation'] == 'v']
            # 垂直的线没见过缺少的,暂时不检查
            collect_h_line(v_edges, target[i], finder)
            complete_table_left_by_v(v_edges, target, finder, i)
        return target

    @property
    def tables(self):
        if self._tables is None:
            if not self.chars:
                self._tables = []
                return self._tables
            # 备份原始的线,如果自定义的方法出错就使用原始的方法
            tmp_edges = self.edges
            try:
                _tables = self.find_tables()
            except Exception as e:
                logger.exception(f'{self.pdf.stream.name}:{self.page_number}')
                self._edges = tmp_edges
                _tables = super(PageExt, self).find_tables()
            # 表格少于3行并且范围接近或者大于页面的不视为表格，剔除
            # 只有一列的表不视为表格
            # 表总面积大于单元格总面积时不是表格，主要是解决色块被误认为表
            for i in range(len(_tables)):
                table = _tables[i]
                if len(table.cells) == len(table.rows):
                    _tables[i] = None
                    continue
                if len(table.rows) < 3:
                    # 行数少，且高度不够的表忽略
                    if table.bbox[3] - table.bbox[1] < self.chars[0]['height'] * (2 * len(table.rows) + 10):
                        _tables[i] = None
                        continue
                    if (table.bbox[0] < self.bbox[0] + 10 or table.bbox[1] < self.bbox[1] + 10 or
                        table.bbox[2] > self.bbox[2] - 10 or table.bbox[3] > self.bbox[3] - 10):
                        _tables[i] = None
                        continue

                # 因为有补充的单元格，所以计算面积需要使用row里面的cells
                if sum(map(rect_area, chain(*map(lambda x: x.cells, table.rows)))) + DEFAULT_Y_TOLERANCE < rect_area(table.bbox):
                    _tables[i] = None
                    continue
            self._tables = [v for v in _tables if v]
        return self._tables

    @property
    def table_chars(self):
        if self._table_chars is None:
            arr = []
            for table in self.tables:
                arr.append(self.__get_table_chars(table))
            self._table_chars = arr
        return self._table_chars

    @property
    def table_arr(self):
        """
        参考self.extract_tables()开发
        :return:
        """
        if self._table_arr is None:
            arr = []
            try:
                for table, chars in zip(self.tables, self.table_chars):
                    arr.append(self._table_extract(table, chars))
            except:
                pass
            self._table_arr = arr
        return self._table_arr

    # def extract_tables(self, table_settings={}):
    #     raise Exception('不要使用这个函数，直接使用table_text属性获取表格的文字')

    # ***********************************************************
    # 自定义的提取table文字的方法，table提取的文字已经被包含在所有的文字中了，如果只要文字片段，不需要提取表格的操作
    # ***********************************************************
    def __get_table_chars(self, table, sign=1):
        """

        :param table:
        :param sign: 是否需要标记表格在文字中的位置，默认是不需要。当sign=0时会标记
        :return:
        """
        table_chars = []
        new_chars = []
        for char in self._d_chars:
            if char_in_bbox(char, table.bbox):
                # # 每个表格一开始，向chars数组中添加一个带table键的字，表示这里有个表
                # if sign == 0:
                #     tmp = char.copy()
                #     tmp['table'] = True
                #     # 显式的把text设置成None,阻止后面直接使用这个字符位
                #     tmp['text'] = None
                #     # 为了保证这个标记在后面提取文本的时候被处理成一个单独的行,加一点高度用于后面根据文本行分类
                #     if new_chars and new_chars[-1]['doctop'] == tmp['doctop']:
                #         tmp['doctop'] += Decimal('0.001')
                #     new_chars.append(tmp)
                #     sign = 1
                table_chars.append(char)
            else:
                new_chars.append(char)
        # 表格以外的字
        self._d_chars = new_chars
        return table_chars

    def _table_extract(self, table, table_chars):
        table_arr = []

        def table_extract_text(chars, width, start):
            frags, _ = self.make_fragment(self.make_line(chars), width, start)
            return frags

        for row_i, row in enumerate(table.rows):
            row_chars = []
            _table_chars = []

            for char in table_chars:
                if char_in_bbox(char, row.bbox):
                    row_chars.append(char)
                else:
                    _table_chars.append(char)
            _row_chars = []
            row_arr = []
            for i, cell in enumerate(row.cells):
                if cell:
                    cell_chars = []
                    for char in row_chars:
                        if char_in_bbox(char, cell):
                            cell_chars.append(char)
                        else:
                            _row_chars.append(char)
                    row_chars = _row_chars
                    _row_chars = []

                    if len(cell_chars):
                        row_arr.append({'cell': table_extract_text(cell_chars, cell[2] - cell[0], cell[0]),
                                        'bbox': bbox_to_str(cell)})
                    else:
                        # 没有内容的单元格要返回一个空占位
                        # if row_i == 0:
                        #     row_arr.append(None)
                        # else:
                        row_arr.append({'cell': [{'text': '', 'page_number': self.page_number, 'index': -1}],
                                        'bbox': bbox_to_str(cell)})
                else:
                    # 这个cell通常不存在，只是为了保证列数一致占位用
                    row_arr.append(None)
            table_chars = _table_chars + row_chars
            _table_chars = []
            table_arr.append(row_arr)
        return {'table_info': table_arr, 'bbox': bbox_to_str(table.bbox), 'page_number': self.page_number,
                'height': str(self.height)}

    # 段落
    @property
    def fragments(self):
        if self._fragments is None:
            self._fragments, self.max_w = self.make_fragment(self.line_chars, self.width)
        return self._fragments

    @classmethod
    def make_fragment(cls, line_chars, width, start=0):
        """
        2.最大宽度：用每行的最后一个字的x0中最大值代替，误差是最后一个字的子宽。末尾是中文符号就取上一个字的x0,只检查常用的几个符号
        3.上一行没有达到最大宽度，当前行为新段；行间距大于最小行间距，当前行为新段；页面上所有行的最大宽度都不在页宽的5/6以外，都按行处理
        :param line_chars:
        :param width:
        :param start: 计算width的起点，表格中的起点通常不是0
        :param need_chars: 是否需要chars字段，默认为需要
        :return:
        """

        if not line_chars:
            return [], None
        if len(line_chars) == 1:
            return line_chars.copy(), 1

        # 页面上最宽的行的最大的x0和是否左对齐
        def max_w_and_mode(_line_chars):
            # 去除只有一个字的行，如果所有行都是1一个字，可能是提取误差，取第一个的值作为结果返回
            line_chars = [line for line in _line_chars if len(line) > 1]
            if not line_chars:
                return _line_chars[0][-1]['x1'], _line_chars[0][0]['x1']
            max_w = 0
            min_x = 10000
            for i in range(len(line_chars)):
                if line_chars[i][-1]['x1'] > max_w:
                    if line_chars[i][-1]['text'] not in '。，）；”、》':
                        max_w = line_chars[i][-1]['x1']
                    else:
                        if line_chars[i][-2]['x1'] > max_w:
                            max_w = line_chars[i][-2]['x1']
                if line_chars[i][0]['x1'] < min_x:
                    min_x = line_chars[i][0]['x1']
            return max_w, min_x

        max_w, minx = max_w_and_mode(line_chars)
        # 所有行都小于页面的5/6宽，认为所有行都是单独的段落,并且不需要拼接页间的段落
        threshold = start + 5 * width / 6
        if max_w < threshold:
            return line_chars.copy(), None

        arr = [[line_chars[0]]]
        for i in range(1, len(line_chars)):
            # 只要有项目编号标记就视为新段
            if 'head' in line_chars[i][0]:
                arr.append([line_chars[i]])
                continue
            pre_line = arr[-1][-1]
            # 上一行剩余的位置不足以放下一个字就认为满行了,没满行就把当前行视为新段
            if 2 * pre_line[-1]['x1'] - pre_line[-1]['x0'] <= max_w:
                arr.append([line_chars[i]])
                continue
            # 上一行是满行的情况下，当前行默认为段落的一部分，以下都是例外的情况
            # 字高不同
            if pre_line[-1]['height'] != line_chars[i][-1]['height']:
                arr.append([line_chars[i]])
                continue
            # 下一行的开头在当前行前面，并且下个行距小于等于当前的行距
            if i + 1 != len(line_chars) \
                    and line_chars[i + 1][0]['x0'] < line_chars[i][0]['x0'] - DEFAULT_X_TOLERANCE \
                    and line_chars[i + 1][-1]['top'] - line_chars[i][-1]['bottom'] <= \
                    line_chars[i][-1]['top'] - pre_line[-1]['bottom']:
                arr.append([line_chars[i]])
                continue
            # 下一行开头在上一行的右面，有冲突的情况，暂时不视为换行
            # if line_chars[i][0]['x0'] < arr[-1][0][0]['x0']:
            #     arr[-1].append(line_chars[i])
            #     continue
            # 行距大于3倍字高
            if line_chars[i][0]['top'] - pre_line[-1]['bottom'] > 3 * line_chars[i][0]['height']:
                arr.append([line_chars[i]])
                continue
            arr[-1].append(line_chars[i])
        return [list(chain(*v)) for v in arr], max_w

    @property
    def page_foot(self):
        if self._page_foot is not None:
            return self._page_foot
        if not self.line_chars:
            self._page_foot = ''
            return self._page_foot
        foot = self.line_chars[-1]
        foot_text = ''.join(map(lambda x: '' if x['text'].isspace() else x['text'], foot))
        res = self.foot_pattern.match(foot_text)
        if res and len(res.group()) == len(foot_text):
            self._page_foot = foot_text
            self.line_chars.pop()
        else:
            self._page_foot = ''
        return self._page_foot

    def simple_images(self):
        arr = []
        for img in self.images:
            arr.append({'x0': int(img['x0']), 'top': int(img['top']), 'x1': int(img['x1']),
                        'bottom': int(img['bottom']), 'page_number': img['page_number'], 'name': img['name']})
        return arr

    def to_dict(self):
        return {'page_number': self.page_number, 'fragments': self.fragments, 'tables': self.table_arr,
                'head_n_lines': [{'text': v} for v in self.head_n_lines], 'page_foot': self.page_foot,
                'height': str(self.height),
                'width': str(self.width), 'images': self.simple_images()}


class MyTableFinder(TableFinder):
    def __init__(self, page, settings={}):
        for k in settings.keys():
            if k not in DEFAULT_TABLE_SETTINGS:
                raise ValueError("Unrecognized table setting: '{0}'".format(
                    k
                ))
        self.page = page
        self.settings = dict(DEFAULT_TABLE_SETTINGS)
        self.settings.update(settings)
        for var, fallback in [
            ("text_x_tolerance", "text_tolerance"),
            ("text_y_tolerance", "text_tolerance"),
            ("snap_x_tolerance", "snap_tolerance"),
            ("snap_y_tolerance", "snap_tolerance"),
            ("join_x_tolerance", "join_tolerance"),
            ("join_y_tolerance", "join_tolerance"),
            ("intersection_x_tolerance", "intersection_tolerance"),
            ("intersection_y_tolerance", "intersection_tolerance"),
        ]:
            if self.settings[var] == None:
                self.settings.update({
                    var: self.settings[fallback]
                })
        self.edges = self.get_edges()
        self.intersections = edges_to_intersections(
            self.edges,
            self.settings["intersection_x_tolerance"],
            self.settings["intersection_y_tolerance"],
        )
        self.cells = intersections_to_cells(
            self.intersections
        )
        self.tables = [ MyTable(self.page, t)
                        for t in cells_to_tables(self.cells) ]


class MyTable(Table):
    def __init__(self, page, cells):
        self.page = page
        self.cells = cells
        self.bbox = (
            min(map(itemgetter(0), cells)),
            min(map(itemgetter(1), cells)),
            max(map(itemgetter(2), cells)),
            max(map(itemgetter(3), cells)),
        )
        self._rows = None

    @property
    def rows(self):
        if self._rows is None:
            _sorted = sorted(self.cells, key=itemgetter(1, 0))
            xs = list(sorted(set(map(itemgetter(0), self.cells))))
            rows = []
            for y, row_cells in itertools.groupby(_sorted, itemgetter(1)):
                xdict = dict((cell[0], cell) for cell in row_cells)
                row = Row([ xdict.get(x) for x in xs ])
                rows.append(row)
            self._rows = rows
        return self._rows


def char_in_bbox(char, bbox):
    v_mid = (char["top"] + char["bottom"]) / 2
    h_mid = (char["x0"] + char["x1"]) / 2
    x0, top, x1, bottom = bbox
    return (
            (h_mid >= x0) and
            (h_mid < x1) and
            (v_mid >= top) and
            (v_mid < bottom)
    )
