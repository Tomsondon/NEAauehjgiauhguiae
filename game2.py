import os
import board
import pygame
import datetime

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
    refX = (x - 12) // 24
    if refX > 29:
        refX = 29
    refY = (y - 12) // 24
    return refX, refY


def drawValue(text, variable, pos, screen):
    my_font = pygame.font.SysFont('Jokerman', 30)
    valText = f"{text}: {variable}"
    val_surface = my_font.render(valText, False, "White")
    screen.blit(val_surface, pos)


def createNodeMap(maze):
    nodeMap = board.createNodeMap(maze)


def Square(x, y, size):
    return pygame.Rect(x - size / 2, y - size / 2, size, size)


class Game:
    def __init__(self, lives, Level):
        if Level == 1:
            self._board = board.boards
        self._time = pygame.time.get_ticks()
        self.__dotsLeft = 0
        self.__score = 0
        self.__lives = lives
        self.__wallPositions = []
        self.__pelletPositions = []
        self.__ogPelletPositions = []
        self.__pelletPositions = []
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

    def Render(self, screen):
        self._time = pygame.time.get_ticks()
        drawValue("Score", self.__score, (0, 800), screen)
        drawValue("Time", self._time / 1000, (300, 800), screen)
        drawValue("Lives", self.__lives, (600, 800), screen)
        drawValue("Dots left", self.getDotsLeft(), (0, 900), screen)
        for i in self.__wallPositions:
            pygame.draw.rect(screen, "blue", i, 1)
        for i in self.__pelletPositions:
            pygame.draw.rect(screen, "white", i)

    def getDotsLeft(self):
        return len(self.__pelletPositions)

    def getTime(self):
        return self._time



class Entity:
    def __init__(self, img, position):
        self._imgJPG = img
        self._img = pygame.transform.scale(pygame.image.load(img), (24, 24))
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

    def Render(self, screen, dt):
        self.Update(dt)
        self._boundBox = Square(self._position.x, self._position.y, 24)
        screen.blit(self._img, (self._position.x-12, self._position.y-12))
        pygame.draw.rect(screen, "red", self._boundBox, 1)
        pygame.draw.circle(screen,"green",self._position,3)


    def Update(self, dt):
        if self._direction != 0:
            if self._direction == 1:
                self._position.y -= self._speed * 300 * dt
            if self._direction == 2:
                self._position.y += self._speed * 300 * dt
            if self._direction == 3:
                self._position.x -= self._speed * 300 * dt
            if self._direction == 4:
                self._position.x += self._speed * 300 * dt

            if self._position.x < 0:
                self._position.x = 720
            if self._position.x > 720:
                self._position.x = 0


class Player(Entity):
    def __init__(self):
        self.__startPoint = getCoord(14, 24)
        Entity.__init__(self, "images/player.jpg", (self.__startPoint[0], self.__startPoint[1]))
        self.__nextDirection = 0

    def addDirection(self, newDirection):
        if self._direction == 0:
            self._direction = newDirection
        else:
            self._direction = newDirection

    def Update(self, dt):
        super().Update(dt)
        self._speed = 1

    def Restart(self):
        self._position = pygame.Vector2(self.__startPoint[0], self.__startPoint[1])
        self._direction = 0
        self.__nextDirection = 0
        pygame.time.delay(1000)


class Ghost(Entity):
    def __init__(self, ghostType):  # 0 is blinky, 1 is inky, 2 is pinky, 3 is clyde
        self._manUp = 9999999999  # timer for scared phase, determines at what tick the ghost should stop being scared
        if ghostType == 0:
            Entity.__init__(self, "images/blinky.jpg", (336, 384))
        elif ghostType == 1:
            Entity.__init__(self, "images/inky.jpg", (336, 360))
        elif ghostType == 2:
            Entity.__init__(self, "images/pinky.jpg", (312, 384))
        elif ghostType == 3:
            Entity.__init__(self, "images/clyde.jpg", (312, 360))
        self._isScared = False
        self._isDead = False
        self._chaseMode = 1  # 0 is scatter state, 1 is chase state

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

    def Update(self, dt):
        super().Update(dt)
        if pygame.time.get_ticks() >= self._manUp:
            self._isScared = False
            self._img = pygame.transform.scale(pygame.image.load(self._imgJPG), (24, 24))
            self._speed = 1
            self._manUp = 9999999999

    def isScared(self):
        return self._isScared


class Blinky(Ghost):
    def __init__(self):
        Ghost.__init__(self, 0)

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
    def __init__(self):
        Ghost.__init__(self, 1)

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
    def __init__(self):
        Ghost.__init__(self, 2)

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
    game = Game(3, level)
    hero = Player()
    blinky = Blinky()
    inky = Inky()
    pinky = Pinky()
    clyde = Ghost(3)

    def ghostCollision():
        if heroBox.colliderect(blinky.getBoundBox()) or heroBox.colliderect(inky.getBoundBox()) or heroBox.colliderect(
                pinky.getBoundBox()) or heroBox.colliderect(clyde.getBoundBox()):
            return True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("black")

        currentPos = hero.getPosition()

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
            print("Level complete!")
            running = False

        drawValue("Speed", hero.getSpeed(), (400, 900), screen)
        # if keys[pygame.K_t]:
        # hero.addSpeed(-0.01)
        #  if keys[pygame.K_y]:
        #       hero.addSpeed(0.01)
        #  if keys[pygame.K_p]:
        #       print(hero.getPosition())

        game.Render(screen)
        hero.Render(screen, dt)
        kys = hero.getDirection()
        if inky.isScared():
            blinky.runAway(currentPos)
            inky.runAway(currentPos)
            clyde.runAway(currentPos)
            pinky.runAway(currentPos)
        else:
            blinky.chasePlayer(currentPos)
            inky.chasePlayer(currentPos, kys, blinky.getPosition())
            pinky.chasePlayer(currentPos, kys)
        blinky.Render(screen, dt)
        inky.Render(screen, dt)
        pinky.Render(screen, dt)
        clyde.Render(screen, dt)

        heroBox = hero.getBoundBox()
        # if game.collidesWithWall(heroBox):
        # hero.setPosition(currentPos)
        # hero.setDirection(0)
        pelletCheck = game.collidesWithPellet(heroBox)
        if pelletCheck == 1:
            game.addScore(10)
        elif pelletCheck == 2:
            game.addScore(50)
            blinky.scareGhost()
            inky.scareGhost()
            pinky.scareGhost()
            clyde.scareGhost()

        if ghostCollision():
            game.addLives(-1)
            hero.Restart()
            blinky = Blinky()
            inky = Inky()
            pinky = Pinky()

        if game.getLives() == 0:
            print("Ran out of lives!")
            running = False

        pygame.display.flip()

        clock.tick(fps)
        dt = clock.tick(fps) / 1000

    ###WRITE TO FILE###
    if not (os.path.exists("leaderboard.txt")):
        print("LEADERBOARD FILE DOES NOT EXIST, CREATING NEW LEADERBOARD FILE")
    else:
        pass

    currentTime = datetime.datetime.now()
    f = open("leaderboard.txt", "a")
    f.write(str(currentTime.strftime("%x")))
    f.write("   ")
    f.write(str(game.getScore()))
    f.write("   ")
    f.write(str(game.getTime()))
    f.write("\n")
    f.close()


########################################################################################################################

if __name__ == "__main__":
    main()
