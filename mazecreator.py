import pygame
import game
import boards


class Creator(game.Game):
    def changeBox(self, x, y):
        self._board[y][x] = (self._board[y][x] + 1) % 4
        print(self._board[y][x])

    def Render(self, screen):
        for i in range(len(self._board)):
            for j in range(len(self._board[i])):
                pos = game.getCoord(j, i)
                if self._board[i][j] == 1:
                    pygame.draw.circle(screen, "white", pos, 3)
                elif self._board[i][j] == 2:
                    pygame.draw.circle(screen, "white", pos, 6)
                elif self._board[i][j] == 3:
                    pygame.draw.circle(screen, "blue", pos, 12)


def main():
    board = boards.blankboard
    pygame.init()
    pygame.display.set_caption('PAC-MAN')
    screen = pygame.display.set_mode((720, 960))
    running = True
    print(board)
    customBoard = Creator(1, 1, board)
    saveButton = pygame.Rect((600, 900), (100,50))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                currentPos = game.getGridRef(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                customBoard.changeBox(currentPos[0], currentPos[1])


        screen.fill("black")
        pygame.draw.rect(screen, "blue", saveButton)
        my_font = pygame.font.SysFont('Jokerman', 30)
        val_surface = my_font.render("Save", False, "White")
        screen.blit(val_surface, (610, 900))
        customBoard.Render(screen)
        pygame.display.flip()


if __name__ == "__main__":
    main()
