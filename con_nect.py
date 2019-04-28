from flask import Flask,request
from flask_pymongo import PyMongo,DESCENDING,ASCENDING
from flask import jsonify
from flask_cors import CORS
import json
import re

app = Flask(__name__)
CORS(app, resources=r'/*')
app.config['MONGO_DBNAME'] = 'All_Comment'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/All_Comment'
app.url_map.strict_slashes = False
app.config['JSON_AS_ASCII'] = False
coll = 'SaoDiJiQiRen'

mongo = PyMongo(app)


@app.route('/api/data',methods=['GET'])
def data():
    # todos = mongo.db.taishixiwanji.find({})
    # star = mongo.db.taishixiwanji.find().sort([('_id',DESCENDING)])
    # 每页数据展示
    page = int(request.args.get('page', 1))        # 当前在第几页
    print(page)
    per_page = int(request.args.get('per_page', 10))           # 每页几条数据
    find_type = request.args.get('type', '')            # 此处{}为str格式，需转换为dict格式
    search = request.args.get('search','')
    finder = {}
    if find_type:
        finder.update({'type': find_type})
    if search:
        finder.update({'comment': re.compile(search)})
    # finder = json.loads(finder)  # 转化为dict格式
    # 总页数查询
    count = mongo.db[coll].find(finder).count()
    if count%10 > 0:
        total_page = int(count/10 +1)
    else:
        total_page = int(count/10)
    # 分页查询
    star = mongo.db[coll].find(finder).sort([('_id', DESCENDING)]).skip(per_page*(page-1)).limit(10)
    # star = mongo.db.taishixiwanji.find()
    output = []
    for s in star:
        try:
            name = s['title']
            brand = s['logo']
            comment = s['comment']
            _type = s['type']
            commenttype = s['comment_type']
            source = s['web']
        except Exception as e:
            print(e)
            continue
        output.append({'type': _type, 'commenttype': commenttype, 'source':source,
            'name': name, 'brand': brand, 'comment': comment})
    return jsonify({'total_count':count,'total_page': total_page, 'result': output})

@app.route('/api/exportdata',methods=['GET'])
def exportdata():
    # todos = mongo.db.taishixiwanji.find({})
    # star = mongo.db.taishixiwanji.find().sort([('_id',DESCENDING)])
    find_type = request.args.get('type', '')            # 此处{}为str格式，需转换为dict格式
    search = request.args.get('search','')
    finder = {}
    if find_type:
        finder.update({'type': find_type})
    if search:
        finder.update({'comment': re.compile(search)})
    # finder = json.loads(finder)  # 转化为dict格式
    # 总页数查询
    count = mongo.db[coll].find(finder).count()
    if count%10 > 0:
        total_page = int(count/10 +1)
    else:
        total_page = int(count/10)
    # 查询符合条件的所有数据
    star = mongo.db[coll].find(finder).sort([('_id', DESCENDING)])
    # star = mongo.db.taishixiwanji.find()
    output = []
    for s in star:
        try:
            name = s['title']
            brand = s['logo']
            comment = s['comment']
            _type = s['type']
            commenttype = s['comment_type']
            source = s['web']
        except Exception as e:
            print(e)
            continue
        output.append({'type': _type, 'commenttype': commenttype, 'source':source,
            'name': name, 'brand': brand, 'comment': comment})
    return jsonify({'total_count':count,'total_page': total_page, 'result': output})

if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=5050,
        debug=True)
