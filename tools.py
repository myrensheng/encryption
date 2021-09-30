import hashlib

import xlrd
import os

excel_path = os.path.join(os.getcwd(), "static", "excel")
ALLOWED_EXTENSIONS = ['xlsx', 'xls']


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def md5_encryption(string,style="md5（小写）"):
    # m = hashlib.sha256()
    m = hashlib.md5()
    m.update(str(string).encode("utf8"))
    if style == 'md5（小写）':
        press = m.hexdigest()
    else:
        press = m.hexdigest().upper()
    return press


def encryption_clos(encry_cols=None):
    # 加密对应的列
    # 当加密的是空字符串是不加密，保留空字符串

    pass


def get_table_values():
    # 获取上传excel的前 5 行数据，默认加密第一个表中的数据
    if os.listdir(excel_path):
        filename = os.path.join(excel_path, os.listdir(excel_path)[0])
        workbook = xlrd.open_workbook(filename=filename)
        table = workbook.sheets()[0]
        # 默认返回前5行数据
        table_rows = 5 if table.nrows >= 5 else table.nrows
        if table_rows == 0:
            return None
        # 获取前5行数据
        row_5_list = []
        for r in range(table_rows):
            row_dict = {}
            for k, v in enumerate(table.row_values(rowx=r)):
                row_dict[str(k + 1)] = v
            row_5_list.append(row_dict)
        return {"table_cols": table.ncols, "row_5_list": row_5_list}
    # 没有excel文件或者上传的不是excel文件
    return None

