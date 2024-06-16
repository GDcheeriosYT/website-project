# packages
import asyncio
import atexit
import json
import math
import random
import string
import traceback
import urllib
import logging

# flask packages
import requests
from flask import Flask, redirect, render_template, request, make_response
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO, emit

# credential variables
import Client_Credentials as client
# scripts
from crap.Initialization import *

initialize_files()  # setup necessary files

# data imports
from crap.osu_crap.Match import Match
from crap.osu_crap.PlayerList import PlayerList
from crap.osu_crap.MatchHandler import MatchHandler

from crap.gentrys_quest_crap.GentrysQuestManager import GentrysQuestManager
from crap.gentrys_quest_crap.GentrysQuestClassicManager import GentrysQuestClassicManager

from crap.ServerData import ServerData
from crap.ApiType import ApiType

from crap.AccountPFPs import pfps

# global vars
#   osu data
live_player_status = {}
player_data = PlayerList
print("\nLoading osu players\n")
time.sleep(client.section_load_time)
PlayerList.load()

match_handler = MatchHandler()
match_handler.load()

#   Gentrys Quest data
GQC_manager = GentrysQuestClassicManager()

# flask set up
app = Flask(  # Create a flask app
    __name__,
    template_folder='templates',  # Name of html file folder
    static_folder='static'  # Name of directory for static files
)
app.config['SECRET_KEY'] = "hugandafortnite"
socketio = SocketIO(app, logger=False)
bcrypt = Bcrypt(app)

# logging config
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


# define at exit action
def exit_func():
    player_data.unload()
    match_handler.unload()
    ServerData.account_manager.unload()


atexit.register(exit_func)


# <editor-fold desc="API">

@app.route("/web-save", methods=['POST'])
def web_save():
    ServerData.api_call(ApiType.WebSave)
    player_data.unload()
    match_handler.unload()
    ServerData.account_manager.unload()

    return "Saved!"


@app.route("/web-backup", methods=['POST'])
def web_backup():
    from crap.Backup import create_backup
    ServerData.api_call(ApiType.WebBackup)
    create_backup()

    return "backed up"


# <editor-fold desc="token API">
@app.route("/api/generate-token")
async def generate_token():
    ServerData.api_call(ApiType.TokenGenerate)
    try:
        token = ""
        for i in range(32):
            token += random.choice(string.ascii_letters)

        ServerData.add_token(token)
        ServerData.token_status.successful()
        return token
    except:
        ServerData.token_status.unsuccessful()
        return "False"


@app.route("/api/clear-tokens")
async def clear_tokens():
    ServerData.clear_tokens()
    return "Done"


@app.route("/api/delete-token/<token>", methods=["POST"])
async def delete_token(token):
    ServerData.remove_token(token)
    return f"removed {token}"


@app.route("/api/verify-token/<token>")
def verify_token(token):
    return ServerData.verify_token(token)


# </editor-fold>

# <editor-fold desc="account API">
@app.route("/api/account/create/<username>+<password>")
async def account_create(username, password, osu_id=0, about_me=""):
    ServerData.api_call(ApiType.AccountCreate)

    try:
        account_count = len(os.listdir("accounts")) + 1
        password = str(password)
        profile_picture = random.choice(pfps)
        about_me = about_me
        password = str(bcrypt.generate_password_hash(password))
        account_data = {
            "id": account_count,
            "pfp url": profile_picture,
            "username": username,
            "password": password[2:-1],
            "osu id": osu_id,
            "about me": about_me
        }

        directory = f"accounts/{account_count}"

        os.mkdir(directory)
        os.mkdir(f"{directory}/gentrys quest classic data")
        os.mkdir(f"{directory}/gentrys quest data")

        with open(f"accounts/{account_count}/data.json", 'w+') as new_account_data:
            json.dump(account_data, new_account_data, indent=4)

        ServerData.account_manager.make_account(account_count)

        ServerData.account_status.successful()
        return account_data
    except:
        ServerData.account_status.unsuccessful()


@app.route("/api/password-cache-gen")
async def password_cache_gen():
    return render_template("password_gen.html",
                           password="poop")


@app.route("/api/password-cache-gen", methods=["POST"])
async def password_cache_gen_post():
    password = request.form.get("password")
    return render_template("password_gen.html", password=str(bcrypt.generate_password_hash(password)))


@app.route("/api/account/receive/<id_or_name>")  # receive account with id
def get_account_with_id_or_name(id_or_name):
    ServerData.api_call(ApiType.AccountReceive)

    successful = ServerData.account_status.successful
    try:
        data = ServerData.account_manager.get_by_username(id_or_name)
        if not data:
            data = ServerData.account_manager.get_by_id(id_or_name)


        successful()
        return data.jsonify() if data else "Not Found"
    except:
        ServerData.account_status.unsuccessful()


@app.route("/api/account/login/<username>+<password>")
async def login(username, password):
    ServerData.api_call(ApiType.AccountLogIn)
    successful = ServerData.account_status.successful
    try:
        account = ServerData.account_manager.get_by_username(username)
        if account:
            if bcrypt.check_password_hash(account.password, password):
                successful()
                return account.jsonify()

        successful()
        return "incorrect info"
    except:
        ServerData.account_status.unsuccessful()


@app.route('/login', methods=['POST'])
def login_cookie():
    username = request.form.get('nm')
    password = request.form.get('pw')
    login_result = asyncio.run(login(username, password))
    if login_result != "incorrect info":
        login_result = ServerData.account_manager.get_by_username(username)
        resp = make_response(
            render_template('account/user-profile.html',
                            id=login_result.id,
                            username=login_result.username,
                            profile_picture=login_result.pfp,
                            about=login_result.about,
                            osuid=login_result.osu_id,
                            gqc_data=GQC_manager.get_player(id),
                            get_buff=GQC_manager.attribute_convert
                            ))
        resp.set_cookie('userID', str(login_result.id))
        return resp
    else:
        resp = make_response(
            render_template('account/login.html', warning="incorrect info"))
        return resp


@app.route("/account/signout")
async def signout():
    ServerData.api_call(ApiType.AccountLogOut)

    try:
        resp = make_response(render_template('account/login.html'))
        resp.delete_cookie('userID')
        ServerData.account_status.successful()
        return resp
    except:
        ServerData.account_status.unsuccessful()


@app.route("/create-account", methods=['POST'])
def create_account():
    username = request.form.get("nm")
    if ServerData.account_manager.get_by_username(username):
        return redirect("/account/create")

    password = request.form.get("pw")
    try:
        osuid = int(request.form.get("id"))
    except:
        osuid = 0
    about_me = request.form.get("am")
    asyncio.run(account_create(username, password, osuid, about_me))
    login_result = asyncio.run(login(username, password))
    if login_result != "incorrect info":
        account = ServerData.account_manager.get_by_username(username)
        resp = make_response(
            render_template('account/user-profile.html',
                            id=account.id,
                            username=account.username,
                            profile_picture=account.pfp,
                            about=account.about,
                            osuid=account.osu_id,
                            gqc_data=GQC_manager.get_player(id),
                            get_buff=GQC_manager.attribute_convert
                            ))
        resp.set_cookie('userID', str(account.id))
        return resp
    else:
        resp = make_response(
            render_template('account/login.html', warning="incorrect info"))
        return resp


@app.route("/api/account/change-pfp", methods=["POST"])
def change_profile_picture():
    ServerData.api_call(ApiType.AccountChangePfp)

    try:
        id = request.cookies.get('userID')
        account_data = ServerData.account_manager.get_by_id(id)
        account_data.pfp = request.form.get("url")
        ServerData.account_status.successful()
        return render_template('account/user-profile.html',
                               id=id,
                               username=account_data.username,
                               profile_picture=account_data.pfp,
                               about=account_data.about,
                               osuid=account_data.osu_id,
                               gqc_data=GQC_manager.get_player(id),
                               get_buff=GQC_manager.attribute_convert
                               )
    except:
        ServerData.account_status.unsuccessful()


@app.route("/api/account/change-username", methods=["POST"])
async def change_username():
    ServerData.api_call(ApiType.AccountChangeUsername)

    try:
        id = request.cookies.get("userID")
        account = ServerData.account_manager.get_by_id(id)
        username = request.form.get("username")
        if not ServerData.account_manager.get_by_username(username):
            account.username = username
            ServerData.account_status.successful()

        return render_template('account/user-profile.html',
                               id=id,
                               username=account.username,
                               profile_picture=account.pfp,
                               about=account.about,
                               osuid=account.osu_id,
                               gqc_data=GQC_manager.get_player(id),
                               get_buff=GQC_manager.attribute_convert
                               )

    except:
        ServerData.account_status.unsuccessful()


# </editor-fold>

# <editor-fold desc="osu API">
# osu auth stuff
@app.route('/code_grab')
def code_grab():
    ServerData.api_call(ApiType.OsuAuthenticate)

    try:
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

        ServerData.osu_status.successful()
        return redirect(f"/account/create?osu_info={json.dumps(info)}")
    except:
        ServerData.osu_status.unsuccessful()


# <editor-fold desc="match API">
@app.route("/api/get_match/<match_name>")
async def grabber(match_name, from_socket: bool = False):
    if not from_socket:
        ServerData.api_call(ApiType.OsuMatchGrab)

    try:
        match = match_handler.get_match(match_name)

        new_dict = {}
        for player in match.players:
            new_dict[player.id] = {
                "background url": player.background,
                "score": match.get_score(player),
                "rank": player.rank,
                "playcount": match.get_playcount(player),
                "liveStatus": None if player.id not in live_player_status else live_player_status[player.id],
            }

        for team in match.team_data:
            for player_ref in team.players:
                new_dict[player_ref.id]["team"] = f"{team.jsonify()}"

        ServerData.osu_status.successful()
        return new_dict
    except Exception as e:
        traceback.print_exc()
        ServerData.osu_status.unsuccessful()


# </editor-fold>

# <editor-fold desc="player API">

@app.route("/refresh/<player_id>", methods=['GET', 'POST'])
async def web_player_refresh(player_id):
    ServerData.api_call(ApiType.OsuRefresh)

    try:
        player = PlayerList.get_users([player_id])[0]
        player.update_data()
        ServerData.osu_status.successful()
        return player.jsonify()
    except:
        ServerData.osu_status.unsuccessful()

    return "{}"


@app.route("/api/grab/<ids>", methods=['GET'])
async def all_grabber(ids):
    ServerData.api_call(ApiType.OsuIdGrab)
    try:
        id_list = ids.split("+")

        data = PlayerList.get_users(id_list)
        player_list = []
        for player in data:
            player_list.append(player.jsonify())

        ServerData.osu_status.successful()
        return player_list
    except:
        return "{}"
        ServerData.osu_status.unsuccessful()


# </editor-fold>

# <editor-fold desc="live API">
@app.route("/api/live/del/<id>", methods=["POST"])
async def del_live_status(id):
    global live_player_status
    ServerData.api_call(ApiType.OsuLiveDelete)

    try:
        live_player_status.pop(int(id))
        ServerData.osu_status.successful()
    except:
        ServerData.osu_status.unsuccessful()


@app.route("/api/live/get/<id>", methods=["get"])
async def get_live_status(id):
    ServerData.api_call(ApiType.OsuLiveGet)

    try:
        player_status = live_player_status[id]
        ServerData.osu_status.successful()
        return player_status
    except:
        ServerData.osu_status.unsuccessful()


@app.route("/api/live/get", methods=["get"])
async def get_all_live_status():
    ServerData.api_call(ApiType.OsuLiveGet)

    try:
        ServerData.osu_status.successful()
        return live_player_status
    except:
        ServerData.osu_status.unsuccessful()


@app.route("/api/live/update/<id>", methods=["POST"])
async def update_live_status(id):
    global live_player_status
    ServerData.api_call(ApiType.OsuLiveUpdate)

    try:
        info = request.json
        live_player_status[id] = info
        ServerData.osu_status.successful()
    except:
        ServerData.osu_status.unsuccessful()


# </editor-fold>

# </editor-fold>

# <editor-fold desc="gentrys quest API">

# <editor-fold desc="GPSystem">

# </editor-fold>

# <editor-fold desc="Classic">

@app.route("/api/gqc/get-leaderboard/<start>+<display_number>", methods=["GET"])
async def get_gq_leaderboard(start, display_number):
    ServerData.api_call(ApiType.GQLeaderboard)

    try:
        players = {}
        counter = 1
        for player in GQC_manager.get_leaderboard(int(start), int(display_number)):
            players[player.id] = {"username": player.account_name, "power level": player.power_level.jsonify(),
                                  "placement": counter,
                                  "ranking": player.ranking.jsonify()}
            counter += 1

        ServerData.gqc_status.successful()
        return players
    except:
        ServerData.gqc_status.unsuccessful()


@app.route("/api/gqc/get-power-level/<id>", methods=["GET"])
async def get_power_level(id):
    ServerData.api_call(ApiType.GQGetPowerLevel)
    return GQC_manager.get_player_power_level(id)


@app.route("/api/gqc/check-in/<id>", methods=["POST"])
async def check_in(id):
    ServerData.api_call(ApiType.GQCheckIn)

    GQC_manager.check_in_player(id)

    return ""


@app.route("/api/gqc/check-out/<id>", methods=["POST"])
async def check_out(id):
    ServerData.api_call(ApiType.GQCheckOut)

    GQC_manager.check_out_player(id)

    return ""


@app.route("/api/gqc/get-online-players", methods=["GET"])
async def get_online_players():
    ServerData.api_call(ApiType.GQGetOnlinePlayers)

    list_of_players = {}
    for player in GQC_manager.online_players:
        player_json = {}
        player_json["username"] = player.account_name
        player_json["power level"] = player.power_level.jsonify()
        player_json["ranking"] = player.ranking.jsonify()
        player_json["placement"] = GQC_manager.players.index(player) + 1
        list_of_players[player.id] = player_json

    return list_of_players


@app.route("/api/gqc/get-version")
async def get_version():
    ServerData.api_call(ApiType.GQGetVersion)

    return GQC_manager.version


@app.route("/api/updateGQCdata/<id>", methods=["POST"])
async def update_gc_data(id):
    ServerData.api_call(ApiType.GQUpdateData)

    try:
        data = request.json
        if verify_token(data["token"]) != "False":
            GQC_manager.update_player_data(id, data["data"])
            ServerData.account_manager.get_by_id(id).gentrys_quest_classic_data = data["data"]

        ServerData.gqc_status.successful()
    except:
        ServerData.gqc_status.unsuccessful()

    return "done"

# </editor-fold>


# </editor-fold>

# </editor-fold>

# <editor-fold desc="templates">

# <editor-fold desc="main">

@app.route("/status")
async def status():
    return render_template(
        "status.html",
        server_data=ServerData,
        api_enum=ApiType
    )


@app.route('/')
async def home():
    return render_template("index.html")


@app.route("/down")
async def down():
    return render_template("down.html")


@app.route("/control")
async def web_control():
    return render_template(
        "control.html",
    )


# </editor-fold>

# <editor-fold desc="gentrys quest">

@app.route("/gentrys-quest")
async def gentrys_quest_home():
    return render_template("gentrys quest/home.html", version=GQC_manager.version[1:])


@app.route("/gentrys-quest/leaderboard")
async def gentrys_quest_leaderboard():
    players = GQC_manager.get_leaderboard()

    return render_template(
        "gentrys quest/leaderboard.html",
        players=players,
        version=GentrysQuestManager.rater_version
    )


@app.route("/gentrys-quest/online-players")
async def gentrys_quest_online_players():
    players = GQC_manager.online_players

    def sort_thing(player):
        return player.power_level.weighted

    players.sort(key=sort_thing, reverse=True)

    return render_template(
        "gentrys quest/online-players.html",
        players=players,
        version=GentrysQuestManager.rater_version
    )


@app.route("/gentrys-quest/ranking")
async def gentrys_quest_ranking():
    return render_template(
        "gentrys quest/ranking.html",
        ranking_info=GentrysQuestManager.rater.get_tiers(),
        colors=GentrysQuestManager.rater.rating_colors,
        gqc_id=GQC_manager.get_player,
        gqc_rank=GQC_manager.get_ranking
    )


# </editor-fold>

# <editor-fold desc="osu">

@app.route('/osu')
async def osu_home():
    return render_template("osu/index.html")


@app.route("/osu/matches/<match_name>")
def load_match(match_name):
    players = {}
    teams = {}

    match: Match = match_handler.get_match(match_name)

    for player in match.players:
        players[player.name] = [
            player.avatar,
            player.background,
            player.link,
            player.id,
            player.accuracy,
        ]

    for team in match.team_data:
        teams[team.team_name] = team.jsonify()

    return render_template(
        'osu/Current.html',
        players=players,
        match=match,
        nicknames=match.nicknames,
        teams=teams,
        live_status=live_player_status,
        get_osu_id=get_osu_id
    )


@app.route("/osu/matches")
async def matches_page():
    return render_template(
        'osu/matches.html',
        matches=match_handler,
        has_perm=ServerData.account_manager.has_permission
    )


@app.route("/osu/create")
async def match_create():
    return render_template(
        'osu/match_creator.html',
        matches=match_handler,
        has_perm=ServerData.account_manager.has_permission
    )

# </editor-fold>

# <editor-fold desc="account">

@app.route("/user/<id>")
async def load_profile(id):
    account_info = ServerData.account_manager.get_by_id(id)
    return render_template("account/user-profile.html",
                           id=id,
                           username=account_info.username,
                           profile_picture=account_info.pfp,
                           about=account_info.about,
                           osuid=account_info.osu_id,
                           gqc_data=GQC_manager.get_player(id),
                           get_buff=GQC_manager.attribute_convert
                           )


@app.route("/account/login")
async def login_page():
    return render_template("account/login.html")


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
                           redirect_uri=f"{client.domain}/code_grab",
                           osu_info=osu_info
                           )


# </editor-fold>


# </editor-fold>

# <editor-fold desc="helper methods">
def get_osu_id(userID):
    return json.load(open(f"accounts/{userID}.json",
                          "r"))["metadata"]["osu id"]


# </editor-fold>

# <editor-fold desc="sockets">
@socketio.on('event')
def test_socket(data):
    print(data)


@socketio.on('update client status')
def update_client_status(data):
    print("updating", data["user"])
    live_player_status[data["user"]] = data


@socketio.on('match data get')
def get_livestatus(data):
    emit('match data receive', asyncio.run(grabber(data, True)), ignore_queue=True)


@socketio.on('get control data')
def get_control_data():
    emit('control data recieve', {
        "live users": len(live_player_status),
        "api uses": 0,
        "websocket uses": 0
    })


@socketio.on('update status')
def update_status():
    emit('status recieve',
         {
             'total apis': len(ServerData.API_history),
             'aph': ServerData.API_rate_hour,
             'apm': ServerData.API_rate_minute,
             'aps': ServerData.API_rate_second,
             'api values': ServerData.get_occurrences()["values"],
             'token status': ServerData.token_status.health,
             'account status': ServerData.account_status.health,
             'osu status': ServerData.osu_status.health,
             'gqc status': ServerData.gqc_status.health,
             'gq status': ServerData.gq_status.health
         })


# </editor-fold>


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


if __name__ == "__main__":
    server_port = os.environ.get('PORT', client.port)
    if client.cert_path and client.key_path:
        ssl_context = (client.cert_path, client.key_path)

        socketio.run(
            app,
            host='0.0.0.0',
            port=server_port,
            allow_unsafe_werkzeug=True,
            debug=client.debug,
            ssl_context=ssl_context
        )
    else:
        socketio.run(
            app,
            host='0.0.0.0',
            port=server_port,
            allow_unsafe_werkzeug=True,
            debug=client.debug
        )
