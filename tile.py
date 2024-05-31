import pygame
from config import *
class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,groups,sprite_type,surface=pygame.Surface((tile_size,tile_size))):
        super().__init__(groups)
        self.image=surface
        self.rect=self.image.get_rect(topleft=pos)
        self.hitbox=self.rect.inflate(0,-hitbox_offset_y[sprite_type])
        self.type=sprite_type
