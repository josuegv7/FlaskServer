import os
import datetime
from jsonEncoder import JSONEncoder
from bson.json_util import dumps, ObjectId

from secret_Key import SECRET

from flask_pymongo import PyMongo
from database import DB

from flask_restful import Resource, Api, reqparse

from flask import Flask, request, jsonify
from flask_cors import CORS



# Adding JWT TO Server:
from flask_jwt_extended import (JWTManager,create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity)
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['PROPAGTE_EXCEPTIONS'] = True
api = Api(app)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# DB Connection:
app.config["MONGO_URI"] = DB.URI
mongo = PyMongo(app)


# JWT Integration:
app.config['JWT_SECRET_KEY'] = SECRET.SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)

flask_bcrypt = Bcrypt(app)
jwt = JWTManager(app)

@jwt.unauthorized_loader
def unauthorized_response(callback):
    return jsonify({
        'ok': False,
        'Message': 'Missing Authorization Header'
    }), 401


@app.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    ''' refresh token endpoint '''
    current_user = get_jwt_identity()
    ret = {
        'token': create_access_token(identity=current_user)
    }
    return jsonify({'ok': True, 'data': ret}), 200



class Auth(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        # required=True,
                        help="The Username Field cannot be left blank!"
                        )
    parser.add_argument('password',
                        type=str,
                        # required=True,
                        help="The Email Field cannot be left blank!"
                        )

    def post(self):
        data = Auth.parser.parse_args()
        user_auth_data = {
            'username': data['username'],
            'password': data['password']
        }
        print(user_auth_data)
        user_found = mongo.db.users.find_one(
            {'username': data['username']}
        )
        print(user_found)

        if user_found and flask_bcrypt.check_password_hash(user_found['password'], data['password']):
            del user_found['password']
            access_token = create_access_token(identity=data)
            refresh_token = create_refresh_token(identity=data)
            user_found['JWT_token'] = access_token
            user_found['refresh_token'] = refresh_token
            # return jsonify({'Message': True, 'data': JSONEncoder().encode(user_found)}), 200
            return JSONEncoder().encode(user_found), 200

        else:
            return jsonify({'Message': False, 'message': 'invalid username or password'}), 401


class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        # required=True,
                        help="The Username Field cannot be left blank!"
                        )
    parser.add_argument('email',
                        type=str,
                        # required=True,
                        help="The Email Field cannot be left blank!"
                        )
    parser.add_argument('password',
                        type=str,
                        # required=True,
                        help="The Password Field cannot be left blank!"
                        )

    @jwt_required
    def get(self):
        data = User.parser.parse_args()
        print(data)
        user_data = {
            '_id': data['_id']
        }
        user_found = mongo.db.items.find_one(
            {'_id': ObjectId(data['_id'])}
        )
        print(user_found)
        return JSONEncoder().encode(user_found), 200

    def post(self):
        data = User.parser.parse_args()
        user_data = {
            'email': data['email'],
            'username': data['username'],
            'password': data['password']
        }
        print(user_data)
        user_data['password'] = flask_bcrypt.generate_password_hash(
            user_data['password'])
        mongo.db.users.find_one_and_update(
            {'username': data['username']}, {'$set': user_data}, upsert=True
        )
        # return JSONEncoder().encode(item), 201
        return {'Message': "User Created"}

    @jwt_required
    def put(self):
        data = User.parser.parse_args()
        print(data)
        user_data = {
            'name': data['name'],
            'email': data['email'],
            'password': data['password']
        }
        print(user_data)
        user_data['password'] = flask_bcrypt.generate_password_hash(
            user_data['password'])
        mongo.db.items.find_one_and_update(
            {'_id': ObjectId(data['_id'])}, {'$set': user_data}
        )
        return JSONEncoder().encode(item), 200

    @jwt_required
    def delete(self):
        data = User.parser.parse_args()
        print(data)
        user_data = {
            '_id': data['_id']
        }
        mongo.db.users.find_one_and_delete(
            {'_id': ObjectId(data['_id'])}
        )
        return {'Message': "User Deleted"}, 200 if user_data != None else 404







class Item(Resource):
    # Fields for item document:
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        # required=True,
                        help="The Name Field cannot be left blank!"
                        )
    parser.add_argument('price',
                        type=float,
                        # required=True,
                        help="The Price Field cannot be left blank!"
                        )
    parser.add_argument('quantity',
                        type=str,
                        # required=True,
                        help="The Quantity Field cannot be left blank!"
                        )
    parser.add_argument('store',
                        type=str,
                        # required=True,
                        help="The Store Field cannot be left blank!"
                        )
    parser.add_argument('_id',
                        type=str
                        )

    def get(self):
        data = Item.parser.parse_args()
        item = {
            '_id': data['_id']
        }
        item_found = mongo.db.items.find_one(
            {'_id': ObjectId(data['_id'])}
        )
        return JSONEncoder().encode(item_found), 200
    
    @jwt_required
    def post(self):
        data = Item.parser.parse_args()
        item = {
            'name': data['name'],
            'price': data['price'],
            'quantity': data['quantity'],
            'store': data['store']
        }
        mongo.db.items.find_one_and_update(
            {'name': data['name']}, {'$set': item}, upsert=True
        )
        return JSONEncoder().encode(item), 201

    def delete(self):
        data = Item.parser.parse_args()
        print(data)
        item = {
            '_id': data['_id']
        }
        mongo.db.items.find_one_and_delete(
            {'_id': ObjectId(data['_id'])}
        )
        return {'Message': "Item Deleted"}, 200 if item != None else 404

    def put(self):
        data = Item.parser.parse_args()
        print(data)
        item = {
            'name': data['name'],
            'price': data['price'],
            'quantity': data['quantity'],
            'store': data['store']
        }
        print(item)
        mongo.db.items.find_one_and_update(
            {'_id': ObjectId(data['_id'])}, {'$set': item}
        )
        return JSONEncoder().encode(item), 200


class Project(Resource):
    # Fields for item document:
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        # required=True,
                        help="The Name Field cannot be left blank!"
                        )
    parser.add_argument('items',
                        type=str,
                        # required=True,
                        help="The Items Field cannot be left blank!"
                        )
    parser.add_argument('project_date',
                        type=str,
                        # required=True,
                        help="The Project Date Field cannot be left blank!"
                        )
    parser.add_argument('project_status',
                        type=str,
                        # required=True,
                        help="The Project Status Field cannot be left blank!"
                        )
    parser.add_argument('_id',
                        type=str
                        )

    # ROUTES FOR THE:
    # @jwt_required()

    def get(self, name):
        project = mongo.db.projects.find_one({'name': name})
        return{'Project': JSONEncoder().encode(project)}, 200 if project != None else 404

    def get(self):
        data = Project.parser.parse_args()
        print(data)
        project = {
            # 'name': data['name'],
            # 'price': data['price'],
            # 'quantity': data['quantity'],
            # 'store': data['store'],
            '_id': data['_id']
        }
        project_found = mongo.db.projects.find_one(
            # {"_id.$oid": data['_id']}
            {'_id': ObjectId(data['_id'])}
        )
        print(project_found)
        return JSONEncoder().encode(project_found), 200

    def post(self):
        data = Project.parser.parse_args()
        project = {
            'name': data['name'],
            'items': data['items'],
            'project_date': data['project_date'],
            'project_status': data['project_status']
        }
        mongo.db.projects.find_one_and_update(
            {'name': data['name']}, {'$set': project}, upsert=True
        )
        return JSONEncoder().encode(project), 201

    def delete(self):
        data = Project.parser.parse_args()
        print("Delete")
        print(data)
        project = {
            # 'name': data['name'],
            # 'price': data['price'],
            # 'quantity': data['quantity'],
            # 'store': data['store'],
            '_id': data['_id']
        }
        # print(item)
        mongo.db.projects.find_one_and_delete(
            {'_id': ObjectId(data['_id'])}
        )
        return {'Message': "Project Deleted"}, 200 if item != None else 404

    def put(self):
        data = Project.parser.parse_args()
        print(data)
        project = {
            'name': data['name'],
            'items': data['items'],
            'project_date': data['project_date'],
            'project_status': data['project_status'],
            # '_id': data['_id']
        }
        print(project)
        mongo.db.projects.find_one_and_update(
            {'_id': ObjectId(data['_id'])}, {'$set': project}
        )
        return JSONEncoder().encode(project), 200


class ItemList(Resource):
    def get(self):
        items = dumps(mongo.db.items.find())
        return jsonify(items)


class ProjectList(Resource):
    def get(self):
        projects = dumps(mongo.db.projects.find())
        return jsonify(projects)






# Routes:
api.add_resource(Item, '/item')
api.add_resource(ItemList, '/items')

api.add_resource(Project, '/project')
api.add_resource(ProjectList, '/projects')

# Route Create User:
api.add_resource(User, '/profile')
# Auth Routes
api.add_resource(Auth, '/login')



app.run(port=5000, debug=True)
