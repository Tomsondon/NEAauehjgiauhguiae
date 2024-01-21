import random

import pygame, board, math, os

f = open("config.txt")
config = f.read()
f.close()
u = config[19:22]
d = config[30:34]
l = config[41:45]
r = config[53:57]


class Maze:
    def __init__(self, isRandom):  # Defines whether the maze is randomly generated or called from the function
        if isRandom:
            self._board = [[], []]
        elif not isRandom:
            self._board = board.board1
        self._time = 0
        self.__dotsLeft = 0


    def getCoord(self, x, y):
        coordX = ((24) * x) + 12
        coordY = ((24) * y) + 12
        return (coordX, coordY)

    def getGridRef(self, x, y):
        refX = round((x - 12) / 24)
        if refX > 29:
            refX = 29
        refY = round((y - 12) / 24)
        return (refX, refY)

    def generate(self):
        self.__dotsLeft = 0
        self._time = pygame.time.get_ticks()
        my_font = pygame.font.SysFont('Jokerman', 30)
        timeText = f"Time elapsed: {(self._time / 1000)}s"
        time_surface = my_font.render(timeText, False, (255, 255, 255))
        screen.blit(time_surface, (300, 800))
        board = self._board
        for j in range(len(board)):
            for i in range(len(board[j])):
                pos = self.getCoord(i, j)
                if board[j][i] == 1:
                    pygame.draw.circle(screen, "white", pos, 3)
                    self.__dotsLeft += 1
                elif board[j][i] == 2:
                    pygame.draw.circle(screen, "white", pos, 6)
                    self.__dotsLeft += 1
                elif board[j][i] > 2:
                    pygame.draw.circle(screen, "blue", pos, 12)

    def getDotsLeft(self):
        return self.__dotsLeft

    def getTime(self):
        return self._time


class Entity(Maze):
    def __init__(self):
        Maze.__init__(self, False)
        self.__colour = "yellow"
        self.__direction = 0  # 0 is stationary, 1 is up, 2 is down, 3 is left, 4 is right
        self.__nextMove = 0
        self.__gridRef = (14, 24)
        self.__posVector = pygame.Vector2(self.getCoord(self.__gridRef[0], self.__gridRef[1]))
        self.__score = 0

    def draw(self):
        pygame.draw.circle(screen, self.__colour, self.__posVector, 12)
        my_font = pygame.font.SysFont('Jokerman', 30)
        scoreText = f"Score: {self.__score}"
        score_surface = my_font.render(scoreText, False, (255, 255, 255))
        screen.blit(score_surface, (0, 800))

    def getCurrentPos(self):
        return self.__posVector

    def getCurrentGridRef(self):
        return self.__gridRef

    def getWallBoundings(self, posX, posY):  # returns a list with wall boundings at position entered to function (1 is up, 2 is down, 3 is left, 4 is right, 5 is left warp, 6 is right warp)
        board = self._board
        boundings = []
        if board[posY - 1][posX] > 2:
            boundings.append(1)
        if board[posY + 1][posX] > 2:
            boundings.append(2)
        try:
            if board[posY][posX - 1] > 2:
                boundings.append(3)
            if board[posY][posX - 1] == -1:
                boundings.append(5)
        except:
            pass
        try:
            if board[posY][posX + 1] > 2:
                boundings.append(4)
            elif board[posY][posX + 1] == -1:
                boundings.append(6)
        except:
            pass
        return boundings

    def addDirection(self, newDirection):
        boundings = self.getWallBoundings(self.__gridRef[0], self.__gridRef[1])
        if self.__direction == self.__nextMove:
            self.__nextMove = 0
        if not (newDirection in boundings):
            self.__direction = newDirection
            self.__nextMove = 0
        else:
            if self.__direction != 0:
                self.__nextMove = newDirection

    def move(self):
        if 6 in self.getWallBoundings(self.__gridRef[0], self.__gridRef[1]) and self.__direction == 4:
            self.__gridRef = (0, 15)
            self.__posVector = pygame.Vector2(self.getCoord(0, 15))
        elif 5 in self.getWallBoundings(self.__gridRef[0], self.__gridRef[1]) and self.__direction == 3:
            self.__gridRef = (29, 15)
            self.__posVector = pygame.Vector2(self.getCoord(29, 15))

        if self.__nextMove not in self.getWallBoundings(self.__gridRef[0], self.__gridRef[1]) and self.__nextMove != 0:
            self.__direction = self.__nextMove
        if self.__direction in self.getWallBoundings(self.__gridRef[0], self.__gridRef[1]):
            self.__direction = self.__nextMove
            self.__nextMove = 0
            if self.__direction in self.getWallBoundings(self.__gridRef[0], self.__gridRef[1]):
                self.__direction = 0

        if self.__direction == 1:
            self.__posVector.y -= 300 * dt
        elif self.__direction == 2:
            self.__posVector.y += 300 * dt
        elif self.__direction == 3:
            self.__posVector.x -= 300 * dt
        elif self.__direction == 4:
            self.__posVector.x += 300 * dt

        self.__gridRef = self.getGridRef(self.__posVector.x, self.__posVector.y)
        if 2 >= self._board[self.__gridRef[1]][self.__gridRef[0]] > 0:
            self.__score += 10
            if self._board[self.__gridRef[1]][self.__gridRef[0]] == 2:
                self.__score += 40
                self.powerUp()
            self._board[self.__gridRef[1]][self.__gridRef[0]] = 0

    def getScore(self):
        return self.__score

    def powerUp(self):
        print("got the power up")


class Ghost(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.__colour = "Red"
        self.__gridRef = (2, 2)
        self.__posVector = pygame.Vector2(self.getCoord(self.__gridRef[0], self.__gridRef[1]))









# pygame setup
pygame.init()
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
arena = Maze(False)
hero = Entity()
clyde = Ghost()

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    # RENDER YOUR GAME HERE

    arena.generate()
    hero.draw()
    clyde.draw()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        hero.addDirection(1)
    if keys[pygame.K_s]:
        hero.addDirection(2)
    if keys[pygame.K_a]:
        hero.addDirection(3)
    if keys[pygame.K_d]:
        hero.addDirection(4)
    if keys[pygame.K_ESCAPE]:
        running = False

    clyde.addDirection(random.randint(1,4))



    hero.move()
    score = hero.getScore()
    if arena.getDotsLeft() == 0:
        f = open("maze.txt","w")
        f.write(arena.getTime())
        f.close()
        running = False

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(fps)  # limits FPS to whatever was set at the start
    dt = clock.tick(fps) / 1000
pygame.quit()
