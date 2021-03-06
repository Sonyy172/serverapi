from flask import Flask, render_template, url_for, request, session, redirect, jsonify
from flask_pymongo import PyMongo, ObjectId
import bcrypt


app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'Phuc'
app.config['MONGO_URI'] = 'mongodb://cb.saostar.vn:27017/Phuc'

mongo = PyMongo(app)


# USER_CMS authentication
@app.route('/')
def index():
    if 'username' in session:
        return 'You are logged in as ' + session['username']

    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.USER_CMS
    login_user = users.find_one({'username': request.form['username']})
    user_activation_key = bcrypt.hashpw(
        login_user['username'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    if login_user:
        if login_user['password'] == request.form['password']:
            users.update_one(
                {'name': login_user['username']},
                {'$set': {'user_activation_key': user_activation_key}}
            )
            return user_activation_key
        else:
            return 'Invalid password'
    else:
        return 'Invalid username'

# @app.route('/logout', methods=['POST'])
# def


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.USER_CMS
        existing_user = users.find_one({'name': request.form['username']})

        if existing_user is None:
            users.insert(
                {'username': request.form['username'], 'password': request.form['password'], 'user_activation_key': '', 'permission': ''})
            session['username'] = request.form['username']
            return redirect(url_for('index'))

        return 'That username already exists!'

    return render_template('register.html')


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
            'id': str(news['_id']),
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


# @app.route('/news/update', methods=['PUT'])
# def update_news():
#     news = mongo.db.NEWS

#     number = request.json['number']
#     title = request.json['title']
#     subtitle = request.json['subtitle']
#     image_url = request.json['image_url']
#     item_url = request.json['item_url']
#     # news = [news for news in NEWS if news['title'] == title]

#     updated_news = news[0].update(
#         {news['number']:  number},
#         {'$inc': {
#             news['number']: number,
#             news['title']: title,
#             news['subtitle']: subtitle,
#             news['image_url']: image_url,
#             news['item_url']: item_url
#         }}
#     )

#     new_news = news.find_one({'_id': updated_news})
#     output = {
#         'number': new_news['number'],
#         'title': new_news['title'],
#         'subtitle': new_news['subtitle'],
#         'image_url': new_news['image_url'],
#         'item_url': new_news['item_url']
#     }
#     return jsonify({'result': output})


if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(host='210.211.109.211', port=3000, debug=True, threaded=True)
