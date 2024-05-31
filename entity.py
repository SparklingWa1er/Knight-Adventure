from config import *
import pygame
from pygame import Vector2 as vector
class Entity(pygame.sprite.Sprite):
    def __init__(self,groups,type,pos,obstacles):
        super().__init__(groups)
        self.direction=vector()
        self.animation_speed=0.15
        self.type=type
        self.image=pygame.transform.scale(pygame.image.load("image/{}/base_image.png".format(self.type)), (tile_size,tile_size))
        self.rect=self.image.get_rect(topleft=pos)
        self.hitbox=(self.image.get_rect(topleft=pos)).inflate(0,-26)
        self.obstacles=obstacles
        self.stats=entity_data[self.type]
        self.health=self.stats["health"]
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
                if (obstacle !=self) and obstacle.hitbox.colliderect(self.hitbox):
                    if(self.direction.x>0):
                        self.hitbox.right=obstacle.hitbox.left
                    if(self.direction.x<0):
                        self.hitbox.left=obstacle.hitbox.right
        if direction=="vertical":
            for obstacle in self.obstacles:
                if (obstacle !=self) and obstacle.hitbox.colliderect(self.hitbox):
                    if (self.direction.y > 0):
                        self.hitbox.bottom = obstacle.hitbox.top
                    if (self.direction.y < 0):
                        self.hitbox.top = obstacle.hitbox.bottom
    def animate(self):
        try:
            if(self.frame_index):pass
        except:
            self.frame_index=0
        animation=self.animations[self.status]
        self.frame_index+=self.animation_speed
        self.frame_index%=len(animation)
        self.image=animation[int(self.frame_index)]
        self.rect=self.image.get_rect(center=self.hitbox.center)
        if not self.vulnerable:
            self.image.set_alpha(255 if (sin(pygame.time.get_ticks())>0)else 0)
        else:
            self.image.set_alpha(255)
