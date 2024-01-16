# packages
import GPSystem.GPmain
from flask import Flask, redirect, render_template, request, make_response
from flask_socketio import SocketIO, emit
import math
import time
import asyncio
from flask_bcrypt import Bcrypt
import random
import requests
import string
import urllib
import json
import atexit

# credential variables
import Client_Credentials as client

# scripts
from crap.Initialization import *
from crap.osu_crap.Match import Match

# data imports
from crap.osu_crap.PlayerList import PlayerList
from crap.osu_crap.Player import Player
from crap.osu_crap.MatchHandler import MatchHandler

from crap.gentrys_quest_crap.GentrysQuestClassicManager import GentrysQuestClassicManager

from crap.ServerData import ServerData
from crap.ApiType import ApiType

initialize_files()  # setup necessary files

# global vars
#   osu data
live_player_status = {}
player_data = PlayerList
print("Loading osu players")
for id_ref in PlayerList.Player_json.keys():  # manual main loop to avoid circular import
    Player(id_ref)

match_handler = MatchHandler()
match_handler.load()

#   Gentrys Quest data
gq_version = requests.get("https://api.github.com/repos/GDcheeriosYT/Gentrys-Quest-Python/releases/latest").json()[
    "name"]
GQC_manager = GentrysQuestClassicManager(gq_version)

# flask set up
app = Flask(  # Create a flask app
    __name__,
    template_folder='templates',  # Name of html file folder
    static_folder='static'  # Name of directory for static files
)
app.config['SECRET_KEY'] = "hugandafortnite"
socketio = SocketIO(app, logger=False)
bcrypt = Bcrypt(app)


# define at exit action
def exit_func():
    player_data.unload()
    match_handler.unload()


atexit.register(exit_func)


# token api stuff
@app.route("/api/generate-token")
async def generate_token():
    ServerData.api_call(ApiType.TokenGenerate)

    token = ""
    for i in range(32):
        token += random.choice(string.ascii_letters)

    ServerData.add_token(token)
    return token


@app.route("/api/clear-tokens")
async def clear_tokens():
    ServerData.clear_tokens()


@app.route("/api/delete-token/<token>", methods=["POST"])
async def delete_token(token):
    ServerData.remove_token(token)


@app.route("/api/verify-token/<token>")
async def verify_token(token):
    return ServerData.verify_token(token)


# osu auth stuff
@app.route('/code_grab')
def code_grab():
    ServerData.api_call(ApiType.OsuAuthenticate)

    code = urllib.parse.parse_qs(request.query_string.decode('utf-8'))["code"][0]

    response = requests.post("https://osu.ppy.sh/oauth/token",
                             json={'client_id': client.osu_client_id,
                                   'code': code,
                                   'client_secret': client.osu_secret,
                                   'grant_type': 'authorization_code',
                                   'redirect_uri': f"{client.domain}/code_grab",
                                   'scope': 'public'},
                             headers={'Accept': 'application/json',
                                      'Content-Type': 'application/json'})

    response = response.json()

    user_info = requests.get("https://osu.ppy.sh/api/v2/me/osu", headers={
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {response['access_token']}"
    }).json()

    info = {
        "username": user_info["username"],
        "id": user_info["id"],
        "avatar": f"https://a.ppy.sh/{user_info['id']}",
        "background url": user_info["cover_url"]
    }

    return redirect(f"/account/create?osu_info={json.dumps(info)}")


# account api
@app.route("/api/account/create/<username>+<password>")
async def account_create(username,
                         password,
                         osu_id=0,
                         about_me=""):
    ServerData.api_call(ApiType.AccountCreate)

    account_count = len(os.listdir("accounts")) + 1
    password = str(password)
    profile_picture = random.choice(pfp_options)
    about_me = about_me
    gqdata = {}
    gqcdata = {}
    backrooms_data = {}
    password = str(bcrypt.generate_password_hash(password))
    metadata = {
        "osu id": osu_id,
        "Gentry's Quest Classic data": gqcdata,
        "Gentry's Quest data": gqdata,
        "backrooms data": backrooms_data,
        "about me": about_me
    }
    account_data = {
        "pfp url": profile_picture,
        "username": username,
        "password": password[2:-1],
        "metadata": metadata
    }
    with open(f"accounts/{account_count}.json", "w+") as file:
        json.dump(account_data, file, indent=4, sort_keys=False)

    return account_data


@app.route("/api/password-cache-gen")
async def password_cache_gen():
    return render_template("password_gen.html",
                           password="poop")


@app.route("/api/password-cache-gen", methods=["POST"])
async def password_cache_gen_post():
    password = request.form.get("password")
    return render_template("password_gen.html", password=str(bcrypt.generate_password_hash(password)))


@app.route("/api/account/receive-account/<id_or_name>")  # receive account with id
def get_account_with_id_or_name(id_or_name):
    ServerData.api_call(ApiType.AccountReceive)

    for file in os.listdir("accounts"):
        account_data = json.load(open(f"accounts/{file}", "r"))
        if file[:-5] == id_or_name:
            return {str(file[:-5]): account_data}
        if account_data["username"] == id_or_name:
            return {str(file[:-5]): account_data}

    return "Not Found"


@app.route("/api/account/login/<username>+<password>")
async def login(username, password):
    ServerData.api_call(ApiType.AccountLogIn)

    for file in os.listdir("accounts"):
        account_info = json.load(open(f"accounts/{file}", encoding="utf-8"))
        account_info["id"] = int(file[:-5])
        if account_info["username"] == username:
            if bcrypt.check_password_hash(account_info["password"], password):
                return account_info
    return "incorrect info"


# player score grab api crap
@app.route("/api/grab/<match_name>")
async def grabber(match_name):
    ServerData.api_call(ApiType.OsuMatchGrab)

    match = MatchHandler.get_match(match_name)

    new_dict = {}
    for player in match.players:
        new_dict[player.id] = {
            "background url": player.background,
            "score": match.get_score(player),
            "rank": player.rank,
            "playcount": match.get_playcount(player),
            "liveStatus": None if int(player.id) not in live_player_status else live_player_status[int(player.id)],
        }

        for team in match.team_data:
            for player_ref in team.players:
                new_dict[player_ref.id]["team"] = f"{team.jsonify()}"

    return new_dict


def get_osu_id(userID):
    return json.load(open(f"accounts/{userID}.json",
                          "r"))["metadata"]["osu id"]


@socketio.on('event')
def test_socket(data):
    print(data)


@socketio.on('update client status')
def update_client_status(data):
    print("updating", data["user"])
    live_player_status[data["user"]] = data


@socketio.on('match data get')
def get_livestatus(data):
    global websocket_uses
    websocket_uses += 1
    global api_uses
    api_uses -= 1
    emit('match data receive', asyncio.run(grabber(data)), ignore_queue=True)


@socketio.on('old match data get')
def get_livestatus(data):
    global websocket_uses
    websocket_uses += 1
    global api_uses
    api_uses -= 1
    emit('match data receive', asyncio.run(old_grabber(data)), ignore_queue=True)


# all players api updater
@app.route("/api/grab/<ids>", methods=['GET'])
async def all_grabber(ids):
    global api_uses
    api_uses += 1
    id_list = ids.split("+")

    data = PlayerList.get_users(id_list)
    player_list = []
    for player in data:
        player_list.append(player.jsonify())

    return player_list


# live status api
@app.route("/api/live/del/<id>", methods=["POST"])
async def del_live_status(id):
    global live_player_status
    ServerData.api_call(ApiType.OsuLiveDelete)

    live_player_status.pop(int(id))


@app.route("/api/live/get/<id>", methods=["get"])
async def get_live_status(id):
    ServerData.api_call(ApiType.OsuLiveGet)

    player_status = live_player_status[id]
    return player_status


@app.route("/api/live/get", methods=["get"])
async def get_all_live_status():
    ServerData.api_call(ApiType.OsuLiveGet)

    return live_player_status


@app.route("/api/live/update/<id>", methods=["POST"])
async def update_live_status(id):
    global live_player_status
    ServerData.api_call(ApiType.OsuLiveUpdate)

    info = request.json
    live_player_status[id] = info


# home website
@app.route('/')
async def home():
    return render_template("index.html")


# osu website side
@app.route('/osu')
async def osu_home():
    return render_template("osu/index.html")


@app.route("/osu/matches/<match_name>")
def load_match(match_name):
    players = {}
    teams = {}

    match: Match = match_handler.get_match(match_name)

    for player in match.players:
        players[player.id] = player.jsonify()

    for team in match.team_data:
        teams[team.team_name] = team.jsonify()

    return render_template(
        'osu/Current.html',
        math=math,
        time=time,
        players=players,
        match_name=match_name,
        mode=match.mode,
        nicknames=match.nicknames,
        teams=teams,
        live_status=live_player_status,
        get_osu_id=get_osu_id
    )


@app.route("/osu/matches")
async def matches_page():
    return render_template(
        'osu/matches.html',
        matches=match_handler
    )


@app.route("/refresh/<player_name>")
async def web_player_refresh(player_name):
    ServerData.api_call(ApiType.OsuRefresh)

    for player in PlayerList.Players:
        if player.name == player_name:
            player.update_data()


# website control
@app.route("/control")
async def web_control():
    return render_template(
        "control.html",
        live_status_users=len(live_player_status)
    )


# minecraft wip

# @app.route("/minecraft")
# async def minecraft():
#     return render_template("minecraft/index.html")
#
#
# @app.route("/minecraft/stats")
# async def stats():
#     player_data = minecraft_data_crap.player_data(False)
#     return render_template("minecraft/server-player-stats.html",
#                            player_data=player_data)
#
#
# @app.route("/api/mc/<update>")
# async def mc(update):
#     global api_uses
#     api_uses += 1
#     if update == "true":
#         minecraft_data_crap.player_data(True)
#         return ("done")
#     else:
#         player_data = minecraft_data_crap.player_data(False)
#         poop = {}
#         poop["poop"] = player_data
#         return (poop)


@app.route("/user/<id>")
async def load_profile(id):
    account_info = json.load(open(f"accounts/{id}.json", encoding="utf-8"))
    return render_template("account/user-profile.html",
                           id=id,
                           username=account_info["username"],
                           profile_picture=account_info["pfp url"],
                           metadata=account_info["metadata"])


@app.route("/account/login")
async def login_page():
    return render_template("account/login.html")


@app.route('/login', methods=['POST'])
def login_cookie():
    username = request.form.get('nm')
    password = request.form.get('pw')
    login_result = asyncio.run(login(username, password))
    if login_result != "incorrect info":
        account_info = json.load(
            open(f"accounts/{login_result['id']}.json", encoding="utf-8"))
        resp = make_response(
            render_template('account/user-profile.html',
                            id=id,
                            username=account_info["username"],
                            profile_picture=account_info["pfp url"],
                            metadata=account_info["metadata"]))
        resp.set_cookie('userID', str(login_result["id"]).encode())
        return resp
    else:
        resp = make_response(
            render_template('account/login.html', warning="incorrect info"))
        return resp


@app.route("/account/signout")
async def signout():
    ServerData.api_call(ApiType.AccountLogOut)

    resp = make_response(render_template('account/login.html'))
    resp.delete_cookie('userID')
    return resp


@app.route("/account")
async def account_home():
    return render_template("account/create-one.html")


@app.route("/account/create")
async def account_create_page():
    osu_info = request.args.get("osu_info")
    if osu_info is not None:
        osu_info = json.loads(osu_info)
    return render_template("account/create.html",
                           client_id=client.osu_client_id,
                           redirect_uri=client.osu_public_url,
                           osu_info=osu_info
                           )


@app.route("/create-account", methods=['POST'])
def create_account():
    username = request.form.get("nm")
    password = request.form.get("pw")
    try:
        osuid = int(request.form.get("id"))
    except:
        osuid = 0
    about_me = request.form.get("am")
    asyncio.run(account_create(username, password, osuid, None, None,
                               about_me))
    login_result = asyncio.run(login(username, password))
    if login_result != "incorrect info":
        account_info = json.load(
            open(f"accounts/{login_result['id']}.json", encoding="utf-8"))
        resp = make_response(
            render_template('account/user-profile.html',
                            id=id,
                            username=account_info["username"],
                            profile_picture=account_info["pfp url"],
                            metadata=account_info["metadata"]))
        resp.set_cookie('userID', str(login_result["id"]).encode())
        return resp
    else:
        resp = make_response(
            render_template('account/login.html', warning="incorrect info"))
        return resp


@app.route("/api/account/change-pfp", methods=["POST"])
def change_profile_picture():
    ServerData.api_call(ApiType.AccountChangePfp)

    id = request.cookies.get('userID')
    account_data = json.load(open(f"accounts/{id}.json"))
    account_data["pfp url"] = request.form.get("url")
    json.dump(account_data,
              open(f"accounts/{id}.json", "w"),
              indent=4,
              sort_keys=False)
    return render_template('account/user-profile.html',
                           id=id,
                           username=account_data["username"],
                           profile_picture=account_data["pfp url"],
                           metadata=account_data["metadata"])


@app.route("/gentrys-quest")
async def gentrys_quest_home():
    return render_template("gentrys quest/home.html", version=gq_version[1:])


@app.route("/gentrys-quest/leaderboard")
async def gentrys_quest_leaderboard():
    players = gqc_data.get_leaderboard()

    return render_template(
        "gentrys quest/leaderboard.html",
        players=players,
        version=1
    )


@app.route("/gentrys-quest/online-players")
async def gentrys_quest_online_players():
    players = gqc_data.online_players
    version = GPSystem.GPmain.GPSystem.version

    def sort_thing(player):
        return player.power_level

    players.sort(key=sort_thing, reverse=True)

    return render_template(
        "gentrys quest/online-players.html",
        players=players,
        version=1
    )


@app.route("/down")
async def down():
    return render_template("down.html")


@app.route("/api/account/updateGCdata/<id>", methods=["POST"])
async def update_gc_data(id):
    ServerData.api_call(ApiType.GQUpdateData)

    data = request.json
    user_data = json.load(open(f"accounts/{id}.json", "r"))
    if verify_token(data["token"]):
        user_data["metadata"]["Gentry's Quest data"] = data["data"]

    json.dump(user_data, open(f"accounts/{id}.json", "w"), indent=4)
    gqc_data.update_player_power_level(id)
    gqc_data.sort_players()
    return "done"


@app.route("/api/gq/get-leaderboard/<start>+<display_number>", methods=["GET"])
async def get_gq_leaderboard(start, display_number):
    ServerData.api_call(ApiType.GQLeaderboard)

    players = {}
    counter = 1
    for player in gqc_data.get_leaderboard(int(start), int(display_number)):
        players[player.id] = {"username": player.account_name, "power level": player.power_level, "placement": counter,
                              "ranking": {'tier': player.ranking[0], 'tier value': player.ranking[1]}}
        counter += 1

    return players


@app.route("/api/gq/get-power-level/<id>", methods=["GET"])
async def get_power_level(id):
    ServerData.api_call(ApiType.GQGetPowerLevel)

    return str(gqc_data.get_player_power_level(id))


@app.route("/api/gq/check-in/<id>", methods=["POST"])
async def check_in(id):
    ServerData.api_call(ApiType.GQCheckIn)

    gqc_data.check_in_player(id)

    return ""


@app.route("/api/gq/check-out/<id>", methods=["POST"])
async def check_out(id):
    ServerData.api_call(ApiType.GQCheckOut)

    gqc_data.check_out_player(id)

    return ""


@app.route("/api/gq/get-online-players", methods=["GET"])
async def get_online_players():
    ServerData.api_call(ApiType.GQGetOnlinePlayers)

    list_of_players = {}
    for player in gqc_data.online_players:
        player_json = {}
        player_json["username"] = player.account_name
        player_json["power level"] = player.power_level
        player_json["ranking"] = {'tier': player.ranking[0], 'tier value': player.ranking[1]}
        player_json["placement"] = gqc_data.players.index(player) + 1
        list_of_players[player.id] = player_json

    return list_of_players


@app.route("/api/gq/get-version")
async def get_version():
    ServerData.api_call(ApiType.GQGetVersion)

    return gq_version


@socketio.on('get control data')
def get_control_data():
    global websocket_uses
    websocket_uses += 1
    emit('control data recieve', {
        "live users": len(live_player_status),
        "api uses": api_uses,
        "websocket uses": websocket_uses
    })


if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=80, debug=False)
