import pygame
from config import *
from pygame import Vector2 as vector
from entity import *
from math import sin
class Player(Entity):
    def __init__(self,pos,groups,obstacles,create_attack,delete_weapon,create_magic):
        super().__init__(groups,"player",pos,obstacles)
        self.import_player_images()
        self.status="down"
        self.create_attack=create_attack
        self.delete_weapon=delete_weapon
        self.create_magic=create_magic
        self.upgrade_cost={i:100 for i in list(self.stats)}
        self.energy=self.stats["energy"]
        self.exp=10000
        self.magic= list(magic_data.keys())[0]
    def import_player_images(self):
        self.animations={i:[] for i in ["up","down","left","right",
                                        "up_idle","down_idle","left_idle","right_idle",
                                        "up_attack","down_attack","left_attack","right_attack"]}
        for i in  ["down","left","right","up"]:
            self.animations[i]=[pygame.transform.scale(pygame.image.load("image/player/walk/{}/{}.png".format(i,j)), (tile_size,tile_size)) for j in range(1,5)]
            self.animations[i+"_idle"]=[pygame.transform.scale(pygame.image.load("image/player/idle/{}.png".format(i)), (tile_size,tile_size))]
            self.animations[i+"_attack"]=[pygame.transform.scale(pygame.image.load("image/player/attack/{}.png".format(i)), (tile_size,tile_size))]
        self.animations["dead"]=[pygame.transform.scale(pygame.image.load("image/player/dead/dead.png"), (tile_size,tile_size))]
    def get_status(self):
        if self.direction==vector(0,0):
            if("_idle" not in self.status)and("_attack" not in self.status):
                self.status=self.status+"_idle"
        try:
            if self.attacking:
                self.direction=vector(0,0)
                if "_attack" not in self.status:
                    if("_idle" in self.status):
                        self.status=self.status[:-5:]
                    self.status+="_attack"
            else:
                if "_attack" in self.status:
                    self.status=self.status[:-7:]
        except:
            self.attacking=False
    def input(self):
        try:
            if(self.can_switch_magic):pass
        except:
            self.can_switch_magic=True
        try:
            if(self.attacking):pass
        except:
            self.attacking=False
        try:
            if(self.magic_index):pass
        except:
            self.magic_index=0
        if(self.attacking):
            return
        keys=pygame.key.get_pressed()
        if(keys[pygame.K_UP]):
            self.status="up"
            self.direction.y=-1
        elif (keys[pygame.K_DOWN]):
            self.status="down"
            self.direction.y = 1
        else:
            self.direction.y=0
        if (keys[pygame.K_LEFT]):
            self.status="left"
            self.direction.x = -1
        elif (keys[pygame.K_RIGHT]):
            self.status="right"
            self.direction.x = 1
        else:
            self.direction.x=0
        #attack input
        if keys[pygame.K_a] and not self.attacking:
            self.attacking=True
            self.attack_time=pygame.time.get_ticks()
            self.create_attack()
        if keys[pygame.K_s] and not self.attacking:
            self.attack_time=pygame.time.get_ticks()
            self.attacking=True
            self.create_magic(self.magic,magic_data[self.magic]["strengh"]+self.stats["magic"],magic_data[self.magic]["cost"])
        if keys[pygame.K_q] and self.can_switch_magic:
            self.can_switch_magic=False
            self.magic_switch_time=pygame.time.get_ticks()
            self.magic_index=(self.magic_index+1)%len(list(magic_data.keys()))
            self.magic = list(magic_data.keys())[self.magic_index]
    def cooldown(self):
        current_time= pygame.time.get_ticks()
        try:
            if(self.vulnerable):pass
        except:
            self.vulnerable=True
        try:
            if(self.hurt_time):pass
        except:
            self.hurt_time=None
        try:
            if self.attacking:
                try:
                    if(current_time-self.attack_time>=self.stats["attack_cooldown"]):
                        self.attacking=False
                        self.delete_weapon()
                except:
                    self.attack_time=None
            if not self.can_switch_magic:
                if(pygame.time.get_ticks()-self.magic_switch_time>=self.stats["switch_magic_cooldown"]):
                    self.can_switch_magic=True
            if not self.vulnerable:
                if current_time - self.hurt_time >=self.stats["invulnerable_duration"]:
                    self.vulnerable=True
        except:
            self.attacking=False
    def energy_recover(self):
        self.energy=min(self.energy+self.stats["magic"]/FPS,self.stats["energy"])
    def check_kill(self):
        if self.health<=0:
            self.stats["attack_cooldown"]=20000
            self.stats["speed"]=0
            self.image=self.animations["dead"][0]
            self.energy=0
            return True
        else:
            return False
    def update(self,_):
        self.input()
        self.cooldown()
        self.get_status()
        self.animate()
        self.move(self.stats["speed"])
        self.energy_recover()
