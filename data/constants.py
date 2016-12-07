__author__ = "kiel.regusters"

# Game Info
SCREEN_SIZE = (800, 600)
TILE_SIZE = 16

# Player info
MAX_VEL_X = 10
MAX_VEL_Y = 20
GRAVITY = 1
JUMP_GRAVITY = 0.5
JUMP_VEL = -7
DOUBLE_JUMP_VEL = -7
LEVEL_CAP = 20
STAT_CAP = 9

# Player states
WALKING = "walking"
IDLE = "idle"
FALLING = "falling"
JUMP = "jump"
DOUBLEJUMP = "djump"
NOTATTACKING = "noattack"
ATTACKING = "attack"
LEVEL_AVAILABLE = "levelavailable"
NO_SP = "nosp"


# Player forces
ACCEL = 0.5

# Game States
MAIN_MENU = "main menu"
LOAD_SCREEN = "load screen"
MAP = "map"
CONTINUE = "continue"
LOADMAP = "loadmap"

# Real Time States
PAUSE = "pause"
UNPAUSE = "unpause"

# SoundManager states
NORMAL = "normal"
s_MENU = "sound menu"


# Level states
LEVEL1 = "level1"

# Cursor states
PLAY = "play"
LOAD = "load"
QUIT = "quit"

# Colors
BLACK	=	(0, 0, 0)

# ZOOM
ZOOM = 3