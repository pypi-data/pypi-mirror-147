# -*-coding:utf-8-*-

"""
对pdf中表的相关操作
"""
import json
import sys
import logging

from decimal import Decimal

logger = logging.getLogger(__file__)


class RowText:
    """
    某个垂直的合并单元格对应多行SubRow,每个subrow实例是children中的一个
    is_tree用来标记children中的cell之间是否树结构，
    通常是true。形如[[1,1,1,1,1],[1,1,None,1,1]]的数据形成的单元格实际只是共用第3列的内容，对应关系还是按索引对应，就设置为False
    """

    def __init__(self, row, start, ori_start=-1, is_tree=True):
        self.children = [SubRow(row, start, ori_start=ori_start, is_tree=is_tree)]
        self.start = start
        self._width = None
        self.is_tree = is_tree

    @staticmethod
    def add_in_row(row, rows, start):
        """
        把数据加到现有的TableText中,如果遇到[[1,1,1,1,1],[1,1,None,1,1]]这种合并单元格在中间的就把前面变成一个Rowtext，并做标记
        :param row: 原始行数据
        :param rows: TableText的rows
        :param start: 对应row中当前执行的起始位置,因为row是原始数据行，所以要根据start裁减
        :return:
        """
        if row[start] is None:
            rows[-1].add_vertical_row(row, start)
        else:
            rows.append(SubRow(row, start))

    @property
    def width(self):
        if self._width is None:
            self._width = self.children[0].width
        return self._width

    def traverse_search(self, target, result, stop):
        for sub in self.children:
            sub.traverse_search(target, result, stop)

    def to_dict(self):
        arr = []
        for sub in self.children:
            arr.append(sub.to_dict())
        return {'info': arr, 'width': str(self.width)}

    def cell_text(self):
        raise Exception('没有遇到过正常案例')
        arr = [cell.cell_text() for cell in self.children]
        max_len = max(map(lambda x: len(x), arr))
        if not max_len:
            return []
        # 假设列名的行一定在同一页上
        return [(''.join(map(lambda x: x[i][0] if len(x) > i else x[-1][0], arr)),) for i in range(max_len)]


class CellText:
    """
    表格解析中最基础的cell
    """

    def __init__(self, cell, start):
        self.text = cell['cell']
        self.bbox = cell['bbox']
        self.size = 1
        self.start = start
        self._width = None

    @property
    def width(self):
        if self._width is None:
            self._width = abs(Decimal(self.bbox[2]) - Decimal(self.bbox[0]))
        return self._width

    @staticmethod
    def make_cells(cells, start):
        """
        CellText实例不需要再次设置start值,原始数据，start就是正确的start起始值
        :param cells: [原始数据或则CellText实例]
        :param start: 起始位置
        :return:
        """
        arr = []
        for i in range(start, len(cells)):
            cell = cells[i]
            if cell:
                if isinstance(cell, dict):
                    arr.append(CellText(cell, i))
                else:
                    arr.append(cell)
            else:
                if arr:
                    arr[-1].size += 1
        return arr

    # result在此处没用，只是为了与其他类的同名函数保持一致
    def traverse_search(self, target, result, stop):
        for v in self.text:
            if target.search(v['text']):
                return True
        return False

    def to_dict(self):
        return {'text': '\n'.join(map(lambda x: x['text'], self.text)), 'width': str(self.width),
                'index': [v['index'] for v in self.text]}

    def cell_text(self):
        return {'text': ''.join(map(lambda x: x['text'], self.text)),
                'index': list(map(lambda x: x['index'], self.text))}


class SubRow:
    """
    保存一行中某一部分同级的cell，直到遇到合并单元格。可以嵌套
    """

    def __init__(self, row, start, ori_start=-1, is_tree=True):
        """

        :param row: 原始数组
        :param start: 取数据的起点
        :param ori_start: 当传入的row不是原始的数据时，元素在原始数据中的索引可能和当前的row中不同，可以用这个参数传递在原始数据中的索引
        """
        self.children = CellText.make_cells(row, start)
        self.start = ori_start if ori_start > -1 else start
        self._width = None
        self.v_size = 1
        self.is_tree = is_tree

    @property
    def width(self):
        if self._width is None:
            self._width = sum(map(lambda x: x.width, self.children))
        return self._width

    def add_vertical_row(self, row, cut_start):
        """
        为垂直的合并单元格后面的Rowtext实例增加一个子行
        :param row: 原始行
        :param cut_start: 当前处理的起始位置
        :param n_start: None的起始位置
        :return:
        """

        def get_next_start():
            return self.children[j + 1].start if len(self.children) > j + 1 else sys.maxsize

        # None的结束位置
        j = 0
        next_start = get_next_start()
        for i in range(cut_start, len(row)):
            if i >= next_start:
                cut_start = i
                j += 1
                next_start = get_next_start()
            if row[i]:
                if isinstance(self.children[j], RowText):
                    self.children[j].add_in_row(row, self.children[j].children, cut_start)
                else:
                    arr = self.children[:j]
                    # 这个地方传进去的row不是原始长度的行，为了补偿make_cells函数的起始位置，拼一个cut_start长度的None数组在前面
                    arr.append(RowText([None] * cut_start + self.children[j:], cut_start))
                    self.children = arr
                    self.children[-1].add_in_row(row, self.children[-1].children, cut_start)
                return

    def traverse_search(self, target, result, stop):
        for i, cell in enumerate(self.children):
            if cell and cell.traverse_search(target, result, stop):
                result.append([v.to_dict() for v in self.children[i:]])
                if stop:
                    return

    def to_dict(self):
        arr = []
        for cell in self.children:
            arr.append(cell.to_dict())
        return arr

    def cell_text(self):
        return [cell.cell_text() for cell in self.children]


class TableText:
    """
    把表格的内容转成字典或者json
    a = TableText(parts)
    print(a.to_dict())
    print(a.to_json())
    """

    # 把处理不了的表格退化成原始的表格
    @classmethod
    def vestige_table(cls, part):
        rows = []
        for row in part['table_info']:
            rows.append(SubRow(row, 0))
        return cls(rows, vestige=True)

    def __init__(self, parts, vestige=False):
        self.rows = parts if vestige else self.make_rows(parts)
        self.row_len = 0
        self.vestige = vestige

    @classmethod
    def make_rows(cls, parts):
        """
        假设：1.需要水平合并单元格的第一个格子一定有内容，后面的None是要和他合并的
             2.需要垂直合并的单元格第一个格子一定有内容，下面的None是要和他合并的
             3.合并单元格一定是在非合并单元格的左侧（自定义的）
             事实上上面的假设就是pdfplumber主要的单元格输出规则

        :param parts:
        :return:
        """

        # 检查上下两行的模式，如果返回True表示需要合并，返回False表示不需要合并
        def is_need_merge(row1, row2):
            if row2[0]:
                return False
            return not any(map(lambda x: row2[x] and not row1[x], range(len(row2))))

        def recursion(ele):
            if isinstance(ele, CellText):
                return ele
            else:
                return recursion(ele.children[-1])

        def row1(tab, rows):
            row = tab[0]
            if rows and len(row[0]['cell']) == 1 and not row[0]['cell'][0]['text']:
                sign = 0
                for i in range(1, len(row)):
                    if not row[i] or (len(row[i]['cell']) == 1 and not row[i]['cell'][0]['text']):
                        sign = i
                # 执行过此处会改变原来的表结构，如果想要重复使用需要打开下面注释
                row = row.copy()
                for i in range(sign + 1):
                    if row[i] and (row[i]['cell'][0]['text'] or len(row[i]['cell']) > 1):
                        for v in rows[-1].children:
                            if v.start == i:
                                tmp = recursion(v)
                                tmp.text.extend(row[i]['cell'])
                                break
                    row[i] = None
            RowText.add_in_row(row, rows, 0)

        rows = []
        for part in parts:
            sub_tab = part['table_info']
            row1(sub_tab, rows)
            tmp = None
            for i in range(1, len(sub_tab)):
                if is_need_merge(tmp if tmp else sub_tab[i - 1], sub_tab[i]):
                    if not tmp:
                        tmp = sub_tab[i - 1]
                    RowText.add_in_row(sub_tab[i], rows, 0)
                else:
                    tmp = None
                    rows.append(SubRow(sub_tab[i], 0))
        return cls.concat_middle_cell(rows)

    @staticmethod
    def concat_middle_cell(rows):
        """
        合并处于表格内部的单元格，即不满足从左到右从属关系的合并单元格
        :param rows:
        :return:
        """
        if not rows:
            return rows
        # 找到所有缺了宽度的单元格的索引
        width = rows[0].width - 3
        src = [(i, v) for i, v in enumerate(rows) if width > v.width]
        if not src:
            return rows
        arr1 = []
        tmp = [src[0]]
        for i in range(1, len(src)):
            if src[i][0] - src[i - 1][0] == 1:
                tmp.append(src[i])
            else:
                arr1.append(tmp)
                tmp = [src[i]]
        arr1.append(tmp)
        # 暂时不使用全部检查，遇到意外情况在全部检查
        arr = []
        for i, v in enumerate(arr1):
            pre = rows[v[0][0] - 1]
            for j, sub in enumerate(zip(pre.children, v[0][1].children)):
                if sub[0].start != sub[1].start:
                    arr.append(pre.children[j].start)
                    break
            # 上一行比下面长，就取下面第一个比下面多的单元格的start
            if len(arr) - 1 != i:
                arr.append(pre.children[len(v[0][1].children)].start)

        # 合并行的函数，如果合并单元格是最右面的，就没有back
        def construct_cell(pre, index, v):
            # 把同行的多个单元格用none补齐数量，有效的单元格放到size的最后
            def none_back(cells):
                res = []
                for i, cell in enumerate(cells):
                    res.append(cell)
                    res.extend([None] * (cell.size - 1))
                return res

            pre.children = none_back(pre.children)
            for sub in v:
                sub[1].children = none_back(sub[1].children)
            tmp = SubRow([], 0, is_tree=False)
            if index + 1 < len(pre.children):
                front = RowText(pre.children[:index], 0, is_tree=False)
                back = RowText(pre.children[index + 1:], 0, ori_start=index + 1, is_tree=False)
                for sub in v:
                    front.children.append(SubRow(sub[1].children[:index], 0))
                    tail = sub[1].children[index:]
                    if any(tail):
                        back.children.append(SubRow(tail, 0, ori_start=index))
                    else:
                        back.children[-1].v_size += 1
                tmp.children = [front, pre.children[index], back]
            else:
                front = RowText(pre.children[:index], 0, is_tree=False)
                for sub in v:
                    front.children.append(SubRow(sub[1].children[:index], 0))
                tmp.children = [front, pre.children[index]]
            return tmp

        # 重新组合单元格
        for index, v in zip(arr, arr1):
            pre = rows[v[0][0] - 1]
            rows[v[0][0] - 1] = construct_cell(pre, index, v)
        # 重新生成表格数组
        skip = [v[0] for v in src]
        return [v for i, v in enumerate(rows) if i not in skip]

    def traverse_search(self, target, stop=False):
        """
        遍历表查找
        :param target: 用regex.compile编译后的正则表达式
        :param stop: True表示找到以后就停止搜索
        :return:
        """
        result = []
        for row in self.rows:
            row.traverse_search(target, result, stop)
        return result

    def to_dict(self):
        arr = []
        for row in self.rows:
            arr.append(row.to_dict())
        return arr

    def to_json(self):
        return json.dumps(self.to_dict(), ensure_ascii=False)

    # 临时方法,以下两个方法只支持没有合并单元格的表
    def get_column_name(self):
        try:
            arr = []
            for cell in self.rows[0].children:
                tmp = cell.cell_text()
                if isinstance(tmp, list):
                    arr.extend(tmp)
                else:
                    arr.append(tmp)
            return [v['text'] for v in arr]
        except Exception as e:
            logger.exception(e)
            return []

    # 根据字典依次取行的指定单元格，并返回所有的字典
    def get_specific_columns_by_key_in_row(self, keys):
        arr = []
        if not keys:
            return []
        for row in self.rows[1:]:
            tmp = {k: row.children[v].cell_text() for k, v in keys.items()}
            arr.append(tmp)
        return arr

    # 解决bug用
    def get_specific_columns_by_key_in_row_new(self, keys):
        arr = []
        if not keys:
            return []
        for row in self.rows[1:]:
            if len(row.children) > 1:
                try:
                    tmp = {}
                    for k, v in keys.items():
                        tmp[k] = row.children[v].cell_text()
                    arr.append(tmp)
                except Exception as e:
                    pass
        return arr


class CompleteTable:
    @staticmethod
    def _after_table(frags, table, file):
        """
        返回true的时候认为表格在当前页结束了
        :param frags:
        :return:
        """
        table_bottom = Decimal(table['bbox'][3])
        n = len(frags)
        for i in (1, 2):
            if n - i < 0:
                return
            bottom_frag = frags[n - i]
            if len(bottom_frag['text'].strip()) < 7:
                continue
            if not file.ori_text[bottom_frag['index']]:
                continue
            if Decimal(file.ori_text[bottom_frag['index']]['chars'][-1]['bottom']) >= table_bottom:
                return True
        return

    @staticmethod
    def _before_table(frags, tables, file):
        """

        :param frags:
        :param tables:
        :return: 返回False表示没有表需要连
        """
        if not tables:
            return False
        table = tables[0]
        table_top = Decimal(table['bbox'][1])
        if not frags:
            return True
        top_frag = frags[0]
        if Decimal(file.ori_text[top_frag['index']]['chars'][-1]['top']) <= table_top:
            return False
        return True

    @classmethod
    def _concat_single_table(cls, frags, page, pre_table, columns, table_parts, file):
        tables = page['tables']
        if not cls._before_table(frags, tables, file):
            return False

        def skip_columns_head(table, columns):
            row1 = [''.join(map(lambda x: x['text'], cell['cell'])).strip() for cell in table['table_info'][0] if cell]
            if len(row1) != len(columns):
                return 0
            for i, v in enumerate(columns):
                if v != row1[i]:
                    return 0
            return 1

        table = tables[0]
        # if abs(Decimal(pre_table['bbox'][2]) - Decimal(pre_table['bbox'][0]) - (
        #         Decimal(table['bbox'][2]) - Decimal(table['bbox'][0]))) < DEFAULT_X_TOLERANCE:
        #     # if len(table['table_info'][0]) != len(pre_table['table_info'][0]):
        #     #     return False
        #     if abs(Decimal(table['bbox'][0]) - Decimal(pre_table['bbox'][0])) > DEFAULT_X_TOLERANCE * 2:
        #         return False
        # 已经能正确处理页眉，如果列数相同且中间没有字就视为一个表,待验证冲突
        if len(pre_table['table_info'][0]) == len(table['table_info'][0]):
            sign = skip_columns_head(table, columns)
            table_parts.append({'table_info': table['table_info'][sign:], 'bbox': table['bbox'],
                                'page_number': page['page_number']})
        if len(tables) > 1:
            return False
        if not cls._before_table(frags, tables, file):
            return False
        return True

    @classmethod
    def _concat_tables(cls, file, pre_table, columns, start_page_num):
        table_parts = [pre_table]
        if start_page_num >= file.page_count:
            return table_parts
        page = file.pages[start_page_num]
        while cls._concat_single_table(page['fragments'], page, pre_table, columns, table_parts, file):
            if page['page_number'] == file.page_count:
                return table_parts
            page = file.pages[page['page_number']]
        return table_parts

    @classmethod
    def complete_table(cls, file, page_info):
        """
        按页返回一个表的所有构成部分,只有最后一个表要检查后续，其他全部原样返回
        :param file: CachedSingleFile实例
        :param page_info: 表的第一部分所在页;{'tables': [], 'fragments': [], 'page_number': 2}
        :return:
        """
        if not page_info['tables']:
            return []
        tables = [[page_info['tables'][i]] for i in range(len(page_info['tables']))]
        table = page_info['tables'][-1]
        if cls._after_table(page_info['fragments'], table, file):
            return tables
        columns = [''.join(map(lambda x: x['text'], cell['cell'])).strip() for cell in table['table_info'][0] if cell]
        tables[-1] = cls._concat_tables(file, table, columns, page_info['page_number'])
        return tables

    @staticmethod
    def iter_table_parts(parts):
        """
        按行返回表的所有信息
        :param parts:
        :return:
        """
        from itertools import chain
        for part in chain(parts):
            for row in part['table_info']:
                yield row