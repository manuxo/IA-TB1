# import the pygame module, so you can use it
import pygame
import csv
from random import choice
from os import path


#TB1 Modules
from tb1util.Enums import GridItemType,Direction
from tb1util.Spritesheet import SpriteSheet


#Constants
GAME_WIDTH = GAME_HEIGHT = 800
SCREEN_BACKGROUND_COLOR = (48,51,49)
FRAME_SIZE = 32
N_FRAMES = GAME_WIDTH // FRAME_SIZE
COLOR_RED = (255,0,0)
COLOR_BLUE = (0,0,255)
COLOR_GREEN = (7, 138, 35)
COLOR_ROAD = (48,51,49)
DELAY = 50
DEBUG = False
PLAYER_COLORKEY = (69,242,39)




class GridItem:
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height

class Player(GridItem):
    def __init__(self,x,y,width,height,vel,spritesheet = None,direction = Direction.RIGHT, frameIndex = 0):
        super().__init__(x,y,width,height)
        self.vel=vel
        self.direction = direction
        self.frameIndex = frameIndex
        self.spritesheet = spritesheet

        if self.spritesheet is not None:
            frames = []
            for i in range(15):
                frames.append((i*FRAME_SIZE,0,FRAME_SIZE,FRAME_SIZE))

            self.images = [None] * 4
            for dir in [Direction.LEFT,Direction.RIGHT,Direction.DOWN,Direction.UP]:
                a = dir * 3
                b = a + 3
                self.images[dir] = self.spritesheet.images_at(frames[a:b],PLAYER_COLORKEY)
    
    def move(self,player,screen):
        if self.direction == Direction.LEFT:
            for i in range(8):
                self.x -= self.vel
                player.blit_on(screen,DEBUG)
                pygame.display.update()
                pygame.time.delay(DELAY)

        if self.direction == Direction.RIGHT:
            for i in range(8):
                self.x += self.vel
                pygame.display.update()
                player.blit_on(screen,DEBUG)
                pygame.time.delay(DELAY)

        if self.direction == Direction.UP:
            for i in range(8):
                self.y -= self.vel
                pygame.display.update()
                player.blit_on(screen,DEBUG)
                pygame.time.delay(DELAY)

        if self.direction == Direction.DOWN:
            for i in range(8):
                self.y += self.vel
                pygame.display.update()
                player.blit_on(screen,DEBUG)
                pygame.time.delay(DELAY)

        if self.frameIndex < 2:
            self.frameIndex += 1
        else:
            self.frameIndex = 0

        """
        if self.direction == Direction.UP:
            self.y -= self.vel
        elif self.direction == Direction.DOWN:
            self.y += self.vel
        elif self.direction == Direction.LEFT:
            self.x -= self.vel
        elif self.direction == Direction.RIGHT:
            self.x += self.vel
        """


    def stop(self):
        self.frameIndex = 0

    def blit_on(self,screen,debug = False):
        if self.images is not None:
            screen.blit(self.images[self.direction][self.frameIndex],(self.x, self.y))
        if debug:
            pygame.draw.rect(screen,COLOR_BLUE,(self.x,self.y,FRAME_SIZE,FRAME_SIZE),1)

    


class Game:
    def __init__(self):
        self.gameover = False
        self.player = None
        self.readScenario()

    def readScenario(self,level = 1):
        with open(path.join('resources','maps',f'map{level}.csv'),'r') as csvFile:
            reader = csv.reader(csvFile)
            self.scenario = [[0 for i in range(N_FRAMES)] for j in range(N_FRAMES)] 
            for i,row in enumerate(reader):
                for j,gridValue in enumerate(row):
                    self.scenario[i][j] = int(gridValue)
            for row in self.scenario:
                print(row)

        csvFile.close()

    def printScenario(self,debug = False):
        for i in range(N_FRAMES):
            for j in range(N_FRAMES):
                value = self.scenario[i][j]
                pos_x = i * FRAME_SIZE
                pos_y = j * FRAME_SIZE
                if value == GridItemType.ROAD:
                    pygame.draw.rect(self.screen,COLOR_ROAD,(pos_x,pos_y,FRAME_SIZE,FRAME_SIZE))
                elif value == GridItemType.GROUND:
                    pygame.draw.rect(self.screen,COLOR_GREEN,(pos_x,pos_y,FRAME_SIZE,FRAME_SIZE))
                elif value == GridItemType.SEMAPH_GREEN:
                    self.screen.blit(self.semaph_green,(pos_x,pos_y))
                elif value == GridItemType.SEMAPH_RED:
                    self.screen.blit(self.semaph_red,(pos_x,pos_y))
                if debug:
                    pygame.draw.rect(self.screen,COLOR_RED,(pos_x,pos_y,FRAME_SIZE,FRAME_SIZE),1)

    def preload(self):
        #Init game
        pygame.init()
        self.screen = pygame.display.set_mode((GAME_WIDTH,GAME_HEIGHT))
        

        #Load resources
        self.logo = pygame.image.load(path.join('resources','logo.png'))
        self.semaph_red = pygame.image.load(path.join('resources','semaphore-red.png'))
        self.semaph_green = pygame.image.load(path.join('resources','semaphore-green.png'))
        self.ss_player = SpriteSheet(path.join('resources','player.png'))

        #Create instances
        self.player=Player(0*FRAME_SIZE,0*FRAME_SIZE,FRAME_SIZE,FRAME_SIZE,4,self.ss_player)

        pygame.display.set_icon(self.logo)
        pygame.display.set_caption("Grin Route")

    def create(self):
        #First draw
        self.screen.fill(SCREEN_BACKGROUND_COLOR) 
        self.printScenario(DEBUG)
        pygame.display.update()

    def update(self):
        c = 1
        path = [Direction.DOWN,Direction.RIGHT,Direction.RIGHT,Direction.UP,Direction.RIGHT]
        self.player.direction = path.pop(0)

        while not self.gameover:
            pygame.time.delay(DELAY)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameover = True
            
            keys = pygame.key.get_pressed()
            
            self.screen.fill(SCREEN_BACKGROUND_COLOR)
            self.printScenario(DEBUG)
            
            move = True
            if len(path) > 0:
                if c == 8:
                    self.player.direction = path.pop(0)
                    move = False
                    self.player.stop()
                    c = 1
                c += 1
            else:
                move = False
                c = 1
            
            if move:
                self.player.move(self.player,self.screen)

            #keys = pygame.key.get_pressed()

            self.player.blit_on(self.screen,DEBUG)
            pygame.display.update()


def main():
    game = Game()
    game.preload()
    game.create()
    game.update()
     

if __name__=="__main__":
    main()
