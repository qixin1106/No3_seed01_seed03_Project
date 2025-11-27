import pygame
import sys
import time
from config import COLORS, WINDOW_WIDTH, WINDOW_HEIGHT, FPS
from player import Player
from track import Track
from elements import ElementManager

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("PGGame - Rocket Car")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.running = True
        self.game_over = False
        self.distance = 0
        self.start_time = time.time()
        
        # 初始化游戏对象
        self.player = Player()
        self.track = Track()
        self.element_manager = ElementManager()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r and self.game_over:
                    self.restart()

    def update(self):
        if self.game_over:
            return

        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        
        # 更新游戏对象
        self.player.update(keys, self.track)
        self.track.update()
        self.element_manager.update(self.player, self.track, current_time)
        
        # 更新行驶距离
        self.distance = int((time.time() - self.start_time) * 100)  # 以米为单位
        
        # 碰撞检测
        if self.element_manager.check_collisions(self.player):
            self.game_over = True
        
        # 边界碰撞检测（防止玩家超出赛道）
        if self.player.x <= self.track.left_border or \
           self.player.x + self.player.width >= self.track.right_border:
            self.game_over = True

    def draw(self):
        # 背景由track.draw()处理，不需要重复绘制
        
        # 绘制游戏对象
        self.track.draw(self.screen)
        self.element_manager.draw(self.screen)
        self.player.draw(self.screen)
        
        # 绘制UI
        self.draw_ui()
        
        # 绘制游戏结束界面
        if self.game_over:
            self.draw_game_over()
        
        # 更新屏幕
        pygame.display.flip()

    def draw_ui(self):
        # 绘制行驶距离
        distance_text = self.font.render(f"Distance: {self.distance}m", True, COLORS['WHITE'])
        self.screen.blit(distance_text, (20, 20))
        
        # 绘制车道数量
        lane_text = self.font.render(f"Lanes: {self.track.lane_count}", True, COLORS['WHITE'])
        self.screen.blit(lane_text, (20, 60))

    def draw_game_over(self):
        # 半透明背景
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # 游戏结束文字
        game_over_text = self.font.render("GAME OVER", True, COLORS['RED'])
        text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        self.screen.blit(game_over_text, text_rect)
        
        # 最终距离
        distance_text = self.font.render(f"Final Distance: {self.distance}m", True, COLORS['WHITE'])
        distance_rect = distance_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 10))
        self.screen.blit(distance_text, distance_rect)
        
        # 重玩提示
        restart_text = self.font.render("Press R to Restart", True, COLORS['WHITE'])
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 70))
        self.screen.blit(restart_text, restart_rect)

    def restart(self):
        # 重置游戏状态
        self.game_over = False
        self.distance = 0
        self.start_time = time.time()
        
        # 重新初始化游戏对象
        self.player = Player()
        self.track = Track()
        self.element_manager = ElementManager()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()