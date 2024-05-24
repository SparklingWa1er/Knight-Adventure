import random
import pygame
screen_width=1280
screen_height=720
FPS=60
tile_size=64
#ui
bar_height=20
health_bar_width=200
energy_bar_width=140
item_box_size=80
map_path="image/pic.png"
ui_font="font/Silver.ttf"
ui_font_size=36
#color
water_color="71ddee"
ui_bg_color="#222222"
ui_border_color="#111111"
text_color="#EEEEEE"
health_color="red"
energy_color="blue"
ui_border_color_active="gold"
magic_data={
    "flame":{"strengh":5, "cost":20, "image_path":"image/magic/flame.png"},
    "heal":{"strengh":20, "cost":10, "image_path":"image/magic/heal.png"}
}
map_pic=pygame.image.load(map_path)
initial_monster_pos=[[random.randint(1,map_pic.get_width()),random.randint(1,map_pic.get_height())]for _ in range(1,36)]
monster_data={"red_goblin":{'health': 100,'exp':100,'damage':20,'attack_type': 'slash', 'attack_sound':'', 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360},
              "black_goblin":{'health': 100,'exp':100,'damage':20,'attack_type': 'slash', 'attack_sound':'', 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360}}