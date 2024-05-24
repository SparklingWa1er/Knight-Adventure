from config import *
import pygame
from pygame import Vector2 as vector
class Weapon(pygame.sprite.Sprite):
    def __init__(self,player,groups):
        super().__init__(groups)
        direction=player.status.split("_")[0]
        self.image=pygame.transform.scale(pygame.image.load("image/weapon/{}.png".format(direction)), (40,40)).convert_alpha()
        if(direction=="right"):
            self.rect=self.image.get_rect(midleft=(player.rect.midright+vector(0,16)))
        elif (direction == "left"):
            self.rect = self.image.get_rect(midright=(player.rect.midleft+vector(0,16)))
        elif (direction == "up"):
            self.rect = self.image.get_rect(midbottom=(player.rect.midtop-vector(16,0)))
        elif(direction == "down"):
            self.rect = self.image.get_rect(midtop=(player.rect.midbottom-vector(16,0)))