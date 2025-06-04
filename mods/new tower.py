import pygame

from tower import Tower # Импортируем базовый класс Tower

class SniperTower(Tower):
    def __init__(self, position, coefficient):
        super().__init__(position, coefficient)
        self.damage = 60  # Высокий урон
        self.attack_speed = 0.4  # Медленная скорость атаки
        self.range = 400  # Увеличенный радиус атаки
        self.price = 54  # Стоимость снайперской башни
        self.color = (5, 100, 0)  # Красный цвет для визуализации
        self.speed = 9
        self.upgrade_price = 38  # Стоимость улучшения

    def draw(self, screen):
        # Отрисовка башни
        pygame.draw.rect(screen, (0, 200, 2), ((self.position[0] * 40 + 5)* self.coefficient, (self.position[1] * 40 + 5)* self.coefficient, self.size, self.size))
        level_text = self.font.render(f'{self.level}', True, (255, 255, 255))  # Белый цвет текста
        screen.blit(level_text, ((self.position[0] * 40 + 5)* self.coefficient, (self.position[1] * 40 + 5)* self.coefficient))

        # Отрисовка пуль
        for bullet in self.bullets[:]:
            bullet.draw(screen)  # Отрисовываем пули

        if self.xp >= 200 + 200*self.xp_level:
            self.xp = 0
            self.xp_level += 1
            self.damage += 4
 
    def upgrade(self):
        self.damage += 12  # Увеличиваем урон
        self.attack_speed += 0.05 # Увеличиваем скорость атаки
        self.level += 1  # Увеличиваем уровень
        self.upgrade_price = round(self.upgrade_price * 1.5)  # Обновляем стоимость улучшения

def get_info(self):
    return ("Sniper Tower Mod",
            "Adding a powerful Sniper Tower with high damage and range.")


def run(game):
    game.tower_types[pygame.K_7] = ('Sniper', SniperTower((0, 0), game.coefficient).price)
    game.tower_classes['Sniper'] = (SniperTower)

def update(game):
    # Эта функция может использоваться для логики, которую нужно обновлять каждый кадр
    pass


def wave_cleared(game):
    pass



