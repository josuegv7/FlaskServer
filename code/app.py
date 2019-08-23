from jsonEncoder import JSONEncoder
from bson.json_util import dumps, loads
from bson.objectid import ObjectId

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity
app = Flask(__name__)
app.secret_key = 'mykey'
api = Api(app)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# DB Connection:
from database import DB
from flask_pymongo import PyMongo
app.config["MONGO_URI"] = DB.URI
mongo = PyMongo(app)

# Import Documents / Routes:
 
jwt = JWT(app, authenticate, identity)


class Item(Resource):
    # Fields for item document:
    parser = reqparse.RequestParser()
    print(parser)
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
# ROUTES FOR THE API:
    # @jwt_required()

    def get(self):
        data = Item.parser.parse_args()
        print(data)
        item = {
            # 'name': data['name'],
            # 'price': data['price'],
            # 'quantity': data['quantity'],
            # 'store': data['store'],
            '_id': data['_id']
        }
        item_found = mongo.db.items.find_one(
            # {"_id.$oid": data['_id']}
            {'_id': ObjectId(data['_id'])}
        )
        print(item_found)
        return JSONEncoder().encode(item_found), 200
        
     
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
            # 'name': data['name'],
            # 'price': data['price'],
            # 'quantity': data['quantity'],
            # 'store': data['store'],
            '_id': data['_id']
        }
        # print(item)
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
            'store': data['store'],
            # '_id': data['_id']
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



app.run(port=5000, debug=True)
