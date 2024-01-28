import pygame
from game import Board, getCoord, getGridRef
import boards
from structures import EventStack


class Creator(Board):
    def __init__(self, board):
        Board.__init__(self, board)
        self.eventStack = EventStack(10)

    def undo(self):
        try:
            changedCells = self.eventStack.pop()
            for item in changedCells:
                self._board[item[1]][item[0]] = changedCells[item]
        except:
            print("Cannot undo further")

    def pushToEventStack(self, value):
        self.eventStack.push(value)


    def changeCell(self, x, y, val):
        try:
            self._board[y][x] = val
        except:
            print("Out of range!")

    def checkGridType(self, x, y):
        if x == 0 or x == 32:
            return 1
        if y == 0 or y == 29:
            return 2
        else:
            return 3

    def isBorderCell(self, x, y):
        if self.checkGridType(x, y) < 3:
            return True

    def createWarp(self, x, y):
        pass

    def render(self, screen):
        for i in range(len(self._board)):
            for j in range(len(self._board[i])):
                pos = getCoord(j, i)
                if self._board[i][j] == 1:
                    pygame.draw.circle(screen, "white", pos, 3)
                elif self._board[i][j] == 2:
                    pygame.draw.circle(screen, "white", pos, 6)
                elif self._board[i][j] == 3:
                    pygame.draw.circle(screen, "blue", pos, 12)


def main():
    board = boards.boardsdict["blank"]
    pygame.init()
    pygame.display.set_caption('PAC-MAN')
    screen = pygame.display.set_mode((720, 960))
    running = True
    print(board)
    customBoard = Creator(board)
    saveButton = pygame.Rect((600, 900), (100, 50))
    changedCells = {}
    keyHeld = False

    while running:
        keys = pygame.key.get_pressed()
        screen.fill("black")
        pygame.draw.rect(screen, "blue", saveButton)
        my_font = pygame.font.SysFont('Jokerman', 30)
        saveText = my_font.render("Save", False, "White")
        screen.blit(saveText, (610, 900))
        customBoard.render(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                customBoard.pushToEventStack(changedCells)
                print(changedCells)
                changedCells = {}
            if event.type == pygame.KEYUP:
                keyHeld = False
        if pygame.mouse.get_pressed()[0]:
            if saveButton.collidepoint(pygame.mouse.get_pos()):
                running = False
            else:
                currentPos = getGridRef(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                if not (customBoard.isBorderCell(currentPos[0], currentPos[1])) and customBoard.getBoard()[currentPos[1]][currentPos[0]] != 3:
                    currentPos = getGridRef(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                    customBoard.changeCell(currentPos[0], currentPos[1], 3)
                    changedCells.update({currentPos: 0})
        elif pygame.mouse.get_pressed()[2]:
            currentPos = getGridRef(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            if not (customBoard.isBorderCell(currentPos[1], currentPos[0])) and customBoard.getBoard()[currentPos[1]][currentPos[0]] != 0:
                currentPos = getGridRef(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                customBoard.changeCell(currentPos[0], currentPos[1], 0)
                changedCells.update({currentPos: 3})
            else:
                customBoard.createWarp(currentPos[0], currentPos[1])

        if saveButton.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (0, 0, 102), saveButton)
            saveText = my_font.render("Save", False, (200, 200, 200))
            screen.blit(saveText, (610, 900))

        if keys[pygame.K_z] and not(keyHeld):
            customBoard.undo()
            keyHeld = True

        pygame.display.flip()


if __name__ == "__main__":
    main()
