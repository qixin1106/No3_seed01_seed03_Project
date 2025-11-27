import pygame
import sys
import random
from settings import *
from ship import Ship
from bullet import Bullet
from meteor import Meteor

class SpaceShooterGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Simple Space Shooter")
        self.clock = pygame.time.Clock()
        
        self.game_state = GAME_STATE['playing']
        self.ship = Ship()
        self.bullets = []
        self.meteors = []
        self.last_shot_time = 0
        self.shot_cooldown = 200  # 子弹冷却时间（毫秒）
        
    def run(self):
        while True:
            self.handle_events()
            
            if self.game_state == GAME_STATE['playing']:
                self.update()
            
            self.draw()
            self.clock.tick(FPS)
            
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_state == GAME_STATE['playing']:
                        self.shoot()
                    elif self.game_state == GAME_STATE['game_over']:
                        self.restart()
                        
                if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                    if self.game_state == GAME_STATE['playing']:
                        self.game_state = GAME_STATE['paused']
                    elif self.game_state == GAME_STATE['paused']:
                        self.game_state = GAME_STATE['playing']
                        
    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.shot_cooldown:
            bullet = Bullet(self.ship.x + self.ship.width // 2, self.ship.y)
            self.bullets.append(bullet)
            self.last_shot_time = current_time
            
    def update(self):
        # 更新飞船
        keys = pygame.key.get_pressed()
        self.ship.update(keys)
        
        # 更新子弹
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.is_off_screen():
                self.bullets.remove(bullet)
                
        # 生成陨石
        # 分数越高，生成概率越大
        spawn_rate = METEOR_SPAWN_RATE + (self.ship.score // 500) * 0.005
        if random.random() < spawn_rate:
            meteor = Meteor(self.ship.score)
            self.meteors.append(meteor)
            
        # 更新陨石
        for meteor in self.meteors[:]:
            meteor.update()
            if meteor.is_off_screen():
                self.meteors.remove(meteor)
                
        # 碰撞检测
        self.check_collisions()
        
    def check_collisions(self):
        # 子弹 vs 陨石
        for bullet in self.bullets[:]:
            for meteor in self.meteors[:]:
                if bullet.rect.colliderect(meteor.get_rect()):
                    self.bullets.remove(bullet)
                    self.meteors.remove(meteor)
                    self.ship.score += 100
                    break
                    
        # 飞船 vs 陨石
        ship_rect = pygame.Rect(self.ship.x, self.ship.y, self.ship.width, self.ship.height)
        for meteor in self.meteors[:]:
            if ship_rect.colliderect(meteor.get_rect()):
                self.meteors.remove(meteor)
                self.ship.lives -= 1
                
                if self.ship.lives <= 0:
                    self.game_state = GAME_STATE['game_over']
                break
                
    def draw(self):
        self.screen.fill(BLACK)
        
        # 绘制游戏元素
        self.ship.draw(self.screen)
        
        for bullet in self.bullets:
            bullet.draw(self.screen)
            
        for meteor in self.meteors:
            meteor.draw(self.screen)
            
        # 绘制UI
        self.draw_ui()
        
        # 绘制暂停界面
        if self.game_state == GAME_STATE['paused']:
            self.draw_pause_screen()
            
        # 绘制游戏结束界面
        if self.game_state == GAME_STATE['game_over']:
            self.draw_game_over_screen()
            
        pygame.display.flip()
        
    def draw_ui(self):
        # 绘制分数
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.ship.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # 绘制生命值
        lives_text = font.render(f"Lives: {self.ship.lives}", True, WHITE)
        self.screen.blit(lives_text, (10, 50))
        
        # 绘制控制提示
        control_text = font.render("WASD to move | SPACE to shoot | P/ESC to pause", True, WHITE)
        text_rect = control_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20))
        self.screen.blit(control_text, text_rect)
        
    def draw_pause_screen(self):
        # 半透明遮罩
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(150)
        self.screen.blit(overlay, (0, 0))
        
        font = pygame.font.Font(None, 72)
        pause_text = font.render("PAUSED", True, WHITE)
        text_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(pause_text, text_rect)
        
        font = pygame.font.Font(None, 36)
        resume_text = font.render("Press P or ESC to resume", True, WHITE)
        text_rect = resume_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(resume_text, text_rect)
        
    def draw_game_over_screen(self):
        # 半透明遮罩
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(150)
        self.screen.blit(overlay, (0, 0))
        
        font = pygame.font.Font(None, 72)
        game_over_text = font.render("GAME OVER", True, RED)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(game_over_text, text_rect)
        
        font = pygame.font.Font(None, 48)
        score_text = font.render(f"Final Score: {self.ship.score}", True, WHITE)
        text_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        self.screen.blit(score_text, text_rect)
        
        font = pygame.font.Font(None, 36)
        restart_text = font.render("Press SPACE to restart", True, WHITE)
        text_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(restart_text, text_rect)
        
    def restart(self):
        self.game_state = GAME_STATE['playing']
        self.ship.reset()
        self.bullets.clear()
        self.meteors.clear()
        self.last_shot_time = 0