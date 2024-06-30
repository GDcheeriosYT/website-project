import os.path

from crap.PSQLConnection import PSQLConnection as DB


class Account:
    id: int
    username: str
    password: str
    email: str
    osu_id: int
    about: str
    pfp: str = str

    def __init__(self, identifier):
        if type(identifier) is int:
            result = DB.get(f"select * from accounts where id = {identifier}")
        else:
            result = DB.get(f"select * from accounts where username = \'{identifier}\'")

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
        DB.do(f"update accounts set username = \'{new_username}\' where id = {id};")

    # </editor-fold>

    # <editor-fold desc="Checks">

    @staticmethod
    def name_exists(name: str) -> bool:
        result = DB.get_group(f"select username from accounts where username = \'{name}\';")
        return len(result) > 0

    # </editor-fold>
