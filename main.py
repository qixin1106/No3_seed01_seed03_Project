import pygame
import sys
import random
from ship import Ship
from bullet import Bullet
from meteor import Meteor

# 忽略Pygame模块的静态分析错误
# pylint: disable=no-member

# 游戏常量
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (0, 0, 0)  # 黑色
TEXT_COLOR = (255, 255, 255)  # 白色

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Simple Space Shooter")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)  # 使用默认字体，确保英文显示正常
        
        # 游戏状态
        self.game_state = "playing"  # "playing", "paused", "game_over"
        self.score = 0
        self.last_shot_time = 0
        self.shot_cooldown = 200  # 子弹发射冷却时间（毫秒）
        self.last_meteor_time = 0
        self.meteor_interval = 1000  # 陨石生成间隔（毫秒）
        
        # 游戏对象
        self.ship = Ship(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.bullets = []
        self.meteors = []

    def run(self):
        while True:
            self.handle_events()
            if self.game_state == "playing":
                self.update()
            self.draw()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_state == "playing":
                        self.shoot_bullet()
                    elif self.game_state == "game_over":
                        self.restart()
                elif event.key == pygame.K_p:
                    if self.game_state == "playing":
                        self.game_state = "paused"
                    elif self.game_state == "paused":
                        self.game_state = "playing"

        # 处理飞船移动
        keys = pygame.key.get_pressed()
        if self.game_state == "playing":
            self.ship.set_direction(keys)

    def shoot_bullet(self):
        # 检查冷却时间
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.shot_cooldown:
            ship_x, ship_y = self.ship.get_position()
            bullet = Bullet(ship_x - 2, ship_y, SCREEN_HEIGHT)
            self.bullets.append(bullet)
            self.last_shot_time = current_time

    def spawn_meteor(self):
        # 生成陨石
        current_time = pygame.time.get_ticks()
        if current_time - self.last_meteor_time > self.meteor_interval:
            meteor = Meteor(SCREEN_WIDTH, SCREEN_HEIGHT)
            # 根据分数调整陨石速度
            speed_multiplier = 1 + (self.score // 10) * 0.1
            meteor.set_speed(meteor.get_speed() * speed_multiplier)
            self.meteors.append(meteor)
            self.last_meteor_time = current_time
            
            # 根据分数调整陨石生成间隔（最小500毫秒）
            interval_reduction = (self.score // 5) * 50
            self.meteor_interval = max(500, 1000 - interval_reduction)

    def update(self):
        # 更新飞船
        self.ship.update()
        
        # 更新子弹
        for bullet in self.bullets[:]:
            bullet.update()
            if not bullet.active:
                self.bullets.remove(bullet)
        
        # 生成陨石
        self.spawn_meteor()
        
        # 更新陨石
        for meteor in self.meteors[:]:
            meteor.update()
            if not meteor.active:
                self.meteors.remove(meteor)
        
        # 碰撞检测
        self.check_collisions()

    def check_collisions(self):
        # 子弹与陨石碰撞
        for bullet in self.bullets[:]:
            for meteor in self.meteors[:]:
                if bullet.check_collision(meteor):
                    self.bullets.remove(bullet)
                    self.meteors.remove(meteor)
                    self.score += 1
                    break
        
        # 飞船与陨石碰撞
        ship_rect = pygame.Rect(self.ship.x, self.ship.y, self.ship.width, self.ship.height)
        for meteor in self.meteors:
            meteor_rect = pygame.Rect(meteor.x, meteor.y, meteor.width, meteor.height)
            if ship_rect.colliderect(meteor_rect):
                self.game_state = "game_over"
                break

    def draw(self):
        # 绘制背景
        self.screen.fill(BACKGROUND_COLOR)
        
        # 绘制游戏对象
        self.ship.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)
        for meteor in self.meteors:
            meteor.draw(self.screen)
        
        # 绘制分数
        score_text = self.font.render(f"Score: {self.score}", True, TEXT_COLOR)
        self.screen.blit(score_text, (10, 10))
        
        # 绘制游戏状态信息
        if self.game_state == "paused":
            pause_text = self.font.render("Paused - Press P to Continue", True, TEXT_COLOR)
            text_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(pause_text, text_rect)
        elif self.game_state == "game_over":
            game_over_text = self.font.render("Game Over", True, TEXT_COLOR)
            score_text = self.font.render(f"Final Score: {self.score}", True, TEXT_COLOR)
            restart_text = self.font.render("Press SPACE to Restart", True, TEXT_COLOR)
            
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            
            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(score_text, score_rect)
            self.screen.blit(restart_text, restart_rect)
        
        # 更新屏幕
        pygame.display.flip()

    def restart(self):
        # 重置游戏
        self.game_state = "playing"
        self.score = 0
        self.last_shot_time = 0
        self.last_meteor_time = 0
        self.meteor_interval = 1000
        self.bullets.clear()
        self.meteors.clear()
        self.ship = Ship(SCREEN_WIDTH, SCREEN_HEIGHT)

if __name__ == "__main__":
    game = Game()
    game.run()
