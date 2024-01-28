import pygame, time


def drawValue(text, variable, pos, screen):
    my_font = pygame.font.SysFont('Jokerman', 30)
    valText = f"{text}: {variable}"
    val_surface = my_font.render(valText, False, "Black")
    screen.blit(val_surface, pos)


class Textbox:
    def __init__(self, left, top, width, height, colour):
        self.textbox = pygame.Rect(left, top, width, height)
        self.colour = colour
        self.inputtedWord = []

    def draw(self, surface):
        pygame.draw.rect(surface, self.colour, self.textbox)
        drawValue('', "dave", (self.textbox.left, self.textbox.top), surface)

    def inputText(self):
        inputtedWord = self.inputtedWord
        keys = pygame.key.get_pressed()
        while not (keys[pygame.k_ENTER]):
            return inputtedWord






pygame.init()
pygame.font.init()
textbox = Textbox(400, 400, 400, 400, "black")
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # RENDER YOUR GAME HERE
    textbox.draw(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()