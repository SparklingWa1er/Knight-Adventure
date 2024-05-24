import pygame
from config import *
from tile import *
from player import *
from doccsv import *
from weapon import *
from ui import *
from entity import Entity
from enemy import Enemy
class Level:
    def __init__(self):
        self.visible_instances=YSortCameraGroup()
        self.obstacle_instances=pygame.sprite.Group()
        self.display_surface=pygame.display.get_surface()
        self.player=None
        self.current_attack=None
        self.monster_pos=initial_monster_pos
        self.create()
        self.ui=UI()
    def create(self):
        self.player = Player([1600, 1000], [self.visible_instances], self.obstacle_instances,self.create_attack,self.delete_weapon,self.create_magic)
        for i in self.monster_pos:
            Enemy(i,[self.visible_instances],self.obstacle_instances)
        layouts={"border":doccsv("layouts/pic_border.csv"), "object":doccsv("layouts/pic_object.csv")}
        object_pic={i:pygame.image.load("image/object_image/{}.png".format(i)).convert_alpha() for i in [0,2,48,49,72]}
        for type,layout in layouts.items():
            for line_index,line in enumerate(layout):
                for index,value in enumerate(line):
                    x=index*tile_size
                    y=line_index*tile_size
                    if (value != "-1"):
                        if(type=="border"):
                            Tile((x,y),[self.obstacle_instances],"invisible")
                        elif(type=="object"):
                            Tile((x,y-tile_size),[self.obstacle_instances,self.visible_instances],"object",object_pic[int(value)])
    def run(self):
        self.visible_instances.draw(self.player)
        self.visible_instances.update(self.player)
        self.ui.display(self.player)
    def create_attack(self):
        self.current_attack=Weapon(self.player,[self.visible_instances])
    def create_magic(self,style,strength,cost):
        print(style,strength,cost)
    def delete_weapon(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack=None
class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface=pygame.display.get_surface()
        self.offset=vector()
        self.ground_image=pygame.image.load(map_path).convert()
        self.ground_rect=self.ground_image.get_rect(topleft=(0,0))
    def draw(self,player):
        """giup nguoi choi luon o tam man hinh"""
        self.offset.x=player.rect.centerx-self.display_surface.get_size()[0]//2
        self.offset.y = player.rect.centery - self.display_surface.get_size()[1] // 2
        self.display_surface.blit(self.ground_image,vector(self.ground_rect.topleft)-self.offset)
        for sprite in sorted(self.sprites(),key=lambda x:x.rect.centery):
            self.display_surface.blit(sprite.image,vector(sprite.rect.topleft)-self.offset)