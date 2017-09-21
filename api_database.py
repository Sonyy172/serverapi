from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'Phuc'
app.config['MONGO_URI'] = 'mongodb://cb.saostar.vn:27017/Phuc'

mongo = PyMongo(app)


@app.route('/star', methods=['GET'])
def get_all_stars():
    star = mongo.db.stars
    output = []
    for s in star.find():
        output.append({'name': s['name'], 'distance': s['distance']})
    return jsonify({'result': output})


@app.route('/star/', methods=['GET'])
def get_one_star(name):
    star = mongo.db.stars
    s = star.find_one({'name': name})
    if s:
        output = {'name': s['name'], 'distance': s['distance']}
    else:
        output = "No such name"
    return jsonify({'result': output})


@app.route('/star', methods=['POST'])
def add_star():
    star = mongo.db.stars
    name = request.json['name']
    distance = request.json['distance']
    star_id = star.insert({'name': name, 'distance': distance})
    new_star = star.find_one({'_id': star_id})
    output = {'name': new_star['name'], 'distance': new_star['distance']}
    return jsonify({'result': output})


# USER
@app.route('/user/get', methods=['GET'])
def get_all_user():
    user = mongo.db.USER
    output = []
    for user in user.find():
        output.append({
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'id_user': user['id_user'],
            'HLV_da_binh_chon': user['HLV_da_binh_chon'],
            'subscribe_news': user['subscribe_news'],
            'message': user['message']
        })
    return jsonify({'result': output})


# NEWS
@app.route('/news/get', methods=['GET'])
def get_all_news():
    news = mongo.db.NEWS
    output = []
    for news in news.find():
        output.append({
            'title': news['title'],
            'subtitle': news['subtitle'],
            'image_url': news['image_url'],
            'item_url': news['item_url']
        })
    return jsonify({'result': output})


@app.route('/news/insert', methods=['POST'])
def add_news():
    news = mongo.db.NEWS
    number = request.json['number']
    title = request.json['title']
    subtitle = request.json['subtitle']
    image_url = request.json['image_url']
    item_url = request.json['item_url']

    check_news = news.find_one({'item_url': item_url})
    if bool(check_news):
        return "news da co trong database"
    else:
        news_id = news.insert({
            'number': number,
            'title': title,
            'subtitle': subtitle,
            'image_url': image_url,
            'item_url': item_url
        })
        new_news = news.find_one({'_id': news_id})
        output = {
            'number': new_news['number'],
            'title': new_news['title'],
            'subtitle': new_news['subtitle'],
            'image_url': new_news['image_url'],
            'item_url': new_news['item_url']
        }
        return jsonify({'result': output})


@app.route('/news/update', methods=['PUT'])
def update_news():
    news = mongo.db.NEWS

    number = request.json['number']
    title = request.json['title']
    subtitle = request.json['subtitle']
    image_url = request.json['image_url']
    item_url = request.json['item_url']
    # news = [news for news in NEWS if news['title'] == title]

    updated_news = news[0].update(
        {news['number']:  number},
        {'$inc': {
            news['number']: number,
            news['title']: title,
            news['subtitle']: subtitle,
            news['image_url']: image_url,
            news['item_url']: item_url
        }}
    )

    new_news = news.find_one({'_id': updated_news})
    output = {
        'number': new_news['number'],
        'title': new_news['title'],
        'subtitle': new_news['subtitle'],
        'image_url': new_news['image_url'],
        'item_url': new_news['item_url']
    }
    return jsonify({'result': output})


if __name__ == '__main__':
    app.run(host='210.211.109.211', port=5000, debug=True, threaded=True)
