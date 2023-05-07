
import pygame
from _thread import *
from random import randint
import random
import math
import os

# hello :D

os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.font.init()

width = 1920
height = 1080

pygame.display.set_caption("Sentry Domination Prototype")
win = pygame.display.set_mode((width, height))

clock = pygame.time.Clock()


class Player():
    def __init__(self, x, y, width, height, img):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.img = img
        self.rect = (x, y, width, height)
        self.vel = 5
        self.particle_list = []
        self.real_rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, win):
        self.real_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        win.blit(self.img, camera.add_offset(player.real_rect))
    
    def move(self):
        self.real_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            if self.check_collisions(self.real_rect, -self.vel, 0) == False:
                self.x -= self.vel
        if keys[pygame.K_d]:
            if self.check_collisions(self.real_rect, self.vel, 0) == False:
                self.x += self.vel
        if keys[pygame.K_w]:
            if self.check_collisions(self.real_rect, 0, -self.vel) == False:
                self.y -= self.vel
        if keys[pygame.K_s]:
            if self.check_collisions(self.real_rect, 0, self.vel) == False:
                self.y += self.vel  

        self.update()
    
    def check_collisions(self, player_rect, vel_x, vel_y):
        collision = False
        rect = pygame.rect.Rect(player_rect[0]+vel_x, player_rect[1]+vel_y, 50, 50)
        for i in wall.wall_list:
            if pygame.Rect.colliderect(rect, i[0]) == True:
                collision = True
        for i in walltop.wall_list:
            if pygame.Rect.colliderect(rect, i[0]) == True:
                collision = True    
        for i in cabinet.cabinet_list:
            if pygame.Rect.colliderect(rect, i[0]) == True:
                collision = True
        for i in desk.desk_list:
            if pygame.Rect.colliderect(rect, i[0]) == True:
                collision = True
        return collision
        

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)

    def display_coords(self, win):
        pos = (self.x, self.y)
        font = pygame.font.SysFont("comicsans", 30)
        text = font.render(str(pos[0]) + ", " + str(pos[1]), 1, (0,0,0))
        win.blit(text, (int(pos[0]-50), int(pos[1])-50))
    
    def check_collision_zombie(self, zombie):
        yes = False
        if self.vel == 5:
            if pygame.Rect.collidelist(self.real_rect, zombie.zombie_rect_list) == True:
                yes = True
                return True
        if yes == False:
            return False


class Sentry():
    def __init__(self, assault_sentry_base_img, assault_sentry_top_img, assault_shotgun_top_img, assault_burst_top_img, bomber_sentry_base_img, bomber_bomb_sentry_top_img, bomber_mine_sentry_top_img, bomber_molotov_sentry_top_img):
        self.assault_sentry_base_img = assault_sentry_base_img
        self.assault_sentry_top_img = assault_sentry_top_img
        self.assault_shotgun_top_img = assault_shotgun_top_img
        self.assault_burst_top_img = assault_burst_top_img

        self.bomber_sentry_base_img = bomber_sentry_base_img
        self.bomber_bomb_sentry_top_img = bomber_bomb_sentry_top_img
        self.bomber_mine_sentry_top_img = bomber_mine_sentry_top_img
        self.bomber_molotov_sentry_top_img = bomber_molotov_sentry_top_img

        self.sentry_list = []
    
    def add_sentry(self, x, y, img):
        real_rect = pygame.Rect(x, y, 100, 100)
        self.sentry_list.append([img, real_rect, 0])
    
    def draw_sentry(self, win):
        for i in self.sentry_list:
            if i[0] == self.assault_sentry_base_img:
                win.blit(self.assault_sentry_base_img, camera.add_offset(i[1]))
            else:
                pos = (i[1][0], i[1][1])
                
                rotated_image = pygame.transform.rotate(i[0], int(i[2])+180)
                new_rect = rotated_image.get_rect(center = i[0].get_rect(topleft = pos).center)

                win.blit(rotated_image, camera.add_offset(new_rect))

    
    def rotate_sentry(self, toggle_sentry_aim):
        for i in self.sentry_list:
            if toggle_sentry_aim == False:
                if i[0] != self.assault_sentry_base_img and i[0] != self.bomber_sentry_base_img:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    rel_x, rel_y = mouse_x - i[1][0]-50+camera.offset[0], mouse_y - i[1][1]-50+camera.offset[1]
                    angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
                    i[2] = int(angle)
            else:
                if len(zombie.zombie_list) > 0:
                    pos = pygame.math.Vector2(i[1][0], i[1][1])
                    enemy = min([e for e in zombie.zombie_list], key=lambda e: pos.distance_to(pygame.math.Vector2(int(e[0][0]+camera.offset[0]), int(e[0][1])+camera.offset[1])))
                    mouse_x, mouse_y = int(enemy[0][0]+25), int(enemy[0][1]+25)
                    rel_x, rel_y = mouse_x - i[1][0]-50, mouse_y - i[1][1]-50
                    angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
                    i[2] = int(angle)


class Tile():
    def __init__(self, tile_selected_img, tile_unselected_img, tile_confirmed_selected_img, tile_confirmed_img):
        self.tile_selected_img = tile_selected_img
        self.tile_unselected_img = tile_unselected_img
        self.tile_confirmed_img = tile_confirmed_img
        self.tile_confirmed_selected_img = tile_confirmed_selected_img
        self.tile_list = []
        self.old_tile_list = []
    
    def add_tile(self, x, y):
        rect = pygame.Rect(x, y, 100, 100)
        self.tile_list.append([1, rect, False])

    def update_tile(self):
        mouse = pygame.mouse.get_pos()
        for i in self.tile_list:
            if i[1][0]-camera.offset[0] <= mouse[0] < i[1][0]+100-camera.offset[0] and i[1][1]-camera.offset[1] <= mouse[1] < i[1][1]+100-camera.offset[1]:
                if i[2] == False:
                    i[0] = 2
                else:
                    i[0] = 4
            else:
                if i[2] == False:
                    i[0] = 1
                else:
                    i[0] = 3
                    
    
    def draw_tile(self, win):
        for i in self.tile_list:
            if i[0] == 1:
                win.blit(tile_unselected_img, camera.add_offset(i[1]))
            elif i[0] == 2:
                win.blit(tile_selected_img, camera.add_offset(i[1]))
            elif i[0] == 3:
                win.blit(tile_confirmed_img, camera.add_offset(i[1]))
            else:
                win.blit(tile_confirmed_selected_img, camera.add_offset(i[1]))

    def place_down_sentry(self,toggle_tile):
        mouse_buttons = pygame.mouse.get_pressed(num_buttons=3)   
        if mouse_buttons[0] == True:
            if toggle_tile == True:
                mouse = pygame.mouse.get_pos()
                for i in tile.tile_list:
                    cannot_place = False
                    if i[1][0]-camera.offset[0] <= mouse[0] < i[1][0]+i[1][2]-camera.offset[0] and i[1][1]-camera.offset[1] <= mouse[1] < i[1][1]+i[1][3]-camera.offset[1]:
                        for j in sentry.sentry_list:
                            if j[1][0]-camera.offset[0] <= mouse[0] < j[1][0]+j[1][2]-camera.offset[0] and j[1][1]-camera.offset[1] <= mouse[1] < j[1][1]+j[1][3]-camera.offset[1]:
                                cannot_place = True
                        if cannot_place == False:
                            try:
                                i[2] = True
                                if ui.sentry_selected == 1:
                                    sentry.add_sentry(i[1][0], i[1][1], sentry.assault_sentry_base_img)
                                    sentry.add_sentry(i[1][0], i[1][1], sentry.assault_sentry_top_img)
                                elif ui.sentry_selected == 2:
                                    sentry.add_sentry(i[1][0], i[1][1], sentry.assault_sentry_base_img)
                                    sentry.add_sentry(i[1][0], i[1][1], sentry.assault_shotgun_top_img)
                                elif ui.sentry_selected == 3:
                                    sentry.add_sentry(i[1][0], i[1][1], sentry.assault_sentry_base_img)
                                    sentry.add_sentry(i[1][0], i[1][1], sentry.assault_burst_top_img)
                                elif ui.sentry_selected == 4:
                                    sentry.add_sentry(i[1][0], i[1][1], sentry.bomber_sentry_base_img)
                                    sentry.add_sentry(i[1][0], i[1][1], sentry.bomber_bomb_sentry_top_img)
                                elif ui.sentry_selected == 5:
                                    sentry.add_sentry(i[1][0], i[1][1], sentry.bomber_sentry_base_img)
                                    sentry.add_sentry(i[1][0], i[1][1], sentry.bomber_mine_sentry_top_img)
                                elif ui.sentry_selected == 6:
                                    sentry.add_sentry(i[1][0], i[1][1], sentry.bomber_sentry_base_img)
                                    sentry.add_sentry(i[1][0], i[1][1], sentry.bomber_molotov_sentry_top_img)
                            except:
                                pass
        elif mouse_buttons[2] == True:
            if toggle_tile == True:
                mouse = pygame.mouse.get_pos()
                for i in tile.tile_list:
                    if i[1][0]-camera.offset[0] <= mouse[0] < i[1][0]+i[1][2]-camera.offset[0] and i[1][1]-camera.offset[1] <= mouse[1] < i[1][1]+i[1][3]-camera.offset[1]:
                        try:
                            i[2] = False
                            num = 0
                            for j in sentry.sentry_list:
                                if j[1][0]-camera.offset[0] <= mouse[0] < j[1][0]+j[1][2]-camera.offset[0] and j[1][1]-camera.offset[1] <= mouse[1] < j[1][1]+j[1][3]-camera.offset[1]:
                                    sentry.sentry_list.pop(num)
                                    sentry.sentry_list.pop(num)
                                num += 1
                        except:
                            pass


class Zombie():     
    def __init__(self, img, img_flipped, enemy_burning_img, enemy_burning_flipped_img):
        self.zombie_list = []      # [rect, health, direction, hitbox, tick, (x,y), [burn, burn_tick, stop_burning_tick]]
        self.zombie_rect_list = []
        self.img = img
        self.img_flipped = img_flipped
        self.enemy_burning_img = enemy_burning_img
        self.enemy_burning_flipped_img = enemy_burning_flipped_img
        self.speed = 3
        self.starting_health = 10
    
    def summon_zombie(self, x, y, width, height):
        real_rect = pygame.Rect(x, y, 100,100)
        hitbox = pygame.Rect(x+25,y+10, 50,80)
        self.zombie_list.append([real_rect, self.starting_health, 1, hitbox, 0, [x,y], [0, 0, 0]])

    def draw_zombie(self, win):
        for i in self.zombie_list:
            if i[4] == 0:
                if i[2] == 1:
                    if i[6][0] == 0:
                        win.blit(self.img, camera.add_offset(i[0]))
                    else:
                        win.blit(self.enemy_burning_img, camera.add_offset(i[0]))
                else:
                    if i[6][0] == 0:
                        win.blit(self.img_flipped, camera.add_offset(i[0]))
                    else:
                        win.blit(self.enemy_burning_flipped_img, camera.add_offset(i[0]))

    
    def draw_health_bar(self, win):
        for i in self.zombie_list:
            centerx = i[0].centerx
            rect_black = pygame.Rect(centerx-55-camera.offset[0], i[0][1]-40-camera.offset[1], 110,20)
            rect_red = pygame.Rect(centerx-50-camera.offset[0], i[0][1]-35-camera.offset[1], 100, 10)
            dist = i[1] * (100/self.starting_health)
            rect_green = pygame.Rect(centerx-50-camera.offset[0], i[0][1]-35-camera.offset[1], dist, 10)
            pygame.draw.rect(win, (0,0,0), rect_black)
            pygame.draw.rect(win, (255,0,0), rect_red)
            pygame.draw.rect(win, (0,255,0), rect_green)

    def move(self, player):
        for i in self.zombie_list:
            try:
                if i[4] == 0:                    
                    y, x = i[0][1] - player.real_rect[1]+25,  i[0][0] - player.real_rect[0]+25
                    angle = math.atan2(y,x)
                    dx = math.cos(angle)
                    dy = math.sin(angle)
                    dist = math.hypot(x, y)
                    if dist <= 500:
                        if dx >= 0:
                            i[2] = 0
                        else:
                            i[2] = 1
                        i[5][0] += dx * -self.speed
                        i[5][1] += dy * -self.speed
                        i[0][0] = i[5][0]
                        i[0][1] = i[5][1]
                        i[3][0] = i[0][0]
                        i[3][1] = i[0][1]
            except:
                continue 
    
    def update_zombies(self):
        self.zombie_rect_list = []
        number_list = []
        number = 0
        for i in self.zombie_list:
            if i[1] <= 0:
                i[4] = i[4] + 1
                if i[4] >= 30:
                    number_list.append(number)
            else:
                self.zombie_rect_list.append(i[3])
            number += 1
        number_list.sort(reverse=True)
        for i in number_list:
            self.zombie_list.pop(i)

    def check_collision(self):
        num2 = 0
        for i in self.zombie_list:            
            if i[4] == 0:
                collide = pygame.Rect.collidelist(i[0], bullet.bullet_rect_list)
                if collide != -1:
                    try:
                        i[1] = int(i[1]) - int(bullet.bullet_list[collide][4])
                        if bullet.bullet_list[collide][7] > 0:
                            bullet.bullet_list[collide][7] = bullet.bullet_list[collide][7] - 1
                            bullet.bullet_list[collide][4] = bullet.bullet_list[collide][4] - 1
                            if bullet.bullet_list[collide][4] < 1:
                                bullet.bullet_list[collide][4] = 1
                        if bullet.bullet_list[collide][7] <= 0:
                            bullet.bullet_list.pop(num2)
                    except:
                        pass
                collide = pygame.Rect.collidelist(i[0], fire.ring_rect_list)
                if collide != -1:   
                    if i[6][0] != 2:
                        i[6][0] = 2
                    i[6][2] = 0
                    i[6][1] = i[6][1] + 1
                    if i[6][1] == 20:
                        i[6][1] = 0
                        i[1] = i[1] - 1
                else:
                    if i[6][0] == 2:
                        i[6][0] = 1
                        i[6][1] = 0
                    if i[6][0] == 1:
                        i[6][1] = i[6][1] + 1
                        i[6][2] = i[6][2] + 1
                        if i[6][1] == 60:
                            i[6][1] = 0
                            i[1] = i[1] - 1
                        if i[6][2] == 300:
                            i[6][0] = 0
        num2 += 1
     

class Bullet():
    def __init__(self, bullet, bomb, red_bomb, mine_img, molotov_img, molotov_flipped_img):
        self.bullet_list = [] 
        self.bullet_rect_list = []
        self.bomb_list = [] 
        self.mine_list = []
        self.molotov_list = []
        self.speed = 20
        self.bomb_speed = 10
        self.bullet_img = bullet
        self.bomb_img = bomb
        self.red_bomb_img = red_bomb
        self.mine_img = mine_img
        self.molotov_img = molotov_img
        self.molotov_flipped_img = molotov_flipped_img

    def update_shotgun_bullet(self):
        self.bullet_rect_list = []
        for i in bullet.bullet_list:
            self.bullet_rect_list.append(i[0])
            if i[6] == 2:
                updated_tick = i[5]
                updated_tick += 1
                i[5] = updated_tick
                if i[5] == 10:
                    i[5] = 0
                    updated_damage = i[4]
                    if updated_damage > 1:
                        updated_damage -= 1  
                    i[4] = updated_damage

    def update_bomb(self):
        number_list = []
        number = 0
        for i in self.bomb_list:
            if float(i[4]) > 1:
                speed = i[4]
                speed = speed-(0.1)
                i[4] = speed    
            else:
                i[4] = 0
            tick = i[5]
            tick += 1
            i[5] = tick
            if i[6] >= 0 and i[6] <= 1:
                if tick == 10:
                    i[5] = 0
                    if i[7] == "bomb":
                        i[7] = "red_bomb"
                    else:
                        i[7] = "bomb"
                    i[6] += 1
            if i[6] >= 2 and i[6] <= 3:
                if tick == 7:
                    i[5] = 0
                    if i[7] == "bomb":
                        i[7] = "red_bomb"
                    else:
                        i[7] = "bomb"
                    i[6] += 1
            elif i[6] >= 4 and i[6] <= 9:
                if tick == 5:
                    i[5] = 0
                    if i[7] == "bomb":
                        i[7] = "red_bomb"
                    else:
                        i[7] = "bomb"
                    i[6] += 1
            elif i[6] >= 10 and i[6] <= 15:
                if tick == 3:
                    i[5] = 0
                    if i[7] == "bomb":
                        i[7] = "red_bomb"
                    else:
                        i[7] = "bomb"
                    i[6] += 1
            elif i[6] > 15:
                explosion.add_explosion(i[0].centerx, i[0].centery, [10,5,3,1])
                number_list.append(number)


            collide = [pygame.Rect.collidelist(i[0], zombie.zombie_rect_list), pygame.Rect.collidelist(i[0], walltop.wall_rect_list), pygame.Rect.collidelist(i[0], wall.wall_rect_list), pygame.Rect.collidelist(i[0], desk.desk_rect_list), pygame.Rect.collidelist(i[0], cabinet.cabinet_rect_list)]
            if collide[0] != -1 or collide[1] != -1 or collide[2] != -1 or collide[3] != -1 or collide[4] != -1:
                if i[8] == False:
                    i[8] = True
                    if collide[0] != -1:
                        zx, zy = zombie.zombie_rect_list[collide[0]].centerx - i[0].centerx, zombie.zombie_rect_list[collide[0]].centery - i[0].centery
                    elif collide[1] != -1:
                        zx, zy = walltop.wall_rect_list[collide[1]].centerx - i[0].centerx, walltop.wall_rect_list[collide[1]].centery - i[0].centery
                    elif collide[2] != -1:
                        zx, zy = wall.wall_rect_list[collide[2]].centerx - i[0].centerx, wall.wall_rect_list[collide[2]].centery - i[0].centery
                    elif collide[3] != -1:
                        zx, zy = desk.desk_rect_list[collide[3]].centerx - i[0].centerx, desk.desk_rect_list[collide[3]].centery - i[0].centery
                    elif collide[4] != -1:
                        zx, zy = cabinet.cabinet_rect_list[collide[4]].centerx - i[0].centerx, cabinet.cabinet_rect_list[collide[4]].centery - i[0].centery
                    y, x = i[0][1] - player.real_rect[1]+25,  i[0][0] - player.real_rect[0]+25
                    angle = math.atan2(y,x)
                    dx = math.cos(angle)
                    dy = math.sin(angle)
                    dist = math.hypot(x, y)
                    if zx > 0 and dx > 0:
                        i[2][0] = i[2][0] * -1
                    if zx > 0 and dx < 0:
                        i[2][0] = i[2][0] * 0.75
                    if zx < 0 and dx < 0:
                        i[2][0] = i[2][0] * -1 
                    if zx < 0 and dx > 0:
                        i[2][0] = i[2][0] * 0.75

                    if zy > 0 and dy > 0:
                        i[2][1] = i[2][1] * -1
                    if zy > 0 and dy < 0:
                        i[2][1] = i[2][1] * 0.75
                    if zy < 0 and dy < 0:
                        i[2][1] = i[2][1] * -1
                    if zy < 0 and dy > 0:
                        i[2][1] = i[2][1] * 0.75

                    if i[4] > 5:
                        i[4] = i[4] *0.5
                    else:
                        i[4] = i[4] *0.75

                    if dist > 500:
                        i[4] = 2  
    
            number += 1
        number_list.sort(reverse=True)
        for i in number_list:
            self.bomb_list.pop(i)

    def update_mine(self):
            number_list = []
            number = 0
            for i in self.mine_list:
                if float(i[4]) > 1:
                    speed = i[4]
                    speed = speed-(0.1)
                    i[4] = speed    
                else:
                    i[4] = 0

                collide = [pygame.Rect.collidelist(i[0], zombie.zombie_rect_list), pygame.Rect.collidelist(i[0], walltop.wall_rect_list), pygame.Rect.collidelist(i[0], wall.wall_rect_list)]
                if collide[0] != -1 or collide[1] != -1 or collide[2] != -1:
                    if i[6] == False:
                        i[6] = True
                        if collide[0] != -1:
                            zx, zy = zombie.zombie_rect_list[collide[0]].centerx - i[0].centerx, zombie.zombie_rect_list[collide[0]].centery - i[0].centery
                        elif collide[1] != -1:
                            zx, zy = walltop.wall_rect_list[collide[1]].centerx - i[0].centerx, walltop.wall_rect_list[collide[1]].centery - i[0].centery
                        elif collide[2] != -1:
                            zx, zy = wall.wall_rect_list[collide[2]].centerx - i[0].centerx, wall.wall_rect_list[collide[2]].centery - i[0].centery
                        y, x = i[0][1] - player.real_rect[1]+25,  i[0][0] - player.real_rect[0]+25
                        angle = math.atan2(y,x)
                        dx = math.cos(angle)
                        dy = math.sin(angle)
                        dist = math.hypot(x, y)
                        if zx > 0 and dx > 0:
                            i[2][0] = i[2][0] * -1
                        if zx > 0 and dx < 0:
                            i[2][0] = i[2][0] * 0.75
                        if zx < 0 and dx < 0:
                            i[2][0] = i[2][0] * -1 
                        if zx < 0 and dx > 0:
                            i[2][0] = i[2][0] * 0.75

                        if zy > 0 and dy > 0:
                            i[2][1] = i[2][1] * -1
                        if zy > 0 and dy < 0:
                            i[2][1] = i[2][1] * 0.75
                        if zy < 0 and dy < 0:
                            i[2][1] = i[2][1] * -1
                        if zy < 0 and dy > 0:
                            i[2][1] = i[2][1] * 0.75

                        if i[4] > 5:
                            i[4] = i[4] *0.5
                        else:
                            i[4] = i[4] *0.75

                        if dist > 500:
                            i[4] = 2   
                        
                    elif i[4] == 0:                            
                        explosion.add_explosion(i[0].centerx, i[0].centery, [5,3,2,1])
                        number_list.append(number)
                tick = i[5]
                tick += 1
                i[5] = tick
                if i[5] >= 1200:
                    number_list.append(number)
                number += 1
            number_list.sort(reverse=True)
            for i in number_list:
                try:
                    self.mine_list.pop(i)
                except:
                    pass

    def update_molotov(self):
        pop_list = []
        num = 0
        for i in self.molotov_list:
            if float(i[4]) > 1:
                speed = i[4]
                speed = speed-(0.1)
                i[4] = speed    
            else:
                i[4] = 0
                speed = 0
                pop_list.append(num)
                explosion.add_mini_explosion(i[0][0], i[0][1])
                fire.create_ring(i[0][0]-camera.offset[0], i[0][1]-camera.offset[1])
            if i[5] == 1:
                i[1] = i[1] + speed*1.5
            else:
                i[1] = i[1] - speed*1.5
            num += 1
        pop_list.sort(reverse=True)
        for i in pop_list:
            self.molotov_list.pop(i)

                    



    def shoot_assault(self, toggle_sentry_aim):
        for i in sentry.sentry_list:
            if i[0] == sentry.assault_sentry_top_img:
                try:
                    if toggle_sentry_aim == False:
                        real_rect = pygame.Rect(i[1][0]+50-2, i[1][1]+50-2, 4, 4)
                        pos = pygame.mouse.get_pos()
                        pos = [pos[0]-2,pos[1]-2]
                        y, x = pos[1] - real_rect[1]+camera.offset[1],  pos[0] - real_rect[0]+camera.offset[0]
                        angle = math.atan2(y,x)
                        random_number = randint(-2,2)
                        angle += random_number/100
                        dx = math.cos(angle)
                        dy = math.sin(angle)
                        x,y = real_rect[0], real_rect[1]
                        self.bullet_list.append([real_rect, i[2], [dx,dy], [x,y], 1, 0, 1, 0, "bullet"])
                    else:
                        pos = pygame.math.Vector2(i[1][0], i[1][1])
                        real_rect = pygame.Rect(i[1][0]+50, i[1][1]+50, 4, 4)
                        pos = min([e for e in zombie.zombie_list], key=lambda e: pos.distance_to(pygame.math.Vector2(int(e[0][0]+camera.offset[0]), int(e[0][1]+camera.offset[1]))))
                        pos = [pos[0]-2,pos[1]-2]
                        y, x = pos[1] - real_rect[1]+camera.offset[1],  pos[0] - real_rect[0]+camera.offset[0]
                        angle = math.atan2(y,x)
                        random_number = randint(-2,2)
                        angle += random_number/100
                        dx = math.cos(angle)
                        dy = math.sin(angle)
                        x,y = real_rect[0], real_rect[1]
                        self.bullet_list.append([real_rect, i[2], [dx,dy], [x,y], 1, 0, 1, 0, "bullet"])
                except:
                    pass

    def shoot_shotgun(self, toggle_sentry_aim):
        for i in sentry.sentry_list:
            if i[0] == sentry.assault_shotgun_top_img:
                pellets = 0
                while pellets < 5:
                    try:
                        if toggle_sentry_aim == False:
                            real_rect = pygame.Rect(i[1][0]+50, i[1][1]+50, 4, 4)
                            pos = pygame.mouse.get_pos()
                            pos = [pos[0]-2,pos[1]-2]
                            y, x = pos[1] - real_rect[1]+camera.offset[1],  pos[0] - real_rect[0]+camera.offset[0]
                            angle = math.atan2(y,x)
                            if pellets == 0:
                                angle -= 0.4
                            if pellets == 1:
                                angle -= 0.2
                            if pellets == 2:
                                angle += 0
                            if pellets == 3:
                                angle += 0.2
                            if pellets == 4:
                                angle += 0.4
                            random_number = randint(-5,5)
                            angle += random_number/100
                            dx = math.cos(angle)
                            dy = math.sin(angle)
                            x,y = real_rect[0], real_rect[1]
                            self.bullet_list.append([real_rect, i[2], [dx,dy], [x,y], 3, 0, 2, 3, "bullet"])
                        else:
                            pos = pygame.math.Vector2(i[1][0], i[1][1])
                            real_rect = pygame.Rect(i[1][0]+50, i[1][1]+50, 4, 4)
                            pos = min([e for e in zombie.zombie_list], key=lambda e: pos.distance_to(pygame.math.Vector2(int(e[0][0]+camera.offset[0]), int(e[0][1]+camera.offset[1]))))
                            pos = [pos[0]-2,pos[1]-2]
                            y, x = pos[1] - real_rect[1]+camera.offset[1],  pos[0] - real_rect[0]+camera.offset[0]
                            angle = math.atan2(y,x)
                            if pellets == 0:
                                angle -= 0.4
                            if pellets == 1:
                                angle -= 0.2
                            if pellets == 2:
                                angle += 0
                            if pellets == 3:
                                angle += 0.2
                            if pellets == 4:
                                angle += 0.4
                            random_number = randint(-5,5)
                            angle += random_number/100
                            dx = math.cos(angle)
                            dy = math.sin(angle)
                            x,y = real_rect[0], real_rect[1]
                            self.bullet_list.append([real_rect, i[2], [dx,dy], [x,y], 3, 0, 2, 3, "bullet"])
                    except:
                        pass
                    pellets += 1

    def shoot_burst(self, toggle_sentry_aim):
        for i in sentry.sentry_list:
            if i[0] == sentry.assault_burst_top_img:
                try:
                    if toggle_sentry_aim == False:
                        real_rect = pygame.Rect(i[1][0]+50, i[1][1]+50, 4, 4)
                        pos = pygame.mouse.get_pos()
                        pos = [pos[0]-2,pos[1]-2]
                        y, x = pos[1] - real_rect[1]+camera.offset[1],  pos[0] - real_rect[0]+camera.offset[0]
                        angle = math.atan2(y,x)
                        random_number = randint(-10,10)
                        angle += random_number/100
                        dx = math.cos(angle)
                        dy = math.sin(angle)
                        x,y = real_rect[0], real_rect[1]
                        self.bullet_list.append([real_rect, i[2], [dx,dy], [x,y], 1, 0, 1, 0, "bullet"])
                    else:
                        pos = pygame.math.Vector2(i[1][0], i[1][1])
                        real_rect = pygame.Rect(i[1][0]+50, i[1][1]+50, 4, 4)
                        pos = min([e for e in zombie.zombie_list], key=lambda e: pos.distance_to(pygame.math.Vector2(int(e[0][0]+camera.offset[0]), int(e[0][1]+camera.offset[1]))))
                        pos = [pos[0]-2,pos[1]-2]
                        y, x = pos[1] - real_rect[1]+camera.offset[1],  pos[0] - real_rect[0]+camera.offset[0]
                        angle = math.atan2(y,x)
                        random_number = randint(-5,5)
                        angle += random_number/100
                        dx = math.cos(angle)
                        dy = math.sin(angle)
                        x,y = real_rect[0], real_rect[1]
                        self.bullet_list.append([real_rect, i[2], [dx,dy], [x,y], 1, 0, 1, 0, "bullet"])
                except:
                    pass
                
    def shoot_bomb(self, toggle_sentry_aim):
        for i in sentry.sentry_list:
            if i[0] == sentry.bomber_bomb_sentry_top_img:
                try:
                    if toggle_sentry_aim == False:
                        real_rect = pygame.Rect(i[1][0]+50-18, i[1][1]+50-18, 36, 36)
                        pos = pygame.mouse.get_pos()

                        pos = [pos[0]-18,pos[1]-18]
                        y, x = pos[1] - real_rect[1]+camera.offset[1],  pos[0] - real_rect[0]+camera.offset[0]
                        angle = math.atan2(y,x)
                        speed = 9
                        dx = math.cos(angle)
                        dy = math.sin(angle)

                        x,y = real_rect[0], real_rect[1]

                        self.bomb_list.append([real_rect, i[2], [dx,dy], [x,y], speed, 0, 0, "bomb", False])
                    else:
                        pos = pygame.math.Vector2(i[1][0], i[1][1])
                        real_rect = pygame.Rect(i[1][0]+50-18, i[1][1]+50-18, 36, 36)
                        pos = min([e for e in zombie.zombie_list], key=lambda e: pos.distance_to(pygame.math.Vector2(int(e[0][0]+camera.offset[0]), int(e[0][1]+camera.offset[1]))))
                        
                        pos = [pos[0]-18,pos[1]-18]
                        y, x = pos[1] - real_rect[1]+camera.offset[1],  pos[0] - real_rect[0]+camera.offset[0]
                        angle = math.atan2(y,x)
                        speed = 9
                        dx = math.cos(angle)
                        dy = math.sin(angle)

                        x,y = real_rect[0], real_rect[1]
                        self.bomb_list.append([real_rect, i[2], [dx,dy], [x,y], speed, 0, 0, "bomb", False])
                except:
                    pass
                
    def shoot_mine(self, toggle_sentry_aim):
        for i in sentry.sentry_list:
            if i[0] == sentry.bomber_mine_sentry_top_img:
                try:
                    if toggle_sentry_aim == False:
                        real_rect = pygame.Rect(i[1][0]+50-25, i[1][1]+50-25, 50, 50)
                        pos = pygame.mouse.get_pos()

                        pos = [pos[0]-25,pos[1]-25]
                        y, x = pos[1] - real_rect[1]+camera.offset[1],  pos[0] - real_rect[0]+camera.offset[0]
                        angle = math.atan2(y,x)
                        speed = 9
                        dx = math.cos(angle)
                        dy = math.sin(angle)

                        x,y = real_rect[0], real_rect[1]

                        self.mine_list.append([real_rect, i[2], [dx,dy], [x,y], speed, 0, False])
                    else:
                        pos = pygame.math.Vector2(i[1][0], i[1][1])
                        real_rect = pygame.Rect(i[1][0]+50-25, i[1][1]+50-25, 50, 50)
                        pos = min([e for e in zombie.zombie_list], key=lambda e: pos.distance_to(pygame.math.Vector2(int(e[0][0]+camera.offset[0]), int(e[0][1]+camera.offset[1]))))
                        
                        pos = [pos[0]-25,pos[1]-25]
                        y, x = pos[1] - real_rect[1]+camera.offset[1],  pos[0] - real_rect[0]+camera.offset[0]
                        angle = math.atan2(y,x)
                        speed = 9
                        dx = math.cos(angle)
                        dy = math.sin(angle)

                        x,y = real_rect[0], real_rect[1]
                        self.bomb_list.append([real_rect, i[2], [dx,dy], [x,y], speed, 0, False])
                except:
                    pass

    def shoot_molotov(self, toggle_sentry_aim):
        for i in sentry.sentry_list:
            if i[0] == sentry.bomber_molotov_sentry_top_img:
                    if toggle_sentry_aim == False:
                        real_rect = pygame.Rect(i[1][0]+50-9, i[1][1]+50-18, 18, 36)
                        pos = pygame.mouse.get_pos()

                        pos = [pos[0]-9,pos[1]-18]
                        y, x = pos[1] - real_rect[1]+camera.offset[1],  pos[0] - real_rect[0]+camera.offset[0]
                        angle = math.atan2(y,x)
                        speed = 8
                        dx = math.cos(angle)
                        dy = math.sin(angle)

                        x,y = real_rect[0], real_rect[1]
                        
                        random_direction = randint(1,2)
                        if random_direction == 1:
                            image = self.molotov_img
                        else:
                            image = self.molotov_flipped_img

                        self.molotov_list.append([real_rect, i[2], [dx,dy], [x,y], speed, random_direction, image])
                    else:
                        pos = pygame.math.Vector2(i[1][0], i[1][1])
                        real_rect = pygame.Rect(i[1][0]+50-18, i[1][1]+50-18, 36, 36)
                        pos = min([e for e in zombie.zombie_list], key=lambda e: pos.distance_to(pygame.math.Vector2(int(e[0][0]+camera.offset[0]), int(e[0][1]+camera.offset[1]))))
                        
                        pos = [pos[0]-18,pos[1]-18]
                        y, x = pos[1] - real_rect[1]+camera.offset[1],  pos[0] - real_rect[0]+camera.offset[0]
                        angle = math.atan2(y,x)
                        speed = 9
                        dx = math.cos(angle)
                        dy = math.sin(angle)

                        x,y = real_rect[0], real_rect[1]
                        self.molotov_list.append([real_rect, i[2], [dx,dy], [x,y], speed, 0, 0])
    
    def draw(self, win):
        for i in self.bullet_list:
            if i[8] == "bullet":
                win.blit(self.bullet_img, (camera.add_offset(i[0]))) 
        for i in self.bomb_list: 
            if i[7] == "bomb":
                win.blit(self.bomb_img, (camera.add_offset(i[0])))  
            elif i[7] == "red_bomb":
                win.blit(self.red_bomb_img, (camera.add_offset(i[0])))
        for i in self.mine_list: 
            win.blit(self.mine_img, (camera.add_offset(i[0])))  
        for i in self.molotov_list: 
            rotated_image = pygame.transform.rotate(i[6], int(i[1])+90)
            new_rect = rotated_image.get_rect(center = i[6].get_rect(topleft = (i[0][0],i[0][1])).center)
            win.blit(rotated_image, (camera.add_offset(new_rect)))

    def move(self):
        for i in self.bullet_list:
            try:
                i[3][0] += i[2][0] * self.speed
                i[3][1] += i[2][1] * self.speed
                i[0][0] = int(i[3][0])
                i[0][1] = int(i[3][1])
            except:
                pass
        for i in self.bomb_list:
            if i[0][1] != 0 and i[0][0] != 0:
                i[3][0] += i[2][0] * i[4]
                i[3][1] += i[2][1] * i[4]
                i[0][0] = int(i[3][0])
                i[0][1] = int(i[3][1])
        for i in self.mine_list:
            if i[0][1] != 0 and i[0][0] != 0:
                i[3][0] += i[2][0] * i[4]
                i[3][1] += i[2][1] * i[4]
                i[0][0] = int(i[3][0])
                i[0][1] = int(i[3][1])
        for i in self.molotov_list:
            if i[0][1] != 0 and i[0][0] != 0:
                i[3][0] += i[2][0] * i[4]
                i[3][1] += i[2][1] * i[4]
                i[0][0] = int(i[3][0])
                i[0][1] = int(i[3][1])
        
    def check_out_of_screen(self,width,height):
        while True:
            pygame.time.delay(100)
            num = 0
            for i in self.bullet_list:
                if 0 < i[0][0] < width and 0 < i[0][1] < height:
                    pass
                else:
                    self.bullet_list.pop(num)
                num += 1
                

class Explosion():
    def __init__(self, b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, mb1, mb2, mb3, mb4, mb5, mb6, mb7, mb8, mb9, mb10, mb11):
        self.bomb_explosion_list = [] # list = [rect, animation_number, tick, exploded, damage]
        self.mini_bomb_explosion_list = []
        self.bomb_explosion_animation = [b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11]
        self.mini_bomb_explosion_animation = [mb1,mb2,mb3,mb4,mb5,mb6,mb7,mb8,mb9,mb10,mb11]

    def add_explosion(self,x,y,damage):
        rect = pygame.Rect(x-100,y-100,100,100)
        self.bomb_explosion_list.append([rect, 0, 0, False, damage])
    
    def add_mini_explosion(self,x,y):
        rect = pygame.Rect(x-16,y-8,50,50)
        self.mini_bomb_explosion_list.append([rect, 0, 0])
        
    def update_mini_explosion(self):
        number_list = []
        number = 0
        for i in self.mini_bomb_explosion_list:
            i[2] = i[2] + 1
            if i[2] == 2:
                if i[1] >= 9:
                    number_list.append(number)
                i[1] = i[1] + 1
                i[2] = 0
            number += 1
        number_list.sort(reverse=True)
        for i in number_list:
            self.mini_bomb_explosion_list.pop(i)

    def update_explosion(self):
        number_list = []
        number = 0
        for i in self.bomb_explosion_list:
            if i[3] == False:
                explosion.explode_zombies(i[0][0], i[0][1], i[4])
                i[3] = True
            i[2] = i[2] + 1
            if i[2] == 2:
                if i[1] >= 9:
                    number_list.append(number)
                i[1] = i[1] + 1
                i[2] = 0
            number += 1
        number_list.sort(reverse=True)
        for i in number_list:
            self.bomb_explosion_list.pop(i)




    def explode_zombies(self,x,y,damage_list):
        for i in zombie.zombie_list:
            dist = math.hypot(x+50-i[3][0]+25, y+50-i[3][1]+40)
            if 100 > dist >= 0:
                damage = damage_list[0]
            elif 150 > dist >= 100:
                damage = damage_list[1]
            elif 200 > dist >= 150:
                damage = damage_list[2]
            elif 400 > dist >= 200:
                damage = damage_list[3]
            else:
                damage = 0
            health = i[1]
            health -= damage
            i[1] = health
    
    def draw_explosion(self, win):
        for i in self.bomb_explosion_list:
            win.blit(self.bomb_explosion_animation[i[1]], camera.add_offset(i[0]))
        for i in self.mini_bomb_explosion_list:            
            win.blit(self.mini_bomb_explosion_animation[i[1]], camera.add_offset(i[0]))


class Desk():
    def __init__(self, image1, image2):
        self.desk_list = []     
        self.desk_rect_list = []
        self.image1 = image1
        self.image2 = image2   
        
    def draw_desk(self, win):
        for i in self.desk_list:
            try:
                if i[1] == 1:
                    win.blit(self.image1, camera.add_offset(i[0]))
                else:
                    win.blit(self.image2, camera.add_offset(i[0]))
            except:
                pass

    def add_desk(self, x, y):
        rect = pygame.Rect(x, y, 100, 100)    
        self.desk_list.append([rect, 1])    
        self.desk_rect_list.append(rect)  
        rect = pygame.Rect(x+100, y, 100, 100)    
        self.desk_list.append([rect, 2])   
        self.desk_rect_list.append(rect)  
        

class Cabinet():
    def __init__(self, image1, image2):
        self.cabinet_list = []     
        self.cabinet_rect_list = []    
        self.image1 = image1 
        self.image2 = image2 
        
    def draw_cabinet(self, win):
        for i in self.cabinet_list:
            try:
                if i[1] == 1:
                    win.blit(self.image1, camera.add_offset(i[0]))
                else:
                    win.blit(self.image2, camera.add_offset(i[0]))
            except:
                pass

    def add_cabinet(self, x, y):
        rect = pygame.Rect(x, y, 100, 100)
        self.cabinet_list.append([rect, 2])
        self.cabinet_rect_list.append(rect)
        rect = pygame.Rect(x, y-100, 100, 100)
        self.cabinet_list.append([rect, 1])
        self.cabinet_rect_list.append(rect)


class Wall():
    def __init__(self, left_wall_top, left_wall_bottom, mid_wall_top, mid_wall_bottom, right_wall_top, right_wall_bottom):
        self.wall_list = []
        self.wall_rect_list = []
        self.left_wall_top = left_wall_top
        self.left_wall_bottom = left_wall_bottom
        self.mid_wall_top = mid_wall_top
        self.mid_wall_bottom = mid_wall_bottom
        self.right_wall_top = right_wall_top
        self.right_wall_bottom = right_wall_bottom

    
    def add_walls(self, x, y, wall):
        rect = pygame.Rect(x, y, 100, 100)
        self.wall_list.append([rect, wall])
        self.wall_rect_list.append(rect)
    
    def draw_walls(self, win):
        for i in self.wall_list:
            if i[1] == "LT":
                win.blit(self.left_wall_top, camera.add_offset(i[0]))
            if i[1] == "LB":
                win.blit(self.left_wall_bottom, camera.add_offset(i[0]))
            if i[1] == "MT":
                win.blit(self.mid_wall_top, camera.add_offset(i[0]))
            if i[1] == "MB":
                win.blit(self.mid_wall_bottom, camera.add_offset(i[0]))
            if i[1] == "RT":
                win.blit(self.right_wall_top, camera.add_offset(i[0]))
            if i[1] == "RB":
                win.blit(self.right_wall_bottom, camera.add_offset(i[0]))

            
class CameraGroup():
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2(0,0)
        self.half_w = self.display_surface.get_size()[0]//2
        self.half_h = self.display_surface.get_size()[1]//2

    def center_target_camera(self,target):
        self.offset.x = target.centerx - self.half_w
        self.offset.y = target.centery - self.half_h
    
    def add_offset(self, rect):
        
        self.center_target_camera(player.real_rect)

        try:
            offset = rect.topleft - self.offset
            return offset
        except:
            offset = (rect[0] - self.offset[0]), (rect[1] - self.offset[1])
            return offset


class Wall_Top():
    def __init__(self, TT, TR, TL, LL, LB, BB, BR, RR, TLI, TRI, BLI, BRI):
        self.wall_list = []
        self.wall_rect_list = []
        self.TT = TT
        self.TR = TR
        self.TL = TL
        self.LL = LL
        self.BL = LB
        self.BB = BB
        self.BR = BR
        self.RR = RR
        self.TLI = TLI
        self.TRI = TRI
        self.BLI = BLI
        self.BRI = BRI

    def add_walls(self, x, y, wall):
        if wall == "TT":
            rect = pygame.Rect(x, y, 100, 100)
            self.wall_list.append([rect, wall])
            self.wall_rect_list.append(rect)
        if wall == "TR":
            rect = pygame.Rect(x, y, 100, 100)
            self.wall_list.append([rect, wall])
            self.wall_rect_list.append(rect)
        if wall == "TL":
            rect = pygame.Rect(x, y, 100, 100)
            self.wall_list.append([rect, wall])
            self.wall_rect_list.append(rect)
        if wall == "LL":
            rect = pygame.Rect(x, y, 100, 100)
            self.wall_list.append([rect, wall])
            self.wall_rect_list.append(rect)
        if wall == "RR":
            rect = pygame.Rect(x, y, 100, 100)
            self.wall_list.append([rect, wall])
            self.wall_rect_list.append(rect)
        if wall == "BL":
            rect = pygame.Rect(x, y, 100, 100)
            self.wall_list.append([rect, wall])
            self.wall_rect_list.append(rect)
        if wall == "BR":
            rect = pygame.Rect(x, y, 100, 100)
            self.wall_list.append([rect, wall])
            self.wall_rect_list.append(rect)
        if wall == "BB":
            rect = pygame.Rect(x, y, 100, 100)
            self.wall_list.append([rect, wall])
            self.wall_rect_list.append(rect)
        if wall == "TLI":
            rect = pygame.Rect(x, y, 100, 100)
            self.wall_list.append([rect, wall])
            self.wall_rect_list.append(rect)
        if wall == "TRI":
            rect = pygame.Rect(x, y, 100, 100)
            self.wall_list.append([rect, wall])
            self.wall_rect_list.append(rect)
        if wall == "BLI":
            rect = pygame.Rect(x, y, 100, 100)
            self.wall_list.append([rect, wall])
            self.wall_rect_list.append(rect)
        if wall == "BRI":
            rect = pygame.Rect(x, y, 100, 100)
            self.wall_list.append([rect, wall])
            self.wall_rect_list.append(rect)
            

    
    def draw_walls(self, win):
        for i in self.wall_list:
            if i[1] == "TT":
                win.blit(self.TT, camera.add_offset(i[0]))
            if i[1] == "TR":
                win.blit(self.TR, camera.add_offset(i[0]))
            if i[1] == "TL":
                win.blit(self.TL, camera.add_offset(i[0]))
            if i[1] == "LL":
                win.blit(self.LL, camera.add_offset(i[0]))
            if i[1] == "RR":
                win.blit(self.RR, camera.add_offset(i[0]))
            if i[1] == "BB":
                win.blit(self.BB, camera.add_offset(i[0]))
            if i[1] == "BR":
                win.blit(self.BR, camera.add_offset(i[0]))
            if i[1] == "BL":
                win.blit(self.BL, camera.add_offset(i[0]))
            if i[1] == "TLI":
                win.blit(self.TLI, camera.add_offset(i[0]))
            if i[1] == "TRI":
                win.blit(self.TRI, camera.add_offset(i[0]))
            if i[1] == "BLI":
                win.blit(self.BLI, camera.add_offset(i[0]))
            if i[1] == "BRI":
                win.blit(self.BRI, camera.add_offset(i[0]))


class Floor():
    def __init__(self, img):
        self.floor_list = []
        self.img = img
            
    def add_floor(self, x, y):
        rect = pygame.Rect(x, y, 100, 100)
        self.floor_list.append(rect)

    def draw(self, win):
        for i in self.floor_list:
            win.blit(self.img, camera.add_offset(i))


class UI():
    def __init__(self, UUC, UC, SUC, SC, floor):
        self.UUC = UUC
        self.UC = UC
        self.SUC = SUC
        self.SC = SC
        self.floor = floor
        self.ui_list = []

        self.sentry_selected = 1

        window_size = pygame.display.get_window_size()

        # DISTANCE BETWEEN EACH RECT IS 150
        # IF THE AMOUNT OF SENTRIES IS EVEN, MIDDLE TWO ARE 75, IF ODD, THE MIDDLE ONE IS 0
        # THEN ADD 150 EACH TIME

        rect = pygame.Rect(window_size[0]/2-50-375, window_size[0]/2-100-50, 100,100)
        self.ui_list.append([rect, self.floor])
        rect = pygame.Rect(window_size[0]/2-50-375, window_size[0]/2-100-50, 100,100)
        self.ui_list.append([rect, self.SUC])
        rect = pygame.Rect(window_size[0]/2-50-375, window_size[0]/2-100-50, 100,100)
        self.ui_list.append([rect, sentry.assault_sentry_base_img])
        rect = pygame.Rect(window_size[0]/2-50-375, window_size[0]/2-100-50, 100,100)
        self.ui_list.append([rect, sentry.assault_sentry_top_img])

        rect = pygame.Rect(window_size[0]/2-50-225, window_size[0]/2-100-50, 100,100)
        self.ui_list.append([rect, self.floor])
        rect = pygame.Rect(window_size[0]/2-50-225, window_size[0]/2-100-50, 100,100)
        self.ui_list.append([rect, self.UUC])
        rect = pygame.Rect(window_size[0]/2-50-225, window_size[0]/2-100-50, 100,100)
        self.ui_list.append([rect, sentry.assault_sentry_base_img])
        rect = pygame.Rect(window_size[0]/2-50-225, window_size[0]/2-100-50, 100,100)
        self.ui_list.append([rect, sentry.assault_shotgun_top_img])

        rect = pygame.Rect(window_size[0]/2-50-75, window_size[0]/2-100-50, 100,100)
        self.ui_list.append([rect, self.floor])
        rect = pygame.Rect(window_size[0]/2-50-75, window_size[0]/2-100-50, 100,100)
        self.ui_list.append([rect, self.UUC])
        rect = pygame.Rect(window_size[0]/2-50-75, window_size[0]/2-100-50, 100,100)
        self.ui_list.append([rect, sentry.assault_sentry_base_img])
        rect = pygame.Rect(window_size[0]/2-50-75, window_size[0]/2-100-50, 100,100)
        self.ui_list.append([rect, sentry.assault_burst_top_img])

        rect = pygame.Rect(window_size[0]/2-50+75, window_size[0]/2-100-50, 100,100)
        self.ui_list.append([rect, self.floor])
        rect = pygame.Rect(window_size[0]/2-50+75, window_size[0]/2-100-50, 100,100)
        self.ui_list.append([rect, self.UUC])
        rect = pygame.Rect(window_size[0]/2-50+75, window_size[0]/2-100-50, 100,100)
        self.ui_list.append([rect, sentry.bomber_sentry_base_img])
        rect = pygame.Rect(window_size[0]/2-50+75, window_size[0]/2-100-50, 100,100)
        self.ui_list.append([rect, sentry.bomber_bomb_sentry_top_img])
        
        rect = pygame.Rect(window_size[0]/2-50+225, window_size[0]/2-100-50, 100,100)
        self.ui_list.append([rect, self.floor])
        rect = pygame.Rect(window_size[0]/2-50+225, window_size[0]/2-100-50, 100,100)
        self.ui_list.append([rect, self.UUC])
        rect = pygame.Rect(window_size[0]/2-50+225, window_size[0]/2-100-50, 100,100)
        self.ui_list.append([rect, sentry.bomber_sentry_base_img])
        rect = pygame.Rect(window_size[0]/2-50+225, window_size[0]/2-100-50, 100,100)
        self.ui_list.append([rect, sentry.bomber_mine_sentry_top_img])

        rect = pygame.Rect(window_size[0]/2-50+375, window_size[0]/2-100-50, 100,100)
        self.ui_list.append([rect, self.floor])
        rect = pygame.Rect(window_size[0]/2-50+375, window_size[0]/2-100-50, 100,100)
        self.ui_list.append([rect, self.UUC])
        rect = pygame.Rect(window_size[0]/2-50+375, window_size[0]/2-100-50, 100,100)
        self.ui_list.append([rect, sentry.bomber_sentry_base_img])
        rect = pygame.Rect(window_size[0]/2-50+375, window_size[0]/2-100-50, 100,100)
        self.ui_list.append([rect, sentry.bomber_molotov_sentry_top_img])

    def update(self):
        self.update_pressed()
    
    def update_pressed(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            self.set_all_false()
            self.sentry_selected = 1
            self.ui_list[1][1] = self.SUC
        elif keys[pygame.K_2]:
            self.set_all_false()            
            self.sentry_selected = 2
            self.ui_list[5][1] = self.SUC
        elif keys[pygame.K_3]:
            self.set_all_false()            
            self.sentry_selected = 3
            self.ui_list[9][1] = self.SUC
        elif keys[pygame.K_4]:
            self.set_all_false()            
            self.sentry_selected = 4
            self.ui_list[13][1] = self.SUC
        elif keys[pygame.K_5]:
            self.set_all_false()            
            self.sentry_selected = 5
            self.ui_list[17][1] = self.SUC
        elif keys[pygame.K_6]:
            self.set_all_false()            
            self.sentry_selected = 6
            self.ui_list[21][1] = self.SUC
                        
    def set_all_false(self):
        for i in self.ui_list:
            if i[1] == self.SUC or i[1] == self.SC or i[1] == self.UC or i[1] == self.UUC:
                i[1] = self.UUC

    def draw(self, win):
        for i in self.ui_list:
            win.blit(i[1], (i[0][0], i[0][1]))


class Fire():
    def __init__(self,img1,img2,img3,ring_of_fire_inner_img, ring_of_fire_outer_img):
        self.animation_list = [img1,img2,img3]
        self.ring_of_fire_inner_img = ring_of_fire_inner_img
        self.ring_of_fire_outer_img = ring_of_fire_outer_img
        self.fire_list = []
        self.ring_list = []
        self.ring_rect_list = []
    
    def update_fire(self):
        delete_list = []
        num = 0
        for i in self.fire_list:
            i[2] = i[2] + 1
            random_number = randint(8,12)
            if i[2] == random_number or i[2] >= 13:
                i[2] = 0
                i[1] = i[1] + 1
                i[3] = i[3] + 1
                if i[1] == 4:
                    i[1] = 1
                if i[3] == 18:
                    delete_list.append(num)
            num += 1
        delete_list.sort(reverse=True)
        for i in delete_list:
            self.fire_list.pop(i)
    
    def update_ring(self):
        self.ring_rect_list = []
        pop_list = []
        num = 0
        for i in self.ring_list:
            i[0][0] = i[0][0] + 1
            if len(i) > 1:
                self.ring_rect_list.append(i[0][1])
            if i[0][0] == 15:
                i[0][0] = 0
                if len(i) > 1:
                    self.add_fire(i[1][0], i[1][1])
                    self.ring_list[num].pop(1)
                else:
                    if i[0][2] == False:
                        i[0][2] = True
                    pop_list.append(num)
            num = num + 1
        pop_list.sort(reverse=True)
        for i in pop_list:
            self.ring_list.pop(i)
                    
    def create_ring(self,x,y):
        rect = pygame.Rect(x-100+camera.offset[0],y-100+camera.offset[1],200,200)
        ring_list = [[0,rect, self.ring_of_fire_outer_img, self.ring_of_fire_inner_img]]
        for i in range(1,18):
            alpha = 2 * math.pi * random.random()
            r = 90 * math.sqrt(random.random())
            dx = r * math.cos(alpha) + x
            dy = r * math.sin(alpha) + y
            ring_list.append((dx+camera.offset[0]-8,dy+camera.offset[1]-16))
        self.ring_list.append(ring_list)
                        
    def draw_fire(self, win):
        for i in self.fire_list:
            try:
                win.blit(self.animation_list[i[1]-1], camera.add_offset(i[0]))
            except:
                pass
        for i in self.ring_list:
            try:
                win.blit(i[0][3], (i[0][1][0]-camera.offset[0],i[0][1][1]-camera.offset[1]))
                win.blit(i[0][2], (i[0][1][0]-camera.offset[0],i[0][1][1]-camera.offset[1]))
            except:
                pass
            
    
    def add_fire(self,x,y):
        rect = pygame.Rect(x,y,32,32)
        self.fire_list.append([rect, 1, 0, 0])




def display_coords(win):
    pos = pygame.mouse.get_pos()
    font = pygame.font.SysFont("comicsans", 30)
    text = font.render(str(pos[0]) + ", " + str(pos[1]), 1, (0,0,0))
    win.blit(text, (int(pos[0]-50), int(pos[1])-50))
    
def redraw_window(win, toggle_pos, toggle_p_pos, toggle_tile, touched_zombie):
    win.fill((0,0,0))    
    floor.draw(win)
    if toggle_tile == True:
        tile.draw_tile(win)
    wall.draw_walls(win)
    walltop.draw_walls(win)
    desk.draw_desk(win)
    cabinet.draw_cabinet(win)
    fire.draw_fire(win)
    zombie.draw_zombie(win)
    sentry.rotate_sentry(toggle_sentry_aim)
    sentry.draw_sentry(win)
    zombie.draw_health_bar(win)
    bullet.draw(win)
    explosion.draw_explosion(win)
    player.draw(win)    
    if toggle_tile == True:
        ui.update()
        ui.draw(win)
    pygame.display.update()

def threaded_dash(player):
    player.vel = player.vel*5
    pygame.time.delay(100)
    player.vel = 5
    pygame.time.delay(750)
    global dash_once
    dash_once = True

def display_health(win):
    for i in zombie.zombie_list:
        font = pygame.font.SysFont("comicsans", 30)
        text = font.render("HP: " + str(i[1]), 1, (0,0,0))
        win.blit(text, camera.add_offset((int(i[0][0]-10), int(i[0][1])-40)))

def create_map():
    for j in range(-100, 1100, 100):
        if j == -100:
            for i in range(0,1900,100):
                if i == 0:
                    walltop.add_walls(i, j, "TL")
                elif i > 0 and i < 1800:

                    walltop.add_walls(i, j, "TT")
                else:
                    walltop.add_walls(i, j, "TR")
        if j == 0:
            for i in range(0,1900,100):
                if i == 0:
                    walltop.add_walls(i, j, "LL")
                elif i > 0 and i < 1800:
                    wall.add_walls(i, j, "MT")
                else:
                    walltop.add_walls(i, j, "RR")
        if j == 100:
            for i in range(0,1900,100):
                if i == 0:
                    walltop.add_walls(i, j, "LL")
                elif i > 0 and i < 1800:
                    wall.add_walls(i, j, "MB")
                else:
                    walltop.add_walls(i, j, "RR")
        if j == 200:
            for i in range(0,1900,100):
                if i == 0:
                    walltop.add_walls(i, j, "LL")
                elif i > 0 and i < 800:
                    tile.add_tile(i, j)
                    floor.add_floor(i, j)
                elif i > 700 and i < 900:
                    floor.add_floor(i, j)
                    desk.add_desk(i, j)
                elif i > 800 and i < 1000:
                    floor.add_floor(i, j)
                elif i > 900 and i < 1100:
                    floor.add_floor(i, j)
                    cabinet.add_cabinet(i, j)
                elif i > 1000 and i < 1800:
                    tile.add_tile(i, j)
                    floor.add_floor(i, j)
                else:
                    walltop.add_walls(i, j, "RR")
        if j == 300:
            for i in range(0,1900,100):
                if i == 0:
                    walltop.add_walls(i, j, "LL")
                elif i > 0 and i < 1800:
                    tile.add_tile(i, j)
                    floor.add_floor(i, j)
                else:
                    walltop.add_walls(i, j, "RR")
        if j == 400:
            for i in range(0,1900,100):
                if i == 0:
                    walltop.add_walls(i, j, "LL")
                elif i > 0 and i < 1800:
                    tile.add_tile(i, j)
                    floor.add_floor(i, j)
                else:
                    walltop.add_walls(i, j, "RR")
        if j == 500:
            for i in range(0,1900,100):
                if i == 0:
                    walltop.add_walls(i, j, "LL")
                elif i > 0 and i < 1800:
                    tile.add_tile(i, j)
                    floor.add_floor(i, j)
                else:
                    walltop.add_walls(i, j, "RR")
        if j == 600:
            for i in range(0,1900,100):
                if i == 0:
                    walltop.add_walls(i, j, "LL")
                elif i > 0 and i < 1800:
                    tile.add_tile(i, j)
                    floor.add_floor(i, j)
                else:
                    walltop.add_walls(i, j, "RR")
        if j == 700:
            for i in range(0,1900,100):
                if i == 0:
                    walltop.add_walls(i, j, "LL")
                elif i > 0 and i < 1800:
                    tile.add_tile(i, j)
                    floor.add_floor(i, j)
                else:
                    walltop.add_walls(i, j, "RR")
        if j == 800:
            for i in range(0,1900,100):
                if i == 0:
                    walltop.add_walls(i, j, "LL")
                elif i > 0 and i < 1800:
                    tile.add_tile(i, j)
                    floor.add_floor(i, j)
                else:
                    walltop.add_walls(i, j, "RR")
        if j == 900:
            for i in range(0,1900,100):
                if i == 0:
                    walltop.add_walls(i, j, "LL")
                elif i > 0 and i < 1800:
                    tile.add_tile(i, j)
                    floor.add_floor(i, j)
                else:
                    walltop.add_walls(i, j, "RR")
        if j == 1000:
            for i in range(0,1900,100):
                if i == 0:
                    walltop.add_walls(i, j, "BL")
                elif i > 0 and i < 1800:
                    walltop.add_walls(i, j, "BB")
                else:
                    walltop.add_walls(i, j, "BR")

def auto_shoot_assault(toggle_sentry_aim):
    bullet.shoot_assault(toggle_sentry_aim)
    pygame.time.delay(200)
    global auto_shoot_delay_assault
    auto_shoot_delay_assault = True

def auto_shoot_shotgun(toggle_sentry_aim):
    bullet.shoot_shotgun(toggle_sentry_aim)
    pygame.time.delay(1000)
    global auto_shoot_delay_shotgun 
    auto_shoot_delay_shotgun = True
    
def auto_shoot_burst(toggle_sentry_aim):
    bullet.shoot_burst(toggle_sentry_aim)
    pygame.time.delay(50)
    bullet.shoot_burst(toggle_sentry_aim)
    pygame.time.delay(50)
    bullet.shoot_burst(toggle_sentry_aim)
    pygame.time.delay(500)
    global auto_shoot_delay_burst
    auto_shoot_delay_burst = True

def auto_shoot_bomb(toggle_sentry_aim):
    bullet.shoot_bomb(toggle_sentry_aim)
    pygame.time.delay(0)
    global auto_shoot_delay_bomb
    auto_shoot_delay_bomb = True
    
def auto_shoot_mine(toggle_sentry_aim):
    bullet.shoot_mine(toggle_sentry_aim)
    pygame.time.delay(2250)
    global auto_shoot_delay_mine
    auto_shoot_delay_mine = True

def auto_shoot_molotov(toggle_sentry_aim):
    bullet.shoot_molotov(toggle_sentry_aim)
    pygame.time.delay(4000)
    global auto_shoot_delay_molotov
    auto_shoot_delay_molotov = True

tile_selected_img = pygame.image.load('assets/tile_selected.png').convert()
tile_unselected_img = pygame.image.load('assets/tile_unselected.png').convert()
tile_confirmed_img = pygame.image.load('assets/tile_confirmed.png').convert()
tile_confirmed_selected_img = pygame.image.load('assets/tile_confirmed_selected.png').convert()
assault_sentry_base_img = pygame.image.load('assets/sentry_assault_base.png').convert()
assault_sentry_top_img = pygame.image.load('assets/assault_auto_sentry_top.png').convert()
assault_shotgun_sentry_top_img = pygame.image.load('assets/assault_shotgun_sentry_top.png').convert()
assault_burst_sentry_top_img = pygame.image.load('assets/assault_burst_sentry_top.png').convert()
bomber_sentry_base_img = pygame.image.load('assets/sentry_bomber_base.png').convert()
bomber_bomb_sentry_top_img = pygame.image.load('assets/bomber_bomb_sentry_top.png').convert()
bomber_mine_sentry_top_img = pygame.image.load('assets/bomber_mine_sentry_top.png').convert()
bomber_molotov_sentry_top_img = pygame.image.load('assets/bomber_molotov_sentry_top.png').convert()
bullet_img = pygame.image.load('assets/bullet.png').convert()
bomb_img = pygame.image.load('assets/bomb.png').convert()
red_bomb_img = pygame.image.load('assets/bomb_red.png').convert()
mine_img = pygame.image.load('assets/mine.png').convert()
molotov_img = pygame.image.load('assets/molotov.png').convert()
molotov_flipped_img = pygame.image.load('assets/molotov_flipped.png').convert()
floortile = pygame.image.load('assets/floortile.png').convert()
desk1 = pygame.image.load('assets/desk1.png').convert()
desk2 = pygame.image.load('assets/desk2.png').convert()
cabinet1 = pygame.image.load('assets/cabinet1.png').convert()
cabinet2 = pygame.image.load('assets/cabinet2.png').convert()
wall_left_top = pygame.image.load('assets/wall_left1.png').convert()
wall_left_bottom = pygame.image.load('assets/wall_left2.png').convert()
wall_mid_top = pygame.image.load('assets/wall_mid1.png').convert()
wall_mid_bottom = pygame.image.load('assets/wall_mid2.png').convert()
wall_right_top = pygame.image.load('assets/wall_right1.png').convert()
wall_right_bottom = pygame.image.load('assets/wall_right2.png').convert()
player_img = pygame.image.load('assets/player.png').convert()

enemy_img = pygame.image.load('assets/enemy.png').convert()
enemy_flipped_img = pygame.image.load('assets/enemy_flipped.png').convert()
enemy_burning_img = pygame.image.load('assets/enemy_burning.png').convert()
enemy_burning_flipped_img = pygame.image.load('assets/enemy_burning_flipped.png').convert()

fire_1_img = pygame.image.load('assets/fire_1.png').convert()
fire_2_img = pygame.image.load('assets/fire_2.png').convert()
fire_3_img = pygame.image.load('assets/fire_3.png').convert()
ring_of_fire_inner_img = pygame.image.load('assets/ring_of_fire_inner.png').convert()
ring_of_fire_outer_img = pygame.image.load('assets/ring_of_fire_outer.png').convert()

explosion_1 = pygame.image.load('assets/explosion_1.png').convert()
explosion_2 = pygame.image.load('assets/explosion_2.png').convert()
explosion_3 = pygame.image.load('assets/explosion_3.png').convert()
explosion_4 = pygame.image.load('assets/explosion_4.png').convert()
explosion_5 = pygame.image.load('assets/explosion_5.png').convert()
explosion_6 = pygame.image.load('assets/explosion_6.png').convert()
explosion_7 = pygame.image.load('assets/explosion_7.png').convert()
explosion_8 = pygame.image.load('assets/explosion_8.png').convert()
explosion_9 = pygame.image.load('assets/explosion_9.png').convert()
explosion_10 = pygame.image.load('assets/explosion_10.png').convert()
explosion_11 = pygame.image.load('assets/explosion_11.png').convert()

TT_img = pygame.image.load('assets/wall_top_top.png').convert()
TR_img = pygame.image.load('assets/wall_top_right_corner.png').convert()
RR_img = pygame.image.load('assets/wall_top_right.png').convert()
BR_img = pygame.image.load('assets/wall_top_bottom_right_corner.png').convert()
BB_img = pygame.image.load('assets/wall_top_bottom.png').convert()
BL_img = pygame.image.load('assets/wall_top_bottom_left_corner.png').convert()
LL_img = pygame.image.load('assets/wall_top_left.png').convert()
TL_img = pygame.image.load('assets/wall_top_left_corner.png').convert()

TRI_img = pygame.image.load('assets/wall_top_right_corner_inner.png').convert()
BRI_img = pygame.image.load('assets/wall_top_bottom_right_corner_inner.png').convert()
BLI_img = pygame.image.load('assets/wall_top_bottom_left_corner_inner.png').convert()
TLI_img = pygame.image.load('assets/wall_top_left_corner_inner.png').convert()


TT_img.set_colorkey((255,255,255))
TR_img.set_colorkey((255,255,255))
RR_img.set_colorkey((255,255,255))
BR_img.set_colorkey((255,255,255))
BB_img.set_colorkey((255,255,255))
BL_img.set_colorkey((255,255,255))
LL_img.set_colorkey((255,255,255))
TL_img.set_colorkey((255,255,255))

TRI_img.set_colorkey((255,255,255))
BRI_img.set_colorkey((255,255,255))
BLI_img.set_colorkey((255,255,255))
TLI_img.set_colorkey((255,255,255))

tile_unselected_img.set_alpha(128)
tile_selected_img.set_alpha(128)
tile_confirmed_img.set_alpha(128)
tile_confirmed_selected_img.set_alpha(128)
ring_of_fire_inner_img.set_alpha(128)

enemy_img.set_colorkey((255,255,255))
enemy_flipped_img.set_colorkey((255,255,255))
enemy_burning_img.set_colorkey((255,255,255))
enemy_burning_flipped_img.set_colorkey((255,255,255))

cabinet1.set_colorkey((255,255,255))
cabinet2.set_colorkey((255,255,255))
desk1.set_colorkey((255,255,255))
desk2.set_colorkey((255,255,255))
assault_sentry_base_img.set_colorkey((255,255,255))
assault_sentry_top_img.set_colorkey((255,255,255))
assault_shotgun_sentry_top_img.set_colorkey((255,255,255))
assault_burst_sentry_top_img.set_colorkey((255,255,255))
bomber_sentry_base_img.set_colorkey((255,255,255))
bomber_bomb_sentry_top_img.set_colorkey((255,255,255))
bomber_mine_sentry_top_img.set_colorkey((255,255,255))
bomber_molotov_sentry_top_img.set_colorkey((255,255,255))
bullet_img.set_colorkey((255,255,255))
bomb_img.set_colorkey((255,255,255))
red_bomb_img.set_colorkey((255,255,255))
mine_img.set_colorkey((255,255,255))
molotov_img.set_colorkey((255,255,255))
molotov_flipped_img.set_colorkey((255,255,255))

fire_1_img.set_colorkey((255,255,255))
fire_2_img.set_colorkey((255,255,255))
fire_3_img.set_colorkey((255,255,255))
ring_of_fire_inner_img.set_colorkey((255,255,255))
ring_of_fire_outer_img.set_colorkey((255,255,255))

explosion_1.set_colorkey((255,255,255))
explosion_2.set_colorkey((255,255,255))
explosion_3.set_colorkey((255,255,255))
explosion_4.set_colorkey((255,255,255))
explosion_5.set_colorkey((255,255,255))
explosion_6.set_colorkey((255,255,255))
explosion_7.set_colorkey((255,255,255))
explosion_8.set_colorkey((255,255,255))
explosion_9.set_colorkey((255,255,255))
explosion_10.set_colorkey((255,255,255))
explosion_11.set_colorkey((255,255,255))

mini_explosion_1 = pygame.transform.scale(explosion_1, (75,75))
mini_explosion_2 = pygame.transform.scale(explosion_2, (75,75)) 
mini_explosion_3 = pygame.transform.scale(explosion_3, (75,75))
mini_explosion_4 = pygame.transform.scale(explosion_4, (75,75))
mini_explosion_5 = pygame.transform.scale(explosion_5, (75,75))
mini_explosion_6 = pygame.transform.scale(explosion_6, (75,75))
mini_explosion_7 = pygame.transform.scale(explosion_7, (75,75))
mini_explosion_8 = pygame.transform.scale(explosion_8, (75,75))
mini_explosion_9 = pygame.transform.scale(explosion_9, (75,75))
mini_explosion_10 = pygame.transform.scale(explosion_10, (75,75))
mini_explosion_11 = pygame.transform.scale(explosion_11, (75,75))

player = Player(500, 500, 50, 50, player_img)
zombie = Zombie(enemy_img, enemy_flipped_img, enemy_burning_img, enemy_burning_flipped_img)
tile = Tile(tile_selected_img, tile_unselected_img, tile_confirmed_selected_img, tile_confirmed_img)
sentry = Sentry(assault_sentry_base_img, assault_sentry_top_img, assault_shotgun_sentry_top_img, assault_burst_sentry_top_img, bomber_sentry_base_img, bomber_bomb_sentry_top_img, bomber_mine_sentry_top_img, bomber_molotov_sentry_top_img)
bullet = Bullet(bullet_img, bomb_img, red_bomb_img, mine_img, molotov_img, molotov_flipped_img)
explosion = Explosion(explosion_1, explosion_2, explosion_3, explosion_4, explosion_5, explosion_6, explosion_7, explosion_8, explosion_9, explosion_10, explosion_11, mini_explosion_1, mini_explosion_2, mini_explosion_3, mini_explosion_4, mini_explosion_5, mini_explosion_6, mini_explosion_7, mini_explosion_8, mini_explosion_9, mini_explosion_10, mini_explosion_11)
desk = Desk(desk1, desk2)
cabinet = Cabinet(cabinet1, cabinet2)
wall = Wall(wall_left_top, wall_left_bottom, wall_mid_top, wall_mid_bottom, wall_right_top, wall_right_bottom)
camera = CameraGroup()
walltop = Wall_Top(TT_img, TR_img, TL_img, LL_img, BL_img, BB_img, BR_img, RR_img, TLI_img, TRI_img, BLI_img, BRI_img)
floor = Floor(floortile)
ui = UI(tile_unselected_img, tile_selected_img, tile_confirmed_img, tile_confirmed_selected_img, floortile)
fire = Fire(fire_1_img, fire_2_img, fire_3_img, ring_of_fire_inner_img, ring_of_fire_outer_img)

toggle_pos = False
toggle_pos_once = True
toggle_p_pos = False
toggle_p_pos_once = True
toggle_tile = False
toggle_tile_once = True
dash_once = True
summon_zombie_once = True
touched_zombie = False
toggle_sentry_aim_once = True
toggle_sentry_aim = False
auto_shoot_delay_assault = True
auto_shoot_delay_shotgun = True
auto_shoot_delay_burst = True
auto_shoot_delay_bomb = True
auto_shoot_delay_mine = True
auto_shoot_delay_molotov = True

start_new_thread(bullet.check_out_of_screen, (width, height))

create_map()

while True:
    clock.tick(60)
    zombie.move(player)
    player.move()
    bullet.move()
    zombie.check_collision()
    tile.update_tile()
    ui.update()
    bullet.update_shotgun_bullet()
    bullet.update_bomb()
    bullet.update_mine()
    bullet.update_molotov()
    explosion.update_explosion()
    explosion.update_mini_explosion()
    zombie.update_zombies()
    fire.update_fire()
    fire.update_ring()
    redraw_window(win, toggle_pos, toggle_p_pos, toggle_tile, touched_zombie)
    buttons = pygame.mouse.get_pressed()
    if player.check_collision_zombie(zombie) == True:
        touched_zombie = True
    else:
        touched_zombie = False
    if buttons[0] == True:
        if toggle_tile == False:
            if auto_shoot_delay_assault == True:
                auto_shoot_delay_assault = False
                start_new_thread(auto_shoot_assault, (toggle_sentry_aim,))
            if auto_shoot_delay_shotgun == True:
                auto_shoot_delay_shotgun = False
                start_new_thread(auto_shoot_shotgun, (toggle_sentry_aim,))
            if auto_shoot_delay_burst == True:
                auto_shoot_delay_burst = False
                start_new_thread(auto_shoot_burst, (toggle_sentry_aim,))
            if auto_shoot_delay_bomb == True:
                auto_shoot_delay_bomb = False
                start_new_thread(auto_shoot_bomb, (toggle_sentry_aim,))
            if auto_shoot_delay_mine == True:
                auto_shoot_delay_mine = False
                start_new_thread(auto_shoot_mine, (toggle_sentry_aim,))
            if auto_shoot_delay_molotov == True:
                auto_shoot_delay_molotov = False
                start_new_thread(auto_shoot_molotov, (toggle_sentry_aim,))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            tile.place_down_sentry(toggle_tile)            
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        pygame.quit
        break
    if keys[pygame.K_LSHIFT] == True:
        if toggle_pos_once == True:
            toggle_pos_once = False
            if toggle_pos == False:
                toggle_pos = True
            else:
                toggle_pos = False
    else:
        toggle_pos_once = True
    if keys[pygame.K_RSHIFT] == True:
        if toggle_p_pos_once == True:
            toggle_p_pos_once = False
            if toggle_p_pos == False:
                toggle_p_pos = True
            else:
                toggle_p_pos = False
    else:
        toggle_p_pos_once = True
    if keys[pygame.K_TAB] == True:
        if toggle_tile_once == True:
            toggle_tile_once = False
            if toggle_tile == False:
                toggle_tile = True
            else:
                toggle_tile = False
    else:
        toggle_tile_once = True
    if keys[pygame.K_SPACE] == True:
        if dash_once == True:
            dash_once = False
            start_new_thread(threaded_dash, (player,))
    if keys[pygame.K_r] == True:
        if summon_zombie_once == True:
            summon_zombie_once = False
            zombie.summon_zombie(randint(1,width), randint(1,height), 50,50)
    else:
        summon_zombie_once = True
    if keys[pygame.K_t] == True:
        if toggle_sentry_aim_once == True:
            toggle_sentry_aim_once = False
            if toggle_sentry_aim == False:
                toggle_sentry_aim = True
            else:
                toggle_sentry_aim = False
    else:
        toggle_sentry_aim_once = True
    if keys[pygame.K_q] == True:
        zombie.zombie_list = []
    if keys[pygame.K_p] == True:
        desk.re_do_desks()
    if keys[pygame.K_l] == True:
        cabinet.re_do_cabinets()
    
pygame.quit()
    
