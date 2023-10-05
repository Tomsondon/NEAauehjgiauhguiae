import board
import pygame

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
    refX = (x - 12) // 24
    if refX > 29:
        refX = 29
    refY = (y - 12) // 24
    return refX, refY


def drawValue(identifier, variable, pos):
    my_font = pygame.font.SysFont('Jokerman', 30)
    valText = f"{identifier}: {variable}"
    val_surface = my_font.render(valText, False, "White")
    screen.blit(val_surface, pos)


def createNodeMap(maze):
    nodeMap = board.createNodeMap(maze)


class Game:
    def __init__(self, lives, Level):
        if Level == 1:
            self._board = board.board1
        self._time = pygame.time.get_ticks()
        self.__dotsLeft = 0
        self.__score = 0
        self.__lives = lives
        self.__wallPositions = []
        self.__pelletPositions = []
        for j in range(len(self._board)):
            for i in range(len(self._board[j])):
                pos = getCoord(i, j)
                if self._board[j][i] == 1:
                    self.__pelletPositions.append(pygame.Rect(pos[0] - 3, pos[1] - 3, 6, 6))
                    self.__dotsLeft += 1
                elif self._board[j][i] == 2:
                    self.__pelletPositions.append(pygame.Rect(pos[0] - 6, pos[1] - 6, 12, 12))
                    self.__dotsLeft += 1
                elif self._board[j][i] > 2:
                    self.__wallPositions.append(pygame.Rect(pos[0] - 12, pos[1] - 12, 24, 24))

    def addLives(self, lives):
        self.__lives += lives

    def getLives(self):
        return self.__lives

    def getScore(self):
        return self.__score

    def addScore(self, score):
        self.__score += score

    def getBoard(self):
        return self._board

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

    def Render(self):
        self._time = pygame.time.get_ticks()
        drawValue("Score", self.__score, (0, 800))
        drawValue("Time", self._time / 1000, (300, 800))
        drawValue("Lives", self.__lives, (600, 800))
        drawValue("Dots left", self.getDotsLeft(), (0, 900))
        for x in self.__wallPositions:
            pygame.draw.rect(screen, "blue", x, 1)
        for y in self.__pelletPositions:
            pygame.draw.rect(screen, "white", y)

    def getDotsLeft(self):
        return len(self.__pelletPositions)

    def getTime(self):
        return self._time


class Entity:
    def __init__(self, img, position):
        self._img = pygame.transform.scale(pygame.image.load(img), (24, 24))
        self._position = pygame.Vector2(position)
        self._direction = 0
        self._speed = 1
        self._boundBox = pygame.Rect(self._position.x - 12, self._position.y - 12, 24, 24)

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

    def Render(self):
        self.updatePos()
        self._boundBox = pygame.Rect(self._position.x, self._position.y, 24, 24)
        screen.blit(self._img, self._position)
        pygame.draw.rect(screen, "red", self._boundBox, 1)

    def updatePos(self):
        if self._direction != 0:
            if self._direction == 1:
                self._position.y -= self._speed * 300 * dt
            if self._direction == 2:
                self._position.y += self._speed * 300 * dt
            if self._direction == 3:
                self._position.x -= self._speed * 300 * dt
            if self._direction == 4:
                self._position.x += self._speed * 300 * dt


class Player(Entity):
    def __init__(self):
        Entity.__init__(self, "pictuer2 053.jpg", (168, 200))
        self.__nextDirection = 0

    def addDirection(self, newDirection):
        if self._direction == 0:
            self._direction = newDirection
        else:
            self._direction = newDirection


class Ghost(Entity):
    def __init__(self, ghostType):  # 0 is blinky, 1 is inky, 2 is pinky, 3 is clyde
        if ghostType == 0:
            Entity.__init__(self, "blinky.jpg", (300, 1))
        elif ghostType == 1:
            Entity.__init__(self, "inky.jpg", (600, 1))
        elif ghostType == 2:
            Entity.__init__(self, "pinky.jpg", (1, 300))
        elif ghostType == 3:
            Entity.__init__(self, "clyde.jpg", (300, 600))


##################################MAIN PROGRAM####################################################

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
game = Game(3, level)
hero = Player()
blinky = Ghost(0)
inky = Ghost(1)
pinky = Ghost(2)
clyde = Ghost(3)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

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
    if game.getDotsLeft() == 0:
        running = False

    if keys[pygame.K_t]:
        hero.addSpeed(-0.1)
    if keys[pygame.K_y]:
        hero.addSpeed(0.1)

    game.Render()
    hero.Render()
    blinky.Render()
    inky.Render()
    pinky.Render()
    clyde.Render()

    heroBox = hero.getBoundBox()
    if game.collidesWithWall(heroBox):
        pass
    pelletCheck = game.collidesWithPellet(heroBox)
    if pelletCheck == 1:
        game.addScore(10)
    elif pelletCheck == 2:
        game.addScore(50)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(fps)  # limits FPS to whatever was set at the start
    dt = clock.tick(fps) / 1000
pygame.quit()
