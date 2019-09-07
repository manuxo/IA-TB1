# import the pygame module, so you can use it
import pygame
 
GAME_WIDTH = GAME_HEIGHT = 800


def preload():
    pygame.init()
    logo = pygame.image.load("./resources/bike.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Grin Route")

def create():
    screen = pygame.display.set_mode((800,800))

def update():
    gameover = False
    # main loop
    while not gameover:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                gameover = True


# define a main function
def main():
    preload()
    create()
    update()
     
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()