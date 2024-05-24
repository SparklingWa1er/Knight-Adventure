from config import *
import pygame
from entity import *
class Enemy(Entity):
    def __init__(self,pos,groups,obstacles):
        super().__init__(groups)
        self.type=random.choice(list(monster_data))
        self.import_monster_images()
        self.status="idle"
        self.image=self.animations[self.status][self.frame_index]
        self.rect=self.image.get_rect(topleft=pos)
        self.hitbox=self.rect.inflate(0,-26)
        self.obstacles=obstacles
        self.stats=monster_data[self.type]
        self.health=self.stats["health"]
        self.can_attack=True
        self.attack_time=None
        self.attack_cooldown=1000
    def import_monster_images(self):
        self.animations={i:[] for i in ["move","idle","attack"]}
        self.animations["move"]=[pygame.transform.scale(pygame.image.load("image/monster/{}/row-{}-column-1.png".format(self.type,i)), (tile_size,tile_size)) for i in range(1,5)]
        self.animations["idle"]=[pygame.transform.scale(pygame.image.load("image/monster/{}/row-{}-column-1.png".format(self.type,i)), (tile_size,tile_size)) for i in [1,2,4]]
        self.animations["attack"]=[pygame.transform.scale(pygame.image.load("image/monster/{}/row-{}-column-1.png".format(self.type,i)), (tile_size,tile_size)) for i in [1,2]]
    def get_status(self,player):
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
            print("attack")
            self.can_attack=False
        elif(self.status=="move"):
            self.direction=direction
        else:
            self.direction=vector(0,0)
    def cooldown(self):
        if not self.can_attack:
            current_time=pygame.time.get_ticks()
            if(current_time-self.attack_time>=self.attack_cooldown):
                self.can_attack=True
    def animate(self):
        animation=self.animations[self.status]
        self.frame_index+=self.animation_speed
        self.frame_index%=len(animation)
        self.image=animation[int(self.frame_index)]
        self.rect=self.image.get_rect(center=self.hitbox.center)
    def update(self,player):
        self.cooldown()
        self.get_status(player)
        self.animate()
        self.move(self.stats["speed"])