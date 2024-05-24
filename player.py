import pygame
from config import *
from pygame import Vector2 as vector
from entity import *
class Player(Entity):
    def __init__(self,pos,groups,obstacles,create_attack,delete_weapon,create_magic):
        super().__init__(groups)
        self.image=pygame.transform.scale(pygame.image.load("image/player/walk/down/1.png"), (tile_size,tile_size))
        self.rect=self.image.get_rect(topleft=pos)
        self.obstacles=obstacles
        self.hitbox=self.rect.inflate(0,-26)
        self.attacking=False
        self.attack_time=None
        self.attack_cooldown=300
        self.import_player_images()
        self.status="down"
        self.create_attack=create_attack
        self.delete_weapon=delete_weapon
        self.stats={"health":100, "energy":60, "attack":10, "magic":4, "speed":5}
        self.health=self.stats["health"]
        self.energy=self.stats["energy"]
        self.exp=100
        self.speed=self.stats["speed"]
        self.magic_index=0
        self.magic= list(magic_data.keys())[self.magic_index]
        self.can_switch_magic=True
        self.magic_switch_time=None
        self.create_magic=create_magic
        self.switch_magic_cooldown=250
    def import_player_images(self):
        self.animations={i:[] for i in ["up","down","left","right",
                                        "up_idle","down_idle","left_idle","right_idle",
                                        "up_attack","down_attack","left_attack","right_attack"]}
        for i in  ["down","left","right","up"]:
            self.animations[i]=[pygame.transform.scale(pygame.image.load("image/player/walk/{}/{}.png".format(i,j)), (tile_size,tile_size)) for j in range(1,5)]
            self.animations[i+"_idle"]=[pygame.transform.scale(pygame.image.load("image/player/idle/{}.png".format(i)), (tile_size,tile_size))]
            self.animations[i+"_attack"]=[pygame.transform.scale(pygame.image.load("image/player/attack/{}.png".format(i)), (tile_size,tile_size))]
    def get_status(self):
        if self.direction==vector(0,0):
            if("_idle" not in self.status)and("_attack" not in self.status):
                self.status=self.status+"_idle"
        if self.attacking:
            self.direction=vector(0,0)
            if "_attack" not in self.status:
                if("_idle" in self.status):
                    self.status=self.status[:-5:]
                self.status+="_attack"
        else:
            if "_attack" in self.status:
                self.status=self.status[:-7:]
    def input(self):
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
        if self.attacking:
            if(current_time-self.attack_time>=self.attack_cooldown):
                self.attacking=False
                self.delete_weapon()
        if not self.can_switch_magic:
            if(pygame.time.get_ticks()-self.magic_switch_time>=self.switch_magic_cooldown):
                self.can_switch_magic=True
    def animate(self):
        animation=self.animations[self.status]
        self.frame_index+=self.animation_speed
        self.frame_index%=len(animation)
        self.image=animation[int(self.frame_index)]
        self.rect=self.image.get_rect(center=self.hitbox.center)
    def update(self,_):
        self.input()
        self.cooldown()
        self.get_status()
        self.animate()
        self.move(self.speed)