from jsonEncoder import JSONEncoder

from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)

app.secret_key = 'mykey'
api = Api(app)


from database import DB
from flask_pymongo import PyMongo

app.config["MONGO_URI"] = DB.URI
mongo = PyMongo(app)
print(DB.URI)




jwt = JWT(app, authenticate, identity)

items = []


mongo.init_app(app)


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
    type=float,
    required=True,
    help="This field cannot be left blank!"
    )

    @jwt_required() 
    def get(self, name):
        # for item in items:
        #     if item['name'] == name:
        #         return item
        item = next(filter(lambda item: item['name']== name ,items), None)
        return {'Item' : item}, 200 if item else 404
    
    def post(self, name):
        if next(filter(lambda item: item['name']  == name, items), None):
            return {"4" : "An item with the name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()

        item = {
            'name': name,
            'price': data['price']
        }
        
        mongo.db.items.insert(item)
        # items.append(item)
        print (item)
        return JSONEncoder().encode(item), 201
    
    def delete(self,name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'Message' : "Item Deleted"}

    def put(self, name):

        data = Item.parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
        else:
            item.update(data)
        return item

class ItemList(Resource):
    def get(self):
        return {'Items' : items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')


app.run(port=5000, debug=True)
