from config import *
import pygame
from pygame import Vector2 as vector
class Entity(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        self.direction=vector()
        self.frame_index=0
        self.animation_speed=0.15
        self.speed=5
    def move(self,speed):
        if self.direction.magnitude()!=0:
            self.direction=self.direction.normalize()
        self.hitbox.x+=self.direction.x*speed
        self.collision("horizontal")
        self.hitbox.y+=self.direction.y*speed
        self.collision("vertical")
        self.rect.center=self.hitbox.center
    def collision(self,direction):
        if direction=="horizontal":
            for obstacle in self.obstacles:
                if obstacle.hitbox.colliderect(self.hitbox):
                    if(self.direction.x>0):
                        self.hitbox.right=obstacle.hitbox.left
                    if(self.direction.x<0):
                        self.hitbox.left=obstacle.hitbox.right
        if direction=="vertical":
            for obstacle in self.obstacles:
                if obstacle.hitbox.colliderect(self.hitbox):
                    if (self.direction.y > 0):
                        self.hitbox.bottom = obstacle.hitbox.top
                    if (self.direction.y < 0):
                        self.hitbox.top = obstacle.hitbox.bottom