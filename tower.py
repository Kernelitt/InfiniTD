import pygame
from enemy import Boss

class Tower:
    def __init__(self, position,coefficient):
        self.coefficient = coefficient
        self.position = position
        self.size = 30 * self.coefficient # Размер квадрата
        self.damage = 20  # Начальный урон
        self.range = 200
        self.attack_speed = 2.0  # Скорость атаки
        self.level = 1  # Уровень башни
        self.upgrade_price = 18  # Стоимость улучшения
        self.last_shot_time = 0  # Время последнего выстрела
        self.price = 12
        self.color = (0, 0, 255)  # Цвет башни (синий)
        self.bullets = []  # Список пуль
        self.speed = 6
        self.price = 24
        self.font = pygame.font.Font(None, round(24* self.coefficient))  # Инициализация шрифта
        self.xp_level = 0
        self.xp = 0
        self.cell_size = round(40 *coefficient)
        self.damage_dealed = 0


    def shoot(self, enemies):
        
        for enemy in enemies:
            if self.is_in_range(enemy):
                if pygame.time.get_ticks() - self.last_shot_time > self.attack_speed:
                    if pygame.time.get_ticks() - self.last_shot_time > 1 / self.attack_speed * 1000:  # Убедитесь, что attack_speed в секундах
                        bullet = Bullet(
                    ((self.position[0] * 40 + 20)* self.coefficient, (self.position[1] * 40 + 20)* self.coefficient),  # Центр башни
                    enemy.position,
                    self.damage,self.speed,self.coefficient
                )
                        self.bullets.append(bullet)
                        self.last_shot_time = pygame.time.get_ticks()  # Обновляем время последнего выстрела
                    break  # Выход из цикла, если враг найден

    def update_bullets(self,enemies):
        # Обновляем и отрисовываем пули
        for bullet in self.bullets[:]:
            bullet.update()
            if not bullet.is_alive():  # Если пуля "умерла", удаляем её из списка
                self.bullets.remove(bullet)
                continue
        
            # Проверка столкновения с врагами
            for enemy in enemies:
                if enemy.is_alive() and self.check_collision(bullet, enemy):
                    enemy.take_damage(bullet.damage)  # Наносим урон врагу
                    self.xp += bullet.damage
                    self.damage_dealed += bullet.damage
                    self.bullets.remove(bullet)  # Удаляем пулю
                    break  # Выходим из цикла после столкновения

    def check_collision(self, bullet, enemy):
        # Создаем прямоугольник для пули
        bullet_rect = pygame.Rect(bullet.position[0] - 5, bullet.position[1] - 5, 8, 8)  # Пуля размером 10x10
    # Создаем прямоугольник для врага
        if isinstance(enemy, Boss):
            enemy_rect = pygame.Rect(enemy.position[0]-10, enemy.position[1]-10, 20, 20)  # Враг размером 40x40
        else:
            enemy_rect = pygame.Rect(enemy.position[0]-5, enemy.position[1]-5, 10,10)

        return bullet_rect.colliderect(enemy_rect)

    def draw(self, screen):
        # Отрисовка башни
        pygame.draw.rect(screen, (0, 0, 255), ((self.position[0] * 40 + 5)* self.coefficient, (self.position[1] * 40 + 5)* self.coefficient, self.size, self.size))
        level_text = self.font.render(f'{self.level}', True, (255, 255, 255))  # Белый цвет текста
        screen.blit(level_text, ((self.position[0] * 40 + 5)* self.coefficient, (self.position[1] * 40 + 5)* self.coefficient))

        # Отрисовка пуль
        for bullet in self.bullets[:]:
            bullet.draw(screen)  # Отрисовываем пули

        if self.xp >= 200 + 200*self.xp_level:
            self.xp = 0
            self.xp_level += 1
            self.damage += 1
            self.range += 1

    def is_in_range(self, enemy):
     # Преобразуем позицию башни из клеток в пиксели
        tower_pixel_x = (self.position[0] * 40 + 20)* self.coefficient  # 50 - размер клетки, 20 - смещение для центрирования
        tower_pixel_y = (self.position[1] * 40 + 20)* self.coefficient  # 50 - размер клетки, 20 - смещение для центрирования

    # Рассчитываем расстояние между башней и врагом
        distance = ((tower_pixel_x - enemy.position[0]) ** 2 + (tower_pixel_y - enemy.position[1]) ** 2) ** 0.5
        return distance <= self.range * self.coefficient


    def upgrade(self):
        self.damage += 8  # Увеличиваем урон
        self.range += 15 # Увеличиваем радиус на 5%
        self.attack_speed += 0.3  # Увеличиваем скорость атаки
        self.level += 1  # Увеличиваем уровень
        self.upgrade_price = round(self.upgrade_price * 1.5)  # Обновляем стоимость улучшения



# Новый класс для быстрой башни
class FastTower(Tower):
    def __init__(self, position,coefficient):
        super().__init__(position,coefficient)
        self.speed = 2
        self.range = 80  
        self.attack_speed = 14.0  # Большая скорострельность
        self.damage = 3  # Можно уменьшить урон, если необходимо
        self.upgrade_price = 25  # Стоимость улучшения для быстрой башни
        self.color = (255, 155, 0)  # Цвет башни (синий)
        self.price = 20
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, ((self.position[0] * 40 + 5)*self.coefficient, (self.position[1] * 40 + 5)*self.coefficient, self.size, self.size))
        level_text = self.font.render(f'{self.level}', True, (255, 255, 255))  # Белый цвет текста
        screen.blit(level_text, ((self.position[0] * 40 + 5)*self.coefficient, (self.position[1] * 40 + 5)*self.coefficient))
        for bullet in self.bullets[:]:
            bullet.draw(screen)  # Отрисовываем пули

        if self.xp >= 200 + 200*self.xp_level:
            self.xp = 0
            self.xp_level += 1
            self.damage += 0.25
            self.attack_speed += 0.05
            self.range += 2

    def upgrade(self):
        self.damage += 2  # Увеличиваем урон

        self.level += 1  # Увеличиваем уровень
        self.upgrade_price = round(self.upgrade_price * 1.5)  # Обновляем стоимость улучшения



# Новый класс для быстрой башни
class RocketTower(Tower):
    def __init__(self, position,coefficient):
        super().__init__(position,coefficient)
        self.speed = 1
        self.range = 300  
        self.attack_speed = 1.0  # Большая скорострельность
        self.damage = 20  # Можно уменьшить урон, если необходимо
        self.upgrade_price = 35  # Стоимость улучшения для быстрой башни
        self.color = (255, 155, 155)  # Цвет башни (синий)
        self.price = 43

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, ((self.position[0] * 40 + 5)*self.coefficient, (self.position[1] * 40 + 5)*self.coefficient, self.size, self.size))
        level_text = self.font.render(f'{self.level}', True, (255, 255, 255))  # Белый цвет текста
        screen.blit(level_text, ((self.position[0] * 40 + 5)*self.coefficient, (self.position[1] * 40 + 5)*self.coefficient))
        for bullet in self.bullets[:]:
            bullet.draw(screen)  # Отрисовываем пули

        if self.xp >= 200 + 200*self.xp_level:
            self.xp = 0
            self.xp_level += 1
            self.damage += 4
            self.range += 1
            if self.speed <= 3:
                self.speed += 0.05

    def upgrade(self):
        self.damage += 19  # Увеличиваем урон
        self.attack_speed += 0.1  # Увеличиваем скорость атаки
        self.level += 1  # Увеличиваем уровень
        self.upgrade_price = round(self.upgrade_price * 1.5)  # Обновляем стоимость улучшения

    def shoot(self, enemies):
        for enemy in enemies:
            if self.is_in_range(enemy):
                if pygame.time.get_ticks() - self.last_shot_time > self.attack_speed:
                    if pygame.time.get_ticks() - self.last_shot_time > 1 / self.attack_speed * 1000:  # Убедитесь, что attack_speed в секундах
                        bullet = Rocket(
                    ((self.position[0] * 40 + 20)* self.coefficient, (self.position[1] * 40 + 20)* self.coefficient),  # Центр башни
                    enemy.position,
                    self.damage,self.speed,self.coefficient
                )
                        self.bullets.append(bullet)
                        self.last_shot_time = pygame.time.get_ticks()  # Обновляем время последнего выстрела
                    break  # Выход из цикла, если враг найден



class ExplosiveTower(Tower):
    def __init__(self, position,coefficient):
        super().__init__(position,coefficient)
        self.damage = 16  # Урон взрывного снаряда
        self.range = 200  
        self.attack_speed = 1.0  # Скорость атаки
        self.explosion_radius = 40  # Радиус взрыва
        self.color = (205, 0, 70)  # Цвет башни (красный)
        self.upgrade_price = 40  # Стоимость улучшения для быстрой башни
        self.price = 36


    def shoot(self, enemies):
        for enemy in enemies:
            if self.is_in_range(enemy):
                if pygame.time.get_ticks() - self.last_shot_time > self.attack_speed:
                    if pygame.time.get_ticks() - self.last_shot_time > 1 / self.attack_speed * 1000:
                        bullet = ExplosiveBullet(
                        ((self.position[0] * 40 + 20)* self.coefficient, (self.position[1] * 40 + 20)* self.coefficient),  # Центр башни
                        enemy.position,
                        self.damage,
                        self.speed,
                        self.explosion_radius,self.coefficient
                        )
                        self.bullets.append(bullet)
                        self.last_shot_time = pygame.time.get_ticks()  # Обновляем время последнего выстрела
                break  # Выход из цикла, если враг найден

    def upgrade(self):
        self.damage += 5  # Увеличиваем урон
        self.attack_speed += 0.2  # Увеличиваем скорость атаки
        self.level += 1  # Увеличиваем уровень
        self.upgrade_price = round(self.upgrade_price * 1.5)  # Обновляем стоимость улучшения

    def update_bullets(self, enemies):
        for bullet in self.bullets[:]:
            bullet.update()
            if not bullet.is_alive():  # Если пуля "умерла", удаляем её из списка
                self.bullets.remove(bullet)
                continue
            
            # Проверка столкновения с врагами
            for enemy in enemies:
                if enemy.is_alive() and self.check_collision(bullet, enemy):
                    exploded = bullet.explode(enemies)  # Вызываем взрыв
                    self.bullets.remove(bullet)  # Удаляем пулю
                    self.xp += self.damage
                    self.damage_dealed += self.damage * exploded
                    break  # Выходим из цикла после столкновения

    def draw(self, screen):
        # Отрисовка башни
        pygame.draw.rect(screen, self.color, ((self.position[0] * 40 + 5)*self.coefficient, (self.position[1] * 40 + 5)*self.coefficient, self.size, self.size))
        level_text = self.font.render(f'{self.level}', True, (255, 255, 255))  # Белый цвет текста
        screen.blit(level_text, ((self.position[0] * 40 + 5)*self.coefficient, (self.position[1] * 40 + 5)*self.coefficient))

        if self.xp >= 200 + 200*self.xp_level:
            self.xp = 0
            self.xp_level += 1
            self.damage += 2
            self.attack_speed += 0.05
            self.range += 2
        # Отрисовка пуль
        for bullet in self.bullets[:]:
            bullet.draw(screen)  # Отрисовываем пули



class OverclockTower(Tower):
    def __init__(self, position,coefficient):
        super().__init__(position,coefficient)
        self.speed = 3
        self.range = 180  
        self.attack_speed = 1.0
        self.base_attack_speed = 2.0  # Базовая скорострельность
        self.last_shot_time = 0  # Время последнего выстрела
        self.damage = 6  # Можно уменьшить урон, если необходимо
        self.upgrade_price = 36  # Стоимость улучшения для быстрой башни
        self.color = (255, 0, 155)  # Цвет башни (синий)
        self.price = 29

    def shoot(self, enemies):

        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > 1000:  # Если прошло более 1 секунды с последнего выстрела
            self.attack_speed = self.base_attack_speed

        for enemy in enemies:
            if self.is_in_range(enemy):
                if pygame.time.get_ticks() - self.last_shot_time > self.attack_speed:
                    if pygame.time.get_ticks() - self.last_shot_time > 1 / self.attack_speed * 1000:  # Убедитесь, что attack_speed в секундах
                        if self.attack_speed < self.base_attack_speed * 4 and self.attack_speed < 40:
                            self.attack_speed = self.attack_speed + 0.2
                        bullet = Bullet(
                    ((self.position[0] * 40 + 20)* self.coefficient, (self.position[1] * 40 + 20)* self.coefficient),  # Центр башни
                    enemy.position,
                    self.damage,self.speed,self.coefficient 
                )
                        self.bullets.append(bullet)
                        self.last_shot_time = pygame.time.get_ticks()  # Обновляем время последнего выстрела
                    break  # Выход из цикла, если враг найден

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, ((self.position[0] * 40 + 5)*self.coefficient, (self.position[1] * 40 + 5)*self.coefficient, self.size, self.size))
        level_text = self.font.render(f'{self.level}', True, (255, 255, 255))  # Белый цвет текста
        screen.blit(level_text, ((self.position[0] * 40 + 5)*self.coefficient, (self.position[1] * 40 + 5)*self.coefficient))
        for bullet in self.bullets[:]:
            bullet.draw(screen)  # Отрисовываем пули
        if self.xp >= 200 + 200*self.xp_level:
            self.xp = 0
            self.xp_level += 1
            self.damage += 1
            self.range += 1

    def upgrade(self):
        self.damage += 2  # Увеличиваем урон
        self.base_attack_speed += 0.4
        self.level += 1  # Увеличиваем уровень
        self.upgrade_price = round(self.upgrade_price * 1.5)  # Обновляем стоимость улучшения

    def new_wave(self):
        self.attack_speed = self.base_attack_speed
        


    
class FarmTower(Tower):
    def __init__(self, position,coefficient):
        super().__init__(position,coefficient)
        self.range = 0
        self.attack_speed = 0
        self.damage = 25  # Можно уменьшить урон, если необходимо
        self.upgrade_price = 50  # Стоимость улучшения для быстрой башни
        self.color = (255, 255, 70)  # Цвет башни (синий)
        self.price = 70


    def upgrade(self):
        self.damage += 15  # Увеличиваем урон

        self.level += 1  # Увеличиваем уровень
        self.upgrade_price = round(self.upgrade_price * 1.5)  # Обновляем стоимость улучшения

    def shoot(self, enemies):
        pass
    def update_bullets(self,enemies):
        pass
    def draw(self, screen):
        # Отрисовка башни
        pygame.draw.rect(screen, self.color, ((self.position[0] * 40 + 5)* self.coefficient, (self.position[1] * 40 + 5)* self.coefficient, self.size, self.size))
        pygame.draw.circle(screen, (225, 225, 70), ((self.position[0] * 40 + 20)* self.coefficient, (self.position[1] * 40 + 20)* self.coefficient), self.size/2)
        level_text = self.font.render(f'{self.level}', True, (55, 55, 55))  # Белый цвет текста
        screen.blit(level_text, ((self.position[0] * 40 + 5)* self.coefficient, (self.position[1] * 40 + 5)* self.coefficient))

        if self.xp >= 200 + 200*self.xp_level:
            self.xp = 0
            self.xp_level += 1
            self.damage += 2

class Bullet:
    def __init__(self, start_position, target_position, damage,speed,coefficient):
        self.coefficient = coefficient
        self.position = list(start_position)  # Начальная позиция пули
        self.target_position = target_position  # Позиция цели
        self.speed = speed * coefficient # Скорость пули
        self.damage = damage  # Урон пули
        self.color = (255, 0, 0)  # Цвет пули (красный)
        self.alive = True  # Флаг, указывающий, жива ли пуля

        # Вычисляем направление
        direction_x = target_position[0] - start_position[0]
        direction_y = target_position[1] - start_position[1]
        length = (direction_x ** 2 + direction_y ** 2) ** 0.5
        self.direction = (direction_x / length, direction_y / length) if length != 0 else (0, 0)


    def update(self):
        # Обновляем позицию пули
        self.position[0] += self.direction[0] * self.speed
        self.position[1] += self.direction[1] * self.speed

        # Проверка, вышла ли пуля за пределы экрана
        if (self.position[0] < 0 or self.position[0] > 1800* self.coefficient or
            self.position[1] < 0 or self.position[1] > 1000* self.coefficient):
            self.alive = False  # Устанавливаем alive в False, если пуля вышла за пределы экрана

    def draw(self, screen):
        # Отрисовка пули
        pygame.draw.circle(screen, self.color, (int(self.position[0]), int(self.position[1])), 5* self.coefficient)

    def is_alive(self):
        return self.alive

class Rocket(Bullet):
    def __init__(self, start_position, target_position, damage,speed,coefficient):
        self.coefficient = coefficient
        self.position = list(start_position)  # Начальная позиция пули
        self.target_position = target_position  # Позиция цели
        self.speed = speed * coefficient   # Скорость пули
        self.damage = damage  # Урон пули
        self.color = (255,255, 0)  # Цвет пули (красный)
        self.alive = True  # Флаг, указывающий, жива ли пуля

        # Вычисляем направление
        direction_x = target_position[0] - start_position[0]
        direction_y = target_position[1] - start_position[1]
        length = (direction_x ** 2 + direction_y ** 2) ** 0.5
        self.direction = (direction_x / length, direction_y / length) if length != 0 else (0, 0)

    def draw(self, screen):
        # Отрисовка пули
        pygame.draw.circle(screen, self.color, (int(self.position[0]), int(self.position[1])), 10* self.coefficient)

class ExplosiveBullet(Bullet):
    def __init__(self, start_position, target_position, damage, speed, explosion_radius,coefficient):
        super().__init__(start_position, target_position, damage, speed,coefficient)
        self.explosion_radius = explosion_radius  # Радиус взрыва
        self.alive = True  # Флаг, указывающий, жива ли пуля

    def update(self):
        super().update()
        # Если снаряд вышел за пределы экрана, он "умирает"
        if not self.is_alive():
            self.alive = False

    def explode(self, enemies):
        total_enemies = 0
        for enemy in enemies:
            distance = ((self.position[0] - enemy.position[0]) ** 2 + (self.position[1] - enemy.position[1]) ** 2) ** 0.5
            if distance <= self.explosion_radius:
                enemy.take_damage(self.damage)  # Наносим урон врагу
                total_enemies += 1
        return total_enemies

