import pygame
from constants import WIDTH, HEIGHT, FPS, SKY_BLUE, GRAY, WHITE, BLACK
from bird import Bird
from pipe import Pipe

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 16)
        self.reset()

    def reset(self):
        self.bird = Bird()
        self.pipes = [Pipe(WIDTH), Pipe(WIDTH + 150)]
        self.score = 0
        self.game_over = False
        self.passed_pipes = set()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if not self.game_over:
                    if event.key == pygame.K_SPACE:
                        self.bird.jump()
                else:
                    if event.key == pygame.K_r:
                        self.reset()
        return True

    def update(self):
        if not self.game_over:
            self.bird.update()
            
            # 更新管道
            for pipe in self.pipes:
                pipe.update()
            
            # 移除超出屏幕的管道并添加新管道
            if self.pipes[0].off_screen():
                self.pipes.pop(0)
                self.pipes.append(Pipe(WIDTH))
            
            # 计分
            for pipe in self.pipes:
                if pipe.passed(self.bird) and pipe not in self.passed_pipes:
                    self.score += 1
                    self.passed_pipes.add(pipe)
            
            # 碰撞检测
            if self.bird.y < 0 or self.bird.y + self.bird.height > HEIGHT - 30:
                self.game_over = True
            
            for pipe in self.pipes:
                if self.bird.rect.colliderect(pipe.top_rect) or self.bird.rect.colliderect(pipe.bottom_rect):
                    self.game_over = True

    def draw(self):
        self.screen.fill(SKY_BLUE)
        
        # 绘制管道
        for pipe in self.pipes:
            pipe.draw(self.screen)
        
        # 绘制地面
        pygame.draw.rect(self.screen, GRAY, (0, HEIGHT - 30, WIDTH, 30))
        
        # 绘制小鸟
        self.bird.draw(self.screen)
        
        # 绘制分数
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # 绘制游戏结束界面
        if self.game_over:
            # 半透明背景
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            # 游戏结束文本
            game_over_text = self.font.render("Game Over!", True, WHITE)
            score_text = self.font.render(f"Score: {self.score}", True, WHITE)
            restart_text = self.font.render("Press R to Restart", True, WHITE)
            
            self.screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 40))
            self.screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
            self.screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 40))
        
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            running = self.handle_events()
            self.update()
            self.draw()
        pygame.quit()
