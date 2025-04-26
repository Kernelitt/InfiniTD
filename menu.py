import pygame
from os.path import basename
import sys
from cryptography.fernet import Fernet
from tkinter import filedialog
from settings import Settings
from pygame_stuff import Button, RotatingSquare

class Menu:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 1800, 1000
        self.resolution = Settings.read_screen_resolution()
        self.coefficient = (self.resolution[0] + self.resolution[1]) / (self.WIDTH + self.HEIGHT)
        self.screen = pygame.display.set_mode((self.WIDTH * self.coefficient, self.HEIGHT * self.coefficient))
        pygame.display.set_caption("InfiniTD")

        self.WHITE = (25, 25, 25)
        self.BLACK = (255, 255, 255)
        self.GREEN = (0, 205, 0)
        self.RED = (255, 0, 0)

        self.font = pygame.font.Font(None, int(54 * self.coefficient))
        self.font_small = pygame.font.Font(None, int(36 * self.coefficient))

        self.wave = 0
        self.curl = 0
        self.menu_active = True
        self.level_select = False
        self.upgrades_menu = False
        self.current_level = 1

        self.settings = Settings()
        self.custom_level_var = False
        self.custom_level = ""

        self.green_papers = self.settings.load_data()["Money"]

        pygame.mixer.music.load("music\Seablue - Aurora Dawn.mp3")
        pygame.mixer.music.play(-1)

        self.squares = []
        self.squares.append(RotatingSquare(self.screen, 0, 0, 80, (0, 0, 255), 0))
        self.squares.append(RotatingSquare(self.screen, 0, 0, 80, (255, 155, 0), 72))
        self.squares.append(RotatingSquare(self.screen, 0, 0, 80, (255, 0, 155), 144))
        self.squares.append(RotatingSquare(self.screen, 0, 0, 80, (255, 155, 155), 216))
        self.squares.append(RotatingSquare(self.screen, 0, 0, 80, (205, 0, 70), 288))

        self.level_buttons = []
        self.menu_buttons = []
        self.upgrades_buttons = []

        self.bossrush = False

        self.menu_buttons.append(Button(1300*self.coefficient, 800*self.coefficient, 300*self.coefficient, 50*self.coefficient, [("Play", (10, 10))], lambda:self.level_menu(), (0, 200, 0)))
        self.menu_buttons.append(Button(1300*self.coefficient, 860*self.coefficient, 300*self.coefficient, 50*self.coefficient, [("Upgrades", (10, 6))], lambda: self.menu_upgrade(), (0, 200, 0)))

        self.upgrades_buttons.append(Button(20*self.coefficient, 900*self.coefficient, 150*self.coefficient, 50*self.coefficient, [("Back", (10, 10))], self.menu_upgrade, (200, 0, 0)))
        self.upgrades_buttons.append(Button(50*self.coefficient, 150*self.coefficient, 350 * self.coefficient, 90 * self.coefficient, 
                    [("Upgrade Start Money", (2, 4)), ("in total:", (250, 30)), ("price:", (10, 30)), 
                    (str(self.settings.load_data()["UpgradesCost"]["StartMoney"]), (10, 55)), (str(self.settings.load_data()["Upgrades"]["StartMoney"]), (250, 55))], 
                    lambda: self.upgrade_anything("StartMoney"), (0, 200, 0)))
        self.upgrades_buttons.append(Button(600*self.coefficient, 150*self.coefficient, 350 * self.coefficient, 90 * self.coefficient, 
                    [("Upgrade Start XP Level", (2, 4)), ("in total:", (250, 30)), ("price:", (10, 30)), 
                    (str(self.settings.load_data()["UpgradesCost"]["StartXPLevel"]), (10, 55)), (str(self.settings.load_data()["Upgrades"]["StartXPLevel"]), (250, 55))], 
                    lambda: self.upgrade_anything("StartXPLevel"), (0, 200, 0)))
         
        for i in range(1, 11):
            self.level_buttons.append(Button(20 * self.coefficient, 0 + i * 50 * self.coefficient - 30, 170 * self.coefficient, 45 * self.coefficient, [("Level " + str(i), (10, 10))], lambda i=i: self.set_current_level(i), (0, 200, 0)))
        self.level_buttons.append(Button(20 * self.coefficient, 800 * self.coefficient, 300 * self.coefficient, 50 * self.coefficient, [("Custom level", (10, 10))], lambda: self.set_custom_lvl(), (0, 200, 0)))
 
        self.level_buttons.append(Button(20*self.coefficient, 900*self.coefficient, 150*self.coefficient, 50*self.coefficient, [("Back", (10, 10))], self.level_menu, (0, 200, 0)))

        self.level_buttons.append(Button(1300*self.coefficient, 800*self.coefficient, 300*self.coefficient, 50*self.coefficient, [("Start Level", (10, 10))], self.start_game, (0, 200, 0)))
        self.level_buttons.append(Button(1300*self.coefficient, 860*self.coefficient, 350*self.coefficient, 50*self.coefficient, [("Boss Rush "+str(self.bossrush), (10, 10))], lambda:self.change_bossrush(), (0, 200, 0)))


    def update_upgrade_buttons(self):
        self.upgrades_buttons.clear()
        self.upgrades_buttons.append(Button(20 * self.coefficient, 900 * self.coefficient, 150 * self.coefficient, 50 * self.coefficient, 
                                            [("Back", (10, 10))], self.menu_upgrade, (200, 0, 0)))
        self.upgrades_buttons.append(Button(50 * self.coefficient, 150 * self.coefficient, 350 * self.coefficient, 90 * self.coefficient, 
                                            [("Upgrade Start Money", (2, 4)), ("in total:", (250, 30)), ("price:", (10, 30)), 
                                            (str(self.settings.load_data()["UpgradesCost"]["StartMoney"]), (10, 55)), 
                                            (str(self.settings.load_data()["Upgrades"]["StartMoney"]), (250, 55))], 
                                            lambda: self.upgrade_anything("StartMoney"), (0, 200, 0)))
        self.upgrades_buttons.append(Button(600 * self.coefficient, 150 * self.coefficient, 350 * self.coefficient, 90 * self.coefficient, 
                                            [("Upgrade Start XP Level", (2, 4)), ("in total:", (250, 30)), ("price:", (10, 30)), 
                                            (str(self.settings.load_data()["UpgradesCost"]["StartXPLevel"]), (10, 55)), 
                                            (str(self.settings.load_data()["Upgrades"]["StartXPLevel"]), (250, 55))], 
                                            lambda: self.upgrade_anything("StartXPLevel"), (0, 200, 0)))


    def set_custom_lvl(self):
        self.custom_level = filedialog.askopenfilename()
        if self.custom_level != None: 
            self.custom_level_var = True

    def level_menu(self):
        if self.level_select == False:
            self.menu_active = False
            self.level_select = True
        else:
            self.menu_active = True
            self.level_select = False

    def menu_upgrade(self):
        if self.upgrades_menu == False:
            self.menu_active = False
            self.upgrades_menu = True 
        else:
            self.menu_active = True
            self.upgrades_menu = False

    def get_waves_for_level(self,level):
        data = self.settings.load_data()  
        if "Levels" in data:    
            if self.custom_level_var == True:
                waves = data["Levels"].get(str(level), 0)  # Возвращаем 0, если уровень не найден
            else:
                waves = data["Levels"].get("levels\lvl"+str(level)+".json", 0)  # Возвращаем
        else:
            waves = 0
        return waves

    def upgrade_anything(self, upgrade_str):
        upgrade = self.settings.load_data()["Upgrades"].get(upgrade_str)
        upgrade_cost = self.settings.load_data()["UpgradesCost"].get(upgrade_str)
        if self.green_papers >= upgrade_cost:
            self.green_papers -= upgrade_cost
            upgrade =  upgrade + self.settings.load_data()["UpgradesPower"].get(upgrade_str)
            upgrade_cost = round(upgrade_cost * 2.42)
            self.settings.save_data({"Money": self.green_papers, "Upgrades":{upgrade_str: upgrade}, "UpgradesCost":{upgrade_str: upgrade_cost}})
            self.update_upgrade_buttons()

        
    def change_bossrush(self):
        if self.bossrush == True:
            self.bossrush = False
        else:
            self.bossrush = True
        self.level_buttons.pop()
        self.level_buttons.append(Button(1300*self.coefficient, 860*self.coefficient, 350*self.coefficient, 50*self.coefficient, [("Boss Rush "+str(self.bossrush), (10, 10))], lambda:self.change_bossrush(), (0, 200, 0)))


    def main_menu(self):
        self.menu_active = True
        wave = self.get_waves_for_level(self.current_level)
        self.green_papers = self.settings.load_data()["Money"]
        while True:
            while self.menu_active:



                self.screen.fill(self.WHITE)


                title_surface = self.font.render("Main Menu", True, self.BLACK)
                self.screen.blit(title_surface, (self.resolution[0] // 2 - title_surface.get_width() // 2, 50*self.coefficient))


                for i in self.squares:
                    i.draw()
                for button in self.menu_buttons:
                    button.draw(self.screen, self.font)

                self.screen.blit(self.font.render("Money "+str(self.green_papers), True, (255, 255, 255)), (1500*self.coefficient, 50*self.coefficient))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    for button in self.menu_buttons:
                        button.check_click(event)

                pygame.display.flip()

            while self.upgrades_menu:
                self.screen.fill(self.WHITE)


                title_surface = self.font.render("Improvements", True, self.BLACK)
                self.screen.blit(self.font.render("Money "+str(self.green_papers), True, (255, 255, 255)), (1500*self.coefficient, 50*self.coefficient))

                self.screen.blit(title_surface, (self.resolution[0] // 2 - title_surface.get_width() // 2, 50*self.coefficient))


                for button in self.upgrades_buttons:
                    button.draw(self.screen, self.font_small)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    for button in self.upgrades_buttons:
                        button.check_click(event)

                pygame.display.flip()

            while self.level_select:
                self.screen.fill(self.WHITE)


                wave = self.get_waves_for_level(self.current_level)

                text = self.font.render("Wave Record "+str(wave), True, (255, 255, 255))
                text_rect = text.get_rect(topleft=(1300*self.coefficient, 700*self.coefficient))
                self.screen.blit(text, text_rect)

                if self.custom_level_var:
                    filename = basename(self.custom_level) 
                    text = self.font.render("Level "+filename, True, (255, 255, 255))
                else:
                    text = self.font.render("Level "+str(self.current_level), True, (255, 255, 255))          
                text_rect = text.get_rect(topleft=(1300*self.coefficient, 600*self.coefficient))
                self.screen.blit(text, text_rect)

                for button in self.level_buttons:
                    button.draw(self.screen, self.font)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    for button in self.level_buttons:
                        button.check_click(event)

                pygame.display.flip()

    def start_game(self):
        from main import Game

        self.menu_active = False  # Скрываем меню
        self.level_select = False  # Скрываем меню
        if self.custom_level_var == False:
            game = Game(self.settings, self.screen, "levels\lvl"+str(self.current_level)+".json",self.coefficient,self.bossrush)  # Создаем экземпляр игры с текущим уровнем и экраном
        else:
            game = Game(self.settings, self.screen, self.custom_level,self.coefficient,self.bossrush)  #
        game.run()  # Запускаем игровой цикл

        self.main_menu()

    def set_current_level(self,level):
        self.current_level = level
        self.custom_level_var = False
    
if __name__ == "__main__":
    menu = Menu()
    menu.main_menu()