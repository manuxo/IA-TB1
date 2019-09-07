# import the pygame module, so you can use it
import pygame
from os import path
 
GAME_WIDTH = GAME_HEIGHT = 800
SCREEN_BACKGROUND_COLOR = (96,96,96)
FRAME_SIZE = 32
N_FRAMES = GAME_WIDTH // FRAME_SIZE
COLOR_RED = (255,0,0)

class Game:

    def __init__(self):
        self.gameover = False

    def preload(self):
        pygame.init()
        self.logo = pygame.image.load(path.join('resources','logo.png'))
        pygame.display.set_icon(self.logo)
        pygame.display.set_caption("Grin Route")  
        self.semaph_red = pygame.image.load(path.join('resources','semaphore-red.png'))
        

    def create(self):
        DISPLAY = pygame.display.set_mode((GAME_WIDTH,GAME_HEIGHT))
        DISPLAY.fill(SCREEN_BACKGROUND_COLOR)
        #draw frames
        for i in range(N_FRAMES):
            for j in range(N_FRAMES):\
                pygame.draw.rect(DISPLAY,COLOR_RED,(i * FRAME_SIZE,j * FRAME_SIZE,FRAME_SIZE,FRAME_SIZE),1)
        pos_x = 5 * FRAME_SIZE
        pos_y = 10 * FRAME_SIZE
        DISPLAY.blit(self.semaph_red,(pos_x,pos_y))
        pygame.display.flip()

    def update(self):
        # main loop
        while not self.gameover:
            # event handling, gets all event from the event queue
            for event in pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    self.gameover = True


# define a main function
def main():
    game = Game()
    game.preload()
    game.create()
    game.update()
     
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()