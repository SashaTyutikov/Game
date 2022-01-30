import pygame
from random import randrange as rnd

WIDTH, HEIGHT = 1200, 800
fps = 60
# настрйоки плотформы
stage_w = 330
stage_h = 35
stage_speed = 15
stage = pygame.Rect(WIDTH // 2 - stage_w // 2, HEIGHT - stage_h - 10, stage_w, stage_h)
# настрйоки мячика
ball_radius = 20
ball_speed = 7
ball_rect = int(ball_radius * 2 ** 0.5)
ball = pygame.Rect(rnd(ball_rect, WIDTH - ball_rect), HEIGHT // 2, ball_rect, ball_rect)
detect_x = 1
detect_y = -1
# настройки квадратов
block_list = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(4)]
color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(10) for j in range(4)]

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
# фон
image = pygame.image.load('2.jpg').convert()
image = pygame.transform.scale(image, (WIDTH, HEIGHT))


def detect_collision(detect_x, detect_y, ball, rect):
    if detect_x > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if detect_y > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top

    if abs(delta_x - delta_y) < 10:
        detect_x, detect_y = -detect_x, -detect_y
    elif delta_x > delta_y:
        detect_y = -detect_y
    elif delta_y > delta_x:
        detect_x = -detect_x
    return detect_x, detect_y


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    screen.blit(image, (0, 0))
    # все предметы
    [pygame.draw.rect(screen, color_list[color], block) for color, block in enumerate(block_list)]
    pygame.draw.rect(screen, pygame.Color('black'), stage)
    pygame.draw.circle(screen, pygame.Color('white'), ball.center, ball_radius)
    # движение мячика
    ball.x += ball_speed * detect_x
    ball.y += ball_speed * detect_y
    # столкновение справа и слева
    if ball.centerx < ball_radius or ball.centerx > WIDTH - ball_radius:
        detect_x = -detect_x
    # столкновение сверху
    if ball.centery < ball_radius:
        detect_y = -detect_y
    # столкновение с плотформой
    if ball.colliderect(stage) and detect_y > 0:
        detect_x, detect_y = detect_collision(detect_x, detect_y, ball, stage)
    # столкновение с квадратами
    hit_index = ball.collidelist(block_list)
    if hit_index != -1:
        hit_rect = block_list.pop(hit_index)
        hit_color = color_list.pop(hit_index)
        detect_x, detect_y = detect_collision(detect_x, detect_y, ball, hit_rect)

    # конец игры
    if ball.bottom > HEIGHT:
        print('ВЫ ПРОИГРАЛИ!')
        exit()
    elif not len(block_list):
        print('ВЫ ВЫЙГРАЛИ!!!')
        exit()
    # движение
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and stage.left > 0:
        stage.left -= stage_speed
    if key[pygame.K_RIGHT] and stage.right < WIDTH:
        stage.right += stage_speed
    # экран
    pygame.display.flip()
    clock.tick(fps)