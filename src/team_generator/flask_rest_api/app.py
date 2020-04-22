from flask_restful import Api, Resource, reqparse
from flask import Flask
from generic_gen_teams import App
# from flask_restful import Api
# from myapi.resources.foo import Foo
# from myapi.resources.bar import Bar
# from myapi.resources.baz import Baz

app = Flask(__name__)
api = Api(app)

obj = App()

# Require Token to use the API
# Use base /api/v1

class GetTeams(Resource):
    def get(self):
        
        return obj.get_teams()


class AddPlayers(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('users', type=str, required=True,
                                   help="User/s was not provided",
                                   location='json')
        # self.reqparse.add_argument('description', type=str, default="",
        #                            location='json')
        super(AddPlayers, self).__init__()


    def post(self):
        args = self.reqparse.parse_args()
        print(args)
        return {"text":"Valid"}

api.add_resource(GetTeams, '/get_teams', '/')
api.add_resource(AddPlayers, '/add', '/')
# api.add_resource(Baz, '/Baz', '/Baz/<string:id>')

if __name__ == '__main__':
    app.run(debug=True)