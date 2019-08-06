from user import User


users = [
    User(1,'bob', 'asdf')
]


username_mapping = {u.username: u for u in users}

userid_mapping = {u.id: u for u in users}


# users = [
#     {
#         'id': 1,
#         'username': 'Bob',
#         'password': 'asdf'
#     }
# ]

# username_mapping = {
#     'bob': {
#         'id': 1,
#         'username': 'Bob',
#         'password': 'asdf'
#     }
# }

# userid_mapping = {
#     1 : {
#         'id': 1,
#         'username': 'Bob',
#         'password': 'asdf'
#     }
# }


def authenticate(username, password):
    user = username_mapping.get(username, None)
    if user and user.password == password:
        return user

# payload in the function below is the JWT content that is recieved 
def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)
