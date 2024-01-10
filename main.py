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

# credential variables
import Client_Credentials as client

# scripts
from crap.Initialization import *
from crap.osu_crap.Match import Match

# data imports
from crap.osu_crap.PlayerList import PlayerList
from crap.osu_crap.Player import Player
from crap.osu_crap.MatchHandler import MatchHandler

from crap.ServerData import ServerData
from crap.ApiType import ApiType

initialize_files()  # setup necessary files

# global vars
#   main server data
tokens = []

#   osu data
live_player_status = {}
player_data = PlayerList
for id_ref in PlayerList.Player_json.keys():  # manual main loop to avoid circular import
    Player(id_ref)

match_handler = MatchHandler()

#   Gentrys Quest data
print("looking for Gentry's Quest latest release")
gq_version = requests.get("https://api.github.com/repos/GDcheeriosYT/Gentrys-Quest-Python/releases/latest").json()["name"]
print(f"Gentry's Quest version is {gq_version}")

# flask set up
app = Flask(  # Create a flask app
    __name__,
    template_folder='templates',  # Name of html file folder
    static_folder='static'  # Name of directory for static files
)
app.config['SECRET_KEY'] = "hugandafortnite"
socketio = SocketIO(app, logger=False)
bcrypt = Bcrypt(app)


# token api stuff
@app.route("/api/generate-token")
async def generate_token():
    ServerData.api_call(ApiType.TokenGenerate)

    token = ""
    for i in range(32):
        token += random.choice(string.ascii_letters)

    tokens.append(token)

    return token


@app.route("/api/clear-tokens")
async def clear_tokens():
    global tokens
    ServerData.api_call(ApiType.TokenClear)

    tokens = []


@app.route("/api/delete-token/<token>", methods=["POST"])
async def delete_token(token):
    global tokens
    ServerData.api_call(ApiType.TokenDelete)

    tokens.remove(token)


@app.route("/api/verify-token/<token>")
async def verify_token(token):
    ServerData.api_call(ApiType.TokenVerify)

    return token in tokens


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
                         gqdata=None,
                         backrooms_data=None,
                         about_me=""):
    global api_uses
    api_uses += 1
    account_count = len(os.listdir("accounts")) + 1
    password = str(password)
    pfp_options = [
        "https://i.pinimg.com/originals/cc/e9/2b/cce92b94514424978c1884f2211252c4.jpg",
        "https://i.ytimg.com/vi/Zr-qM5Vrd0g/maxresdefault.jpg",
        "https://i.scdn.co/image/ab67616d00001e02d45ec66aa3cf3864205fd068",
        "https://www.memesmonkey.com/images/memesmonkey/60/60af97651f29dd12fb75e7e86824dbca.jpeg",
        "https://c.tenor.com/GnoI-2HabJAAAAAM/john-dance.gif",
        "https://static01.nyt.com/images/2021/04/03/multimedia/03xp-april/merlin_185893383_8e41433f-4a32-4b1e-bf02-457290d0d534-superJumbo.jpg",
        "https://www.savacations.com/wp-content/uploads/2021/02/Blog-Capybara-Pantanal-Brazil3.jpg",
        "https://media.npr.org/assets/news/2009/11/24/herbivore_custom-1972e6887b4d01652e38a2f92ddf41e59463ad6a-s1100-c50.jpg",
        "https://c.tenor.com/6Rbpa8xH9f8AAAAC/yes-yes-yes-yes-osu-player-player-player.gif",
        "https://media.discordapp.net/attachments/828998201066651690/997964078666485900/5185344a7bd3b76fd9d1802a1be019d3.gif"
    ]
    profile_picture = random.choice(pfp_options)
    about_me = about_me
    gqdata = gqdata
    backrooms_data = backrooms_data
    password = str(bcrypt.generate_password_hash(password))
    metadata = {
        "osu id": osu_id,
        "Gentry's Quest data": gqdata,
        "backrooms_data": backrooms_data,
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


@app.route("/api/account/migrate_osu_data")
async def migrate_osu_data():
    global api_uses
    api_uses += 1
    for account_file in os.listdir("accounts"):
        account_data = json.load(open(f"accounts/{account_file}", "r"))
        account_data["metadata"]["osu info"] = {"osu id": account_data["metadata"]["osu id"]}
        del account_data["metadata"]["osu id"]
        json.dump(account_data, open(f"accounts/{account_file}", "w"), indent=4)
    return "finished!"


@app.route("/api/account/receive-account/<id_or_name>")  # receive account with id
def get_account_with_id_or_name(id_or_name):
    global api_uses
    api_uses += 1
    for file in os.listdir("accounts"):
        account_data = json.load(open(f"accounts/{file}", "r"))
        if file[:-5] == id_or_name:
            return {str(file[:-5]): account_data}
        if account_data["username"] == id_or_name:
            return {str(file[:-5]): account_data}

    return "Not Found"


@app.route("/api/account/login/<username>+<password>")
async def login(username, password):
    global api_uses
    api_uses += 1
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
    global api_uses
    api_uses += 1

    global_osu_data = json.load(open("player_data.json", "r"))

    with open(f"matches/{match_name}.json") as f:
        match_data = json.load(f)

    id_list = match_data["users"]
    new_dict = {}
    if match_data["mode"] == "ffa":
        for id in id_list:
            pos = match_data["users"].index(id)
            score = global_osu_data[id]["user data"]["score"] - match_data["initial score"][pos]
            rank = global_osu_data[id]["user data"]["rank"]
            playcount = global_osu_data[id]["user data"]["playcount"] - match_data["initial playcount"][pos]
            background_url = global_osu_data[id]["user data"]["background url"]
            new_dict[id] = {
                "background url": background_url,
                "score": score,
                "rank": rank,
                "playcount": playcount,
                "liveStatus": None if int(id) not in live_player_status else live_player_status[int(id)]
            }

    else:
        for id in id_list:
            pos = match_data["users"].index(id)
            score = global_osu_data[id]["user data"]["score"] - match_data["initial score"][pos]
            rank = global_osu_data[id]["user data"]["rank"]
            playcount = global_osu_data[id]["user data"]["playcount"] - match_data["initial playcount"][pos]
            background_url = global_osu_data[id]["user data"]["background url"]
            for team in match_data["team metadata"]:
                if id in match_data['team metadata'][team]['players']:
                    new_dict[id] = {
                        "background url": background_url,
                        "score": score,
                        "rank": rank,
                        "playcount": playcount,
                        "liveStatus": None if int(id) not in live_player_status else live_player_status[int(id)],
                        "team": f"{team}"
                    }

    return new_dict


@app.route("/api/grab/old/<match_name>")
async def old_grabber(match_name):
    global api_uses
    api_uses += 1

    global_osu_data = json.load(open("player_data.json", "r"))

    with open(f"match_history/{match_name}.json") as f:
        match_data = json.load(f)

    id_list = match_data["users"]
    new_dict = {}
    if match_data["mode"] == "ffa":
        for id in id_list:
            pos = match_data["users"].index(id)
            score = match_data["final score"][pos] - match_data["initial score"][pos]
            rank = global_osu_data[id]["user data"]["rank"]
            playcount = match_data["final playcount"][pos] - match_data["initial playcount"][pos]
            background_url = global_osu_data[id]["user data"]["background url"]
            new_dict[id] = {
                "background url": background_url,
                "score": score,
                "rank": rank,
                "playcount": playcount,
                "liveStatus": None if int(id) not in live_player_status else live_player_status[int(id)]
            }

    else:
        for id in id_list:
            pos = match_data["users"].index(id)
            score = match_data["final score"][pos] - match_data["initial score"][pos]
            rank = global_osu_data[id]["user data"]["rank"]
            playcount = match_data["final playcount"][pos] - match_data["initial playcount"][pos]
            background_url = global_osu_data[id]["user data"]["background url"]
            for team in match_data["team metadata"]:
                if id in match_data['team metadata'][team]['players']:
                    new_dict[id] = {
                        "background url": background_url,
                        "score": score,
                        "rank": rank,
                        "playcount": playcount,
                        "liveStatus": None if int(id) not in live_player_status else live_player_status[int(id)],
                        "team": f"{team}"
                    }

    return new_dict


@app.route("/api/daily/get")
def get_daily():
    global api_uses
    api_uses += 1
    return daily_osu_gains


def get_osu_id(userID):
    return json.load(open(f"accounts/{userID}.json",
                          "r"))["metadata"]["osu id"]


@app.route("/api/set-daily-info/<json_string>")
def set_daily_osu_info(json_string):
    global daily_osu_gains
    global api_uses
    api_uses += 1
    daily_osu_gains = json.loads(json_string)
    update_server_instance_info(daily_data=daily_osu_gains)

    return daily_osu_gains


@socketio.on('event')
def test_socket(data):
    print(data)


@app.route("/test-live")
async def test_live():
    global api_uses
    api_uses += 1
    return live_player_status


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
    global api_uses
    api_uses += 1
    live_player_status.pop(int(id))


@app.route("/api/live/get/<id>", methods=["get"])
async def get_live_status(id):
    global api_uses
    api_uses += 1
    player_status = live_player_status[id]
    return player_status


@app.route("/api/live/get", methods=["get"])
async def get_all_live_status():
    global api_uses
    api_uses += 1
    return live_player_status


@app.route("/api/live/update/<id>", methods=["POST"])
async def update_live_status(id):
    global live_player_status
    global api_uses
    api_uses += 1
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
       match_data=match_data,
       players=players,
       match_name=match_name,
       teams=teams,
       live_status=live_player_status,
       get_osu_id=get_osu_id
    )


@app.route("/osu/matches")
async def matches_page():

    return render_template(
        'osu/matches.html',
       match_data=match_crap.get_match_data,
       player_data=player_crap.user_data_grabber,
       current_matches=current_matches,
       previous_matches=previous_matches
   )


@app.route("/refresh/<player_name>")
async def web_player_refresh(player_name):
    global daily_osu_gains
    global api_uses
    api_uses += 1


# website control
@app.route("/control")
async def web_control():
    return render_template(
        "control.html",
        total_websockets=websocket_uses,
        total_apis=api_uses,
        live_status_users=len(live_player_status)
    )


@app.route("/osu/info")
async def warning_info():
    return render_template("info.html")


@app.route("/client")
async def client_webpage():
    return render_template("client.html")


@app.route("/minecraft")
async def minecraft():
    return render_template("minecraft/index.html")


@app.route("/minecraft/stats")
async def stats():
    player_data = minecraft_data_crap.player_data(False)
    return render_template("minecraft/server-player-stats.html",
                           player_data=player_data)


@app.route("/api/mc/<update>")
async def mc(update):
    global api_uses
    api_uses += 1
    if update == "true":
        minecraft_data_crap.player_data(True)
        return ("done")
    else:
        player_data = minecraft_data_crap.player_data(False)
        poop = {}
        poop["poop"] = player_data
        return (poop)


@app.route("/overlays/")
async def overlays():
    overlays = []
    for file in os.listdir("templates/stream-overlays/"):
        overlays.append(file)

    return render_template("stream-overlays/overlay-index.html",
                           overlays=overlays)


@app.route("/overlays/<overlay>")
async def overlay(overlay):
    return render_template(f"stream-overlays/{overlay}/index.html")


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
    global api_uses
    api_uses += 1
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
        version=gentrys_quest_crap.GPSystem.version
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
        version=version
    )


@app.route("/down")
async def down():
    return render_template("down.html")


@app.route("/api/account/updateGCdata/<id>", methods=["POST"])
async def update_gc_data(id):
    global api_uses
    api_uses += 1
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
    global api_uses
    api_uses += 1
    players = {}
    counter = 1
    for player in gqc_data.get_leaderboard(int(start), int(display_number)):
        players[player.id] = {"username": player.account_name, "power level": player.power_level, "placement": counter,
                              "ranking": {'tier': player.ranking[0], 'tier value': player.ranking[1]}}
        counter += 1

    return players


@app.route("/api/gq/get-power-level/<id>", methods=["GET"])
async def get_power_level(id):
    global api_uses
    api_uses += 1
    return str(gqc_data.get_player_power_level(id))


@app.route("/api/gq/check-in/<id>", methods=["POST"])
async def check_in(id):
    global api_uses
    api_uses += 1
    gqc_data.check_in_player(id)

    return ""


@app.route("/api/gq/check-out/<id>", methods=["POST"])
async def check_out(id):
    global api_uses
    api_uses += 1
    gqc_data.check_out_player(id)

    return ""


@app.route("/api/gq/get-online-players", methods=["GET"])
async def get_online_players():
    global api_uses
    api_uses += 1
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
    global api_uses
    api_uses += 1
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
