# import the pygame module, so you can use it
import pygame
from os import path

#Constants
GAME_WIDTH = GAME_HEIGHT = 800
SCREEN_BACKGROUND_COLOR = (96,96,96)
FRAME_SIZE = 32
N_FRAMES = GAME_WIDTH // FRAME_SIZE
COLOR_RED = (255,0,0)
DELAY = 50


class Player:
    def __init__(self,x,y,width,height,vel):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.vel=vel




class Game:
    def __init__(self):
        self.gameover = False
        self.player = None
    

    def printGrid(self):
        for i in range(N_FRAMES):
            for j in range(N_FRAMES):\
                pygame.draw.rect(self.screen,COLOR_RED,(i * FRAME_SIZE,j * FRAME_SIZE,FRAME_SIZE,FRAME_SIZE),1)

    def preload(self):
        pygame.init()
        
        #Load resources
        self.logo = pygame.image.load(path.join('resources','logo.png'))
        self.semaph_red = pygame.image.load(path.join('resources','semaphore-red.png'))

        #Init game
        pygame.display.set_icon(self.logo)
        pygame.display.set_caption("Grin Route")

        #Create instances
        self.player=Player(0,0,FRAME_SIZE,FRAME_SIZE,4)
        self.screen = pygame.display.set_mode((GAME_WIDTH,GAME_HEIGHT))
        self.semaph_red = pygame.image.load(path.join('resources','semaphore-red.png'))
        self.semaph_green = pygame.image.load(path.join('resources','semaphore-green.png'))

    def create(self):
        #First draw
        self.screen.fill(SCREEN_BACKGROUND_COLOR) 
        self.printGrid()
        
        pygame.draw.rect(self.screen, COLOR_RED, (self.player.x, self.player.y, self.player.width, self.player.height))  

        pos_x = 5 * FRAME_SIZE
        pos_y = 10 * FRAME_SIZE
        self.screen.blit(self.semaph_red,(pos_x,pos_y))

        pygame.display.update()

    def update(self):

        while not self.gameover:
            pygame.time.delay(DELAY)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameover = True
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player.x -= self.player.vel
            if keys[pygame.K_RIGHT]:
                self.player.x += self.player.vel
            if keys[pygame.K_UP]:
                self.player.y -= self.player.vel
            if keys[pygame.K_DOWN]:
                self.player.y += self.player.vel
            self.screen.fill(SCREEN_BACKGROUND_COLOR)
            self.printGrid()
            pos_x = 5 * FRAME_SIZE
            pos_y = 10 * FRAME_SIZE
            self.screen.blit(self.semaph_red,(pos_x,pos_y))

            pos_x = 24 * FRAME_SIZE
            pos_y = 24 * FRAME_SIZE
            self.screen.blit(self.semaph_green,(pos_x,pos_y))

            pygame.draw.rect(self.screen, COLOR_RED, (self.player.x, self.player.y, self.player.width, self.player.height))   
            pygame.display.update() 


def main():
    game = Game()
    game.preload()
    game.create()
    game.update()
     

if __name__=="__main__":
    main()