import hashlib

import xlrd
import xlwt
import os

excel_path = os.path.join(os.getcwd(), "static", "excel")
md5_excel_path = os.path.join(os.getcwd(), "static", "md5_excel")
ALLOWED_EXTENSIONS = ['xlsx', 'xls']


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def md5_encryption(string, style="md5（小写）"):
    # m = hashlib.sha256()
    m = hashlib.md5()
    m.update(str(string).encode("utf8"))
    if style == 'md5（小写）':
        press = m.hexdigest()
    else:
        press = m.hexdigest().upper()
    return press


def encryption_clos(encry_cols=None, encry_style=None):
    # 当加密的是空字符串是不加密，保留空字符串
    if not encry_style or not encry_cols:
        return None
    if os.listdir(excel_path):
        filename = os.path.join(excel_path, os.listdir(excel_path)[0])
        workbook = xlrd.open_workbook(filename=filename)
        table = workbook.sheets()[0]
        # excel 中没有数据
        if table.ncols == 0:
            return None
        if max(encry_cols) - 1 > table.ncols:
            # 输入的加密列不在excel中
            return None
        # 开始加密数据
        md5_workbook = xlwt.Workbook()
        work_sheet = md5_workbook.add_sheet("md5加密数据")
        c = 0
        for col in encry_cols:
            r = 0
            col_values = table.col_values(colx=col-1)
            work_sheet.write(r, c, str(col))
            work_sheet.write(r, c + 1, str(col) + "_"+encry_style)
            for v in col_values:
                if v == '':
                    md5_v = v
                else:
                    md5_v = md5_encryption(v, style=encry_style)
                work_sheet.write(r + 1, c, v)
                work_sheet.write(r + 1, c + 1, md5_v)
                r += 1
            c += 2
        md5_file = os.path.join(md5_excel_path,'md5加密数据.xlsx')
        md5_workbook.save(md5_file)
        # 返回md5文件的前5行数据
        md5_table_info = get_table_values(file_path=md5_excel_path)
        return md5_table_info
    return None


def get_table_values(file_path=excel_path):
    # 获取上传excel的前 5 行数据，默认加密第一个表中的数据
    if os.listdir(file_path):
        filename = os.path.join(file_path, os.listdir(file_path)[0])
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
