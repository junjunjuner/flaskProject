# -*- encoding: utf-8 -*-
'''
Created on $(DATE)

@author: jnnr

@requirments: Pycharm 2019.1; Python 3.5 | Anaconda 3(64-bit)

@decription:
'''

import flask,os,time
import json
from flask_cors import CORS
from flask import request,send_from_directory,jsonify
app = flask.Flask(__name__)#创建一个app，代表这个web服务
app.config['JSON_AS_ASCII'] = False
@app.route('/get_file',methods=['get'])
def get_file():
    #下载文件接口
    filename = request.values.get('fname',None)
    #获取需要下载的文件名
    if filename:#如果获取到的文件名话
        if os.path.isfile(filename):#判断是否是一个文件
            #返回要下载的文件
            return send_from_directory('.',filename,as_attachment=True)
        else:
            return jsonify({"msg":"文件不存在!"})
    else:
        return jsonify({'msg':'文件名不能为空'})
@app.route('/files',methods=['get'])
def file_list():
    #获取文件列表接口
    files = os.listdir('.')#获取当前目录下所有文件
    new_files = [f for f in files if os.path.isfile(f)]
    #三元运算符，把是文件的放到list中
    return jsonify({"files":new_files})
@app.route('/upload',methods=['post','get'])
def upload():
    #上传文件接口
    print(request.files)
    x1 = request.files['file1']
    x2 = request.files['file2']
    # x = json.loads(request.get_data().decode(encoding='utf-8'))
    print(x1,x2)
    # result = request.args.get("data")
    # print(result)
    f1 = x1.filename
    f2 = x2.filename
    print(f1,f2)
    # f = request.files.get('filename',None)
    if f1:
        # t = time.strftime('%Y%m%d%H%M%S')#获取当前时间
        # new_file_name = t+f.filename#给文件重命名，防止有重复文件覆盖
        new_file_name = f1
        x1.save(new_file_name)#保存文件
        x2.save(f2)
        print("ok")
        return jsonify({"code":"ok"})
    else:
        # return result
        return jsonify({"msg":"请上传文件！"})


if __name__ == '__main__':
    CORS(app, supports_credentials=True)
    app.run(host='0.0.0.0',debug=True,port=8888)#启动这个web服务