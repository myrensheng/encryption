from flask import Flask, render_template, request, jsonify
import json
from flask_cors import *
from tools import allowed_file, excel_path, get_table_values, md5_excel_path, encryption_clos
import os

app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route("/")
def hello():
    return render_template('hello.html')


@app.route("/upload", methods=["POST"])
def upload():
    # 上传文件到 static/excel 文件夹中
    # 清空数据文件
    if os.listdir(excel_path):
        excel_file = os.path.join(excel_path, os.listdir(excel_path)[0])
        os.remove(excel_file)
    # 清空已加密的excel文件
    if os.listdir(md5_excel_path):
        md5_excel_file = os.path.join(md5_excel_path, os.listdir(md5_excel_path)[0])
        os.remove(md5_excel_file)
    if 'file' not in request.files:
        print("request中没有files参数")
        return jsonify({"status": 400, "msg": "请上传excel文件！"})
    # 获取文件
    file = request.files['file']
    if file.filename != '' and allowed_file(file.filename):
        # 文件名不为空并且是excel文件
        filename = file.filename
        file.save(os.path.join(excel_path, filename))
        return jsonify({"status": 200, "msg": filename + "保存成功！"})
    return jsonify({"status": 400, "msg": "请上传excel文件"})


@app.route("/table", methods=["GET", "POST"])
def table():
    excel_values = get_table_values()
    if excel_values:
        return jsonify({"status": 200, "msg": "获取数据成功！", "excel_values": excel_values})
    else:
        return jsonify({"status": 400, "msg": "请上传excel文件"})


@app.route("/encryption", methods=["GET", "POST"])
def encryption():
    r_json = request.json
    encry_cols = r_json["encryCols"]
    encry_style = r_json["encry_style"]
    if False in [i.isnumeric() for i in encry_cols.split(",")]:
        return jsonify({"status": 400, "msg": "加密列以英文‘,’隔开！"})
    # 加密成功，直接返回加密后的数据
    encry_cols = [int(i) for i in encry_cols.split(",")]
    md5_excel_values = encryption_clos(encry_cols, encry_style)
    return jsonify({"status": 200, "msg": "加密成功！", "excel_values": md5_excel_values})


if __name__ == '__main__':
    app.run(debug=True)
