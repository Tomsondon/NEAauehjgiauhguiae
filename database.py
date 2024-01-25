class Leaderboard:
    def __init__(self):
        import sqlite3
        self.con = sqlite3.connect('leaderboard.db')
        self.cur = self.con.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS matches (
                    matchID integer,
                    datePlayed text,
                    matchLength integer,
                    Score integer)
            """)
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users (
                    username text,
                    creationDate text,
                    numberofGames integer,
                    bestGame integer)
            """)
        self.cur.execute("""CREATE TABLE IF NOT EXISTS mazes (
                    mazeName text,
                    mazeHash text,
                    creationDate text,
                    numberOfPlays integer)
            """)

    def InputScore(self, username, dateplayed, matchlength, score):              #PARAMETERISED BABY!!!!!!!!
        matchparameters = [username, dateplayed, matchlength, score]
        self.cur.executemany("INSERT INTO matches VALUES (?,?,?,?)", [matchparameters])

    def Close(self):
        self.con.commit()
        self.con.close()


leaderboard = Leaderboard()
leaderboard.InputScore("Balls", "27/06/06", 5, 5)
leaderboard.Close()
