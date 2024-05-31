from config import *
import pygame
from entity import *
from math import sin
from particles import *
class Enemy(Entity):
    def __init__(self,pos,groups,obstacles,damage_player):### NHO BO SUNG TYPE
        super().__init__(groups,"enemy/red_goblin",pos,obstacles)
        self.import_enemy_images()
        self.status="idle"
        self.damage_player=damage_player
    def import_enemy_images(self):
        self.animations={i:[] for i in ["move","idle","attack"]}
        self.animations["move"]=[pygame.transform.scale(pygame.image.load("image/{}/row-{}-column-1.png".format(self.type,i)), (tile_size,tile_size)) for i in range(1,5)]
        self.animations["idle"]=[pygame.transform.scale(pygame.image.load("image/{}/row-{}-column-1.png".format(self.type,i)), (tile_size,tile_size)) for i in [1,2,4]]
        self.animations["attack"]=[pygame.transform.scale(pygame.image.load("image/{}/row-{}-column-1.png".format(self.type,i)), (tile_size,tile_size)) for i in [1,2]]
    def get_status(self,player):
        try:
            if(self.can_attack):pass
        except:
            self.can_attack=True
        direction=vector(player.hitbox.center)-vector(self.hitbox.center)
        distance=direction.magnitude()
        if(distance>0):
            direction=direction.normalize()
        else:
            direction=vector(0,0)
        if(distance<=self.stats["attack_radius"])and(self.can_attack):
            if self.status!="attack":
                self.frame_index=0
            self.status="attack"
        elif(distance<=self.stats["notice_radius"]):
            self.status="move"
        else:
            self.status="idle"
        if(self.status=="attack")and(self.can_attack):
            self.attack_time=pygame.time.get_ticks()
            self.damage_player(self.stats["damage"],self.stats["attack_type"])
            self.can_attack=False
        elif(self.status=="move"):
            self.direction=direction
        else:
            self.direction=vector(0,0)
    def cooldown(self,player):
        try:
            if(self.can_attack):pass
        except:
            self.can_attack=True
        try:
            if(self.vulnerable):pass
        except:
            self.vulnerable=True
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if(current_time-self.attack_time>=self.stats["attack_cooldown"]):
                self.can_attack=True
        if(not self.vulnerable):
            if(pygame.time.get_ticks()-self.hit_time>=player.stats["attack_cooldown"]):
                self.vulnerable=True
    def get_damage(self,player,attack_type):
        try:
            if(self.vulnerable):pass
        except:
            self.vulnerable=True
        if(self.vulnerable):
            new_direction=vector(player.hitbox.center)-vector(self.hitbox.center)
            if new_direction.magnitude()>0:
                self.direction=new_direction.normalize()
            else:
                self.direction=vector(0,0)
            if(attack_type=="weapon"):
                self.health-=player.stats["attack"]
            if(attack_type=="flame"):
                self.health-=player.stats["magic"]*magic_data["flame"]["strengh"]
            self.hit_time=pygame.time.get_ticks()
            self.vulnerable=False
            return True
        return False

    def check_dead(self,player):
        if(self.health<=0):
            player.exp+=self.stats["exp"]
            self.kill()
    def hit_reaction(self):
        try:
            if(self.vulnerable):pass
        except:
            self.vulnerable=True
        if not self.vulnerable:
            self.direction*=(-self.stats["resistance"])
    def update(self,player):
        self.hit_reaction()
        self.move(self.stats["speed"])
        self.animate()
        self.cooldown(player)
        self.check_dead(player)
        self.get_status(player)
