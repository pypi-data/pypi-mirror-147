# -*-coding:utf-8-*-

# 参数是cachedfile就直接执行，否则自动转成cachedfile
import os
import json
import pickle
import requests

from decimal import Decimal
from itertools import chain

from cache_file_view.bsjc_import_pdf_table import TableText, CompleteTable
from cache_file_view.bsjc_import_utils import _base_rect
from cache_file_view.bsjc_import_pdfplumber_extends import MultipleProcessMyPDF


def bounding_rough_rect(fragments, height):  # 根据一堆字画出一个框
    arr = list(chain(*map(lambda x: x['chars'], fragments)))
    return _base_rect(arr, Decimal(height))


def page_num_2_int_from_json(file):  # dic中的页码在存成json时会变成字符串，通过此函数转回原来的数字形式
    with open(file, encoding='utf-8') as f:
        return {int(k): v for k, v in json.load(f, strict=False).items()}


def cached_file(file, tmp_pdfs, local_cache, project=None):
    """

    :param file: pdf文件路径
    :param tmp_pdfs: 临时保存pdf文件的地址
    :param local_cache: 本地缓存文件夹
    :param project: id
    :return:
    """

    # from inspect import getframeinfo,stack
    if isinstance(file, CachedSingleFile):
        return file
    # caller = getframeinfo(stack()[1][0])
    return CachedSingleFile.get_instance(file, project, tmp_pdfs, local_cache)


# 带本地缓存的SingleFile文件
class CachedSingleFile:

    @classmethod
    def save_pdf_info(cls, url, pkl_path, project, tmp_pdfs):
        if url.startswith("http"):
            res = requests.get(url)
            project_dir = os.path.join(tmp_pdfs, project)
            os.makedirs(project_dir, exist_ok=True)
            file_path = os.path.join(project_dir, os.path.basename(url).split(".pdf")[0] + ".pdf")
            with open(file_path, 'wb+') as f:
                f.write(res.content)
        else:
            file_path = url

        dic = MultipleProcessMyPDF.read_info(file_path)
        if 'error' in dic:
            raise dic['error']
        dic['cache_path'] = pkl_path
        file = cls(**dic)
        if not check_cache(file.cache_path):
            with open(pkl_path, 'wb+') as f:
                pickle.dump(file, f)
        return file

    @classmethod
    def get_instance(cls, file_path, project, tmp_pdfs, local_cache):
        # local_cache 本地缓存文件夹
        # tmp_pdfs 临时保存pdf文件的地址，必传
        # project有值，就以project为准；没值时按下面的规则进行
        # 如果文件路径是tmp_pdfs/xxxx/xx.pdf,就把xxxx视为project;否则就使用local_project
        if not project:
            tmp_proj_dir = os.path.dirname(file_path)
            if os.path.dirname(tmp_proj_dir) == tmp_pdfs:
                project = os.path.basename(tmp_proj_dir)
            else:
                project = 'local_project'
        pkl_prefix = os.path.join(local_cache, project, os.path.basename(file_path).split(".pdf")[0] + ".pdf")
        pkl_path = pkl_prefix + '.pkl'
        if os.path.exists(pkl_path):
            with open(pkl_path, 'rb') as f:
                file = pickle.load(f)
            return file
        if not os.path.exists(os.path.join(local_cache, project)):
            os.makedirs(os.path.join(local_cache, project), exist_ok=True)
        file = cls.save_pdf_info(file_path, pkl_path, project, tmp_pdfs)
        return file

    def __init__(self, **kwargs):
        # 项目
        self.project = kwargs.get('project')
        # 文件名
        self.name = kwargs.get('name')
        # 文件id
        self.file_id = kwargs.get('file_id')
        # 文件保存路径
        self.file_path = kwargs.get('file_path')
        # 缓存文件的地址
        self.cache_path = kwargs['cache_path'] if kwargs.get('cache_path') else \
            os.path.join(kwargs.get('local_cache'), os.path.basename(self.file_path) + '.pkl')
        # 目录信息
        self.outlines = kwargs.get('outlines')
        # 页信息
        self.pages = kwargs.get('pages', [])
        self.page_count = len(self.pages)
        # 标记表格是否格式化成对象
        self.struct = False
        self.imgs = {}
        self.ori_text = kwargs.get('ori_texts', [])
        # 为了使用img_idx可以取到需要的数据,保持代码的一致性
        self.img_detail = {}

    def get_imgs(self, img_dic):
        self.imgs = img_dic
        detail_dic = {}
        for page_idx, imgs in self.imgs.items():
            for img in imgs:
                detail_dic[img['img_idx']] = (int(page_idx) + 1, img['bbox'])
        self.img_detail = detail_dic

    def get_imgs_in_range(self, start, end):
        img_dic = {}
        for key in range(start, end):
            if key in self.imgs:
                img_dic[key] = self.imgs[key]
        return img_dic

    # 强制刷新文件,其实就是把缓存删除
    def force_refresh(self):
        if os.path.exists(self.cache_path):
            os.remove(self.cache_path)
        self.cache_path = None

    # 把处理失败的表格以单个原始表的形式保存到page上
    def vestige_tables(self, tables):
        for table in tables:
            tmp = TableText.vestige_table(table)
            page = self.pages[table['page_number'] - 1]
            if 's_tables' in page:
                page['s_tables'].append(tmp)
            else:
                page['s_tables'] = [tmp]

    def struct_tables(self):
        if self.struct:
            return
        i = 0
        while i < self.page_count:
            page = self.pages[i]
            if page['tables']:
                tmp = []
                # 跨页表尾巴的同页上还有一个表，可能会有重复的问题，没遇到样本
                tables = CompleteTable.complete_table(self, page)
                for parts in tables:
                    try:
                        table = TableText(parts)
                        tmp.append(table)
                    except:
                        self.vestige_tables(parts)
                if tmp:
                    if 's_tables' in page:
                        tmp.extend(page['s_tables'])
                        page['s_tables'] = tmp
                    else:
                        page['s_tables'] = tmp
                i += len(tables[-1])
            else:
                i += 1
        self.struct = True

    def traversal_search(self, target):
        result = []
        if not self.struct:
            self.struct_tables()

        def get_fragment(fragments):
            for frag in fragments:
                if target.search(frag['text']):
                    result.append(frag)

        for page in self.pages:
            get_fragment(page['fragments'])
            if 's_tables' in page:
                table_res = []
                for table in page['s_tables']:
                    res = table.traverse_search(target)
                    if res:
                        table_res.append(res)
                for v in chain(*table_res):
                    result.append(v)
        return result

    def page_pos_by_index(self, indices):
        page_number = self.ori_text[indices[0]]['page_number']
        pos = bounding_rough_rect(map(lambda x: self.ori_text[x], indices), self.pages[page_number - 1]['height'])
        return page_number, [pos]

    def img_bbox_by_index(self, idx):
        if idx in self.img_detail:
            return self.img_detail[idx]
        return None, None


# 检查是否有缓存
def check_cache(pkl_path):
    if os.path.exists(pkl_path):
        return True
    else:
        return False

