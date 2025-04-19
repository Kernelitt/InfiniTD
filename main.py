import os
from cryptography.fernet import Fernet
import pygame
import sys
from tower import Tower,FastTower,RocketTower,ExplosiveTower,OverclockTower,FarmTower
from enemy import Basic,Fast,Strong,Boss
from settings import Settings
from pygame_stuff import Button
import json



class Game:
    def __init__(self, settings, screen,current_level,coefficient):
        self.current_level = current_level
        self.settings = settings
        self.screen = screen
        self.coefficient = coefficient
        self.enemies = []
        self.towers = []
        self.selected_tower = None
        self.enemy_spawn_time = 0
        self.enemy_spawn_interval = 500
        self.last_update_time = pygame.time.get_ticks()
        self.wave = 0
        self.max_enemies_per_wave = 5
        self.enemies_spawned = 0
        self.enemy_count = 0
        self.group_num = 0
        self.enemy_type = 'Basic'
        self.selected_tower_type = 'Basic'
        self.grid_width = self.grid_height = 24
        self.grid = [[0 for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        self.cell_size = round(40 *coefficient)
        self.base_health = 100
        self.economy = 50 + self.settings.load_data()["StartMoney"]
        self.load_map(current_level)
        self.green_papers = 0
        self.selected_tower_price = 24

    def load_map(self, file_path):
        with open(file_path, 'r') as file:
            map_data = json.load(file)
        self.path = [(p[0], p[1]) for p in map_data['paths']]
        self.platforms = [(p[0], p[1]) for p in map_data['platforms']]
        self.base_health = map_data['base_health']
        self.difficulty_multiplier = map_data['difficulty_multiplier']
        try:
            self.custom_waves = map_data['waves']
        except:
            self.custom_waves = []
        self.spawn_position = self.path[0]  




    def handle_tower_click(self, grid_x, grid_y):
        tower = self.get_tower_at(grid_x, grid_y)
        if tower:
            self.selected_tower = tower

    def get_tower_at(self, grid_x, grid_y):
        for tower in self.towers:
            if tower.position == (grid_x, grid_y):
                return tower
        return None

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    mouse_x, mouse_y = event.pos
                    grid_x = mouse_x // self.cell_size
                    grid_y = mouse_y // self.cell_size
                    if (1200*self.coefficient >= mouse_x):
                        self.handle_click(grid_x, grid_y)
                    if (1650*self.coefficient <= mouse_x <= 1790*self.coefficient and
                        50*self.coefficient <= mouse_y <= 90*self.coefficient):
                        self.upgrade_tower()  
                    if (1650*self.coefficient <= mouse_x <= 1790*self.coefficient and
                    100*self.coefficient <= mouse_y <= 140*self.coefficient):
                        self.demolish_tower() 
                    if (0 <= mouse_x <= 140*self.coefficient and
                    960*self.coefficient <= mouse_y <= 1000*self.coefficient):
                        self.base_health = 0     
            self.tower_types = {
            pygame.K_1: ('Basic', Tower((0, 0),self.coefficient).price),
            pygame.K_2: ('Fast', FastTower((0, 0),self.coefficient).price),
            pygame.K_3: ('Rocket', RocketTower((0, 0),self.coefficient).price),
            pygame.K_4: ('Explosive', ExplosiveTower((0, 0),self.coefficient).price),
            pygame.K_5: ('Overclock', OverclockTower((0, 0),self.coefficient).price),
            pygame.K_6: ('Farm', FarmTower((0, 0),self.coefficient).price)
            }
            if event.type == pygame.KEYDOWN:
                if event.key in self.tower_types:
                    self.selected_tower_type, self.selected_tower_price = self.tower_types[event.key]

    def handle_click(self, grid_x, grid_y):
        if (grid_x, grid_y) in self.platforms: 
            if self.grid[grid_y][grid_x] == 0: 
                if self.selected_tower_type == 'Basic':
                    tower = Tower((grid_x, grid_y),self.coefficient) 
                elif self.selected_tower_type == 'Fast':
                    tower = FastTower((grid_x, grid_y),self.coefficient)  
                elif self.selected_tower_type == 'Rocket':
                    tower = RocketTower((grid_x, grid_y),self.coefficient) 
                elif self.selected_tower_type == 'Explosive':
                    tower = ExplosiveTower((grid_x, grid_y),self.coefficient)  
                elif self.selected_tower_type == 'Overclock':
                    tower = OverclockTower((grid_x, grid_y),self.coefficient)  
                elif self.selected_tower_type == 'Farm':
                    tower = FarmTower((grid_x, grid_y),self.coefficient)  
                if self.economy >= tower.price: 
                    self.build_tower((grid_x, grid_y)) 
                    self.economy -= tower.price 
            else:
                self.handle_tower_click(grid_x, grid_y)
        else:
            self.selected_tower = None

    def build_tower(self, position):
        if self.selected_tower_type == 'Basic':
            self.towers.append(Tower(position,self.coefficient))  
        elif self.selected_tower_type == 'Fast':
            self.towers.append(FastTower(position,self.coefficient)) 
        elif self.selected_tower_type == 'Rocket':
            self.towers.append(RocketTower(position,self.coefficient)) 
        elif self.selected_tower_type == 'Explosive':
            self.towers.append(ExplosiveTower(position,self.coefficient)) 
        elif self.selected_tower_type == 'Overclock':
            self.towers.append(OverclockTower(position,self.coefficient))
        elif self.selected_tower_type == 'Farm':
            self.towers.append(FarmTower(position,self.coefficient))
        self.grid[position[1]][position[0]] = 1  

    def upgrade_tower(self):
        if self.selected_tower and self.economy >= self.selected_tower.upgrade_price:
            self.economy -= self.selected_tower.upgrade_price 
            self.selected_tower.upgrade()  

    def spawn_enemy(self):
        enemy_types = [Basic, Fast, Strong,Boss]  
        self.max_health = (40 + 5 * self.wave * round(self.wave / 4)) * self.difficulty_multiplier
        health = (40 + 5 * self.wave * round(self.wave / 4)) * self.difficulty_multiplier

        if self.wave < len(self.custom_waves):
            wave_data = self.custom_waves[self.wave]
            if self.group_num < len(wave_data): 
                group_data = wave_data[self.group_num]

                if self.enemies_spawned == self.enemy_count:
                    self.enemy_type = enemy_types[int(group_data[0]) - 1]
                    self.enemy_count = int(group_data[1])
                    self.enemy_spawn_interval = int(group_data[2])
                    self.enemies_spawned = 0  
                    self.group_num += 1  

                else:
                    new_enemy = self.enemy_type(self.path, health, self.coefficient)
                    new_enemy.position = (self.spawn_position[0] * self.cell_size, self.spawn_position[1] * self.cell_size)
                    self.enemies.append(new_enemy)
                    self.enemies_spawned += 1
            else:
                if not self.enemies:
                    self.group_num = 0  
                    self.wave += 1  
                    self.enemies_spawned = 0 
                    self.max_enemies_per_wave += 0.3  
                    self.green_papers = self.green_papers + self.wave * self.difficulty_multiplier
                    for tower in self.towers:
                        if isinstance(tower, OverclockTower):
                            tower.new_wave()
        else:
            self.enemy_spawn_interval = 500
            if self.enemies_spawned < self.max_enemies_per_wave:
                enemy_type = enemy_types[self.wave % len([Basic, Fast, Strong])]
                new_enemy = enemy_type(self.path, health, self.coefficient)
                new_enemy.position = (self.spawn_position[0] * self.cell_size, self.spawn_position[1] * self.cell_size)
                self.enemies.append(new_enemy)
                self.enemies_spawned += 1 

    def update(self):
        current_time = pygame.time.get_ticks()
        delta_time = (current_time - self.last_update_time) / 1000.0 

        if current_time - self.enemy_spawn_time > self.enemy_spawn_interval:
            self.spawn_enemy()
            self.enemy_spawn_time = current_time


        for enemy in self.enemies:
            if enemy.is_alive() == False:
                self.economy += 1 + 1 * round(self.wave * 0.15)
                self.enemies.remove(enemy)

    
        for enemy in self.enemies:
            if enemy.update(delta_time) and enemy == Boss:
                self.base_health -= 100  
                self.enemies.remove(enemy)                 
            if enemy.update(delta_time) and not enemy == Boss:
                self.base_health -= 10  
                self.enemies.remove(enemy) 
            
        if not self.enemies and self.enemies_spawned > 0:
            if (self.wave + 1) % 20 == 0:
                self.enemies.append(Boss(self.path,(5 * self.wave * round(self.wave / 4)) * self.difficulty_multiplier,self.coefficient))
            self.economy += 10 + 2 * self.wave
            self.wave += 1 
            self.max_enemies_per_wave += 0.3  
            self.enemies_spawned = 0  
            self.green_papers = self.green_papers + self.wave * self.difficulty_multiplier
            for tower in self.towers:
                if isinstance(tower, OverclockTower):
                    tower.new_wave()
            for tower in self.towers:
                if isinstance(tower, FarmTower):
                    self.economy += tower.damage

        for tower in self.towers:
            tower.shoot(self.enemies)  
            tower.update_bullets(self.enemies)
        self.last_update_time = current_time 

    def draw_grid(self):
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                color = (200, 200, 200)  
                pygame.draw.rect(self.screen, color, (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size), 1) 


    def draw_platforms(self):
        for (col, row) in self.platforms:
            pygame.draw.rect(self.screen, (0, 165, 0), (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size))  
    def draw_path(self):
        for (x, y) in self.path:
            pygame.draw.rect(self.screen, (105, 0, 0), (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))  


    def draw_info(self):
        font = pygame.font.SysFont('Arial', int(24*self.coefficient))  

        info_x = 1000 * self.coefficient
        info_items = [
        (f"Money: {self.economy}", (info_x,75*self.coefficient)),
        (f"Wave: {self.wave}", (info_x,125*self.coefficient)),
        (f"Base Health: {self.base_health}", (info_x,175*self.coefficient), (255, 0, 0)),  
        (f"Tower Type: {self.selected_tower_type}", (info_x,225*self.coefficient)),
        (f"Tower price: {self.selected_tower_price}", (info_x,275*self.coefficient)),
        (f"Enemy Health: {(40 + 5 * self.wave * round(self.wave / 2)) * self.difficulty_multiplier}", (info_x, 975*self.coefficient), (255, 0, 0)),  
        ]

        for text, position, *color in info_items:
            text_color = color[0] if color else (255, 255, 255)  
            rendered_text = font.render(text, True, text_color)
            text_rect = rendered_text.get_rect(topleft=position)
            self.screen.blit(rendered_text, text_rect)

    # Отображение характеристик выбранной башни
        if self.selected_tower:
            tower_font = pygame.font.SysFont('Arial', int(20*self.coefficient))
            tower_info_x = 1500 *self.coefficient
            tower_info_items = [
            (f"Damage: {self.selected_tower.damage}", (tower_info_x, 150*self.coefficient)),
            (f"Range: {self.selected_tower.range}", (tower_info_x,175*self.coefficient)),
            (f"Attack Speed: {self.selected_tower.attack_speed:.2f}", (tower_info_x,200*self.coefficient)),
            (f"Upgrade Cost: {self.selected_tower.upgrade_price:.2f}", (tower_info_x,225*self.coefficient)),
            (f"Level: {self.selected_tower.level}", (tower_info_x,250*self.coefficient))
            ]

            for text, position in tower_info_items:
                rendered_text = tower_font.render(text, True, (255, 255, 255))
                text_rect = rendered_text.get_rect(topleft=position)
                self.screen.blit(rendered_text, text_rect)
            self.draw_upgrade_button() 
            self.draw_demolish_button()

    def draw(self):
        self.screen.fill(self.settings.bg_color) 
        self.draw_grid()  
        self.draw_platforms()
        self.draw_path()  
        self.draw_info()
        self.draw_exit_button()
        for tower in self.towers:
            tower.draw(self.screen) 
        for enemy in self.enemies:
            enemy.draw(self.screen,self.max_health)  

        if self.base_health > 0:
            pygame.display.flip()


    def draw_defeat_screen(self):

        self.screen.fill((50, 50, 50, 128))
        font = pygame.font.SysFont('Arial', int(80 * self.coefficient))
        text = font.render("Game Over", True, (255, 0, 0))
        text_rect = text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 - 100 * self.coefficient))
        self.screen.blit(text, text_rect)

        font = pygame.font.SysFont('Arial', int(40 * self.coefficient))
        text = font.render(f"Waves passed: {self.wave}", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 - 50 * self.coefficient))
        self.screen.blit(text, text_rect)

        text = font.render(f"Money earned: {self.green_papers}", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2))
        self.screen.blit(text, text_rect)

        font = pygame.font.SysFont('Arial', int(24 * self.coefficient))
        text = font.render("Press any button to continue", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 + 100 * self.coefficient))
        self.screen.blit(text, text_rect)

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False


    def draw_upgrade_button(self):
        button_rect = pygame.Rect(1650*self.coefficient, 50*self.coefficient, 140*self.coefficient, 40*self.coefficient)
        pygame.draw.rect(self.screen, (0, 255, 0), button_rect) 
        font = pygame.font.SysFont('Arial', int(20*self.coefficient))
        text = font.render("Upgrade Tower", True, (255, 255, 255))
        text_rect = text.get_rect(center=button_rect.center)
        self.screen.blit(text, text_rect)

    def demolish_tower(self):
        if self.selected_tower:
            self.economy += self.selected_tower.price // 2
            self.towers.remove(self.selected_tower) 
            self.grid[self.selected_tower.position[1]][self.selected_tower.position[0]] = 0 
            self.selected_tower = None 

    def draw_demolish_button(self):
        button_rect = pygame.Rect(1650*self.coefficient, 100*self.coefficient, 140*self.coefficient, 40*self.coefficient)
        pygame.draw.rect(self.screen, (255, 0, 0), button_rect) 
        font = pygame.font.SysFont('Arial', int(20*self.coefficient))
        text = font.render("Demolish Tower", True, (255, 255, 255))
        text_rect = text.get_rect(center=button_rect.center)
        self.screen.blit(text, text_rect)

    def draw_exit_button(self):
        button_rect = pygame.Rect(0, 960*self.coefficient, 140*self.coefficient, 40*self.coefficient)
        pygame.draw.rect(self.screen, (185, 0, 110), button_rect)
        font = pygame.font.SysFont('Arial', int(20*self.coefficient))
        text = font.render("Surrender", True, (255, 255, 255))
        text_rect = text.get_rect(center=button_rect.center)
        self.screen.blit(text, text_rect)






    def run(self):
        settings = Settings() 
        from menu import Menu
        while True:
            self.check_events()
            self.update()
            self.draw()
            if self.base_health <= 0:
                break
        self.draw_defeat_screen()
        settings.save_game_data(self.green_papers, self.current_level, self.wave)
        print("game over")
        menu = Menu()
        menu.main_menu()
        return

