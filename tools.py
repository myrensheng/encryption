import hashlib
import xlrd
import xlwt
import os
ALLOWED_EXTENSIONS = ['xlsx', 'xls']


def get_file_path():
    """
    获取 Excel 和加密 excel 的路径
    """
    encry = os.path.join(os.getcwd(), "encry")
    excel = os.path.join(os.getcwd(), "encry", "excel")
    encry_excel = os.path.join(os.getcwd(), "encry", "encry_excel")
    if not os.path.exists(encry):
        os.mkdir(encry)
        os.mkdir(excel)
        os.mkdir(encry_excel)

    return excel, encry_excel


excel_path, encry_excel_path = get_file_path()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def encryption_str(string, encry_model="md5_32", encry_style=True):
    # 加密为 utf-8 编码
    utf_8_str = str(string).encode("utf8")
    # 函数字典
    param_dict = {
        "md5_32": hashlib.md5(utf_8_str),
        "md5_16": hashlib.md5(utf_8_str),
        "sha1": hashlib.sha1(utf_8_str),
        "sha224": hashlib.sha224(utf_8_str),
        "sha256": hashlib.sha256(utf_8_str),
        "sha512": hashlib.sha512(utf_8_str)
    }
    encry_result = param_dict[encry_model].hexdigest()
    if encry_model == 'md5_16':
        encry_result = encry_result[8:-8]
    # 返回结果
    return encry_result if encry_style == "小写" else encry_result.upper()


def encryption_clos(encry_cols=None, encry_model=None, encry_style=None):
    # 当加密的是空字符串是不加密，保留空字符串
    if not encry_model or not encry_cols or not encry_style:
        return None
    if os.listdir(excel_path):
        filename = os.path.join(excel_path, os.listdir(excel_path)[0])
        workbook = xlrd.open_workbook(filename=filename)
        table = workbook.sheets()[0]
        # excel 中没有数据
        if table.ncols == 0:
            return "excel 中没有数据！"
        if max(encry_cols) - 1 > table.ncols:
            # 输入的加密列不在excel中
            return str(max(encry_cols)) + "超过excel中最大的列"
        # 开始加密数据
        encry_workbook = xlwt.Workbook()
        work_sheet = encry_workbook.add_sheet("md5加密数据")
        c = 0
        for col in encry_cols:
            r = 0
            col_values = table.col_values(colx=col - 1)
            work_sheet.write(r, c, str(col))
            work_sheet.write(r, c + 1, str(col) + "_" + encry_model + "_" + encry_style)
            for v in col_values:
                if v == '':
                    encry_v = v
                else:
                    encry_v = encryption_str(string=v, encry_model=encry_model, encry_style=encry_style)
                work_sheet.write(r + 1, c, v)
                work_sheet.write(r + 1, c + 1, encry_v)
                r += 1
            c += 2
        encry_file = os.path.join(encry_excel_path, '加密数据.xlsx')
        encry_workbook.save(encry_file)
        # 返回md5文件的前5行数据
        encry_table_info = get_table_values(file_path=encry_excel_path)
        return encry_table_info
    return "服務器內部錯誤"


def get_table_values(file_path=excel_path):
    # 获取上传excel的前 5 行数据，默认加密第一个表中的数据
    if os.listdir(file_path):
        filename = os.path.join(file_path, os.listdir(file_path)[0])
        workbook = xlrd.open_workbook(filename=filename)
        table = workbook.sheets()[0]
        # 默认返回前5行数据
        # table_rows = 5 if table.nrows >= 5 else table.nrows
        table_rows = table.nrows
        if table_rows == 0:
            return {"status": 400, "msg": "excel中没有数据！"}
        # 获取数据
        row_list = []
        for r in range(table_rows):
            row_dict = {}
            for k, v in enumerate(table.row_values(rowx=r)):
                row_dict[str(k + 1)] = v
            row_list.append(row_dict)
        return {"table_cols": table.ncols, "row_list": row_list, "excel_name": os.listdir(file_path)[0],
                "sheet_name": workbook.sheet_names()[0]}
    # 没有excel文件或者上传的不是excel文件
    return None
