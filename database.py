class Leaderboard:
    def __init__(self):
        import sqlite3
        self.con = sqlite3.connect('leaderboard.db')
        self.cur = self.con.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS matches (
                    datePlayed text,
                    matchLength integer,
                    Score integer)
            """)
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users (
                    username text PRIMARY KEY,
                    creationDate text
                    numberOfGames integer
                    bestGame integer)
            """)
        self.cur.execute("""CREATE TABLE IF NOT EXISTS mazes (
                    mazeID integer
                    mazeName text,
                    mazeHash text,
                    creationDate date)
            """)

    def InputScore(self, username, dateplayed, matchlength, score):  # PARAMETERISED BABY!!!!!!!!
        matchparameters = [username, dateplayed, matchlength, score]
        self.cur.executemany("INSERT INTO matches VALUES (?,?,?,?)", [matchparameters])

    def NumberOfGames(self, username):
        games = self.cur.execute(f'SELECT username FROM matches WHERE username = "{username}"')
        return len(games.fetchall())

    def CheckIfUserExists(self, username):
        users = self.cur.execute(f'SELECT username FROM users WHERE username = "{username}"')
        if len(users.fetchall()) == 0:
            return False
        elif len(users.fetchall()) == 1:
            return True
        else:
            raise Exception("Duplicate Users Found")

    def AddUserToDatabase(self, username, creationDate):
        userparameters = [username, creationDate]
        self.cur.executemany("INSERT INTO users(username,creationDate) VALUES (?,?)", [userparameters])

    def DeleteUser(self, username):
        self.cur.execute(f'DELETE FROM users WHERE username = "{username}"')
        self.cur.execute(f'DELETE FROM matches WHERE username = "{username}"')

    def Close(self):
        self.con.commit()
        self.con.close()


leaderboard = Leaderboard()
print(leaderboard.CheckIfUserExists("Dave"))

print(leaderboard.CheckIfUserExists("Simon"))
leaderboard.Close()
