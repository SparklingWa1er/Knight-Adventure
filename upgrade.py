import pygame
from config import *
class Upgrade:
    def __init__(self,player):
        self.display_surface=pygame.display.get_surface()
        self.player=player
        self.number_of_stats=5
        self.stats_name=[i for i in list(self.player.stats.keys())[:5:]]
        self.max_stats={i:self.player.stats[i]*3 for i in self.stats_name}
        self.font=pygame.font.Font(ui_font,ui_font_size)
        self.selection_index = 1
        self.selection_time=None
        self.can_move=True
        self.height=self.display_surface.get_height()*0.8
        self.width=self.display_surface.get_width()//(self.number_of_stats+1)
        self.create_items()
    def display(self):
        self.input()
        self.cooldown()
        for i,value in enumerate(self.item_list,0):
            stat_name=self.stats_name[i]
            value.display(self.display_surface,self.selection_index,stat_name,self.player.stats[stat_name],self.max_stats[stat_name],self.player.upgrade_cost[stat_name])
    def input(self):
        if self.can_move:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                self.selection_index+=1
                self.selection_time = pygame.time.get_ticks()
                self.can_move = False
            elif keys[pygame.K_LEFT]:
                self.selection_index-=1
                self.selection_time = pygame.time.get_ticks()
                self.can_move = False
            self.selection_index%=(self.number_of_stats+1)
            self.selection_index=max(1,self.selection_index)
            if keys[pygame.K_SPACE]:
                stat_name=self.stats_name[self.selection_index-1]
                if(self.player.exp>=self.player.upgrade_cost[stat_name])and(self.player.stats[stat_name]<self.max_stats[stat_name]):
                    self.player.exp-=self.player.upgrade_cost[stat_name]
                    self.player.stats[stat_name]*=1.2
                    self.player.upgrade_cost[stat_name]*=1.2
                if(self.player.stats[stat_name]>=self.max_stats[stat_name]):
                    self.player.stats[stat_name] = self.max_stats[stat_name]
                self.selection_time = pygame.time.get_ticks()
                self.can_move = False
    def create_items(self):
        self.item_list=[]
        top=self.height//8
        left=(self.display_surface.get_width()//self.number_of_stats-self.width)//2
        for i in range(0,self.number_of_stats):
            item=Item(left,top,self.width,self.height,self.font,i+1)
            left+=self.display_surface.get_width()//self.number_of_stats
            self.item_list.append(item)
    def cooldown(self):
        if not self.can_move:
            current_time=pygame.time.get_ticks()
            self.can_move=((current_time-self.selection_time)>=300)
class Item:
    def __init__(self,left,top,width,height,font,index):
        self.rect=pygame.Rect(left,top,width,height)
        self.index=index
        self.font=font
    def display_names(self,surface,name,cost,selected):
        cost=str(cost)
        color=text_color if not selected else text_color_selected
        title_surf=self.font.render(name,False,color)
        title_rect=title_surf.get_rect(midtop=self.rect.midtop +vector(0,20))
        surface.blit(title_surf,title_rect)
        cost_surf=self.font.render(cost,False,color)
        cost_rect=cost_surf.get_rect(midbottom=self.rect.midbottom +vector(0,-20))
        surface.blit(cost_surf,cost_rect)
    def display_bar(self,surface,value,max_value,selected):
        top=self.rect.midtop+vector(0,60)
        bottom=self.rect.midbottom+vector(0,-60)
        color=bar_color if not selected else bar_color_selected
        full_height=bottom[1]-top[1]
        relative_number=value/max_value*full_height
        value_rect=pygame.Rect(top[0]-15,bottom[1]-relative_number,30,10)
        pygame.draw.line(surface,color,top,bottom,6)
        pygame.draw.rect(surface,color,value_rect)
    def display(self,surface,selection_index,name,value,max_value,cost):
        cost=int(cost)
        name=name[0].upper()+name[1::]
        selected=self.index==selection_index
        pygame.draw.rect(surface,ui_bg_color if not selected else upgrade_color_selected,self.rect)
        pygame.draw.rect(surface,ui_border_color,self.rect,4)
        self.display_names(surface,name,cost,selected)
        self.display_bar(surface,value,max_value,selected)
