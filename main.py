import pygame, sys
from config import *
from level import *
class Game:
    def __init__(self):
        pygame.init()
        self.screen=pygame.display.set_mode((screen_width,screen_height))
        self.clock=pygame.time.Clock()
        self.level=Level()
        pygame.display.set_caption("Knight Adventure")
    def run(self):
        while(True):
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_m:
                        self.level.toggle_menu()
            self.screen.fill((102, 217, 255))
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)
if  __name__=="__main__":
    game=Game()
    game.run()
