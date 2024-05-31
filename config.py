import random
import pygame
from math import sin
from pygame import Vector2 as vector
screen_width=1280
screen_height=720
FPS=60
tile_size=64
animation_speed=0.15
#ui
bar_height=20
health_bar_width=200
energy_bar_width=140
item_box_size=80
map_path="image/pic.png"
ui_font="font/Silver.ttf"
ui_font_size=36
hitbox_offset_y={"invisible":0,"object":40,"player":-26,"enemy":-26}
#color
water_color="71ddee"
ui_bg_color="#222222"
ui_border_color="#111111"
text_color="#EEEEEE"
health_color="red"
energy_color="blue"
ui_border_color_active="gold"
text_color_selected="#111111"
bar_color="#EEEEEE"
bar_color_selected="#111111"
upgrade_color_selected="#EEEEEE"
magic_data={
    "flame":{"strengh":5, "cost":20, "image_path":"image/magic/flame.png"},
    "heal":{"strengh":20, "cost":10, "image_path":"image/magic/heal.png"}
}
map_pic=pygame.image.load(map_path)
initial_monster_pos=[[random.randint(1,map_pic.get_width()),random.randint(1,map_pic.get_height())]for _ in range(1,36)]
entity_data={"player":{"health":100, "energy":60, "attack":25, "magic":3, "speed":5, "attack_cooldown":400,"switch_magic_cooldown":250,"invulnerable_duration":666},
        "enemy/red_goblin":{'health': 100,'exp':100,'damage':20,'attack_type': 'claw', 'attack_sound':'', 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360, "attack_cooldown":1000},
        "enemy/black_goblin":{'health': 100,'exp':100,'damage':20,'attack_type': 'x_slash', 'attack_sound':'', 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360,"attack_cooldown":1000}}
animation_frames=({i:[pygame.transform.scale(pygame.image.load("image/animation_frames/{}/row-1-column-{}.png".format(i,j)), (tile_size,tile_size))for j in range(1,5)] for i in ["claw","x_slash"]} |
                {i:[pygame.transform.scale(pygame.image.load("image/animation_frames/{}/row-1-column-{}.png".format(i,j)), (tile_size+36,tile_size+36))for j in range(1,6)] for i in ["heal"]} |
                {i:[pygame.transform.scale(pygame.image.load("image/animation_frames/{}/row-1-column-{}.png".format(i,j)), (tile_size,tile_size))for j in range(1,13)] for i in ["flame"]} |
                  {"enemy_get_hit":[]})
for i in range(2,6):
    for j in range(1,7):
        animation_frames["enemy_get_hit"].append(pygame.transform.scale(pygame.image.load("image/animation_frames/enemy_get_hit/row-{}-column-{}.png".format(i,j)), (tile_size,tile_size)))
