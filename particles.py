from config import *
import pygame
class Particle_effect(pygame.sprite.Sprite):
    def __init__(self,pos,frames_name,groups):
        super().__init__(groups)
        self.animation_speed = 0.15
        self.animations = animation_frames[frames_name]
        self.image = self.animations[0]
        self.rect = self.image.get_rect(center=pos)
        self.type=frames_name
    def update(self,_):
        try:
            if(self.frame_index):pass
        except:
            self.frame_index=0
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animations):
            self.kill()
        else:
            self.image = self.animations[int(self.frame_index)]
