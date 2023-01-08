# packages
from flask import Flask, jsonify, redirect, render_template, request, make_response
from flask_socketio import SocketIO, send, emit
from engineio import payload
import math
import json
import time
import shutil
import asyncio
import datetime as dt
from tabulate import tabulate
from flask_bcrypt import Bcrypt
import socketio
import random
import os
import requests
import string

# credential variables
import Client_Credentials as client

live_player_status = {}
daily_osu_gains = {}
console_outputs = []

websocket_uses = 0
api_uses = 0

print("\n")
print("verifying directory 0%")
if os.path.isdir("matches") == False:
    os.mkdir("matches")
print("verifying directory 20%")
if os.path.isdir("match_history") == False:
    os.mkdir("match_history")
print("verifying directory 40%")
if os.path.isdir("accounts") == False:
    os.mkdir("accounts")
print("verifying directory 60%")
if os.path.exists("player_data.json") == False:
    poop = open("player_data.json", "w+")
    poop.write("{}")
    poop.close()
print("verifying directory 80%")
if os.path.exists("info.json") == False:
    server_instance_info = open("info.json", "w+").close()
    server_instance_info = {}
    server_instance_info["tokens"] = []
    server_instance_info["daily data"] = daily_osu_gains
    json.dump(server_instance_info, open("info.json", "w"), indent=4)
    server_instance_info = json.load(open("info.json", "r"))
else:
    server_instance_info = json.load(open("info.json", "r"))
print("verifying directory 100%")

print("setting up gentry's quest data handler")
from crap.gentrys_quest_crap import GentrysQuestDataHolder

gq_data = GentrysQuestDataHolder()
print("done")

def update_server_instance_info(tokens=None, daily_data=None):
    global server_instance_info
    if tokens == None:
        tokens = server_instance_info["tokens"]
    if daily_data == None:
        daily_data = server_instance_info["daily data"]
    server_instance_info["daily data"] = daily_data
    server_instance_info["tokens"] = tokens
    json.dump(server_instance_info, open("info.json", "w"), indent=4)
    server_instance_info = json.load(open("info.json", "r"))


def contains_token(token):
    if token in server_instance_info["tokens"]:
        return True
    else:
        return False


payload.Payload.max_decode_packets = 50000


# my packages
# adding this after initialization of files because some of them require these directories to exist
from crap import authentication_crap, match_crap, player_crap, function_crap, console_interface_crap, minecraft_data_crap, gentrys_quest_crap
from crap.team_crap import Teams


# console methods
def update_server_conosle():
    os.system("clear")
    print("live users: " + len(live_player_status))
    if len(console_outputs) >= 4:
        last_message = console_outputs[3]
        console_outputs.clear()
        console_outputs.append(last_message)
    print("[")
    for output in console_outputs:
        print(output + "\n")
    print("]")


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
    global api_uses
    api_uses += 1
    token = ""
    for i in range(32):
        token += random.choice(string.ascii_letters)

    tokens = server_instance_info["tokens"]
    tokens.append(token)

    update_server_instance_info(tokens)

    return token


@app.route("/api/clear-tokens")
async def clear_tokens():
    global api_uses
    api_uses += 1
    update_server_instance_info([])
    return "tokens cleared"


@app.route("/api/clear-daily-data")
async def clear_daily_data():
    global api_uses
    api_uses += 1
    update_server_instance_info(daily_data={})
    return "tokens cleared"


@app.route("/api/delete-token/<token>", methods=["POST"])
async def delete_token(token):
    global api_uses
    api_uses += 1
    print(token)
    if contains_token(token):
        new_list = []
        for token2 in server_instance_info["tokens"]:
            print(token, token2)
            if token2 != token:
                new_list.append(token)
            else:
                print("OHPHOPOPHPFPD")

        update_server_instance_info(new_list)

        return "deleted"
    return "could not find token"


@app.route("/api/verify-token/<token>")
async def verify_token(token):
    global api_uses
    api_uses += 1
    return str(contains_token(token))


#osu auth stuff
@app.route('/code_grab')
def code_grab():
    code = request.query_string

    response = requests.post("https://osu.ppy.sh/oauth/token",
                             json={'client_id': client.osu_client_id, 'client_secret': client.osu_secret, 'grant_type': 'client_credentials',
                                   'scope': 'public'},
                             headers={'Accept': 'application/json', 'Content-Type': 'application/json'})

    token_thing = response.json()

    access_token = token_thing["access_token"]

    return redirect(f"{client.osu_public_url}")

# account api
@app.route("/api/account/create/<username>+<password>")
async def account_create(username,
                         password,
                         osu_info={"osu id": 0},
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
        "osu id": osu_info,
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
                          password = "poop")


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
    try:
        int(id_or_name)
    except ValueError:
        for file in os.listdir("accounts"):
            account_data = json.load(open(f"accounts/{file}", "r"))
            if account_data["username"] == id_or_name:
                return file[:-5], account_data
                
    for file in os.listdir("accounts"):
        if file[:-5] == id:
            return file[:-5], json.load(open(f"accounts/{file}", "r"))
    

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
    with open(f"matches/{match_name}.json") as f:
        match_data = json.load(f)

    id_list = match_data["users"]
    new_dict = {}
    if match_data["mode"] == "ffa":
        for id in id_list:
            user_pos = match_data["users"].index(id)
            score = player_crap.user_data_grabber(
                id=f"{id}", specific_data=[
                    "score"
                ])[0] - match_data["initial score"][user_pos]
            rank = player_crap.user_data_grabber(id=f"{id}",
                                                 specific_data=["rank"])[0]
            background_url = player_crap.user_data_grabber(
                id=f"{id}", specific_data=["background url"])[0]
            if int(id) in live_player_status:
                new_dict[id] = {
                    "background url": background_url,
                    "score": score,
                    "rank": rank,
                    "liveStatus": live_player_status[int(id)]
                }
            else:
                new_dict[id] = {
                    "background url": background_url,
                    "score": score,
                    "rank": rank,
                    "liveStatus": None
                }

    else:
        for id in id_list:
            user_pos = match_data["users"].index(id)
            score = player_crap.user_data_grabber(
                id=f"{id}", specific_data=[
                    "score"
                ])[0] - match_data["initial score"][user_pos]
            rank = player_crap.user_data_grabber(id=f"{id}",
                                                 specific_data=["rank"])[0]
            background_url = player_crap.user_data_grabber(
                id=f"{id}", specific_data=["background url"])[0]
            for team in match_data["team metadata"]:
                if id in match_data['team metadata'][team]['players']:
                    if int(id) in live_player_status:
                        new_dict[id] = {
                            "background url": background_url,
                            "score": score,
                            "rank": rank,
                            "liveStatus": live_player_status[int(id)],
                            "team": f"{team}"
                        }
                    else:
                        new_dict[id] = {
                            "background url": background_url,
                            "score": score,
                            "rank": rank,
                            "liveStatus": None,
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
    live_player_status[data["user"]] = data


@socketio.on('match data get')
def get_livestatus(data):
    global websocket_uses
    websocket_uses += 1
    global api_uses
    api_uses -= 1
    emit('match data receive', asyncio.run(grabber(data)), ignore_queue=True)


# all players api updater
@app.route("/api/grab/<ids>/all")
async def all_grabber(ids):
    global api_uses
    api_uses += 1
    id_list = ids.split("+")

    new_dict = {}

    for id in id_list:
        data = player_crap.user_data_grabber(
            id=f"{id}", specific_data=["score", "rank", "background url"])
        new_dict[id] = {
            "background url": data[2],
            "score": data[0],
            "rank": data[1],
            "liveStatus": None
        }

        print(
            f"{player_crap.user_data_grabber(id, specific_data=['name'])[0]}: ",
            new_dict[id])

    return new_dict


@app.route('/get-graph/<matchname>/<time>/<type>', methods=["GET"])
def get_graph_data(matchname, time, type):
    if time == "current":
        for match in os.listdir("/matches"):
            if match[:-5] == matchname:
                match_data = json.load(open(f"matches/{match}", "r"))
                return match_data["graph_data"]


def update_graph_data():
    today = dt.datetime.now().strftime("%m-%d-%Y")
    for match in os.listdir("matches"):
        match_data = json.load(open(f"matches/{match}", "r"))
        overall_score_data = match_data["graph data"]["overall score"]
        overall_score_data_score_list = []
        daily_stats = match_data["graph data"]["daily stats"]
        daily_stats_list = []
        for user in match_data["users"]:
            score = player_crap.user_data_grabber(id=user,
                                                  specific_data=["score"])[0]
            overall_score_data_score_list.append(
                score -
                match_data["initial score"][match_data["users"].index(user)])
            daily_stats_list.append([
                int(daily_osu_gains[user]["current"][0]),
                int(daily_osu_gains[user]["current"][1])
            ])

        overall_score_data[today] = overall_score_data_score_list
        daily_stats[today] = daily_stats_list

        match_data["graph data"]["overall score"] = overall_score_data
        match_data["graph data"]["daily stats"] = daily_stats

        print(match_data)

        json.dump(match_data,
                  open(f"matches/{match}", "w"),
                  indent=4,
                  sort_keys=False)


@app.route("/api/daily-reset")
def daily_reset():
    global daily_osu_gains
    global api_uses
    api_uses += 1
    daily_osu_gains = {}
    asyncio.run(player_crap.refresh_all_players())
    for player in json.load(open("player_data.json", "r")):
        player_info = player_crap.user_data_grabber(
            id=player, specific_data=["score", "playcount"])
        start = [player_info[0], player_info[1]]
        current = [player_info[0], player_info[1]]
        daily_osu_gains[player] = {"start": start, "current": current}

    update_graph_data()
    update_server_instance_info(daily_data=daily_osu_gains)

    return daily_osu_gains


@app.route("/api/update-graphs")
def update_graph_endpoint():
    global api_uses
    api_uses += 1
    update_graph_data()
    return redirect(f"{client.osu_public_url}/matches")


# api for refresh client
# match grabber
@app.route('/api/matches/<time>')
def api_match_request(time):
    global api_uses
    api_uses += 1
    returns = {}
    returns["matches"] = []
    if time == "current":
        for match in os.listdir("matches/"):
            returns["matches"].append(match)
        return returns
    else:
        for match in os.listdir("match_history/"):
            returns["matches"].append(match)
        return returns


# match data grabber
@app.route('/api/match-get/<time>/<match>')
def match_get(time, match):
    global api_uses
    api_uses += 1
    with open("player_data.json") as f:
        player_data = json.load(f)
    if time == "current":
        with open(f"matches/{match}") as f:
            match_data = json.load(f)

        table = {}
        table["rank"] = []
        table["players"] = []
        table["score"] = []
        table["playcount"] = []
        table["player_rank"] = []

        players = {}

        for user in match_data["users"]:
            player = player_crap.player_match_constructor(user, match_data)

            players[player[1][8]] = player[1]

        players_sorted = dict(
            sorted(players.items(), key=lambda x: x[1], reverse=True))

        x = 1

        for key in players_sorted.keys():
            user_pos = match_data["users"].index(str(key))
            player_thing = player_crap.user_data_grabber(
                id=key, specific_data=["name", "score", "playcount", "rank"])
            table["rank"].append(f"#{x}")
            table["players"].append(player_thing[0])
            table["score"].append(
                "{:,}".format(player_thing[1] -
                              match_data["initial score"][user_pos]))
            table["playcount"].append(
                "{:,}".format(player_thing[2] -
                              match_data["initial playcount"][user_pos]))
            if player_thing[3] == 999999999:
                player_thing[3] = "unranked"
                table["player_rank"].append(player_thing[3])
            else:
                table["player_rank"].append("{:,}".format(player_thing[3]))
            x += 1

        print("\n", match_data["match name"])
        print(tabulate(table, headers="keys"))
        return (table)
    else:
        return None


# get delay api
@app.route("/api/get-delay")
async def get_delay():
    global api_uses
    api_uses += 1
    return (str(len(live_player_status.items()) / 4))


# start match api
@app.route("/api/start-match", methods=["POST"])
async def api_start_match():
    global api_uses
    api_uses += 1
    info = request.json
    match_crap.start_match()


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
    player_info = live_player_status[id]
    return (player_info)


@app.route("/api/live/update/<id>", methods=["POST"])
async def update_live_status(id):
    global live_player_status
    global api_uses
    api_uses += 1
    info = request.json
    live_player_status[id] = info
    return ({})


# home website
@app.route('/')
async def home():
    return render_template("index.html")


# home osu website
@app.route('/osu')
async def osu_home():
    return render_template("osu/index.html")


# start console interface
@app.route("/start")
async def start():
    await console_interface_crap.main_process()
    return redirect(f"{client.public_url}/matches")


@app.route("/osu/players")
async def players():
    players_dict = {}

    with open("player_data.json") as f:
        player_data = json.load(f)

    for id in player_data.keys():
        name = player_data[id]["user data"]["name"]
        score = player_data[id]["user data"]["score"]
        avatar = player_data[id]["user data"]["avatar url"]
        background = player_data[id]["user data"]["background url"]
        profile_link = player_data[id]["user data"]["profile url"]
        tags = player_data[id]["user tags"]
        playcount = player_data[id]["user data"]["playcount"]
        playcount = ("{:,}".format(playcount))
        score_formatted = ("{:,}".format(score))
        id = id

        players_dict[name] = [
            score, avatar, background, profile_link, tags, playcount,
            score_formatted, id
        ]

        players_sorted = dict(
            sorted(players_dict.items(), key=lambda x: x[1], reverse=True))

    return render_template(
        'osu/players.html',  # Template file
        players=players_sorted)


@app.route("/osu/matches/<match_name>/<graph_view>")
async def match(match_name, graph_view):
    players = {}

    with open(f"matches/{match_name}") as joe:
        match_data = json.load(joe)

    with open("player_data.json", "r") as kfc:
        player_data = json.load(kfc)

    if match_data["mode"] == "ffa":
        player_score_data = {}

        for id in match_data["users"]:
            player = player_crap.player_match_constructor(id, match_data)
            players[player[0]] = player[1]
            player_score_data[player[0]] = player[1][0]

        with open(f"matches/{match_name}", "w") as file:
            json.dump(match_data, file, indent=4, sort_keys=False)

        with open(f"matches/{match_name}", "r") as file:
            match_data = json.load(file)

        return render_template('osu/Current.html',
                               math=math,
                               time=time,
                               match_data=match_data,
                               teams={},
                               players=players,
                               match_name=match_name,
                               get_data=player_crap.user_data_grabber,
                               live_status=live_player_status,
                               get_osu_id=get_osu_id)

    else:
        players = {}
        teams = {}
        team_score_data = {}

        for id in match_data["users"]:
            player = player_crap.player_match_constructor(id, match_data)
            players[player[0]] = player[1]

        for team in match_data["team metadata"]:
            new_team = Teams(team, match_name)
            teams[team] = {
                'score': new_team.score,
                'players': new_team.users,
                "color": match_data["team metadata"][team]["team color"]
            }
            # team_score_data[team] = ("{:,}".format(new_team.score))

        with open(f"matches/{match_name}", "w") as file:
            json.dump(match_data, file, indent=4, sort_keys=False)

        with open(f"matches/{match_name}", "r") as file:
            match_data = json.load(file)

        return render_template('osu/Current.html',
                               match_data=match_data,
                               players=players,
                               teams=teams,
                               get_data=player_crap.user_data_grabber,
                               get_osu_id=get_osu_id)


# work on future old matches
@app.route("/osu/matches/old/<match_name>")
def old_match(match_name):
    players = {}
    print(match_name)
    global match_data

    with open(f"match_history/{match_name}") as joe:
        match_data = json.load(joe)

    with open("player_data.json", "r") as kfc:
        player_data = json.load(kfc)

    if match_data["mode"] == "ffa":
        for id in match_data["users"]:
            player = player_crap.player_match_constructor(id, match_data)
            players[player[0]] = player[1]
            players_sorted = dict(
                sorted(players.items(), key=lambda x: x[1], reverse=True))

        return render_template(
            'osu/old_match.html',  # Template file
            # recent = player_recent
            math=math,
            # biggest_score = biggest_score,
            time=time,
            match_data=match_data,
            # previous_score_segment = previous_score_segment,
            # get_key_of = get_key_of,
            players=players_sorted,
            match_name=match_name,
            # graph_view = graph_view,
            get_data=player_crap.user_data_grabber,
            live_status=live_player_status)

    else:
        teams = {}
        score_data = match_data["match score history"]
        team_score_data = {}

        for team in match_data["team metadata"]:
            new_team = Teams(team, match_name)
            teams[team] = [new_team.score, new_team.users]
            team_score_data[team] = new_team.score

        score_data[f"{dt.date.today()}"] = dict(sorted(
            team_score_data.items()))
        teams_sorted = dict(
            sorted(teams.items(), key=lambda x: x[0], reverse=True))
        score_data[f"{dt.date.today()}"] = team_score_data
        match_data["match score history"] = score_data

        return render_template(
            'Current.html',  # Template file
            # recent = player_recent
            time=time,
            match_data=match_data,
            teams=teams_sorted,
            get_data=player_crap.user_data_grabber)


@app.route("/osu/matches")
async def matches():
    current_matches = []

    previous_matches = []

    for match in os.listdir("matches/"):
        current_matches.append(match)

    for match in os.listdir("match_history/"):
        previous_matches.append(match)

    return render_template('osu/matches.html',
                           match_data=match_crap.get_match_data,
                           player_data=player_crap.user_data_grabber,
                           random_number=function_crap.randnum,
                           current_matches=current_matches,
                           previous_matches=previous_matches)


@app.route("/refresh/<player_name>")
async def web_player_refresh(player_name):
    global daily_osu_gains
    global api_uses
    api_uses += 1
    if player_name == "all":
        await player_crap.refresh_all_players()

    else:
        await player_crap.player_refresh(player_name)

    players = json.load(open("player_data.json", "r"))
    for player in players:
        player_info = player_crap.user_data_grabber(
            id=player, specific_data=["score", "playcount"])
        try:
            daily_osu_gains[player]["current"] = [
                player_info[0] - daily_osu_gains[player]["start"][0],
                player_info[1] - daily_osu_gains[player]["start"][1]
            ]
        except:
            daily_osu_gains[player] = {
                "current": [
                    player_info[0] - player_info[0],
                    player_info[1] - player_info[1]
                ],
                "start": [player_info[0], player_info[1]]
            }

    update_server_instance_info(daily_data=daily_osu_gains)

    return redirect(f"{client.osu_public_url}/matches")


@app.route("/refresh/<player_name>", methods=["POST"])
async def post_player_refresh(player_name):
    global daily_osu_gains
    if player_name == "all":
        await player_crap.refresh_all_players()
    else:
        try:
            int(player_name) + 0
        except:
            player_name = player_crap.user_data_grabber(name=f"{player_name}",
                                                        specific_data=["id"
                                                                       ])[0]

        await player_crap.player_refresh(player_name)
        player_info = player_crap.user_data_grabber(
            id=player_name, specific_data=["score", "play count"])
        try:
            daily_osu_gains[player_name]["current"] = [
                player_info[0] - daily_osu_gains[player_name]["start"][0],
                player_info[1] - daily_osu_gains[player_name]["start"][1]
            ]
        except:
            daily_osu_gains[player_name] = {
                "current": [
                    player_info[0] - player_info[0],
                    player_info[1] - player_info[1]
                ],
                "start": [player_info[0], player_info[1]]
            }

    return ("refreshed")


# tests
@app.route("/tests/<test_num>")
async def tests(test_num):
    return render_template(f"tests/{test_num}.html", test_num=test_num)


@app.route("/tests/create")
async def test_create():
    test_new_id = len(os.listdir("templates/tests"))
    template = open("templates/tests/test-template.html", "r")
    f = open(f"templates/tests/test{test_new_id}.html", "w+")
    for line in template:
        f.write(line)
    f.close()
    return render_template(f"tests/test{test_new_id}.html")


# website control
@app.route("/control")
async def web_control():
    return render_template(
        "control.html",
        total_websockets = websocket_uses,
        total_apis = api_uses,
        live_status_users = len(live_player_status)
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
    return render_template("account/create.html",
                           client_id=client.osu_client_id,
                           host_name=client.osu_public_url
                          )


@app.route("/create-account", methods=['POST'])
def create_account():
    username = request.form.get("nm")
    password = request.form.get("pw")
    try:
        osuid = int(request.form.get("osuid"))
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
    return render_template("gentrys quest/home.html")

@app.route("/gentrys-quest/leaderboard")
async def gentrys_quest_leaderboard():

    players = gq_data.get_leaderboard()

    return render_template(
        "gentrys quest/leaderboard.html",
        players = players
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
    gq_data.update_player_power_level(id)
    return "done"

@app.route("/dev/gc/artifact")
async def artifact_creator():
    return render_template(
        "gentrys quest/dev/artifact.html",
        artifact_output = None
    )

@app.route("/dev/gc/artifact/create", methods=["POST"])
async def artifact_created():
    name = request.form.get("name")
    name_segments = name.split()
    class_name = ""
    name = ""
    family = request.form.get("family")
    family_segments = family.split()
    family = ""
    for word in name_segments:
        class_name += (word[0].upper() + word[1:])
        name += (word[0].upper() + word[1:] + " ")
    for word in family_segments:
        family += (word[0].upper() + word[1:] + " ")
    buff = request.form.get("buff")
    if buff == "":
        buff = ""
    else:
        buff = f"StatTypes.{buff}"
    string = f"class {class_name}(Artifact):\n\tdef __init__(self, star_rating):\n\t\tsuper().__init__(\n\t\t\t\"{name}\",\n\t\t\tstar_rating,\n\t\t\t\"{family}\",\n\t\t\tBuff({buff})\n\t\t)"
    print(string)
    return render_template(
        "gentrys quest/dev/artifact.html",
        artifact_output = string
    )
@app.route("/api/gq/get-leaderboard/<start>+<display_number>", methods=["GET"])
async def get_gq_leaderboard(start, display_number):
    players = []
    for index in display_number:
        try:
            players.append(gq_player_leaderboard[start + index])
        except IndexError:
            pass

    return {"players": players}

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
    socketio.run(app, host='0.0.0.0', port=80, debug=True)