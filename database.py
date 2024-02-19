class Leaderboard:
    def __init__(self):
        import sqlite3
        self.__con = sqlite3.connect('leaderboard.db')
        self.__cur = self.__con.cursor()
        # Dates are stored in YYYY-MM-DD HH:MM:SS Format
        self.__cur.execute("""CREATE TABLE IF NOT EXISTS Users (
                    username TEXT PRIMARY KEY,
                    password TEXT,
                    salt TEXT,
                    creationDate INTEGER)
            """)
        self.__cur.execute("""CREATE TABLE IF NOT EXISTS Mazes (
                    mazeName TEXT PRIMARY KEY,
                    mazeString TEXT,
                    creator TEXT,
                    creationDate INTEGER,
                    FOREIGN KEY (creator) REFERENCES Users(username))
            """)
        self.__cur.execute("""CREATE TABLE IF NOT EXISTS Matches (
                    matchID INTEGER PRIMARY KEY,
                    datePlayed INTEGER,
                    matchLength INTEGER,
                    score INTEGER,
                    mazeName TEXT,
                    FOREIGN KEY (mazeName) REFERENCES Mazes(mazeName))
            """)
        self.__cur.execute("""CREATE TABLE IF NOT EXISTS MatchBook (
                    matchBookID INTEGER PRIMARY KEY,
                    username TEXT,
                    matchID INTEGER,
                    entityType TEXT,
                    FOREIGN KEY (username) REFERENCES Users(username),
                    FOREIGN KEY (matchID) REFERENCES Matches(matchID))
            """)
        self.__cur.execute("""CREATE TABLE IF NOT EXISTS Replays (
                    matchID INTEGER,
                    replayHash TEXT,
                    FOREIGN KEY (matchID) REFERENCES Matches(matchID))
            """)

    def inputScore(self, datePlayed, matchLength, score, mazeName):
        matchparameters = [datePlayed, matchLength, score, mazeName]
        self.__cur.executemany("INSERT INTO Matches(datePlayed, matchLength, score, mazeName) VALUES (?,?,?,?)",
                               [matchparameters])

    def getAllMatchInfo(self):
        matches = self.__cur.execute("""SELECT
                            Matches.datePlayed,
                            Matches.matchLength,
                            Matches.score,
                            (SELECT MatchBook.username
                                FROM MatchBook
                                WHERE MatchBook.matchID = Matches.matchID
                                AND MatchBook.entityType = "Pacman"
                                ) AS Host,
                            (SELECT GROUP_CONCAT(MatchBook.username, ', ')
                                FROM MatchBook
                                WHERE MatchBook.matchID = Matches.matchID
                                AND (MatchBook.entityType = "Blinky"
                                    OR MatchBook.entityType = "Inky"
                                    OR MatchBook.entityType = "Pinky"
                                    OR MatchBook.entityType = "Clyde")) AS ghosts,
                            Matches.mazeName
                            FROM Matches
        """)
        return matches.fetchall()

    def getAllUserInfo(self):
        users = self.__cur.execute("""SELECT
                            Users.username,
                            Users.creationDate,
                            (SELECT COUNT(MatchBook.username)
                                FROM MatchBook
                                WHERE Users.username = MatchBook.username
                                AND MatchBook.entityType = "Pacman") as pacmanGames,
                            (SELECT COUNT(MatchBook.username)
                                FROM MatchBook
                                WHERE Users.username = MatchBook.username
                                AND (MatchBook.entityType = "Blinky"
                                    OR MatchBook.entityType = "Inky"
                                    OR MatchBook.entityType = "Pinky"
                                    OR MatchBook.entityType = "Clyde")) as ghostGames,
                            (SELECT AVG(Matches.score)
                                FROM Matches
                                INNER JOIN MatchBook ON MatchBook.matchID = Matches.matchID
                                WHERE Users.username = MatchBook.username
                                AND MatchBook.entityType = "Pacman") as averageScore,
                            (SELECT MAX(Matches.score)
                                FROM Matches
                                INNER JOIN MatchBook ON MatchBook.matchID = Matches.matchID
                                WHERE Users.username = MatchBook.username
                                AND MatchBook.entityType = "Pacman") as highScore
                            FROM Users
                            ORDER BY highscore DESC
        """)
        return users.fetchall()

    def getMatchID(self):
        matchID = int(str(self.__cur.execute("SELECT last_insert_rowid()").fetchone()).strip("[(,)]"))
        return matchID

    def addToMatchBook(self, username, matchID, entityType):
        matchbookparameters = [username, matchID, entityType]
        self.__cur.executemany("INSERT INTO MatchBook(username, matchID, entityType) VALUES (?,?,?)",
                               [matchbookparameters])

    def addReplay(self, matchID, replayHash):
        replayparameters = [matchID, replayHash]
        self.__cur.executemany("INSERT INTO Replays VALUES (?,?)", [replayparameters])

    def getNumberOfGames(self, username):
        games = self.__cur.execute("SELECT username FROM Matches WHERE username = (?)", [username])
        return len(games.fetchall())

    def isUserExists(self, username):
        users = self.__cur.execute("SELECT username FROM Users WHERE username = (?)", [username])
        if len(users.fetchall()) == 0:
            return False
        else:
            return True

    def addUserToDatabase(self, username, password):
        import hashlib
        import secrets
        import time
        h = hashlib.sha256()
        salt = secrets.token_urlsafe(15)
        dbPassword = salt + password
        h.update(dbPassword.encode())
        userparameters = [username, h.hexdigest(), salt, time.strftime("%Y-%m-%d %H:%M:%S")]
        self.__cur.executemany("INSERT INTO Users(username, password, salt, creationDate) VALUES (?,?,?,?)",
                               [userparameters])

    def storeMaze(self, mazeName, mazeString, creator, creationDate):
        mazeparameters = [mazeName, mazeString, creator, creationDate]
        self.__cur.executemany("INSERT INTO Mazes VALUES (?,?,?,?)", [mazeparameters])

    def getMazes(self):
        mazes = self.__cur.execute("SELECT mazeName, creator, mazeString FROM Mazes")
        return mazes.fetchall()

    def getMazeName(self, string):
        query = self.__cur.execute("SELECT mazeName FROM Mazes WHERE mazeString = (?)", [string])
        name = query.fetchone()
        if name:
            return name[0]
        return ''

    def getReplayDetails(self, inputHash):
        details = self.__cur.execute("""SELECT Matches.datePlayed, 
                                Matches.score,
                                COUNT(MatchBook.matchID)
                                FROM Matches 
                                INNER JOIN Replays ON Replays.matchID = Matches.matchID
                                INNER JOIN MatchBook ON MatchBook.matchID = Matches.matchID
                                WHERE Replays.replayHash = (?)
                                   """, [inputHash])
        values = details.fetchone()
        if values == (None, None, 0):
            return inputHash
        else:
            return f'{values[0]}, Score: {values[1]}, Players: {values[2]}'

    def checkValidLogin(self, username, password):
        if self.isUserExists(username):
            import hashlib
            h = hashlib.sha256()
            salt = self.__cur.execute("SELECT salt FROM Users WHERE username = (?)", [username])
            h.update((salt.fetchone()[0] + password).encode())
            correctPassword = self.__cur.execute("SELECT password FROM Users WHERE username = (?)", [username])
            correctPassword = correctPassword.fetchone()[0]
            if str(h.hexdigest()) == correctPassword:
                return 0  # 0 indicates valid login
            else:
                return 1  # 1 indicates incorrect password
        else:
            return 2  # 2 indicates non-existent user

    def deleteUser(self, username):
        self.__cur.execute("DELETE FROM Users WHERE username = (?)", [username])  # Remove user from database
        self.__cur.execute("""UPDATE MatchBook
                            SET username = ""
                            WHERE username = (?)
                    """, [username])  # Change all mentions of user to a null user

    def deleteMatch(self, matchID):
        self.__cur.execute("DELETE FROM Matches WHERE matchID = (?)", [matchID])
        self.__cur.execute("DELETE FROM MatchBook WHERE matchID = (?)", [matchID])

    def close(self):
        self.__con.commit()
        self.__con.close()
