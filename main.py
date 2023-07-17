from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from, LazyJSONEncoder
from manager.user_base import UserBase
from manager.team_base import TeamBase
from manager.project_board_base import ProjectBoardBase
import json

app = Flask(__name__)

app.config["SWAGGER"] = {"title": "Project Planner API", "uiversion": 2}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec_1",
            "route": "/apispec_1.json",
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/swagger/",
}

app.json_encoder = LazyJSONEncoder
swagger = Swagger(app, config=swagger_config)

user_base = UserBase()
team_base = TeamBase()
project_board_base = ProjectBoardBase()


@app.route('/create_user', methods=['POST'])
@swag_from('swagger_yaml/create_user.yml')
def create_user():
    request_data = request.get_json()
    response = user_base.create_user(json.dumps(request_data))
    return response


@app.route('/list_users', methods=['GET'])
@swag_from('swagger_yaml/list_users.yml')
def list_users():
    response = user_base.list_users()
    return response


@app.route('/describe_user', methods=['POST'])
@swag_from('swagger_yaml/describe_user.yml')
def describe_user():
    request_data = request.get_json()
    response = user_base.describe_user(json.dumps(request_data))
    return response


@app.route('/update_user', methods=['POST'])
@swag_from('swagger_yaml/update_user.yml')
def update_user():
    request_data = request.get_json()
    response = user_base.update_user(json.dumps(request_data))
    return response


@app.route('/get_user_teams', methods=['POST'])
@swag_from('swagger_yaml/get_user_teams.yml')
def get_user_teams():
    request_data = request.get_json()
    response = user_base.get_user_teams(json.dumps(request_data))
    return response


@app.route('/create_team', methods=['POST'])
@swag_from('swagger_yaml/create_team.yml')
def create_team():
    request_data = request.get_json()
    response = team_base.create_team(json.dumps(request_data))
    return response


@app.route('/list_teams', methods=['GET'])
@swag_from('swagger_yaml/list_teams.yml')
def list_teams():
    response = team_base.list_teams()
    return response


@app.route('/describe_team', methods=['POST'])
@swag_from('swagger_yaml/describe_team.yml')
def describe_team():
    request_data = request.get_json()
    response = team_base.describe_team(json.dumps(request_data))
    return response


@app.route('/update_team', methods=['POST'])
@swag_from('swagger_yaml/update_team.yml')
def update_team():
    request_data = request.get_json()
    response = team_base.update_team(json.dumps(request_data))
    return response


@app.route('/add_users_to_team', methods=['POST'])
@swag_from('swagger_yaml/add_users_to_team.yml')
def add_users_to_team():
    request_data = request.get_json()
    response = team_base.add_users_to_team(json.dumps(request_data))
    return response


@app.route('/remove_users_from_team', methods=['POST'])
@swag_from('swagger_yaml/remove_users_from_team.yml')
def remove_users_from_team():
    request_data = request.get_json()
    response = team_base.remove_users_from_team(json.dumps(request_data))
    return response


@app.route('/list_team_users', methods=['POST'])
@swag_from('swagger_yaml/list_team_users.yml')
def list_team_users():
    request_data = request.get_json()
    response = team_base.list_team_users(json.dumps(request_data))
    return response


@app.route('/create_board', methods=['POST'])
@swag_from('swagger_yaml/create_board.yml')
def create_board():
    request_data = request.get_json()
    response = project_board_base.create_board(json.dumps(request_data))
    return response


@app.route('/close_board', methods=['POST'])
@swag_from('swagger_yaml/close_board.yml')
def close_board():
    request_data = request.get_json()
    response = project_board_base.close_board(json.dumps(request_data))
    return response


@app.route('/add_task', methods=['POST'])
@swag_from('swagger_yaml/add_task.yml')
def add_task():
    request_data = request.get_json()
    response = project_board_base.add_task(json.dumps(request_data))
    return response


@app.route('/update_task_status', methods=['POST'])
@swag_from('swagger_yaml/update_task_status.yml')
def update_task_status():
    request_data = request.get_json()
    response = project_board_base.update_task_status(json.dumps(request_data))
    return response


@app.route('/list_boards', methods=['POST'])
@swag_from('swagger_yaml/list_boards.yml')
def list_boards():
    request_data = request.get_json()
    response = project_board_base.list_boards(json.dumps(request_data))
    return response


@app.route('/export_board', methods=['POST'])
@swag_from('swagger_yaml/export_board.yml')
def export_board():
    request_data = request.get_json()
    response = project_board_base.export_board(json.dumps(request_data))
    return response


if __name__ == '__main__':
    app.run(debug=True)
