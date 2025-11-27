import pygame
import random
from config import (
    COLORS, WINDOW_WIDTH, WINDOW_HEIGHT, ELEMENT_SPEED, PLAYER_SPEED_MULTIPLIER,
    CAR_WIDTH, CAR_HEIGHT, TRUCK_WIDTH, TRUCK_HEIGHT, OBSTACLE_RADIUS,
    SPAWN_PROBABILITIES, AI_REACTION_DISTANCE, AI_MOVE_SPEED
)

class BaseElement:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = ELEMENT_SPEED * PLAYER_SPEED_MULTIPLIER
        self.active = True

    def update(self):
        self.y += self.speed
        # 当元素超出屏幕底部时标记为非活动
        if self.y > WINDOW_HEIGHT:
            self.active = False

    def draw(self, screen):
        pass

    def check_collision(self, player):
        pass


class NormalCar(BaseElement):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.width = CAR_WIDTH
        self.height = CAR_HEIGHT
        self.rect = pygame.Rect(self.x - self.width // 2, self.y, self.width, self.height)

    def update(self):
        super().update()
        self.rect.x = self.x - self.width // 2
        self.rect.y = self.y

    def draw(self, screen):
        pygame.draw.rect(screen, COLORS['GRAY'], self.rect)
        pygame.draw.rect(screen, COLORS['BLACK'], self.rect.inflate(-8, -8), 2)
        # 绘制车窗
        window_rect = pygame.Rect(self.rect.x + 10, self.rect.y + 8, self.width - 20, self.height - 40)
        pygame.draw.rect(screen, COLORS['LIGHT_GRAY'], window_rect)
        pygame.draw.rect(screen, COLORS['BLACK'], window_rect, 1)

    def check_collision(self, player):
        return self.rect.colliderect(player.rect)


class RedCar(BaseElement):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.width = CAR_WIDTH
        self.height = CAR_HEIGHT
        self.target_x = x
        self.rect = pygame.Rect(self.x - self.width // 2, self.y, self.width, self.height)

    def update(self, player, track):
        super().update()
        
        # 当玩家靠近时，向玩家方向移动
        distance = abs(player.y - self.y)
        if distance < AI_REACTION_DISTANCE:
            # 计算目标位置（玩家的x位置）
            self.target_x = player.x + player.width // 2
            
            # 平滑移动到目标位置
            if abs(self.x - self.target_x) > 1:
                if self.x < self.target_x:
                    self.x += AI_MOVE_SPEED
                else:
                    self.x -= AI_MOVE_SPEED
            
            # 确保不超出赛道边界
            self.x = max(track.left_border + self.width // 2, self.x)
            self.x = min(track.right_border - self.width // 2, self.x)
        
        self.rect.x = self.x - self.width // 2
        self.rect.y = self.y

    def draw(self, screen):
        pygame.draw.rect(screen, COLORS['RED'], self.rect)
        pygame.draw.rect(screen, COLORS['BLACK'], self.rect.inflate(-8, -8), 2)
        # 绘制车窗
        window_rect = pygame.Rect(self.rect.x + 10, self.rect.y + 8, self.width - 20, self.height - 40)
        pygame.draw.rect(screen, COLORS['LIGHT_GRAY'], window_rect)
        pygame.draw.rect(screen, COLORS['BLACK'], window_rect, 1)

    def check_collision(self, player):
        return self.rect.colliderect(player.rect)


class BlueCar(BaseElement):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.width = CAR_WIDTH
        self.height = CAR_HEIGHT
        self.original_x = x
        self.rect = pygame.Rect(self.x - self.width // 2, self.y, self.width, self.height)

    def update(self, player, track):
        super().update()
        
        # 当玩家靠近时，远离玩家方向移动
        distance = abs(player.y - self.y)
        if distance < AI_REACTION_DISTANCE:
            # 计算远离玩家的目标位置
            if player.x < self.x:
                self.target_x = self.original_x + 50
            else:
                self.target_x = self.original_x - 50
            
            # 平滑移动到目标位置
            if abs(self.x - self.target_x) > 1:
                if self.x < self.target_x:
                    self.x += AI_MOVE_SPEED
                else:
                    self.x -= AI_MOVE_SPEED
            
            # 确保不超出赛道边界
            self.x = max(track.left_border + self.width // 2, self.x)
            self.x = min(track.right_border - self.width // 2, self.x)
        else:
            # 远离玩家后，缓慢回到原始位置
            if abs(self.x - self.original_x) > 1:
                if self.x < self.original_x:
                    self.x += AI_MOVE_SPEED // 2
                else:
                    self.x -= AI_MOVE_SPEED // 2
        
        self.rect.x = self.x - self.width // 2
        self.rect.y = self.y

    def draw(self, screen):
        pygame.draw.rect(screen, COLORS['BLUE'], self.rect)
        pygame.draw.rect(screen, COLORS['BLACK'], self.rect.inflate(-8, -8), 2)
        # 绘制车窗
        window_rect = pygame.Rect(self.rect.x + 10, self.rect.y + 8, self.width - 20, self.height - 40)
        pygame.draw.rect(screen, COLORS['LIGHT_GRAY'], window_rect)
        pygame.draw.rect(screen, COLORS['BLACK'], window_rect, 1)

    def check_collision(self, player):
        return self.rect.colliderect(player.rect)


class Truck(BaseElement):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.width = TRUCK_WIDTH
        self.height = TRUCK_HEIGHT
        self.rect = pygame.Rect(self.x - self.width // 2, self.y, self.width, self.height)

    def update(self):
        super().update()
        self.rect.x = self.x - self.width // 2
        self.rect.y = self.y

    def draw(self, screen):
        pygame.draw.rect(screen, COLORS['DARK_GRAY'], self.rect)
        pygame.draw.rect(screen, COLORS['BLACK'], self.rect.inflate(-8, -8), 2)
        # 绘制车窗
        window_rect = pygame.Rect(self.rect.x + 15, self.rect.y + 10, self.width - 60, self.height - 50)
        pygame.draw.rect(screen, COLORS['LIGHT_GRAY'], window_rect)
        pygame.draw.rect(screen, COLORS['BLACK'], window_rect, 1)
        # 绘制货箱分隔线
        pygame.draw.line(screen, COLORS['BLACK'], 
                        (self.rect.x + self.width // 2, self.rect.y),
                        (self.rect.x + self.width // 2, self.rect.y + self.height), 2)

    def check_collision(self, player):
        return self.rect.colliderect(player.rect)


class Obstacle(BaseElement):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.radius = OBSTACLE_RADIUS
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, 
                               self.radius * 2, self.radius * 2)

    def update(self):
        super().update()
        self.rect.x = self.x - self.radius
        self.rect.y = self.y - self.radius

    def draw(self, screen):
        pygame.draw.circle(screen, COLORS['GRAY'], (self.x, self.y + self.radius), self.radius)
        pygame.draw.circle(screen, COLORS['BLACK'], (self.x, self.y + self.radius), self.radius, 2)

    def check_collision(self, player):
        # 圆形碰撞检测
        distance_x = abs(self.x - (player.x + player.width // 2))
        distance_y = abs((self.y + self.radius) - (player.y + player.height // 2))
        
        if distance_x > (player.width // 2 + self.radius):
            return False
        if distance_y > (player.height // 2 + self.radius):
            return False
        
        if distance_x <= (player.width // 2):
            return True
        if distance_y <= (player.height // 2):
            return True
        
        corner_distance_sq = (distance_x - player.width // 2)**2 + (distance_y - player.height // 2)**2
        return corner_distance_sq <= (self.radius**2)


class ElementManager:
    def __init__(self):
        self.elements = []
        self.last_spawn_time = 0
        self.spawn_interval = 1000  # 毫秒

    def update(self, player, track, current_time):
        # 更新所有元素
        for element in self.elements:
            if isinstance(element, (RedCar, BlueCar)):
                element.update(player, track)
            else:
                element.update()

        # 移除非活动元素
        self.elements = [e for e in self.elements if e.active]

        # 生成新元素
        if current_time - self.last_spawn_time > self.spawn_interval:
            self.spawn_element(track)
            self.last_spawn_time = current_time
            # 随机调整生成间隔
            self.spawn_interval = random.randint(800, 2000)

    def spawn_element(self, track):
        lane_positions = track.get_lane_positions()
        if not lane_positions:
            return

        # 随机选择车道
        lane_x = random.choice(lane_positions)
        y = -100  # 从屏幕顶部外生成

        # 根据概率选择元素类型
        rand = random.randint(1, 100)
        cumulative = 0
        
        for element_type, probability in SPAWN_PROBABILITIES.items():
            cumulative += probability
            if rand <= cumulative:
                if element_type == 'normal_car':
                    self.elements.append(NormalCar(lane_x, y))
                elif element_type == 'red_car':
                    self.elements.append(RedCar(lane_x, y))
                elif element_type == 'blue_car':
                    self.elements.append(BlueCar(lane_x, y))
                elif element_type == 'truck':
                    # 确保卡车不会超出赛道边界
                    adjusted_x = max(track.left_border + TRUCK_WIDTH // 2, lane_x)
                    adjusted_x = min(track.right_border - TRUCK_WIDTH // 2, adjusted_x)
                    self.elements.append(Truck(adjusted_x, y))
                elif element_type == 'obstacle':
                    self.elements.append(Obstacle(lane_x, y))
                break

    def draw(self, screen):
        for element in self.elements:
            element.draw(screen)

    def check_collisions(self, player):
        for element in self.elements:
            if element.check_collision(player):
                return True
        return False