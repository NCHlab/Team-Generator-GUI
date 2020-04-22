from flask_restful import Api, Resource, reqparse
from flask import Flask, Blueprint
from generic_gen_teams import App

# from flask_restful import Api
# from myapi.resources.foo import Foo
# from myapi.resources.bar import Bar
# from myapi.resources.baz import Baz

app = Flask(__name__)
# api = Api(app)

blueprint = Blueprint("api", __name__, url_prefix="/v1")
api = Api(blueprint)
app.register_blueprint(blueprint)

obj = App()

# Require Token to use the API
# Use base /api/v1


class GetTeams(Resource):
    def get(self):

        return obj.get_teams()


class AddPlayers(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "data",
            type=str,
            required=True,
            help="player/s to add was not provided <players separated by a comma>",
            location="json",
        )
        # self.reqparse.add_argument('description', type=str, default="",
        #                            location='json')
        super(AddPlayers, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        # print(args["players"])

        players_list = args["data"].split(",")
        players_list = [x.strip().title() for x in players_list]
        # print(players_list)

        returned_data = []
        for player in players_list:
            resp = obj.add_mode(player)
            returned_data.append(resp)

        players_ok = list(filter(lambda x: x["status"] == "ok", returned_data))

        if len(returned_data) == len(players_ok):
            players_ok = list(map(lambda x: x["name"], players_ok))
            response = ({"text": f"Users Added: {', '.join(players_ok)}"}, 201)
        else:
            players_error = list(
                filter(lambda x: x["status"] == "error", returned_data)
            )
            players_error = list(map(lambda x: x["name"], players_error))
            response = (
                {"text": f"Players already Exist: {', '.join(players_error)}"},
                409,
            )

        return response


class DeletePlayers(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "data",
            type=str,
            required=True,
            help="player/s to delete was not provided <players separated by a comma>",
            location="json",
        )
        super(DeletePlayers, self).__init__()

    def delete(self):
        args = self.reqparse.parse_args()

        players_list = args["data"].split(",")
        players_list = [x.strip().title() for x in players_list]

        returned_data = []
        for player in players_list:
            resp = obj.delete_mode(player)
            returned_data.append(resp)

        players_ok = list(filter(lambda x: x["status"] == "ok", returned_data))

        if len(returned_data) == len(players_ok):
            players_ok = list(map(lambda x: x["name"], players_ok))
            response = ({"text": f"Users Deleted: {', '.join(players_ok)}"}, 200)
        else:
            players_error = list(
                filter(lambda x: x["status"] == "error", returned_data)
            )
            players_error = list(map(lambda x: x["name"], players_error))
            response = (
                {"text": f"Players don't exist: {', '.join(players_error)}"},
                404,
            )

        return response


class UpdateTeamNum(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "data",
            type=int,
            required=True,
            help="Number of Players <int>",
            location="json",
        )
        super(UpdateTeamNum, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        resp = obj.update_mode(args["data"])

        if resp["status"] == "ok":
            response = ({"text": "Team Number Updated"}, 200)

        return response


api.add_resource(GetTeams, "/get_teams", "/")
api.add_resource(AddPlayers, "/add", "/")
api.add_resource(DeletePlayers, "/delete", "/")
api.add_resource(UpdateTeamNum, "/update_team_number", "/")
# api.add_resource(AddPlayers, "/activate", "/")
# api.add_resource(AddPlayers, "/deactivate", "/")

# api.add_resource(Baz, '/Baz', '/Baz/<string:id>')

if __name__ == "__main__":
    app.run(debug=True)
