import pygame
import pygame_menu
from pygame_menu import themes
import game2

pygame.init()
surface = pygame.display.set_mode((720, 960))
pygame.display.set_caption('PAC-MAN')
icon = pygame.image.load("pictuer2 053.jpg")
pygame.display.set_icon(icon)


def set_difficulty(value, difficulty):
    print(value)
    print(difficulty)

def start_the_game():
    game2.main()

def leaderboard_table():
    mainmenu._open(level)


mainmenu = pygame_menu.Menu('Welcome', 720, 960, theme=themes.THEME_SOLARIZED)
mainmenu.add.button('Play', start_the_game)
mainmenu.add.button('Leaderboard', leaderboard_table)
mainmenu.add.button('Settings', leaderboard_table)
mainmenu.add.button('Replay', leaderboard_table)
mainmenu.add.button('Quit', pygame_menu.events.EXIT)




level = pygame_menu.Menu('Select a Difficulty', 600, 400, theme=themes.THEME_BLUE)
level.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)

loading = pygame_menu.Menu('Loading the Game...', 600, 400, theme=themes.THEME_DARK)
loading.add.progress_bar("Progress", progressbar_id = "1", default=0, width = 200, )

arrow = pygame_menu.widgets.LeftArrowSelection(arrow_size = (10, 15))

update_loading = pygame.USEREVENT + 0

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == update_loading:
            progress = loading.get_widget("1")
            progress.set_value(progress.get_value() + 1)
            if progress.get_value() == 100:
                pygame.time.set_timer(update_loading, 0)
        if event.type == pygame.QUIT:
            exit()

    if mainmenu.is_enabled():
        mainmenu.update(events)
        mainmenu.draw(surface)
        if (mainmenu.get_current().get_selected_widget()):
            arrow.draw(surface, mainmenu.get_current().get_selected_widget())
    pygame.display.update()