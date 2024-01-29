import os
from tkinter import messagebox
import time
import boards
import pygame
import datetime
# import database
import tkinter
import random

f = open("config.txt")
config = f.read()
f.close()
u = config[19:22]
d = config[30:34]
l = config[41:45]
r = config[53:57]


def getCoord(x, y):
    coordX = (24 * x) + 12
    coordY = (24 * y) + 12
    return coordX, coordY


def getGridRef(x, y):
    refX = x // 24
    refY = y // 24
    return int(refX), int(refY)


def getDirectionPreference(vector):
    directionPreference = []
    if vector.x ** 2 > vector.y ** 2:
        if vector.x < 0:
            directionPreference.append(3)
            if vector.y < 0:
                directionPreference.append(1)
                directionPreference.append(2)
            else:
                directionPreference.append(2)
                directionPreference.append(1)
            directionPreference.append(4)
        else:
            directionPreference.append(4)
            if vector.y < 0:
                directionPreference.append(1)
                directionPreference.append(2)
            else:
                directionPreference.append(2)
                directionPreference.append(1)
            directionPreference.append(3)
    else:
        if vector.y < 0:
            directionPreference.append(1)
            if vector.x < 0:
                directionPreference.append(3)
                directionPreference.append(4)
            else:
                directionPreference.append(4)
                directionPreference.append(3)
            directionPreference.append(2)
        else:
            directionPreference.append(2)
            if vector.x < 0:
                directionPreference.append(3)
                directionPreference.append(4)
            else:
                directionPreference.append(4)
                directionPreference.append(3)
            directionPreference.append(1)
    return directionPreference


def drawValue(text, variable, pos, screen):
    my_font = pygame.font.SysFont('Jokerman', 30)
    valText = f"{text}: {variable}"
    val_surface = my_font.render(valText, False, "White")
    screen.blit(val_surface, pos)


def Square(x, y, size):
    return pygame.Rect(x - size / 2, y - size / 2, size, size)


class Board:
    def __init__(self, boardName):
        self._board = boardName
        self.__dotsLeft = 0
        self.__wallPositions = []
        self.__pelletPositions = []
        self.__ogPelletPositions = []
        self.__junctionPositions = []

        for j in range(len(self._board)):
            for i in range(len(self._board[j])):
                pos = getCoord(i, j)
                if self._board[j][i] == 1:
                    self.__ogPelletPositions.append(Square(pos[0], pos[1], 6))
                    self.__pelletPositions.append(Square(pos[0], pos[1], 6))
                    self.__dotsLeft += 1
                elif self._board[j][i] == 2:
                    self.__ogPelletPositions.append(Square(pos[0], pos[1], 12))
                    self.__pelletPositions.append(Square(pos[0], pos[1], 12))
                    self.__dotsLeft += 1
                elif self._board[j][i] == 3:
                    self.__wallPositions.append(Square(pos[0], pos[1], 24))

        for junctions in boards.mazeMapping(self._board):
            pos = getCoord(junctions[1], junctions[0])
            self.__junctionPositions.append(Square(pos[0], pos[1], 2))

    def getBoard(self):
        return self._board

    def getJunctionPositions(self):
        return self.__junctionPositions

    def collidesWithWall(self, rect):
        for i in self.__wallPositions:
            if i.colliderect(rect):
                return True
        return False

    def collidesWithPellet(self, rect):  # returns 1 if there is a collision with small pellet, returns 2 if
        for i in self.__pelletPositions:  # collision with power pellet, returns 0 if no collision
            if i.colliderect(rect):
                self.__pelletPositions.remove(i)
                if i.width == 12:
                    return 2
                elif i.width == 6:
                    return 1
        return 0

    def getDotsLeft(self):
        return len(self.__pelletPositions)

    def coordInJunction(self, xcoord, ycoord):
        for junctions in self.getJunctionPositions():
            if junctions.collidepoint(xcoord, ycoord):
                return True
        return False

    def render(self, screen):
        for i in self.__wallPositions:
            pygame.draw.rect(screen, "blue", i, 1)
        for i in self.__pelletPositions:
            pygame.draw.rect(screen, "white", i)
        for i in self.__junctionPositions:
            pygame.draw.rect(screen, "yellow", i, 3)

    def resetBoard(self):  # method is implemented like this rather than a simple assignment statement
        for pellet in self.__ogPelletPositions:  # to avoid the original list being permanently associated with the modified list
            self.__pelletPositions.append(pellet)

    def getCoord(self, x, y):
        coordX = (24 * x) + 12
        coordY = (24 * y) + 12
        return coordX, coordY

    def getGridRef(self, x, y):
        refX = x // 24
        refY = y // 24
        return int(refX), int(refY)

    def isNextBlockWall(self, direction, gridPosition):
        if direction == 1:
            if self._board[gridPosition[1] - 1][gridPosition[0]] == 3:
                return True
            else:
                return False

        if direction == 2:
            if self._board[gridPosition[1] + 1][gridPosition[0]] == 3:
                return True
            else:
                return False

        if direction == 3:
            if self._board[gridPosition[1]][gridPosition[0] - 1] == 3:
                return True
            else:
                return False

        try:
            if direction == 4:
                if self._board[gridPosition[1]][gridPosition[0] + 1] == 3:
                    return True
                else:
                    return False
        except IndexError:  # Error handling for the case where the player enters a right side warp; in this case there wouldn't be an incoming collision
            return False


class Game:
    def __init__(self, lives, Level, board, ghosts, pacman):
        self._time = 0
        self.__originalTime = pygame.time.get_ticks()
        self.__score = 0
        self.__lives = lives
        self.__level = Level
        self._board = board
        self._ghosts = ghosts
        self._pacman = pacman

    def addLives(self, lives):
        self.__lives += lives

    def getLives(self):
        return self.__lives

    def getScore(self):
        return self.__score

    def addScore(self, score):
        self.__score += score

    def getLevel(self):
        return self.__level

    def loadNextLevel(self):
        self.__level += 1
        self._board.resetBoard()
        self._ghosts.resetGhosts()
        self._pacman.restart()
        time.sleep(2)

    def loseLevel(self):
        self.__lives -= 1
        self._ghosts.resetGhosts()
        self._pacman.restart()
        time.sleep(1)

    def render(self, screen, dt):
        self._time = pygame.time.get_ticks() - self.__originalTime
        self._board.render(screen)
        self._pacman.render(screen, dt)
        for ghost in self._ghosts.getGhosts():
            ghost.render(screen, dt)

        drawValue("Score", self.__score, (0, 800), screen)
        drawValue("Time", self._time / 1000, (300, 800), screen)
        drawValue("Lives", self.__lives, (600, 800), screen)
        drawValue("Level", self.__level, (600, 900), screen)

    def getTime(self):
        return self._time


class Entity:
    def __init__(self, img, position):
        self._imgJPG = img
        self._img = pygame.transform.scale(pygame.image.load(img), (24, 24))
        self._startPos = position
        self._position = pygame.Vector2(position)
        self._direction = 0
        self._speed = 1
        self._boundBox = Square(self._position.x, self._position.y, 24)

    def getBoundBox(self):
        return self._boundBox

    def getPosition(self):
        return self._position

    def addSpeed(self, newSpeed):
        self._speed += newSpeed
        if self._speed < 0:
            self._speed = 0

    def setDirection(self, direction):
        self._direction = direction

    def getDirection(self):
        return self._direction

    def setPosition(self, pos):
        self._position = pos

    def getSpeed(self):
        return self._speed

    def render(self, screen, dt):
        self.updatePos(dt)
        self._boundBox = Square(self._position.x, self._position.y, 24)
        screen.blit(self._img, (self._position.x - 12, self._position.y - 12))
        pygame.draw.rect(screen, "red", self._boundBox, 1)
        pygame.draw.circle(screen, "green", self._position, 3)

    def updatePos(self, dt):  # Direction 1 is up, 2 is down, 3 is left, 4 is right
        if self._direction == 1:
            self._position.y -= self._speed * 300 * dt
        if self._direction == 2:
            self._position.y += self._speed * 300 * dt
        if self._direction == 3:
            self._position.x -= self._speed * 300 * dt
        if self._direction == 4:
            self._position.x += self._speed * 300 * dt
        if self._direction == 0:
            print("lmaooo")

        if self._position.x < 0:
            self._position.x = 720
        if self._position.x > 720:
            self._position.x = 0


class Pacman(Entity):
    def __init__(self):
        self.__startPoint = getCoord(14, 24)
        Entity.__init__(self, "images/player.jpg", (self.__startPoint[0], self.__startPoint[1]))

    def restart(self):
        self._position = pygame.Vector2(self.__startPoint[0], self.__startPoint[1])
        self._direction = 0


class Ghost(Entity):
    def __init__(self, ghostType):  # 0 is blinky, 1 is inky, 2 is pinky, 3 is clyde
        self._normalTick = 9999999999  # timer for scared phase, determines at what tick the ghost should stop being scared
        if ghostType == 0:
            Entity.__init__(self, "images/blinky.jpg", (396, 396))
        elif ghostType == 1:
            Entity.__init__(self, "images/inky.jpg", (396, 348))
        elif ghostType == 2:
            Entity.__init__(self, "images/pinky.jpg", (324, 396))
        elif ghostType == 3:
            Entity.__init__(self, "images/clyde.jpg", (324, 348))
        self._isScared = False
        self._isDead = False
        self._chaseMode = 1  # 0 is scatter state, 1 is chase state

    def reset(self):  # resets the ghost
        self._position = pygame.Vector2(self._startPos)
        self._speed = 1
        self._normalTick = 9999999999
        self._isScared = False
        self._isDead = False
        self._chaseMode = 1
        self._img = pygame.transform.scale(pygame.image.load(self._imgJPG), (24, 24))

    def scareGhost(self):
        self._normalTick = pygame.time.get_ticks() + 5000
        self._isScared = True
        self._img = pygame.transform.scale(pygame.image.load("images/scared.jpg"), (24, 24))
        self._speed = 0.5

    def runAway(self, vector):
        targetVector = self.getPosition() - vector   # When running away, this is the vector the ghosts target.
        return getDirectionPreference(targetVector)  # It is the vector opposite the vector facing pac-man

    def killGhost(self):
        self._position = pygame.Vector2(self._startPos)
        self._isDead = True
        self._isScared = False
        self._img = pygame.transform.scale(pygame.image.load("images/dead.jpg"), (24, 24))
        self._normalTick = pygame.time.get_ticks() + 5000
        self._direction = 0

    def updateState(self, dt):
        if pygame.time.get_ticks() >= self._normalTick:
            self._isScared = False
            self._isDead = False
            self._img = pygame.transform.scale(pygame.image.load(self._imgJPG), (24, 24))
            self._speed = 1
            self._normalTick = 9999999999

    def render(self, screen, dt):
        super().render(screen, dt)
        self.updateState(dt)

    def isScared(self):
        return self._isScared

    def isDead(self):
        return self._isDead


class Blinky(Ghost):
    def __init__(self):
        Ghost.__init__(self, 0)

    def getChaseDirections(self, playerPos):
        displacementVector = pygame.Vector2(playerPos - self.getPosition())
        return getDirectionPreference(displacementVector)


class Inky(Ghost):
    def __init__(self):
        Ghost.__init__(self, 1)

    def getChaseDirections(self, playerPos, playerDir, blinkyPos):
        posArr = list(playerPos)
        if playerDir == 1:
            posArr[1] -= 2 * 24
        elif playerDir == 2:
            posArr[1] += 2 * 24
        elif playerDir == 3:
            posArr[0] -= 2 * 24
        elif playerDir == 4:
            posArr[0] += 2 * 24

        displacementVector = [0, 0]
        invDisplacementVector = list(blinkyPos - posArr)
        displacementVector[0] = -1 * invDisplacementVector[0]
        displacementVector[1] = -1 * invDisplacementVector[1]
        targetVector = [0, 0]
        targetVector[0] = displacementVector[0] + posArr[0]
        targetVector[1] = displacementVector[1] + posArr[1]
        return getDirectionPreference(pygame.Vector2(targetVector))


class Pinky(Ghost):
    def __init__(self):
        Ghost.__init__(self, 2)

    def getChaseDirections(self, playerPos, playerDir):
        targetVector = list(playerPos)
        if playerDir == 1:
            targetVector[1] -= 4 * 24
        elif playerDir == 2:
            targetVector[1] += 4 * 24
        elif playerDir == 3:
            targetVector[0] -= 4 * 24
        elif playerDir == 4:
            targetVector[0] += 4 * 24
        displacementVector = list(targetVector - self.getPosition())
        return getDirectionPreference(pygame.Vector2(displacementVector))


class Clyde(Ghost):
    def __init__(self):
        Ghost.__init__(self, 3)

    def getChaseDirections(self, playerPos):
        targetVector = list(playerPos)
        displacementVector = (targetVector - self.getPosition())
        if displacementVector[0] ** 2 + displacementVector[1] ** 2 < (
                8 * 24) ** 2:  # only chase if magnitude less than 8 tiles
            return getDirectionPreference(displacementVector)
        else:
            directionPreference = [1, 2, 3, 4]
            random.shuffle(directionPreference)
            return directionPreference


class GhostGroup:
    def __init__(self, *ghosts):
        self.__ghosts = []
        for entity in ghosts:
            self.__ghosts.append(entity)

    def normalGhostCollision(self, boundBox):
        for ghost in self.__ghosts:
            if boundBox.colliderect(ghost.getBoundBox()):
                if ghost.isScared():
                    return True

    def scaredGhostCollision(self, boundBox):
        for ghost in self.__ghosts:
            if boundBox.colliderect(ghost.getBoundBox()):
                if not (ghost.isScared()):
                    return True

    def resetGhosts(self):
        for ghost in self.__ghosts:
            ghost.reset()

    def scareGhosts(self):
        for ghost in self.__ghosts:
            if not (ghost.isDead()):
                ghost.scareGhost()

    def inScaredPhase(self):
        for ghost in self.__ghosts:
            if ghost.isScared():
                return True

    def getGhosts(self):
        return self.__ghosts

    def render(self, screen, dt):
        for ghost in self.__ghosts:
            ghost.render(screen, dt)


class Bots(GhostGroup):

    def addBot(self, bot):
        self.__ghosts.append(bot)


class PlayerGhosts(GhostGroup):  # This class is useful for multiplayer

    def removePlayer(self, player):
        self.__ghosts.remove(player)


########################################################MAIN PROGRAM####################################################
def main(players):
    pygame.init()
    pygame.display.set_caption('PAC-MAN')
    print(u, d, l, r)
    # up = pygame.key.key_code(u)
    # down = pygame.key.key_code(d)                                                          dont work for some reason
    # left = pygame.key.key_code(l)
    # right = pygame.key.key_code(r)
    screen = pygame.display.set_mode((720, 960))  # sets resolution to 3:4
    clock = pygame.time.Clock()
    running = True
    fps = 240
    dt = 0
    level = 1
    extraPlayers = players
    selectedBoard = boards.boardsdict["default"]
    board = Board(selectedBoard)
    pacman = Pacman()
    blinky = Blinky()
    inky = Inky()
    pinky = Pinky()
    clyde = Clyde()
    ghosts = GhostGroup(blinky, inky, pinky, clyde)

    if extraPlayers == 1:
        playerGhosts = PlayerGhosts(blinky)
        botGhosts = Bots(inky, pinky, clyde)

    elif extraPlayers == 2:
        playerGhosts = PlayerGhosts(blinky, inky)
        botGhosts = Bots(pinky, clyde)

    elif extraPlayers == 3:
        playerGhosts = PlayerGhosts(blinky, inky, pinky)
        botGhosts = Bots(pinky, clyde)

    elif extraPlayers == 4:
        playerGhosts = PlayerGhosts(blinky, inky, pinky, clyde)
        botGhosts = Bots()

    else:
        playerGhosts = PlayerGhosts()
        botGhosts = Bots(blinky, inky, pinky, clyde)

    game = Game(3, level, board, ghosts, pacman)

    for bot in botGhosts.getGhosts():
        print(bot)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("black")

        currentPos = pacman.getPosition()

        newDirection = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            newDirection = 1
        elif keys[pygame.K_s]:
            newDirection = 2
        elif keys[pygame.K_a]:
            newDirection = 3
        elif keys[pygame.K_d]:
            newDirection = 4

        if keys[pygame.K_ESCAPE]:
            running = False
        if board.getDotsLeft() == 0 or keys[pygame.K_j]:
            print("Level complete!")
            game.loadNextLevel()

        drawValue("Speed", pacman.getSpeed(), (400, 900), screen)
        if keys[pygame.K_t]:
            pacman.addSpeed(-0.01)
        if keys[pygame.K_y]:
            pacman.addSpeed(0.01)
        if keys[pygame.K_p]:
            print(pacman.getPosition())

        pacmanDirection = pacman.getDirection()
        for ghost in ghosts.getGhosts():
            if ghost in playerGhosts.getGhosts():
                pass  # do the player stuff
            elif ghost in botGhosts.getGhosts() and board.coordInJunction(ghost.getPosition()[0],
                                                                          ghost.getPosition()[1]) and not(ghost.isDead()):
                if ghost.isScared():
                    chaseDirections = ghost.runAway(currentPos)
                else:
                    try:
                        chaseDirections = ghost.getChaseDirections(currentPos)
                    except:
                        try:
                            chaseDirections = ghost.getChaseDirections(currentPos, pacmanDirection)
                        except:
                            chaseDirections = ghost.getChaseDirections(currentPos, pacmanDirection,
                                                                       blinky.getPosition())
                position = ghost.getPosition()
                gridPosition = getGridRef(position[0], position[1])
                for direction in chaseDirections:
                    if not (board.isNextBlockWall(direction, gridPosition)):
                        ghost.setDirection(direction)
                        break

        pacman.setDirection(newDirection)

        pacmanBox = pacman.getBoundBox()
        # if game.collidesWithWall(pacmanBox):
        # pacman.setPosition(currentPos)
        # pacman.setDirection(0)
        pelletCheck = board.collidesWithPellet(pacmanBox)
        if pelletCheck == 1:
            game.addScore(10)
        elif pelletCheck == 2:
            game.addScore(50)
            ghosts.scareGhosts()

        for ghost in ghosts.getGhosts():
            if pacmanBox.colliderect(ghost.getBoundBox()):
                if ghost.isScared():
                    ghost.killGhost()
                elif not (ghost.isScared()):
                    game.loseLevel()

        if game.getLives() == 0:
            print("Ran out of lives!")
            running = False

        game.render(screen, dt)
        pygame.display.flip()

        clock.tick(fps)
        dt = clock.tick(fps) / 1000

    ###INPUT TO DATABASE###

    leaderboard = database.Leaderboard()

    # userName = input("Enter Name: ")

    # currentTime = datetime.datetime.now()
    # leaderboard.InputScore(userName, str(currentTime.strftime("%x")), game.getTime(), game.getScore())
    leaderboard.Close()


########################################################################################################################

if __name__ == "__main__":
    main(0)
