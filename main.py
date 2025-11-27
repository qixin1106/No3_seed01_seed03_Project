import pygame
import sys
from game import Game
from config import Config

# Ignore pygame static analysis errors
# pyright: reportAttributeAccessIssue=false

def main():
    pygame.init()
    
    config = Config()
    screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
    pygame.display.set_caption("Pixel Link")
    
    game = Game(config)
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    game.handle_click(event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game.reset()
        
        game.update()
        game.render(screen)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
