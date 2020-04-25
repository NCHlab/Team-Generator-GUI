import os
from functools import wraps
import json

from flask_restful import Api, Resource, reqparse
from flask import Flask, Blueprint, request, Response
from generic_gen_teams import App

import requests
import threading

# from flask_restful import Api
# from myapi.resources.add_players import AddPlayers
# from myapi.resources.bar import Bar
# from myapi.resources.baz import Baz

app = Flask(__name__)
# api = Api(app)

blueprint = Blueprint("api", __name__, url_prefix="/v1")
api = Api(blueprint)
app.register_blueprint(blueprint)

obj = App()

# Require Token to use the API
ACCESS_TOKEN = os.environ["TMG_API_TOKEN"]
SLACK_TOKEN = os.environ["SLACK_TOKEN"]

list_of_teams = []


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        Auth = request.headers.get("Authorization", "")
        if not Auth:
            return {"message": "Authorization Required in Header"}, 401

        elif Auth[7:] != ACCESS_TOKEN:
            return {"message": "UnAuthorized Access! Credentials Incorrect"}, 401

        return f(*args, **kwargs)

    return decorated_function


def create_slack_modal(triggerid):
    # list_of_teams = obj.get_teams()

    test_modal_obj = {
        "trigger_id": triggerid,
        "view": {
            "type": "modal",
            "title": {"type": "plain_text", "text": "Team Generator"},
            "submit": {"type": "plain_text", "text": "Submit", "emoji": True},
            "close": {"type": "plain_text", "text": "Cancel", "emoji": True},
            "blocks": [
                {"type": "divider"},
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": ":ghost: *Select Players to generate a team*",
                    },
                },
                {"type": "divider"},
                {
                    "block_id": "channel_to_post",
                    "type": "input",
                    "optional": True,
                    "label": {
                        "type": "plain_text",
                        "text": "Select a channel to post the result on",
                    },
                    "element": {
                        "action_id": "send_to_channel",
                        "type": "channels_select",
                        "response_url_enabled": True,
                    },
                },
                {
                    "type": "input",
                    "block_id": "num_of_teams",
                    "label": {"type": "plain_text", "text": "Select Number Of Teams",},
                    "element": {
                        "type": "static_select",
                        "action_id": "num_of_teams_action",
                        "initial_option": {
                            "text": {"type": "plain_text", "text": "2"},
                            "value": "2",
                        },
                        "options": [
                            {
                                "text": {"type": "plain_text", "text": "1"},
                                "value": "1",
                            },
                            {
                                "text": {"type": "plain_text", "text": "2"},
                                "value": "2",
                            },
                            {
                                "text": {"type": "plain_text", "text": "3"},
                                "value": "3",
                            },
                            {
                                "text": {"type": "plain_text", "text": "4"},
                                "value": "4",
                            },
                            {
                                "text": {"type": "plain_text", "text": "5"},
                                "value": "5",
                            },
                            {
                                "text": {"type": "plain_text", "text": "6"},
                                "value": "6",
                            },
                        ],
                    },
                },
                {
                    "type": "input",
                    "block_id": "player_list",
                    "label": {"type": "plain_text", "text": "Players", "emoji": True,},
                    "element": {
                        "type": "checkboxes",
                        "action_id": "player_list_action",
                        "options": [
                            {
                                "text": {"type": "plain_text", "text": "Player1"},
                                "value": "Player1",
                            },
                            {
                                "text": {"type": "plain_text", "text": "Player2"},
                                "value": "Player2",
                            },
                        ],
                    },
                },
            ],
        },
    }

    return test_modal_obj


def send_slack_modal(triggerid):

    data = create_slack_modal(triggerid)

    res = requests.post(
        "https://slack.com/api/views.open",
        json=data,
        headers={
            "Content-Type": "application/json;charset=utf-8",
            "Authorization": SLACK_TOKEN,
        },
    )

    resp = res.json()

    print(resp)
    process_tg_modal_data(resp)


def process_tg_modal_data(data):

    response_url = data["payload"]["response_urls"][0]["response_url"]

    data = data["payload"]["view"]["state"]["values"]

    num_of_team = data["num_of_teams"]["num_of_teams_action"]["selected_option"][
        "value"
    ]
    players_data = data["player_list"]["player_list_action"]["selected_options"]

    list_of_players = []

    for player in players_data:
        list_of_players.append(player["value"])

    # print(data["payload"]["view"]["state"]["values"]["num_of_teams"]["num_of_teams_action"]["selected_option"]["value"])
    # data["payload"]["view"]["state"]["values"]["player_list"]["player_list_action"]["selected_options"]


class SlackData(Resource):
    def post(self):
        data = dict(request.form)

        print(data)
        return Response(status=200)


class SlackInitialMsg(Resource):
    def post(self):
        data = dict(request.form)

        triggerid = data["trigger_id"]

        # Start a different thread to process the post request for modal
        thread = threading.Thread(target=send_slack_modal, args=(triggerid,))
        thread.start()

        # Immediately send back empty HTTP 200 response
        return Response(status=200)


class GetTeams(Resource):
    # @login_required
    def get(self):

        global list_of_teams

        # Only Allow Authorised users to generate new team, otherwise return ucnahnged list
        Auth = request.headers.get("Authorization", "")
        if Auth[7:] == ACCESS_TOKEN:
            list_of_teams = obj.get_teams()

        elif not list_of_teams:
            list_of_teams = obj.get_teams()

        formatted_obj = {}
        for e, i in enumerate(list_of_teams):
            formatted_obj[f"TEAM {e+1}"] = i

        return formatted_obj


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
        super(AddPlayers, self).__init__()

    @login_required
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

    @login_required
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

    @login_required
    def post(self):
        args = self.reqparse.parse_args()
        resp = obj.update_mode(args["data"])

        if resp["status"] == "ok":
            response = ({"text": "Team Number Updated"}, 200)

        return response


class ActivatePlayers(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "data",
            type=str,
            required=True,
            help="Name of Players to activate <string seperated by comma> or all",
            location="json",
        )
        super(ActivatePlayers, self).__init__()

    @login_required
    def post(self):
        args = self.reqparse.parse_args()

        players_list = args["data"].split(",")
        players_list = [x.strip().title() for x in players_list]

        if "All" in players_list and len(players_list) == 1:
            resp = obj.set_all_players(activate=True)
            if resp["status"] == "ok":
                response = ({"text": "All Players Activated"}, 200)
            else:
                response = ({"text": "Internal Server Error"}, 500)
        else:

            returned_data = []
            for player in players_list:
                resp = obj.activate_player(player)
                returned_data.append(resp)

            if None not in returned_data and len(returned_data) == len(players_list):
                response = ({"text": "Player/s Activated"}, 200)
            elif None in returned_data and returned_data.count(None) != len(
                players_list
            ):
                returned_data = [x for x in returned_data if x is not None]
                activated_players = list(map(lambda x: x["name"], returned_data))
                activated_players = ", ".join(activated_players)
                response = (
                    {
                        "text": f"Some Players were not activated as they don't exist. Activated Players: {activated_players}"
                    },
                    404,
                )
            else:
                response = (
                    {"text": f"No Players were activated as they don't exist"},
                    404,
                )

        return response


class DeactivatePlayers(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "data",
            type=str,
            required=True,
            help="Name of Players to activate <string seperated by comma> or all",
            location="json",
        )
        super(DeactivatePlayers, self).__init__()

    @login_required
    def post(self):
        args = self.reqparse.parse_args()

        players_list = args["data"].split(",")
        players_list = [x.strip().title() for x in players_list]

        if "All" in players_list and len(players_list) == 1:
            resp = obj.set_all_players(activate=False)
            if resp["status"] == "ok":
                response = ({"text": "All Players Deactivated"}, 200)
            else:
                response = ({"text": "Internal Server Error"}, 500)
        else:

            returned_data = []
            for player in players_list:
                resp = obj.deactivate_player(player)
                returned_data.append(resp)

            if None not in returned_data and len(returned_data) == len(players_list):
                response = ({"text": "Player/s Deactivated"}, 200)
            elif None in returned_data and returned_data.count(None) != len(
                players_list
            ):
                returned_data = [x for x in returned_data if x is not None]
                deactivated_players = list(map(lambda x: x["name"], returned_data))
                deactivated_players = ", ".join(deactivated_players)
                response = (
                    {
                        "text": f"Some Players were not deactivated as they don't exist. Deactivated Players: {deactivated_players}"
                    },
                    404,
                )
            else:
                response = (
                    {"text": f"No Players were deactivated as they don't exist"},
                    404,
                )

        return response


class AddToBalance(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "data",
            type=str,
            required=True,
            help="player/s to add was not provided <players separated by a comma>",
            location="json",
        )
        super(AddToBalance, self).__init__()

    @login_required
    def post(self):
        args = self.reqparse.parse_args()

        players_list = args["data"].split(",")
        players_list = [x.strip().title() for x in players_list]

        returned_data = []
        for player in players_list:
            resp = obj.add_to_balance(player)
            returned_data.append(resp)

        players_ok = list(
            filter(
                lambda x: x["status"] == "ok" or x["status"] == "ok_2", returned_data
            )
        )

        if len(returned_data) == len(players_ok):
            players_ok = list(map(lambda x: x["name"], players_ok))
            response = (
                {"text": f"Users Added to Balance: {', '.join(players_ok)}"},
                201,
            )
        else:
            players_error = list(
                filter(lambda x: x["status"] == "error", returned_data)
            )
            players_error = list(map(lambda x: x["name"], players_error))
            response = (
                {"text": f"Players do not exist: {', '.join(players_error)}"},
                409,
            )

        return response


class DeleteFromBalance(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "data",
            type=str,
            required=True,
            help="player/s to delete was not provided <players separated by a comma>",
            location="json",
        )
        super(DeleteFromBalance, self).__init__()

    @login_required
    def delete(self):
        args = self.reqparse.parse_args()

        players_list = args["data"].split(",")
        players_list = [x.strip().title() for x in players_list]

        returned_data = []
        for player in players_list:
            resp = obj.delete_from_balance(player)
            returned_data.append(resp)

        players_ok = list(filter(lambda x: x["status"] == "ok", returned_data))

        if len(returned_data) == len(players_ok):
            players_ok = list(map(lambda x: x["name"], players_ok))
            response = ({"text": f"Users Removed: {', '.join(players_ok)}"}, 200)
        else:
            players_error = list(
                filter(lambda x: x["status"] == "error", returned_data)
            )
            players_error = list(map(lambda x: x["name"], players_error))
            response = (
                {
                    "text": f"Players don't exist in balance list: {', '.join(players_error)}"
                },
                404,
            )

        return response


api.add_resource(GetTeams, "/get_teams")
api.add_resource(AddPlayers, "/add")
api.add_resource(DeletePlayers, "/delete")
api.add_resource(UpdateTeamNum, "/update_team_number")
api.add_resource(ActivatePlayers, "/activate")
api.add_resource(DeactivatePlayers, "/deactivate")
api.add_resource(AddToBalance, "/add_b")
api.add_resource(DeleteFromBalance, "/delete_b")
api.add_resource(SlackData, "/slack")
api.add_resource(SlackInitialMsg, "/mainmodal")

# api.add_resource(Baz, '/Baz', '/Baz/<string:id>')

if __name__ == "__main__":
    app.run(debug=True)
