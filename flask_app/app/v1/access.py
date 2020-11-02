from app.v1 import app , api , Resource , JWT , jwt_required
from app.v1.security.auth import authenticate , identity
api.secret_key = 'aR4QpGzGgHcY7haxHT9g89Puph3NgvNBBMBMnHEC'

jwt = JWT(app , authenticate , identity)

class Access(Resource):

    @jwt_required()   
    def get(self):
        return 'Works fine'

api.add_resource(Access,'/access')


# @app.route('/')
# def index():
#     return 'Hello World !'

# @app.route('/healthz')
# def health():
#     return 'Up and Running !!!'