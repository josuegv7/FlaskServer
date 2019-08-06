
class DB:
    URI = "mongodb://pymongo_user:password1@ds259577.mlab.com:59577/pymongo"
   
    

# class DB(object):
#     # URI = "mongodb://pymongo_user:password1@ds259577.mlab.com:59577/pymongo"
#     # URI = "mongodb://pymongo_user:password1@ds259577.mlab.com:59577/"

    # @staticmethod
    # def init():
    #     client = pymongo.MongoClient(DB.URI)
    #     DB.DATABASE = client['pymongo']

#     @staticmethod
#     def insert(collection, data):
#         DB.DATABASE[collection].insert(data)

#     @staticmethod
#     def find_one(collection, query):
#         return DB.DATABASE[collection].find_one(query)
