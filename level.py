import pygame
from config import *
from tile import *
from player import *
from doccsv import *
from weapon import *
from ui import *
from entity import Entity
from enemy import Enemy
from particles import *
from upgrade import *
class Level:
    def __init__(self):
        self.visible_instances=YSortCameraGroup()
        self.obstacle_instances=pygame.sprite.Group()
        self.display_surface=pygame.display.get_surface()
        self.attack_instances=pygame.sprite.Group()
        self.attackable_instances=pygame.sprite.Group()
        self.player=None
        self.current_attack=None
        self.font=pygame.font.Font(ui_font,ui_font_size*10)
        self.monster_pos=initial_monster_pos
        self.create()
        self.ui=UI()
        self.upgrade=Upgrade(self.player)
    def create(self):
        self.player = Player([1600, 1000], [self.visible_instances,self.obstacle_instances], self.obstacle_instances,self.create_attack,self.delete_weapon,self.create_magic)
        for i in self.monster_pos:
            Enemy(i,[self.visible_instances,self.attackable_instances,self.obstacle_instances],self.obstacle_instances,self.damage_player)
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
        try:
            if(self.game_paused):pass
        except:
            self.game_paused=False
        self.visible_instances.draw(self.player)
        if self.game_paused:
            self.upgrade.display()
        else:
            self.ui.display(self.player)
            self.visible_instances.update(self.player)
            self.player_attack()
            self.check_end()
    def create_attack(self):
        self.current_attack=Weapon(self.player,[self.visible_instances,self.attack_instances])
    def create_magic(self,style,strength,cost):
        if self.player.energy>=cost:
            if style=="heal":
                self.player.health=min(self.player.stats["health"],self.player.health+strength)
                Particle_effect(self.player.rect.center,"heal",[self.visible_instances])
            elif style=="flame":
                direction_dict={"up":vector(0,-1),"down":vector(0,1),"left":vector(-1,0),"right":vector(1,0)}
                direction=direction_dict[self.player.status.split("_")[0]]
                for i in range(1,6):
                    Particle_effect((self.player.rect.centerx+direction.x*i*tile_size,self.player.rect.centery+direction.y*i*tile_size),"flame",[self.visible_instances,self.attack_instances])
            self.player.energy-=cost
    def delete_weapon(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack=None
    def player_attack(self):
        if self.attack_instances:
            for attack_instance in self.attack_instances:
                collision_instances=pygame.sprite.spritecollide(attack_instance,self.attackable_instances,False)
                if collision_instances:
                    for collision_instance in collision_instances:
                        if(collision_instance.get_damage(self.player,attack_instance.type)):
                            Particle_effect(collision_instance.rect.center,"x_slash",[self.visible_instances])
    def toggle_menu(self):
        try:
            if(self.game_paused):pass
        except:
            self.game_paused=False
        self.game_paused=not self.game_paused
    def damage_player(self,damage,attack_type):
        if self.player.vulnerable:
            self.player.health-=damage
            self.player.vulnerable=False
            self.player.hurt_time=pygame.time.get_ticks()
            Particle_effect(self.player.rect.center,attack_type,[self.visible_instances])
    def check_end(self):
        if(self.player.check_kill()):
            try:
                if (-self.dead_time+pygame.time.get_ticks()>=2000):
                    text_surface = self.font.render("Game over", False, text_color)
                    surface_size = self.display_surface.get_size()
                    text_rect = text_surface.get_rect(center=(surface_size[0]//2,surface_size[1]//2))
                    self.display_surface.fill(ui_bg_color)
                    self.display_surface.blit(text_surface, text_rect)
            except:
                self.dead_time=pygame.time.get_ticks()

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
            if(sprite.type[:5:]=="enemy"):
                bg_rect = pygame.Rect(sprite.rect.x-self.offset.x,sprite.rect.y-20-self.offset.y, 64, 15)
                pygame.draw.rect(self.display_surface, ui_bg_color, bg_rect)
                ratio = sprite.health / sprite.stats["health"]
                pygame.draw.rect(self.display_surface, health_color,pygame.Rect(bg_rect.x, bg_rect.y, bg_rect.width * ratio, bg_rect.height))
                pygame.draw.rect(self.display_surface, ui_border_color, bg_rect, 3)
            self.display_surface.blit(sprite.image,vector(sprite.rect.topleft)-self.offset)
