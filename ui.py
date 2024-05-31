import pygame
from pygame import Vector2 as vector
from config import *
class UI:
    def __init__(self):
        self.display_surface=pygame.display.get_surface()
        self.font=pygame.font.Font(ui_font,ui_font_size)
        self.health_bar_rect=pygame.Rect(10,10,health_bar_width,bar_height)
        self.energy_bar_rect=pygame.Rect(10,16+bar_height,energy_bar_width,bar_height)
        self.magic_graphics={i:pygame.image.load(magic_data[i]["image_path"]).convert_alpha()for i in magic_data}
    def show_bar(self,current_stat,max_stat,bg_rect,color):
        pygame.draw.rect(self.display_surface,ui_bg_color,bg_rect)
        ratio=current_stat/max_stat
        pygame.draw.rect(self.display_surface,color,pygame.Rect(bg_rect.x,bg_rect.y,bg_rect.width*ratio,bg_rect.height))
        pygame.draw.rect(self.display_surface,ui_border_color,bg_rect,3)
    def show_exp(self,exp):
        text_surface=self.font.render(str(int(exp)),False,text_color)
        surface_size=self.display_surface.get_size()
        text_rect=text_surface.get_rect(bottomright=(surface_size[0]-20,surface_size[1]-20))
        pygame.draw.rect(self.display_surface,ui_bg_color,text_rect.inflate(20,20))
        self.display_surface.blit(text_surface,text_rect)
        pygame.draw.rect(self.display_surface,ui_bg_color,text_rect.inflate(20,20),3)
    def display(self,player):
        try:
            if(player.can_switch_magic):pass
        except:
            player.can_switch_magic=True
        self.show_bar(player.health,player.stats["health"],self.health_bar_rect,health_color)
        self.show_bar(player.energy,player.stats["energy"],self.energy_bar_rect,energy_color)
        self.show_exp(player.exp)
        self.magic_overlay(player.magic,not player.can_switch_magic)
    def selection_box(self,left,top,has_switched):
        bg_rect = pygame.Rect(left,top,item_box_size,item_box_size)
        pygame.draw.rect(self.display_surface,ui_bg_color,bg_rect)
        if has_switched:
            pygame.draw.rect(self.display_surface,ui_border_color_active,bg_rect,3)
        else:
            pygame.draw.rect(self.display_surface,ui_border_color,bg_rect,3)
        return bg_rect
    def magic_overlay(self,player_magic,has_switched):
        bg_rect=self.selection_box(10,630,has_switched)
        magic_surface=self.magic_graphics[player_magic]
        magic_rect=magic_surface.get_rect(center=bg_rect.center)
        self.display_surface.blit(magic_surface,magic_rect)
