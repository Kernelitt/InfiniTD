import pygame


class Basic:
    def __init__(self, path, health,coefficient):
        self.coefficient = coefficient
        self.path = path
        self.speed = 40 * self.coefficient
        self.health = health  # Начальное здоровье врага
        self.position = ((path[0][0] * 40 + 20)*coefficient, (path[0][1] * 40 + 20)*coefficient)  # Центр первой клетки
        self.current_path_index = 0  # Индекс текущей точки пути

    def update(self, delta_time):
        if self.current_path_index < len(self.path):
            target = self.path[self.current_path_index]
            target_position = ((target[0] * 40 + 20)*self.coefficient, (target[1] * 40 + 20)*self.coefficient)

            direction = (
                target_position[0] - self.position[0],
                target_position[1] - self.position[1]
            )
            distance = (direction[0] ** 2 + direction[1] ** 2) ** 0.5

            if distance > 0:
                direction = (direction[0] / distance, direction[1] / distance)
                self.position = (
                    self.position[0] + direction[0] * self.speed * delta_time,
                    self.position[1] + direction[1] * self.speed * delta_time
                )

            if distance < self.speed * delta_time:
                self.current_path_index += 1  # Переходим к следующей точке пути

        # Проверяем, достигли ли мы конца пути
        return self.current_path_index >= len(self.path)

    def take_damage(self, amount):
        self.health -= amount  # Уменьшаем здоровье
        return self.health <= 0  # Возвращаем True, если враг мертв

    def is_alive(self):
        return self.health > 0  # Проверяем, жив ли враг

    def draw(self, screen,max_health):
        # Рисуем врага как круг
        pygame.draw.circle(screen, (0, 255, 0), (int(self.position[0]), int(self.position[1])), 8* self.coefficient)  # Красный круг
        pygame.draw.circle(screen, (0, 155, 0), (int(self.position[0]), int(self.position[1])), 6* self.coefficient)  # Красный круг
        

# Отображаем здоровье врага
        health_bar_length = 30 * self.coefficient
        health_ratio = self.health / max_health  # Рассчитываем процент оставшегося здоровья
        health_bar_width = health_bar_length * health_ratio  # Длина полоски здоровья

# Ограничиваем ширину полоски здоровья, чтобы она не превышала максимальную длину
        health_bar_width = max(0, health_bar_width)  # Убедитесь, что ширина не отрицательная

    # Отрисовка фона полоски здоровья
        pygame.draw.rect(screen, (25, 25, 25), (self.position[0] - health_bar_length / 2, self.position[1] - 20, health_bar_length, 7* self.coefficient))  # Фоновая полоса здоровья
    # Отрисовка зеленой полоски здоровья
        pygame.draw.rect(screen, (0, 255, 0), (self.position[0] - health_bar_length / 2, self.position[1] - 20, health_bar_width, 5* self.coefficient))  # Зеленая полоса здоровья

class Fast(Basic):
    def __init__(self, path, health,coefficient):
        self.coefficient = coefficient        
        self.path = path
        self.speed = 70* self.coefficient
        self.health = round(health / 1.8) # Начальное здоровье врага
        self.current_path_index = 0  # Индекс текущей точки пути
        self.position = ((path[0][0] * 40 + 20)*coefficient, (path[0][1] * 40 + 20)*coefficient)  # Центр первой клетки

    def draw(self, screen,max_health):
        # Рисуем врага как круг

        pygame.draw.circle(screen, (255, 255, 0), (int(self.position[0]), int(self.position[1])), 8* self.coefficient)  # Красный круг
        pygame.draw.circle(screen, (155, 155, 0), (int(self.position[0]), int(self.position[1])), 6* self.coefficient)  # Красный круг
        

# Отображаем здоровье врага
        health_bar_length = 30 * self.coefficient
        health_ratio = self.health / max_health * 1.8 # Рассчитываем процент оставшегося здоровья
        health_bar_width = health_bar_length * health_ratio  # Длина полоски здоровья

# Ограничиваем ширину полоски здоровья, чтобы она не превышала максимальную длину
        health_bar_width = max(0, health_bar_width)  # Убедитесь, что ширина не отрицательная

    # Отрисовка фона полоски здоровья
        pygame.draw.rect(screen, (25, 25, 25), (self.position[0] - health_bar_length / 2, self.position[1] - 20, health_bar_length, 7* self.coefficient))  # Фоновая полоса здоровья
    # Отрисовка зеленой полоски здоровья
        pygame.draw.rect(screen, (0, 255, 0), (self.position[0] - health_bar_length / 2, self.position[1] - 20, health_bar_width, 5* self.coefficient))  # Зеленая полоса здоровья

class Strong(Basic):
    def __init__(self, path, health,coefficient):
        self.coefficient = coefficient
        self.path = path
        self.speed = 30* self.coefficient
        self.health = round(health * 1.5) # Начальное здоровье врага
        self.current_path_index = 0  # Индекс текущей точки пути
        self.position = ((path[0][0] * 40 + 20)*coefficient, (path[0][1] * 40 + 20)*coefficient)  # Центр первой клетки

    def draw(self, screen,max_health):
        # Рисуем врага как круг
        pygame.draw.rect(screen, (155, 0, 0), (int(self.position[0]), int(self.position[1]), 14* self.coefficient,14* self.coefficient))  # Красный круг
        pygame.draw.rect(screen, (255, 0, 0), (int(self.position[0]), int(self.position[1]), 12* self.coefficient,12* self.coefficient))  # Красный круг
        
        

# Отображаем здоровье врага
        health_bar_length = 30* self.coefficient
        health_ratio = self.health / max_health / 1.5  # Рассчитываем процент оставшегося здоровья
        health_bar_width = health_bar_length * health_ratio  # Длина полоски здоровья

# Ограничиваем ширину полоски здоровья, чтобы она не превышала максимальную длину
        health_bar_width = max(0, health_bar_width)  # Убедитесь, что ширина не отрицательная

    # Отрисовка фона полоски здоровья
        pygame.draw.rect(screen, (25, 25, 25), (self.position[0] - health_bar_length / 2, self.position[1] - 20, health_bar_length, 7* self.coefficient))  # Фоновая полоса здоровья
    # Отрисовка зеленой полоски здоровья
        pygame.draw.rect(screen, (0, 255, 0), (self.position[0] - health_bar_length / 2, self.position[1] - 20, health_bar_width, 5* self.coefficient))  # Зеленая полоса здоровья

class Boss(Basic):
    def __init__(self, path, health,coefficient):
        self.coefficient = coefficient        
        self.path = path
        self.speed = 5* self.coefficient
        self.health = round(health * 100) # Начальное здоровье врага
        self.current_path_index = 0  # Индекс текущей точки пути
        self.position = ((path[0][0] * 40 + 20)*coefficient, (path[0][1] * 40 + 20)*coefficient)  # Центр первой клетки
        self.bonus_enemies = []
    def draw(self, screen,max_health):
        # Рисуем врага как круг

        pygame.draw.circle(screen, (255, 255, 155), (int(self.position[0]), int(self.position[1])), 15* self.coefficient)  # Красный круг
        pygame.draw.circle(screen, (155, 155, 100), (int(self.position[0]), int(self.position[1])), 9* self.coefficient)  # Красный круг
        

# Отображаем здоровье врага
        health_bar_length = 120 * self.coefficient
        health_ratio = self.health / max_health / 100 # Рассчитываем процент оставшегося здоровья
        health_bar_width = health_bar_length * health_ratio  # Длина полоски здоровья

# Ограничиваем ширину полоски здоровья, чтобы она не превышала максимальную длину
        health_bar_width = max(0, health_bar_width)  # Убедитесь, что ширина не отрицательная

    # Отрисовка фона полоски здоровья
        pygame.draw.rect(screen, (75, 75, 75), (self.position[0] - health_bar_length / 2, self.position[1] - 62, health_bar_length, 15* self.coefficient))  # Фоновая полоса здоровья
    # Отрисовка зеленой полоски здоровья
        pygame.draw.rect(screen, (0, 255, 0), (self.position[0] - health_bar_length / 2, self.position[1] - 60, health_bar_width, 11* self.coefficient))  # Зеленая полоса здоровья
    # Создаем шрифт для текста
        font = pygame.font.SysFont(None, 30)
        health_text = str(int(self.health)) 
        text_surface = font.render(health_text, True, (255, 255, 255))
        screen.blit(text_surface, (self.position[0] - health_bar_length / 2 + 5, self.position[1] - 58))

    def update(self, delta_time):
        if self.current_path_index < len(self.path):
            target = self.path[self.current_path_index]
            target_position = ((target[0] * 40 + 20)*self.coefficient, (target[1] * 40 + 20)*self.coefficient)

            direction = (
                target_position[0] - self.position[0],
                target_position[1] - self.position[1]
            )
            distance = (direction[0] ** 2 + direction[1] ** 2) ** 0.5

            if distance > 0:
                direction = (direction[0] / distance, direction[1] / distance)
                self.position = (
                    self.position[0] + direction[0] * self.speed * delta_time,
                    self.position[1] + direction[1] * self.speed * delta_time
                )

            if distance < self.speed * delta_time:
                self.current_path_index += 1  # Переходим к следующей точке пути

        # Проверяем, достигли ли мы конца пути
        return self.current_path_index >= len(self.path)
    
