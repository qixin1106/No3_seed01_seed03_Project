# 窗口配置
WINDOW_WIDTH = 480
WINDOW_HEIGHT = 800  # 调整为更合适的比例
FPS = 60

# 颜色配置
COLORS = {
    'BLACK': (0, 0, 0),
    'WHITE': (255, 255, 255),
    'RED': (255, 0, 0),
    'YELLOW': (255, 255, 0),
    'GRAY': (128, 128, 128),
    'DARK_GRAY': (64, 64, 64),
    'BLUE': (0, 0, 255),
    'LIGHT_GRAY': (192, 192, 192)
}

# 玩家配置
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 80
PLAYER_SPEED = 7  # 横向移动速度
PLAYER_Y = WINDOW_HEIGHT - 150  # 玩家固定Y位置

# 赛道配置
LANE_COUNT_OPTIONS = [3, 4, 5]
LANE_CHANGE_INTERVAL = 3000  # 最小车道切换间隔（毫秒）
MAX_LANE_WIDTH = 140  # 最大车道宽度
MIN_LANE_WIDTH = 80   # 最小车道宽度
LANE_BORDER_WIDTH = 6
LANE_LINE_WIDTH = 3
LANE_LINE_HEIGHT = 30
LANE_LINE_GAP = 15
ROAD_MARGIN = 40  # 赛道边缘与屏幕边缘的最小距离

# 游戏元素配置
ELEMENT_SPEED = 5  # 基础元素移动速度
PLAYER_SPEED_MULTIPLIER = 1.2  # 玩家速度比其他元素快

# 车辆配置
CAR_WIDTH = 45
CAR_HEIGHT = 70
TRUCK_WIDTH = 70  # 1.5车道宽
TRUCK_HEIGHT = 90

# 障碍配置
OBSTACLE_RADIUS = 25

# 生成概率（总和为100）
SPAWN_PROBABILITIES = {
    'normal_car': 60,
    'red_car': 15,
    'blue_car': 15,
    'truck': 5,
    'obstacle': 5
}

# 碰撞检测阈值
COLLISION_THRESHOLD = 10

# AI车辆行为距离阈值
AI_REACTION_DISTANCE = 300
AI_MOVE_SPEED = 1.5  # 降低AI移动速度以确保玩家更灵敏