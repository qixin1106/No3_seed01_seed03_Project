import pygame

class Bullet:
    def __init__(self, x, y, screen_height):
        self.x = x
        self.y = y
        self.width = 4
        self.height = 15
        self.speed = 8
        self.color = (255, 255, 0)  # 黄色
        self.screen_height = screen_height
        self.active = True

    def update(self):
        # 向上移动
        self.y -= self.speed
        # 超出屏幕顶部则失效
        if self.y < -self.height:
            self.active = False

    def draw(self, screen):
        if self.active:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def check_collision(self, target):
        # 检测子弹与目标的碰撞
        if not self.active:
            return False
        
        bullet_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        target_rect = pygame.Rect(target.x, target.y, target.width, target.height)
        
        return bullet_rect.colliderect(target_rect)
