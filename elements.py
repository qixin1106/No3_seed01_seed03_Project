import pygame
import random
from constants import *

class BaseElement:
    def __init__(self, x, y):
        self.rect = None
        self.x = x
        self.y = y
        self.speed = GAME_SPEED
        
    def update(self):
        self.y += self.speed
        if self.rect:
            self.rect.y = self.y
            
    def draw(self, screen):
        pass
        
    def is_off_screen(self):
        return self.y > WINDOW_HEIGHT

class NormalCar(BaseElement):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.rect = pygame.Rect(x, y, NORMAL_CAR_WIDTH, NORMAL_CAR_HEIGHT)
        self.color = GRAY
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect.inflate(-10, -10), 2)
        pygame.draw.rect(screen, WHITE, (self.rect.x + 8, self.rect.y + 8, self.rect.width - 16, 25))

class RedCar(BaseElement):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.rect = pygame.Rect(x, y, NORMAL_CAR_WIDTH, NORMAL_CAR_HEIGHT)
        self.color = RED
        self.aggression = 1.5  # 横向移动速度（降低到1.5，让玩家更容易躲开）
        
    def update(self, player=None):
        super().update()
        # 靠近玩家时向玩家方向移动
        if player and abs(self.y - player.rect.y) < 300:
            if self.rect.x < player.rect.x:
                self.rect.x += self.aggression
            elif self.rect.x > player.rect.x:
                self.rect.x -= self.aggression
        self.x = self.rect.x

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect.inflate(-10, -10), 2)
        pygame.draw.rect(screen, WHITE, (self.rect.x + 8, self.rect.y + 8, self.rect.width - 16, 25))

class BlueCar(BaseElement):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.rect = pygame.Rect(x, y, NORMAL_CAR_WIDTH, NORMAL_CAR_HEIGHT)
        self.color = BLUE
        self.fear = 3  # 横向移动速度
        
    def update(self, player=None):
        super().update()
        # 靠近玩家时远离玩家方向移动
        if player and abs(self.y - player.rect.y) < 300:
            if self.rect.x < player.rect.x:
                self.rect.x -= self.fear
            elif self.rect.x > player.rect.x:
                self.rect.x += self.fear
        self.x = self.rect.x

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect.inflate(-10, -10), 2)
        pygame.draw.rect(screen, WHITE, (self.rect.x + 8, self.rect.y + 8, self.rect.width - 16, 25))

class Truck(BaseElement):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.rect = pygame.Rect(x, y, TRUCK_WIDTH, TRUCK_HEIGHT)
        self.color = BLACK
        self.stability = 0.5  # 横向移动速度（基本不移动）
        
    def update(self, player=None):
        super().update()
        # 偶尔轻微移动
        if random.random() < 0.01:
            self.rect.x += random.choice([-self.stability, self.stability])
        self.x = self.rect.x

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, LIGHT_GRAY, self.rect.inflate(-15, -15), 2)
        pygame.draw.rect(screen, WHITE, (self.rect.x + 15, self.rect.y + 15, self.rect.width - 30, 40))

class Rock(BaseElement):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = GRAY
        self.radius = ROCK_RADIUS
        self.rect = pygame.Rect(x - self.radius, y - self.radius, self.radius * 2, self.radius * 2)
        
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        pygame.draw.circle(screen, BLACK, (self.x, self.y), self.radius, 2)

class ElementManager:
    def __init__(self):
        self.elements = []
        self.last_spawn_time = pygame.time.get_ticks()
        
    def spawn_element(self, track):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time >= ELEMENT_SPAWN_INTERVAL:
            # 随机选择元素类型
            element_type = random.choices(ELEMENT_TYPES, weights=ELEMENT_WEIGHTS)[0]
            
            # 计算生成位置（在当前赛道范围内）
            track_width = track.right_bound - track.left_bound
            
            if element_type == 'normal_car':
                x = random.randint(track.left_bound, track.right_bound - NORMAL_CAR_WIDTH)
                element = NormalCar(x, -NORMAL_CAR_HEIGHT)
            elif element_type == 'red_car':
                x = random.randint(track.left_bound, track.right_bound - NORMAL_CAR_WIDTH)
                element = RedCar(x, -NORMAL_CAR_HEIGHT)
            elif element_type == 'blue_car':
                x = random.randint(track.left_bound, track.right_bound - NORMAL_CAR_WIDTH)
                element = BlueCar(x, -NORMAL_CAR_HEIGHT)
            elif element_type == 'truck':
                # 确保大货车不会超出赛道
                max_x = track.right_bound - TRUCK_WIDTH
                x = random.randint(max(track.left_bound, 0), max_x)
                element = Truck(x, -TRUCK_HEIGHT)
            elif element_type == 'rock':
                x = random.randint(track.left_bound + ROCK_RADIUS, track.right_bound - ROCK_RADIUS)
                element = Rock(x, -ROCK_RADIUS)
            
            self.elements.append(element)
            self.last_spawn_time = current_time
            
    def update(self, player):
        # 更新所有元素
        for element in self.elements:
            if hasattr(element, 'update') and element.update.__code__.co_argcount > 1:
                element.update(player)
            else:
                element.update()
        
        # 移除出屏元素
        self.elements = [element for element in self.elements if not element.is_off_screen()]
        
    def draw(self, screen):
        for element in self.elements:
            element.draw(screen)
            
    def check_collision(self, player):
        for element in self.elements:
            if player.rect.colliderect(element.rect):
                return True
        return False
