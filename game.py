import pygame
from constants import *
from player import Player
from track import Track
from elements import ElementManager

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("PGGame - 竖版火箭车")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.reset()
        
    def reset(self):
        self.player = Player()
        self.track = Track()
        self.element_manager = ElementManager()
        self.distance = 0
        self.game_over = False
        self.start_time = pygame.time.get_ticks()
        
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and self.game_over:
                        self.reset()
            
            keys = pygame.key.get_pressed()
            
            if not self.game_over:
                # 更新游戏状态
                self.player.update(keys, self.track)
                self.track.update()
                self.element_manager.spawn_element(self.track)
                self.element_manager.update(self.player)
                
                # 计算行驶距离
                current_time = pygame.time.get_ticks()
                self.distance = (current_time - self.start_time) // 100  # 每10毫秒1米
                
                # 碰撞检测
                if self.element_manager.check_collision(self.player):
                    self.game_over = True
            
            # 绘制游戏
            self.screen.fill(BLACK)
            self.track.draw(self.screen)
            self.element_manager.draw(self.screen)
            self.player.draw(self.screen)
            
            # 绘制UI
            self.draw_ui()
            
            pygame.display.flip()
            self.clock.tick(60)
            
        pygame.quit()
        
    def draw_ui(self):
        # 绘制行驶距离
        distance_text = self.font.render(f"Distance: {self.distance}m", True, WHITE)
        self.screen.blit(distance_text, (20, 20))
        
        # 绘制游戏结束信息
        if self.game_over:
            game_over_text = self.font.render("Game Over! Press R to Restart", True, RED)
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.screen.blit(game_over_text, text_rect)
