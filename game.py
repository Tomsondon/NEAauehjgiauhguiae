import os
from tkinter import messagebox

import boards
import pygame
import datetime
import database
import tkinter

f = open("config.txt")
config = f.read()
f.close()
u = config[19:22]
d = config[30:34]
l = config[41:45]
r = config[53:57]


def approachVector(vector):
    if vector.x ** 2 > vector.y ** 2:
        if vector.x < 0:
            return 3
        else:
            return 4
    else:
        if vector.y < 0:
            return 1
        else:
            return 2


def getCoord(x, y):
    coordX = (24 * x) + 12
    coordY = (24 * y) + 12
    return coordX, coordY


def getGridRef(x, y):
    refX = x // 24
    refY = y // 24
    return int(refX), int(refY)


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

    def resetBoard(self):
        for pellet in self.__ogPelletPositions:
            self.__pelletPositions.append(pellet)

    def getCoord(self, x, y):
        coordX = (24 * x) + 12
        coordY = (24 * y) + 12
        return coordX, coordY

    def getGridRef(self, x, y):
        refX = x // 24
        refY = y // 24
        return int(refX), int(refY)


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
        self._board.Reset()
        self._ghosts.resetGhosts()
        self._pacman.reset()

    def render(self, screen):
        self._time = pygame.time.get_ticks() - self.__originalTime
        drawValue("Score", self.__score, (0, 800), screen)
        drawValue("Time", self._time / 1000, (300, 800), screen)
        drawValue("Lives", self.__lives, (600, 800), screen)
        drawValue("Level", self.__level, (600, 900), screen)

    def getTime(self):
        return self._time


class Entity:
    def __init__(self, img, position, isPlayer):
        self._imgJPG = img
        self._img = pygame.transform.scale(pygame.image.load(img), (24, 24))
        self._startPos = position
        self._position = pygame.Vector2(position)
        self._direction = 0
        self._speed = 1
        self._boundBox = Square(self._position.x, self._position.y, 24)
        self._isPlayer = isPlayer

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
        Entity.__init__(self, "images/player.jpg", (self.__startPoint[0], self.__startPoint[1]), True)
        self.__nextDirection = 0

    def addDirection(self, newDirection, isFree):
        if isFree:
            self._direction = newDirection
            self.__nextDirection = 0
            print(self._direction)
        else:
            self.__nextDirection = newDirection
        print("Current Direction", self._direction)
        print("Next Direction", self.__nextDirection)

    def restart(self):
        self._position = pygame.Vector2(self.__startPoint[0], self.__startPoint[1])
        self._direction = 0
        self.__nextDirection = 0
        pygame.time.delay(1000)


class Ghost(Entity):
    def __init__(self, ghostType, isPlayer):  # 0 is blinky, 1 is inky, 2 is pinky, 3 is clyde
        self._manUp = 9999999999  # timer for scared phase, determines at what tick the ghost should stop being scared
        if ghostType == 0:
            Entity.__init__(self, "images/blinky.jpg", (336, 384), isPlayer)
        elif ghostType == 1:
            Entity.__init__(self, "images/inky.jpg", (336, 360), isPlayer)
        elif ghostType == 2:
            Entity.__init__(self, "images/pinky.jpg", (312, 384), isPlayer)
        elif ghostType == 3:
            Entity.__init__(self, "images/clyde.jpg", (312, 360), isPlayer)
        self._isScared = False
        self._isDead = False
        self._chaseMode = 1  # 0 is scatter state, 1 is chase state

    def reset(self):  # resets the ghost
        self._position = pygame.Vector2(self._startPos)
        self._speed = 1
        self._manUp = 9999999999
        self._isScared = False
        self._isDead = False
        self._chaseMode = 1

    def scareGhost(self):
        self._manUp = pygame.time.get_ticks() + 5000
        self._isScared = True
        self._img = pygame.transform.scale(pygame.image.load("images/scared.jpg"), (24, 24))
        self._speed = 0.5
        if self._direction != 0:
            if self._direction // 2 == 0:
                self._direction -= 1
            elif self._direction // 2 == 1:
                self._direction += 1
        self._direction = 4

    def runAway(self, targetVector):
        displacementVector = targetVector - self.getPosition()
        if displacementVector.x ** 2 < displacementVector.y ** 2:
            if displacementVector.x < 0:
                self._direction = 4
            else:
                self._direction = 3
        else:
            if displacementVector.y < 0:
                self._direction = 2
            else:
                self._direction = 1

    def killGhost(self):
        self._isDead = True
        self._isScared = False

    def update(self, dt):
        super().update(dt)
        if pygame.time.get_ticks() >= self._manUp:
            self._isScared = False
            self._img = pygame.transform.scale(pygame.image.load(self._imgJPG), (24, 24))
            self._speed = 1
            self._manUp = 9999999999

    def isScared(self):
        return self._isScared

    def isDead(self):
        return self._isDead


class Blinky(Ghost):
    def __init__(self, isPlayer):
        Ghost.__init__(self, 0, isPlayer)

    def chasePlayer(self, playerPos):
        displacementVector = list(playerPos - self.getPosition())
        if displacementVector[0] ** 2 > displacementVector[1] ** 2:
            if displacementVector[0] < 0:
                self._direction = 3
            else:
                self._direction = 4
        else:
            if displacementVector[1] < 0:
                self._direction = 1
            else:
                self._direction = 2


class Inky(Ghost):
    def __init__(self, isPlayer):
        Ghost.__init__(self, 1, isPlayer)

    def chasePlayer(self, playerPos, playerDir, blinkyPos):
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
        self._direction = approachVector(pygame.Vector2(targetVector))


class Pinky(Ghost):
    def __init__(self, isPlayer):
        Ghost.__init__(self, 2, isPlayer)

    def chasePlayer(self, playerPos, playerDir):
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
        if displacementVector[0] ** 2 > displacementVector[1] ** 2:
            if displacementVector[0] < 0:
                self._direction = 3
            else:
                self._direction = 4
        else:
            if displacementVector[1] < 0:
                self._direction = 1
            else:
                self._direction = 2


class GhostGroup:
    def __init__(self, *ghosts):
        self.__ghosts = []
        for entity in ghosts:
            self.__ghosts.append(entity)

    def ghostCollision(self, boundBox, screen):
        for ghost in self.__ghosts:
            if boundBox.colliderect(ghost.getBoundBox()):
                return True

    def resetGhosts(self):
        for ghost in self.__ghosts:
            ghost.reset()

    def scareGhosts(self):
        for ghost in self.__ghosts:
            if not (ghost.isDead()):
                ghost.scareGhost()

class Referee(Board):

    def isNextBlockWall(self, direction, gridPosition):
        if direction == 1:
            if self._board.getBoard()[gridPosition[1] - 1][gridPosition[0]] == 3:
                return True
            else:
                return False

        if direction == 2:
            if self._board.getBoard()[gridPosition[1] + 1][gridPosition[0]] == 3:
                return True
            else:
                return False

        if direction == 3:
            if self._board.getBoard()[gridPosition[1]][gridPosition[0] - 1] == 3:
                return True
            else:
                return False

        try:
            if direction == 4:
                if self._board.getBoard()[gridPosition[1]][gridPosition[0] + 1] == 3:
                    return True
                else:
                    return False
        except IndexError:  # Error handling for the case where the player enters a right side warp; in this case there wouldn't be an incoming collision
            return False









########################################################MAIN PROGRAM####################################################
def main():
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
    selectedBoard = boards.boardsdict["default"]
    board = Board(selectedBoard)
    pacman = Pacman()
    blinky = Blinky(False)
    inky = Inky(False)
    pinky = Pinky(False)
    clyde = Ghost(3, False)
    ghosts = GhostGroup(blinky, inky, pinky, clyde)
    game = Game(3, level, board, ghosts, pacman)
    referee = Referee(selectedBoard)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("black")

        currentPos = pacman.getPosition()
        gridPosition = getGridRef(currentPos[0], currentPos[1])

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
        if board.getDotsLeft() == 0:
            print("Level complete!")
            game.restart()
            pacman.restart()
            ghosts.resetGhosts()

        drawValue("Speed", pacman.getSpeed(), (400, 900), screen)
        # if keys[pygame.K_t]:
        # pacman.addSpeed(-0.01)
        #  if keys[pygame.K_y]:
        #       pacman.addSpeed(0.01)
        #  if keys[pygame.K_p]:
        #       print(pacman.getPosition())

        board.render(screen)
        game.render(screen)
        pacman.render(screen, dt)
        kys = pacman.getDirection()
        if inky.isScared():
            blinky.runAway(currentPos)
            inky.runAway(currentPos)
            clyde.runAway(currentPos)
            pinky.runAway(currentPos)
        else:
            blinky.chasePlayer(currentPos)
            inky.chasePlayer(currentPos, kys, blinky.getPosition())
            pinky.chasePlayer(currentPos, kys)
        blinky.render(screen, dt)
        inky.render(screen, dt)
        pinky.render(screen, dt)
        clyde.render(screen, dt)

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

        if ghosts.ghostCollision(pacmanBox, screen):
            game.addLives(-1)
            pacman.restart()
            ghosts.resetGhosts()

        if game.getLives() == 0:
            print("Ran out of lives!")
            running = False

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
    main()
