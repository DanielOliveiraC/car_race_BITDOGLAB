import time
import random
from pimoroni_bus import SPIBus
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2, PEN_RGB332
from machine import Pin

# ==========================
# DISPLAY
# ==========================
spibus = SPIBus(cs=17, dc=4, sck=18, mosi=19, bl=9)
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2, bus=spibus, pen_type=PEN_RGB332, rotate=0)
display.set_backlight(1.0)
WIDTH, HEIGHT = display.get_bounds()

# ==========================
# CORES
# ==========================
BG = display.create_pen(10,10,30)          # fundo escuro
CAR_COLOR = display.create_pen(0,255,128)  # carro verde
OBSTACLE_COLOR = display.create_pen(255,50,50) # obstáculo vermelho
TEXT_COLOR = display.create_pen(255,255,255)  # branco
BORDER_COLOR = display.create_pen(0,0,0)
ROAD_COLOR = display.create_pen(50,50,50)
LINE_COLOR = display.create_pen(200,200,200)

# ==========================
# BOTÕES (substituem joystick)
# ==========================
BUTTON_LEFT_PIN = 5
BUTTON_RIGHT_PIN = 6

btn_left = Pin(BUTTON_LEFT_PIN, Pin.IN, Pin.PULL_UP)   # ativo LOW
btn_right = Pin(BUTTON_RIGHT_PIN, Pin.IN, Pin.PULL_UP) # ativo LOW

dir_input = None

def read_buttons():
    """
    Lê os botões. Se pressionado -> "LEFT" ou "RIGHT".
    Como usamos pull-up, o estado pressionado é 0 (LOW).
    """
    global dir_input
    left = not btn_left.value()   # True quando pressionado
    right = not btn_right.value() # True quando pressionado

    # se ambos pressionados, ignora (ou escolhe nenhum)
    if left and not right:
        dir_input = "LEFT"
    elif right and not left:
        dir_input = "RIGHT"
    else:
        dir_input = None

# ==========================
# CARRO E OBSTÁCULOS
# ==========================
CAR_WIDTH_PX = 22
CAR_HEIGHT_PX = 14
CAR_SPEED = 6  

OBSTACLE_WIDTH_PX = 33
OBSTACLE_HEIGHT_PX = 12
OBSTACLE_BASE_SPEED = 3
OBSTACLE_SPEED = OBSTACLE_BASE_SPEED


car_x_px = WIDTH // 2
car_y_px = HEIGHT - CAR_HEIGHT_PX - 2

obstacles_px = []
score = 0
rankings = []

# limites da estrada (onde o carro pode andar)
ROAD_LEFT = WIDTH // 4
ROAD_RIGHT = 3 * WIDTH // 4 - CAR_WIDTH_PX

# ==========================
# DESENHO
# ==========================
def draw_road():
    # Fundo (grama ou acostamento)
    display.set_pen(display.create_pen(0, 150, 0))  # verde escuro (grama)
    display.clear()

    # Estrada
    display.set_pen(ROAD_COLOR)
    display.rectangle(WIDTH//4, 0, WIDTH//2, HEIGHT)

    # Faixa central tracejada animada
    display.set_pen(LINE_COLOR)
    for i in range(0, HEIGHT, 20):
        display.rectangle(WIDTH//2-1, int((i + score*OBSTACLE_SPEED) % HEIGHT), 2, 10)

    # Bordas da pista (faixas brancas laterais)
    display.set_pen(TEXT_COLOR)
    display.rectangle(WIDTH//4 - 2, 0, 2, HEIGHT)       # borda esquerda fora da estrada
    display.rectangle(3*WIDTH//4 + 1, 0, 2, HEIGHT)         # borda direita fora da estrada

def draw_car():
    display.set_pen(CAR_COLOR)
    display.rectangle(int(car_x_px), int(car_y_px), CAR_WIDTH_PX, CAR_HEIGHT_PX)
    # luzes frontais
    display.set_pen(display.create_pen(255,255,0))
    display.rectangle(int(car_x_px), int(car_y_px), 4, 4)
    display.rectangle(int(car_x_px) + CAR_WIDTH_PX - 4, int(car_y_px), 4, 4)

def draw_obstacles():
    for ox, oy in obstacles_px:
        display.set_pen(OBSTACLE_COLOR)
        display.rectangle(int(ox), int(oy), OBSTACLE_WIDTH_PX, OBSTACLE_HEIGHT_PX)
        display.set_pen(BORDER_COLOR)
        display.rectangle(int(ox), int(oy), OBSTACLE_WIDTH_PX, 1)
        display.rectangle(int(ox), int(oy), 1, OBSTACLE_HEIGHT_PX)
        display.rectangle(int(ox) + OBSTACLE_WIDTH_PX - 1, int(oy), 1, OBSTACLE_HEIGHT_PX)
        display.rectangle(int(ox), int(oy) + OBSTACLE_HEIGHT_PX - 1, OBSTACLE_WIDTH_PX, 1)

def draw_score():
    display.set_pen(TEXT_COLOR)
    display.text(f"Score", 5, 5, WIDTH//2)
    display.text(f"{score}", 10, 20, WIDTH)

# ==========================
# FUNÇÕES DE JOGO
# ==========================
def reset_game():
    global car_x_px, car_y_px, obstacles_px, score
    car_x_px = WIDTH // 2
    car_y_px = HEIGHT - CAR_HEIGHT_PX - 2
    obstacles_px.clear()
    score = 0
    display.set_pen(BG)
    display.clear()

def add_to_rankings(s):
    global rankings
    rankings.append(s)
    rankings.sort(reverse=True)
    if len(rankings) > 5:
        rankings.pop()

def display_rankings():
    global rankings
    display.set_pen(BG)
    display.clear()
    display.set_pen(TEXT_COLOR)
    display.text("RANKINGS", WIDTH//4, 10, WIDTH//2)
    for i, s in enumerate(rankings):
        display.text(f"{i+1}. {s}", WIDTH//4, 30 + i*20, WIDTH//2)
    display.update()
    time.sleep(3)

def update_obstacles():
    global obstacles_px
    # move obstáculos para baixo (pixel a pixel)
    for i in range(len(obstacles_px)):
        x, y = obstacles_px[i]
        obstacles_px[i] = (x, y + OBSTACLE_SPEED)
    # remove fora da tela
    obstacles_px[:] = [o for o in obstacles_px if o[1] < HEIGHT]
    # adiciona novos obstáculos aleatórios (dentro da estrada)
    # chance de spawn cresce lentamente (máximo de 8%)
    spawn_chance = 0.02 + min(score / 10000, 0.06)

    # controla número de obstáculos simultâneos
    num_obs = 1
    if score > 2000 and random.random() < 0.3:
        num_obs = 2  # 30% de chance de 2 obstáculos após 2000 pontos

    # adiciona obstáculos com base na chance calculada
    if random.random() < spawn_chance:
        for _ in range(num_obs):
            ox = random.randint(ROAD_LEFT, 3 * WIDTH // 4 - OBSTACLE_WIDTH_PX)
            obstacles_px.append((ox, 0))


def check_collision():
    global car_x_px, car_y_px, obstacles_px
    for ox, oy in obstacles_px:
        if (car_x_px < ox + OBSTACLE_WIDTH_PX) and (car_x_px + CAR_WIDTH_PX > ox):
            if (car_y_px < oy + OBSTACLE_HEIGHT_PX) and (car_y_px + CAR_HEIGHT_PX > oy):
                return True
    return False

# ==========================
# LOOP PRINCIPAL (sem Timer)
# ==========================
def game_tick():
    global score, car_x_px, obstacles_px, OBSTACLE_SPEED

    # movimentação
    if dir_input == "LEFT" and car_x_px > ROAD_LEFT:
        car_x_px -= CAR_SPEED
    elif dir_input == "RIGHT" and car_x_px < ROAD_RIGHT:
        car_x_px += CAR_SPEED

    if check_collision():
        add_to_rankings(score)
        display_rankings()
        reset_game()
        return

    # aumenta velocidade gradualmente
    OBSTACLE_SPEED = OBSTACLE_BASE_SPEED + (score / 100.0)

    update_obstacles()
    score += 1

    draw_road()
    draw_car()
    draw_obstacles()
    draw_score()
    display.update()


# controle de frame ~30 FPS usando ticks_ms
last_tick = time.ticks_ms()
FRAME_MS = 16

while True:
    now = time.ticks_ms()
    if time.ticks_diff(now, last_tick) >= FRAME_MS:
        last_tick = now
        game_tick()
    read_buttons()
    # pequeno atraso para liberar CPU e melhorar debounce simples
    time.sleep(0.01)
    OBSTACLE_SPEED += 1  # aumenta a velocidade dos obstáculos com o tempo


