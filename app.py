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
COLOR_SKYBLUE = (7, 218, 230)
COLOR_BLUE = (0,0,255)
COLOR_GREEN = (7, 138, 35)
COLOR_ROAD = (48,51,49)
DELAY = 50
DEBUG = True
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
    
    def move(self):
        if self.direction == Direction.UP:
            self.y -= self.vel
        elif self.direction == Direction.DOWN:
            self.y += self.vel
        elif self.direction == Direction.LEFT:
            self.x -= self.vel
        elif self.direction == Direction.RIGHT:
            self.x += self.vel
        
        if self.frameIndex < 2:
            self.frameIndex += 1
        else:
            self.frameIndex = 0
        
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
                    pos_x = i * FRAME_SIZE
                    pos_y = j * FRAME_SIZE
                    self.scenario[i][j] = (int(gridValue),pygame.Rect(pos_x,pos_y,FRAME_SIZE,FRAME_SIZE))
        csvFile.close()

    def getScenarioRects(self):
        n = N_FRAMES ** 2
        num_columns = N_FRAMES
        rects = [None] * n
        for index in range(n):
            x = index % num_columns
            y = index // num_columns
            _,rects[index] = self.scenario[x][y]
        return rects


    def getCoordsFromScenarioRectsIndex(self,rectIndex):
        num_columns = N_FRAMES
        x = rectIndex % num_columns
        y = rectIndex // num_columns
        return (x,y)

    def printScenario(self,debug = False):
        for i in range(N_FRAMES):
            for j in range(N_FRAMES):
                value,rect = self.scenario[i][j]
                if value == GridItemType.ROAD:
                    pygame.draw.rect(self.screen,COLOR_ROAD,rect)
                elif value == GridItemType.GROUND:
                    pygame.draw.rect(self.screen,COLOR_GREEN,rect)
                elif value == GridItemType.SEMAPH_GREEN:
                    self.screen.blit(self.semaph_green,(rect.x,rect.y))
                elif value == GridItemType.SEMAPH_RED:
                    self.screen.blit(self.semaph_red,(rect.x,rect.y))
                elif value == GridItemType.TARGET:
                    pygame.draw.rect(self.screen,COLOR_SKYBLUE,rect)
                if debug:
                    pygame.draw.rect(self.screen,COLOR_RED,rect,1)

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
        path = []
        c = 1
        move = None
        currentTarget = None

        while not self.gameover:
            pygame.time.delay(DELAY)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameover = True

                # click event and get the position
                if event.type ==pygame.MOUSEBUTTONDOWN:
                    mx,my=pygame.mouse.get_pos()
                    mx=int(mx/32)*32
                    my=int(my/32)*32
                    
                    mouseRect = pygame.Rect(mx,my,FRAME_SIZE,FRAME_SIZE)
                    scenarioRects = self.getScenarioRects()
                    collideIndex = mouseRect.collidelist(scenarioRects)
                    print(f'collide index: {collideIndex}')
                    x,y = self.getCoordsFromScenarioRectsIndex(collideIndex)
                    print(f'coords: {x,y}')
                    gridType,_ = self.scenario[x][y]
                    print(f'gridType: {gridType}')

                    if gridType is GridItemType.ROAD:
                        _,r = self.scenario[x][y]
                        self.scenario[x][y] = (GridItemType.TARGET,r)
                        if currentTarget is not None:
                            a,b = currentTarget
                            _,d = self.scenario[a][b]
                            self.scenario[a][b] = (1,d)
                        currentTarget = (x,y)

                
            #keys = pygame.key.get_pressed()

            self.screen.fill(SCREEN_BACKGROUND_COLOR)
            self.printScenario(DEBUG)

            self.player.blit_on(self.screen,DEBUG)
            if c == 9:
                if len(path) > 0:
                    move = path.pop(0)
                else:
                    move = None
                c = 1
            if move is not None:
                self.player.direction = move
                self.player.move()
            c += 1
            pygame.display.update()


def main():
    game = Game()
    game.preload()
    game.create()
    game.update()
     

if __name__=="__main__":
    main()


