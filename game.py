import pygame
import sys
from config import *
from bird import Bird
from pipe import Pipe

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 16)
        
        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.game_over = False
        
        # 初始化管道
        for i in range(3):
            self.pipes.append(Pipe(WINDOW_WIDTH + i * PIPE_SPACING))
    
    def reset(self):
        self.bird.reset()
        self.pipes.clear()
        self.score = 0
        self.game_over = False
        
        # 重新生成管道
        for i in range(3):
            self.pipes.append(Pipe(WINDOW_WIDTH + i * PIPE_SPACING))
    
    def update(self):
        if not self.game_over:
            self.bird.update()
            
            # 更新管道
            for pipe in self.pipes:
                pipe.update()
                
                # 检查是否穿过管道
                if not pipe.passed and pipe.x + pipe.width < self.bird.x:
                    pipe.passed = True
                    self.score += 1
            
            # 移除超出屏幕的管道并生成新管道
            if self.pipes[0].off_screen():
                self.pipes.pop(0)
                self.pipes.append(Pipe(self.pipes[-1].x + PIPE_SPACING))
            
            # 碰撞检测
            for pipe in self.pipes:
                if pipe.collides_with(self.bird):
                    self.game_over = True
                    break
            
            # 检查是否碰到地面或顶部
            if self.bird.y + BIRD_SIZE > WINDOW_HEIGHT - 30 or self.bird.y < 0:
                self.game_over = True
    
    def draw(self):
        # 绘制天空
        self.screen.fill(SKY_COLOR)
        
        # 绘制管道
        for pipe in self.pipes:
            pipe.draw(self.screen)
        
        # 绘制地面
        pygame.draw.rect(self.screen, GROUND_COLOR, (0, WINDOW_HEIGHT - 30, WINDOW_WIDTH, 30))
        
        # 绘制小鸟
        self.bird.draw(self.screen)
        
        # 绘制分数
        score_text = self.font.render(f"Score: {self.score}", True, TEXT_COLOR)
        self.screen.blit(score_text, (10, 10))
        
        # 游戏结束界面
        if self.game_over:
            game_over_text = self.font.render(f"Game Over! Score: {self.score}", True, TEXT_COLOR)
            restart_text = self.font.render("Press R to Restart", True, TEXT_COLOR)
            
            game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20))
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
            
            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(restart_text, restart_rect)
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if not self.game_over:
                        if event.key == pygame.K_SPACE:
                            self.bird.jump()
                    else:
                        if event.key == pygame.K_r:
                            self.reset()
            
            self.update()
            self.draw()
            
            pygame.display.flip()
            self.clock.tick(60)
