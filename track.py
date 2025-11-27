import pygame
import random
import time
from config import (
    COLORS, WINDOW_WIDTH, WINDOW_HEIGHT, LANE_COUNT_OPTIONS, 
    LANE_CHANGE_INTERVAL, LANE_BORDER_WIDTH, LANE_LINE_WIDTH,
    LANE_LINE_HEIGHT, LANE_LINE_GAP, MAX_LANE_WIDTH, MIN_LANE_WIDTH,
    ROAD_MARGIN
)

class Track:
    def __init__(self):
        self.lane_count = random.choice(LANE_COUNT_OPTIONS)
        self.target_lane_count = self.lane_count
        self.left_border = ROAD_MARGIN
        self.right_border = WINDOW_WIDTH - ROAD_MARGIN
        self.target_left_border = self.left_border
        self.target_right_border = self.right_border
        self.last_change_time = time.time()
        self.line_offset = 0  # 用于分隔线动画
        self.transition_speed = 1.5  # 赛道切换时的平滑移动速度
        self.base_road_width = WINDOW_WIDTH - 2 * ROAD_MARGIN
        self.lane_width = self.calculate_lane_width(self.lane_count)

    def calculate_lane_width(self, lane_count):
        # 根据车道数量计算合适的车道宽度
        target_width = self.base_road_width // lane_count
        return max(MIN_LANE_WIDTH, min(MAX_LANE_WIDTH, target_width))

    def update(self):
        current_time = time.time()
        
        # 随机切换车道数量（间隔≥3秒）
        if current_time - self.last_change_time >= LANE_CHANGE_INTERVAL / 1000:
            self.target_lane_count = random.choice([c for c in LANE_COUNT_OPTIONS if c != self.lane_count])
            
            # 根据目标车道数量计算新的道路宽度
            target_road_width = self.target_lane_count * self.calculate_lane_width(self.target_lane_count)
            
            # 计算新的边界位置，保持赛道在屏幕中央
            self.target_left_border = (WINDOW_WIDTH - target_road_width) // 2
            self.target_right_border = WINDOW_WIDTH - self.target_left_border
            
            # 确保边界不会超出屏幕边缘的限制
            self.target_left_border = max(ROAD_MARGIN, self.target_left_border)
            self.target_right_border = min(WINDOW_WIDTH - ROAD_MARGIN, self.target_right_border)
            
            self.last_change_time = current_time

        # 平滑过渡边界位置
        if abs(self.left_border - self.target_left_border) > 0.5:
            if self.left_border < self.target_left_border:
                self.left_border += self.transition_speed
            else:
                self.left_border -= self.transition_speed
        else:
            self.left_border = self.target_left_border
            
        if abs(self.right_border - self.target_right_border) > 0.5:
            if self.right_border < self.target_right_border:
                self.right_border += self.transition_speed
            else:
                self.right_border -= self.transition_speed
        else:
            self.right_border = self.target_right_border
            # 边界稳定后更新车道数量和宽度
            self.lane_count = self.target_lane_count
            current_road_width = self.right_border - self.left_border
            self.lane_width = current_road_width // self.lane_count

        # 更新分隔线偏移量（营造移动效果）
        self.line_offset += 5
        if self.line_offset >= LANE_LINE_HEIGHT + LANE_LINE_GAP:
            self.line_offset = 0

    def draw(self, screen):
        # 绘制屏幕背景（黑色）
        screen.fill(COLORS['BLACK'])
        
        # 绘制赛道背景（深灰色）
        track_rect = pygame.Rect(self.left_border, 0, self.right_border - self.left_border, WINDOW_HEIGHT)
        pygame.draw.rect(screen, COLORS['DARK_GRAY'], track_rect)

        # 绘制红色边界
        pygame.draw.rect(screen, COLORS['RED'], 
                        (self.left_border - LANE_BORDER_WIDTH, 0, LANE_BORDER_WIDTH, WINDOW_HEIGHT))
        pygame.draw.rect(screen, COLORS['RED'], 
                        (self.right_border, 0, LANE_BORDER_WIDTH, WINDOW_HEIGHT))
        
        # 绘制赛道边缘的阴影效果
        shadow_width = 8
        pygame.draw.rect(screen, (0, 0, 0, 100), 
                        (self.left_border - LANE_BORDER_WIDTH - shadow_width, 0, shadow_width, WINDOW_HEIGHT))
        pygame.draw.rect(screen, (0, 0, 0, 100), 
                        (self.right_border + LANE_BORDER_WIDTH, 0, shadow_width, WINDOW_HEIGHT))

        # 绘制白色分隔线
        if self.lane_count >= 3:
            for i in range(1, self.lane_count):
                lane_x = self.left_border + i * self.lane_width
                
                # 绘制虚线分隔线
                y = self.line_offset
                while y < WINDOW_HEIGHT:
                    pygame.draw.rect(screen, COLORS['WHITE'], 
                                    (lane_x - LANE_LINE_WIDTH // 2, y, LANE_LINE_WIDTH, LANE_LINE_HEIGHT))
                    y += LANE_LINE_HEIGHT + LANE_LINE_GAP

    def get_lane_positions(self):
        # 返回每个车道的中心位置
        positions = []
        for i in range(self.lane_count):
            lane_center = self.left_border + (i + 0.5) * self.lane_width
            positions.append(lane_center)
        return positions