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
    def __init__(self, settings, screen,current_level,coefficient,bossrush,music_volume):
        # Basic
        self.current_level = current_level
        self.settings = settings
        self.screen = screen
        self.coefficient = coefficient
        # Grid
        self.grid_width = self.grid_height = 24
        self.grid = [[0 for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        self.cell_size = round(40 *coefficient)

        self.load_map(current_level)

        self.bossrush = bossrush
        self.alpha_surface = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        self.last_update_time = pygame.time.get_ticks()  
        self.clock = pygame.time.Clock()
        # Wave
        self.wave = 0
        self.wave_started = False
        self.auto_start = False

        # Enemies
        self.enemies = []
        self.enemy_spawn_time = 0
        self.enemy_spawn_interval = 100
        self.enemy_spawn_intervals = [200,280,380,200,500,600,300,800]
        self.max_enemies_per_wave = 5
        self.enemies_spawned = 0
        self.enemy_count = 0
        self.group_num = 0
        self.enemy_type = 'Basic'
        # Towers
        self.towers = []
        self.selected_tower = None
        self.selected_tower_type = 'Basic'
        self.selected_tower_price = 24
        # Upgrades
        self.base_health = 20 + self.settings.load_data()["Upgrades"]["StartBaseHP"]
        self.economy = 50 + self.settings.load_data()["Upgrades"]["StartMoney"]

        self.green_papers = 0

        if self.bossrush == True:
            pygame.mixer.music.load("music/4mat - Blank Page.mp3")
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(music_volume)


        self.run_plugins()

    def load_map(self, file_path):
        with open(file_path, 'r') as file:
            map_data = json.load(file)
        self.path = [(p[0], p[1]) for p in map_data['paths']]
        self.platforms = [(p[0], p[1]) for p in map_data['platforms']]
        self.difficulty_multiplier = map_data['difficulty_multiplier']
        try:
            self.custom_waves = map_data['waves']
        except:
            self.custom_waves = []
        self.spawn_position = self.path[0]  


    def run_plugins(self):
        for plugin in self.settings.plugins:
            if hasattr(plugin, 'run'):
                plugin.run(self) 

    def update_plugins(self):
        for plugin in self.settings.plugins:
            if hasattr(plugin, 'update'):
                plugin.update(self)  

    def wave_cleared_plugins(self):
        for plugin in self.settings.plugins:
            if hasattr(plugin, 'wave_cleared'):
                plugin.wave_cleared(self)  

    def handle_tower_click(self, grid_x, grid_y):
        tower = self.get_tower_at(grid_x, grid_y)
        if tower:
            self.selected_tower = tower
        self.alpha_surface.fill((0, 0, 0, 0))  # Fill with transparent black
        self.screen.blit(self.alpha_surface, (0, 0))


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

                    if (1650*self.coefficient <= mouse_x <= 1790*self.coefficient and 50*self.coefficient <= mouse_y <= 90*self.coefficient):
                        if self.selected_tower and self.economy >= self.selected_tower.upgrade_price: # Upgrade Tower
                            self.economy -= self.selected_tower.upgrade_price 
                            self.selected_tower.upgrade()  

                    if (1650*self.coefficient <= mouse_x <= 1790*self.coefficient and 100*self.coefficient <= mouse_y <= 140*self.coefficient):
                        if self.selected_tower: # Destroy Tower
                            self.economy += self.selected_tower.price // 2
                            self.towers.remove(self.selected_tower) 
                            self.grid[self.selected_tower.position[1]][self.selected_tower.position[0]] = 0 
                            self.selected_tower = None 

                    if (0 <= mouse_x <= 140*self.coefficient and 960*self.coefficient <= mouse_y <= 1000*self.coefficient):
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
                if event.key == pygame.K_SPACE:
                    if self.wave % 20 == 0 and self.wave_started == False:
                        self.enemies.append(Boss(self.path,(5 * self.wave * round(self.wave / 4)) * self.difficulty_multiplier,self.coefficient))
                    self.wave_started = True
                if event.key == pygame.K_r:
                    self.auto_start = True


    def handle_click(self, grid_x, grid_y):
        if (grid_x, grid_y) in self.platforms: 
            if self.grid[grid_y][grid_x] == 0: 
                tower_class = None
                
                if self.selected_tower_type == 'Basic':
                    tower_class = Tower
                elif self.selected_tower_type == 'Fast':
                    tower_class = FastTower
                elif self.selected_tower_type == 'Rocket':
                    tower_class = RocketTower
                elif self.selected_tower_type == 'Explosive':
                    tower_class = ExplosiveTower
                elif self.selected_tower_type == 'Overclock':
                    tower_class = OverclockTower
                elif self.selected_tower_type == 'Farm':
                    tower_class = FarmTower
                
                if tower_class is not None:
                    tower = tower_class((grid_x, grid_y), self.coefficient)
                    if self.economy >= tower.price: 
                        self.towers.append(tower)  # Добавляем башню в список
                        self.grid[grid_y][grid_x] = 1  # Обновляем сетку
                        self.economy -= tower.price  # Уменьшаем экономику
                        for i in range(self.settings.load_data()["Upgrades"]["StartXPLevel"]):
                            self.towers[len(self.towers)-1].xp += 999990
                            self.towers[len(self.towers)-1].draw(self.screen)
            else:
                self.handle_tower_click(grid_x, grid_y)
        else:
            self.selected_tower = None

    def spawn_enemy(self):
        self.enemy_types = [Basic, Fast, Strong,Boss]  
        self.max_health = (40 + 5 * self.wave * round(self.wave / 4)) * self.difficulty_multiplier
        health = (40 + 5 * self.wave * round(self.wave / 4)) * self.difficulty_multiplier
        if self.bossrush == False:
            if self.wave < len(self.custom_waves):
                wave_data = self.custom_waves[self.wave]
                if self.group_num < len(wave_data): 
                    group_data = wave_data[self.group_num]

                    if self.enemies_spawned == self.enemy_count:
                        self.enemy_type = self.enemy_types[int(group_data[0]) - 1]
                        self.enemy_count = int(group_data[1])
                        self.enemy_spawn_interval = int(group_data[2])
                        self.enemies_spawned = 0  
                        self.group_num += 1  
                    else:                       
                        self.enemies.append(self.enemy_type(self.path, health, self.coefficient))
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
                            if isinstance(tower, FarmTower):
                                self.economy += tower.damage
            else:
                self.enemy_spawn_interval = self.enemy_spawn_intervals[self.wave % len(self.enemy_spawn_intervals)] 
                if self.enemies_spawned < self.max_enemies_per_wave:                 
                    self.enemies.append(self.enemy_types[self.wave % len([Basic, Fast, Strong])](self.path, health, self.coefficient))
                    self.enemies_spawned += 1 
        else:
            if self.enemies_spawned < 1:
                self.enemies.append(Boss(self.path, health, self.coefficient))
                self.enemies_spawned += 1 

    def update(self):
        current_time = pygame.time.get_ticks()
        delta_time = (current_time - self.last_update_time) / 1000.0

        if current_time - self.enemy_spawn_time > self.enemy_spawn_interval and self.wave_started:
            self.spawn_enemy()
            self.enemy_spawn_time = current_time


        for enemy in self.enemies:
            if enemy.is_alive() == False:
                if isinstance(enemy, Boss):
                    self.economy += 25 + 25 * round(self.wave * 0.15)
                else:
                    self.economy += 1 + 1 * round(self.wave * 0.15)
                self.enemies.remove(enemy)

            if enemy.update(delta_time) and isinstance(enemy, Boss):
                self.base_health = 0
                self.enemies.remove(enemy)                 
            if enemy.update(delta_time) and not isinstance(enemy, Boss):
                self.base_health -= 1
                self.enemies.remove(enemy) 
            
        if not self.enemies and self.enemies_spawned >= self.max_enemies_per_wave: #Wave Cleared

            self.economy += 10 + 2 * self.wave
            self.wave += 1 
            self.max_enemies_per_wave += 0.3  
            self.enemies_spawned = 0  

            if self.bossrush:
                self.green_papers = self.green_papers + self.wave * self.difficulty_multiplier * 3
            else:
                self.green_papers = self.green_papers + self.wave * self.difficulty_multiplier

            for tower in self.towers:
                if isinstance(tower, OverclockTower):
                    tower.new_wave()
                if isinstance(tower, FarmTower):
                    self.economy += tower.damage
            self.wave_cleared_plugins()

            if self.auto_start == False:
                self.wave_started = False
            else:
                if self.wave % 20 == 0:
                    self.enemies.append(Boss(self.path,(5 * self.wave * round(self.wave / 4)) * self.difficulty_multiplier,self.coefficient))
        for tower in self.towers:
            tower.shoot(self.enemies)  
            tower.update_bullets(self.enemies)
        self.last_update_time = current_time 

    def draw_grid(self):
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                color = (200, 200, 200)  
                pygame.draw.rect(self.screen, color, (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size), 1) 
        for (col, row) in self.platforms:
            pygame.draw.rect(self.screen, (0, 165, 0), (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size))  
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

        self.fps = self.clock.get_fps()
        self.fps_text = f"FPS: {round(self.fps,1)}"
        text_surface = font.render(self.fps_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (1650*self.coefficient,970*self.coefficient))

        if self.wave_started == False:           
            self.screen.blit(font.render(f"Press 'Space' to start a new wave", True, (255, 255, 255)), (1200*self.coefficient,670*self.coefficient))

        if self.selected_tower:
            tower_font = pygame.font.SysFont('Arial', int(20 * self.coefficient))
            tower_info_x = 1500 * self.coefficient

            # Подготовка текстов
            tower_info_items = [
                (f"Damage Dealed: {self.selected_tower.damage_dealed}", (1200 * self.coefficient, 20 * self.coefficient)),
                (f"Damage: {self.selected_tower.damage}", (tower_info_x, 150 * self.coefficient)),
                (f"Range: {self.selected_tower.range}", (tower_info_x, 175 * self.coefficient)),
                (f"Attack Speed: {self.selected_tower.attack_speed:.2f}", (tower_info_x, 200 * self.coefficient)),
                (f"Upgrade Cost: {self.selected_tower.upgrade_price:.2f}", (tower_info_x, 225 * self.coefficient)),
                (f"Level: {self.selected_tower.level}", (tower_info_x, 250 * self.coefficient))
            ]

            # Отрисовка текста
            rendered_texts = [tower_font.render(text, True, (255, 255, 255)) for text, _ in tower_info_items]
            for rendered_text, (_, position) in zip(rendered_texts, tower_info_items):
                text_rect = rendered_text.get_rect(topleft=position)
                self.screen.blit(rendered_text, text_rect)

            button_rect = pygame.Rect(1650*self.coefficient, 50*self.coefficient, 140*self.coefficient, 40*self.coefficient)
            pygame.draw.rect(self.screen, (0, 255, 0), button_rect) 
            text = tower_font.render("Upgrade Tower", True, (255, 255, 255)) 
            self.screen.blit(text, text.get_rect(center=button_rect.center))

            button_rect = pygame.Rect(1650*self.coefficient, 100*self.coefficient, 140*self.coefficient, 40*self.coefficient)
            pygame.draw.rect(self.screen, (255, 0, 0), button_rect) 
            text = tower_font.render("Demolish Tower", True, (255, 255, 255))
            self.screen.blit(text, text.get_rect(center=button_rect.center))

            circle_position = (self.selected_tower.position[0] * self.cell_size + (20 * self.coefficient),
                            self.selected_tower.position[1] * self.cell_size + (20 * self.coefficient))
            pygame.draw.circle(self.alpha_surface, (0, 255, 0, 70), circle_position, self.selected_tower.range * self.coefficient)  
            self.screen.blit(self.alpha_surface, (0, 0))

            xp_bar_length = 250 * self.coefficient
            xp_ratio = self.selected_tower.xp / (200 + 200 * self.selected_tower.xp_level)
            xp_bar_width = xp_bar_length * xp_ratio 

            pygame.draw.rect(self.screen, (85, 85, 85), (1500 * self.coefficient - xp_bar_length / 2, 100 * self.coefficient - 20, xp_bar_length, 15 * self.coefficient))  
            pygame.draw.rect(self.screen, (255, 255, 0), (1500 * self.coefficient - xp_bar_length / 2, 100 * self.coefficient - 20, xp_bar_width, 12 * self.coefficient)) 

            xp_text = f"{self.selected_tower.xp} / {200 + 200 * self.selected_tower.xp_level} Xp Level {self.selected_tower.xp_level}"
            text_surface = tower_font.render(xp_text, True, (255, 255, 255))
            self.screen.blit(text_surface, (1400 * self.coefficient, 50 * self.coefficient))


    def draw(self):
        self.screen.fill(self.settings.bg_color) 
        self.draw_grid()  
        self.draw_info()
        
        button_rect = pygame.Rect(0, 960*self.coefficient, 140*self.coefficient, 40*self.coefficient)
        pygame.draw.rect(self.screen, (185, 0, 110), button_rect)
        font = pygame.font.SysFont('Arial', int(20*self.coefficient))
        text = font.render("Surrender", True, (255, 255, 255))
        self.screen.blit(text, text.get_rect(center=button_rect.center))
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

    def run(self):
        settings = Settings() 

        while True:
            self.clock.tick(120)
            self.check_events()
            self.update()
            self.draw()
            self.update_plugins()
            if self.base_health <= 0:
                break
        self.draw_defeat_screen()
        settings.save_game_data(self.green_papers, self.current_level, self.wave)
        print("game over")

        return

