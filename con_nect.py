from flask import Flask,request
from flask_pymongo import PyMongo,DESCENDING,ASCENDING
from flask import jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app, resources=r'/*')
app.config['MONGO_DBNAME'] = 'JiaDianErYuan_TaiShiXiWanJi'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/JiaDianErYuan_TaiShiXiWanJi'
app.url_map.strict_slashes = False
app.config['JSON_AS_ASCII'] = False

mongo = PyMongo(app)



@app.route('/api/data',methods=['GET'])
def index():
    # todos = mongo.db.taishixiwanji.find({})
    # star = mongo.db.taishixiwanji.find().sort([('_id',DESCENDING)])
    # 每页数据展示
    page = int(request.args.get('page', 1))        # 当前在第几页
    print(page)
    per_page = int(request.args.get('per_page', 10))           # 每页几条数据
    finder = request.args.get('finder', {})
    finder=json.loads(finder)
    # 总页数查询
    count = mongo.db.taishixiwanji.find(finder).count()
    if count%10 > 0:
        total_page = int(count/10 +1)
    else:
        total_page = int(count/10)
    # 分页查询
    star = mongo.db.taishixiwanji.find(finder).sort([('_id', DESCENDING)]).skip(per_page*(page-1)).limit(10)
    # star = mongo.db.taishixiwanji.find()
    output = []
    for s in star:
        try:
            name = s['name']
            brand = s['brand']
            comment = s['goodcomment']
            _type = '台式洗碗机'
            commenttype = '好评'
            source = '京东'

        except:
            continue
        output.append({'type': _type, 'commenttype': commenttype, 'source':source,
            'name': name, 'brand': brand, 'comment': comment})
    return jsonify({'total_count':count,'total_page': total_page, 'result': output})



if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=5050,
        debug=True)
