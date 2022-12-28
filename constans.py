RAND_RAN_NUM = 0

SHOW_BEST = False
READ_PAR = True
FILE_PAR = '106'
DEBAG_MODE = False

TRACK_NUM = '3'
if TRACK_NUM == '3':
    CAR_START_X = 250
    CAR_START_Y = 830.
    START_ANGLE = 0
    START_DIRECT = [1,0]
elif TRACK_NUM == '1':
    CAR_START_X = 120
    CAR_START_Y = 555.
    START_ANGLE = -90
    START_DIRECT = [0,-1]
elif TRACK_NUM == '0':
    CAR_START_X = 130
    CAR_START_Y = 300.
    START_ANGLE = 90
    START_DIRECT = [0,1]


TICK_SUM = 0
TICK_MAX = 1000
AI_INPUT_SHAPE = 8
AI_MIDDLE_SHAPE = 7
AI_OUTPUT_SHAPE = 6

LENGTH_CHROM = 217
LOW = -1.0
UP = 1.0
ETA = 8.0

# константы генетического алгоритма
POPULATION_SIZE = 16   # количество индивидуумов в популяции
P_CROSSOVER = 0.9       # вероятность скрещивания
P_MUTATION = 0.2        # вероятность мутации индивидуума
MAX_GENERATIONS = 50000    # максимальное количество поколений
HALL_OF_FAME_SIZE = 1

MAX_SPEED = 450.0
MAX_SPEED_ROT = 3.0
ACCELERATION_RATE_START = 0.4
ACCELERATION_RATE_STOP = 0.4
ACCELERATION_RATE_ROT = 1.6
ENGINEFORCE = 1600000
BRAKINGFORCE = ENGINEFORCE / 10
C_DRAG = 0.7
C_RR = 3000
MASS = 900
WHEEL_ROT_PER_SEC = 0.5 * 60
WHEEL_ROT_MAX = 5

COUNT_CARS = 8


CUR_TICK = 1
GEN = 1

SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 900
SCREEN_TITLE = "CAR_AI"
