import pygame

class Button:
    def __init__(self, x, y, width, height, texts, action,color,pre_action=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.texts = texts
        self.action = action
        self.color = color
        self.click_start = False
        self.pre_action = pre_action

    def draw(self, window, font):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))
        for i, (text, offset) in enumerate(self.texts):
            text_surface = font.render(text, True, (255, 255, 255))
            window.blit(text_surface, (self.x + offset[0], self.y + offset[1]))

        pos = pygame.mouse.get_pos()
        if self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height and self.pre_action != None:
            self.pre_action()

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            self.click_start = False
            if self.x < event.pos[0] < self.x + self.width and self.y < event.pos[1] < self.y + self.height:
                self.action()





import pygame
import sys
import math

class RotatingSquare:
    def __init__(self, screen, x, y, size, color,angle):
        self.screen = screen
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.angle = angle

    def draw(self):
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.size, self.size))

        self.angle += 0.05
        if self.angle > 360:
            self.angle = 0
        self.x = round(self.screen.get_width() // 2 - self.size // 2 + int(150 * math.cos(math.radians(self.angle))))
        self.y = round(self.screen.get_height() // 2 - self.size // 2 + int(150 * math.sin(math.radians(self.angle))))






                