import os.path

from crap.PSQLConnection import PSQLConnection as DB


class Account:
    id: int
    username: str
    password: str
    email: str
    osu_id: int
    about: str
    pfp: str
    status: str

    def __init__(self, identifier):
        print(f"Loading account {identifier}")
        try:
            identifier = int(identifier)
            result = DB.get(f"select * from accounts where id = %s", params=(identifier,))
        except ValueError:
            result = DB.get(f"select * from accounts where username = %s", params=(identifier,))

        self.id = result[0]
        self.username = result[1]
        self.password = result[2]
        self.email = result[3]
        self.osu_id = result[4]
        self.about = result[5]
        if os.path.exists(f"static/pfps/{self.id}.png"):
            self.pfp = f"static/pfps/{self.id}.png"
        elif os.path.exists(f"static/pfps/{self.id}.jpg"):
            self.pfp = f"static/pfps/{self.id}.jpg"
        else:
            self.pfp = f"static/pfps/huh.png"
        self.status = result[6]

    # <editor-fold desc="Modifiers">
    @staticmethod
    def create(username: str, password: str, email: str, osu_id: int, about: str):
        query = """
        INSERT INTO accounts (username, password, email, osu_id, about)
        VALUES (%s, %s, %s, %s, %s)
        """

        params = (
            username,
            password,
            email,
            osu_id,
            about
        )

        DB.do(query, params)

    @staticmethod
    def change_username(id: int, new_username: str):
        DB.do(f"update accounts set username = %s where id = %s;", params=(new_username, id))

    # </editor-fold>

    # <editor-fold desc="Checks">

    @staticmethod
    def name_exists(name: str) -> bool:
        result = DB.get_group(f"select username from accounts where username = %s;", params=(name,))
        return len(result) > 0

    # </editor-fold>

    def jsonify(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "osuid": self.osu_id,
            "about": self.about,
            "pfp": self.pfp,
            "status": self.status
        }
