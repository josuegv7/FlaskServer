from jsonEncoder import JSONEncoder
from bson.json_util import dumps, loads


from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity
app = Flask(__name__)
app.secret_key = 'mykey'
api = Api(app)

# DB Connection:
from database import DB
from flask_pymongo import PyMongo
app.config["MONGO_URI"] = DB.URI
mongo = PyMongo(app)
# mongo.init_app(app)

# Import Documents / Routes:
import documents
# 
jwt = JWT(app, authenticate, identity)


class Item(Resource):
    # Fields for item document:
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="The Price Field cannot be left blank!"
                        )
    parser.add_argument('quantity',
                        type=int,
                        required=True,
                        help="The Quantity Field cannot be left blank!"
                        )
    parser.add_argument('store',
                        type=str,
                        required=True,
                        help="The Store Field cannot be left blank!"
                        )
# ROUTES FOR THE API:
    # @jwt_required()

    def get(self, name):
        # for item in items:
        #     if item['name'] == name:
        #         return item
        # item = next(filter(lambda item: item['name']== name ,items), None)
        # return {'Item' : item}, 200 if item else 404

        item = mongo.db.items.find_one({'name': name})
        return{'Item': JSONEncoder().encode(item)}, 200 if item != None else 404

    def post(self, name):
        # if next(filter(lambda item: item['name']  == name, items), None):
        #     return {"4" : "An item with the name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()
        print(data)

        item = {
            'name': name,
            'price': data['price'],
            'quantity': data['quantity'],
            'store': data['store']
        }

        mongo.db.items.find_one_and_update(
            {'name': name}, {'$set': item}, upsert=True)
        # items.append(item)
        # print (item)
        return JSONEncoder().encode(item), 201

    def delete(self, name):
        item = {'name': name}
        mongo.db.items.delete_one(item)
        return {'Message': "Item Deleted"}, 200 if item != None else 404

        # old code:
        # global items
        # items = list(filter(lambda x: x['name'] != name, items))
        # return {'Message' : "Item Deleted"}

        # Don't need this route b/c the insert is either updating a document or inserting a new one is the name is not found.
        # def put(self, name):

        #     data = Item.parser.parse_args()
        #     item = next(filter(lambda x: x['name'] == name, items), None)
        #     if item is None:
        #         item = {'name': name, 'price': data['price']}
        #     else:
        #         item.update(data)
        #     return item


class Project(Resource):
    # Fields for item document:
    parser = reqparse.RequestParser()
    parser.add_argument('items',
                        type=str,
                        required=True,
                        help="The Items Field cannot be left blank!"
                        )
    parser.add_argument('project_date',
                        type=str,
                        required=True,
                        help="The Project Date Field cannot be left blank!"
                        )
    parser.add_argument('project_status',
                        type=str,
                        required=True,
                        help="The Project Status Field cannot be left blank!"
                        )

    # ROUTES FOR THE:
    # @jwt_required()
    def get(self, name):
        project = mongo.db.projects.find_one({'name': name})
        return{'Project': JSONEncoder().encode(project)}, 200 if project != None else 404

    def post(self, name):

        data = Project.parser.parse_args()
        

        project = {
            'name': name,
            'items': data['items'],
            'project_date': data['project_date'],
            'project_status': data['project_status']
        }

        mongo.db.projects.find_one_and_update(
        {'name': name}, {'$set': project}, upsert=True)
        # items.append(item)
        # print (item)
        return JSONEncoder().encode(project), 201

    def delete(self, name):
        project = {'name': name}
        mongo.db.projects.delete_one(project)
        return {'Message': "Project was deleted"}, 200 if project != None else 404


class ItemList(Resource):
    def get(self):
        items = dumps(mongo.db.items.find())
        return {'Items': items}, 200 if items != None else 404
        # return items


class ProjectList(Resource):
    def get(self):
        projects = dumps(mongo.db.projects.find())
        return {'Projects': projects}, 200 if projects != None else 404



# Routes:
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

api.add_resource(Project, '/project/<string:name>')
api.add_resource(ProjectList, '/projects')







app.run(port=5000, debug=True)
