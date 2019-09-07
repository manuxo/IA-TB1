# import the pygame module, so you can use it
import pygame
from os import path

#Constants
GAME_WIDTH = GAME_HEIGHT = 800


class Player:
    def __init__(self,x,y,width,height,vel):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.vel=vel

player=Player(32,32,32,32,5)

# this function is used to load all the resources
def preload():
    pygame.init()
    logo = pygame.image.load(path.join("./resources/bike.png"))
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Grin Route")

# this function is used to show the player and can do the algorithm
def update():
    gameover = False

    # main loop
    while not gameover:

        pygame.time.delay(50)

        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                gameover = True

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            player.x -= player.vel

        if keys[pygame.K_RIGHT]:
            player.x += player.vel

        if keys[pygame.K_UP]:
            player.y -= player.vel

        if keys[pygame.K_DOWN]:
            player.y += player.vel
        
        # set the size of screen
        screen = pygame.display.set_mode((GAME_WIDTH,GAME_HEIGHT))
        # fill is use to paint many times the background
        screen.fill((0,0,0)) 
        # paint the player
        pygame.draw.rect(screen, (255,0,0), (player.x, player.y, player.width, player.height))   
        # show the player in screen
        pygame.display.update() 
        


# define a main function
def main():
    preload()
    update()
     
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()