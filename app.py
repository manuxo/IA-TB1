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


class spritesheet(object):
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert()
    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey = None):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image
    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey = None):
        "Loads multiple images, supply a list of coordinates" 
        return [self.image_at(rect, colorkey) for rect in rects]
    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey = None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)

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
            for j in range(N_FRAMES):
                pygame.draw.rect(self.screen,COLOR_RED,(i * FRAME_SIZE,j * FRAME_SIZE,FRAME_SIZE,FRAME_SIZE),1)

    def preload(self):
        #Init game
        pygame.init()
        self.screen = pygame.display.set_mode((GAME_WIDTH,GAME_HEIGHT))
        

        #Load resources
        self.logo = pygame.image.load(path.join('resources','logo.png'))
        self.semaph_red = pygame.image.load(path.join('resources','semaphore-red.png'))
        self.semaph_green = pygame.image.load(path.join('resources','semaphore-green.png'))

        self.ss_player = spritesheet(path.join('resources','player.png'))

        rects = []
        for i in range(15):
            rects.append((i*FRAME_SIZE,0,FRAME_SIZE,FRAME_SIZE))
        

        #LEFT
        self.images_player_left = self.ss_player.images_at(rects[0:3],(7,242,169))
        #RIGHT
        self.images_player_right = self.ss_player.images_at(rects[3:7],(7,242,169))

        #DOWN
        self.images_player_down = self.ss_player.images_at(rects[7:11],(7,242,169))

        #UP
        self.images_player_up = self.ss_player.images_at(rects[11:15],(7,242,169))

        #Create instances
        self.player=Player(0,0,FRAME_SIZE,FRAME_SIZE,4)

        pygame.display.set_icon(self.logo)
        pygame.display.set_caption("Grin Route")

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
        c = 0
        images_player = self.images_player_right
        while not self.gameover:
            pygame.time.delay(DELAY)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameover = True
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player.x -= self.player.vel
                images_player = self.images_player_left
            if keys[pygame.K_RIGHT]:
                self.player.x += self.player.vel
                images_player = self.images_player_right
            if keys[pygame.K_UP]:
                images_player = self.images_player_up
                self.player.y -= self.player.vel
            if keys[pygame.K_DOWN]:
                images_player = self.images_player_down
                self.player.y += self.player.vel
            
            self.screen.fill(SCREEN_BACKGROUND_COLOR)
            self.printGrid()
            pos_x = 5 * FRAME_SIZE
            pos_y = 10 * FRAME_SIZE
            self.screen.blit(self.semaph_red,(pos_x,pos_y))

            pos_x = 24 * FRAME_SIZE
            pos_y = 24 * FRAME_SIZE
            self.screen.blit(self.semaph_green,(pos_x,pos_y))

            self.screen.blit(images_player[c],(self.player.x, self.player.y))
            n_player = len(images_player)
            if c < n_player - 1:
                c += 1
            else:
                c = 0
            pygame.display.update()


def main():
    game = Game()
    game.preload()
    game.create()
    game.update()
     

if __name__=="__main__":
    main()