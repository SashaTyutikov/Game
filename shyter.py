# coding: utf8
import pygame, sys
import time

# window
window = pygame.display.set_mode([400, 400])
pygame.display.set_caption('Шутер')

screen = pygame.Surface([400, 440])
score = pygame.Surface([400,40])




class Sprite:
    def __init__(self, xpos, ypos, filename):
        self.x = xpos
        self.y = ypos
        self.bitmap = pygame.image.load(filename)
    def render(self):
        screen.blit(self.bitmap,(self.x, self.y))


def Intersect(s1_x, s2_x, s1_y, s2_y):
    if ((s1_x>s2_x-40) and (s1_x<s2_x+40) and (s1_y>s2_y-40) and (s1_y<s2_y+40)):
        return 1
    else:
        return 0

def load_menu():
    items = [(160, 140, 'Game', (0, 0, 0), (255, 0, 0), 0),
    (160, 210, 'Quit', (0, 0, 0), (255, 0, 0), 1)]

    pygame.key.set_repeat(0, 0)
    pygame.mouse.set_visible(True)

    done = False
    item = 0
    while not done:
        screen.fill([131, 35, 35])
        score.fill([131, 35, 35])

        for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if item == 0:
                        done = True
                        pygame.mixer.music.load('lasttrek.wav')
                        pygame.mixer.music.play(-1)
                    elif item == 1:
                        pygame.quit()
                        sys.exit()

        pointer = pygame.mouse.get_pos()
        for i in items:
            if pointer[0]>i[0] and pointer[0]<i[0]+155 and pointer[1]>i[1] and pointer[1]<i[1]+50:
                item = i[5]

        for i in items:
            if item == i[5]:
                screen.blit(myFont.render(i[2], 1, i[4]), [i[0], i[1]-40])
            else:
                screen.blit(myFont.render(i[2], 1, i[3]), [i[0], i[1]-40])

        window.blit(score, [0, 0])
        window.blit(screen, [0, 40])
        pygame.display.flip()

def you_win():
    done = False
    while not done:
        screen.fill([131, 35, 35])
        score.fill([131, 35, 35])

        for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        win = myFont.render("YOU WIN", 1, [255, 0, 0])
        screen.blit(win, [150, 150])
        window.blit(score, [0, 0])
        window.blit(screen, [0, 40])
        pygame.display.flip()

def loser():
    done = False
    while not done:
        screen.fill([131, 35, 35])
        score.fill([131, 35, 35])

        for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        win = myFont.render("YOU LOSER", 1, [255, 0, 0])
        screen.blit(win, [150, 150])
        window.blit(score, [0, 0])
        window.blit(screen, [0, 40])
        pygame.display.flip()

# герой
hero = Sprite(200, 320, 'archer.png')
hero.right = True
hero.up = True
# враг
enemy = Sprite(2, 5, 'zlodei.gif')
enemy.right = True
enemy.step = 1
# оружие
weapon = Sprite(-10, 350, 'arrow.png')
weapon.push = False
weapon.n = 5


pygame.font.init()
myFont = pygame.font.Font('murderer.ttf', 38)
boomFont = pygame.font.Font('Nosifer.ttf', 48)
scaleFont = pygame.font.Font(None, 12)

pygame.mixer.init()
sound = pygame.mixer.Sound('boom.wav')
load_menu()
running = True
pygame.key.set_repeat(1,1)
counter = 0


while running:
    # обработка событий
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running  = False
        # движение героя
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                load_menu()
                pygame.key.set_repeat(1, 1)
                pygame.mouse.set_visible(False)
            if e.key == pygame.K_LEFT:
                if hero.x > 10:
                    hero.x -= 1
            if e.key == pygame.K_RIGHT:
                if hero.x < 350:
                    hero.x += 1
            if e.key == pygame.K_UP:
                if hero.y > 200:
                    hero.y -= 1
            if e.key == pygame.K_DOWN:
                if hero.y < 350:
                    hero.y += 1
            # спуск курка
            if e.key == pygame.K_SPACE:
                if weapon.push == False:
                    weapon.x = hero.x + 15
                    weapon.y = hero.y
                    weapon.push = True
                    if weapon.n > 0:
                        weapon.n -= 1

    # задайте фоновый цвет
    screen.fill([131, 35, 35])
    score.fill([51, 0, 51])

    # движение врага
    if enemy.right == True:
        enemy.x += enemy.step
        if enemy.x > 360:
            enemy.right = False
    else:
        enemy.x -= enemy.step
        if enemy.x < 0:
            enemy.right = True

    # движение оружия
    if weapon.y < 30:
        weapon.push = False
        if weapon.n == 0:
            loser()

    if weapon.push == False:
        weapon.y = 350
        weapon.x = -100
    else:
        weapon.y -= 1

    boom = boomFont.render("CHPOK", 1, [180, 0, 0])

    # попадание во врага
    if Intersect(weapon.x, enemy.x, weapon.y, enemy.y):
        sound.play()
        weapon.push = False
        enemy.step += 0.1
        counter+=1
        if counter == 3:
            you_win()
            pygame.mixer.music.stop('lasttrek.wav')
        else:
            screen.blit(boom, [110, 140])
            window.blit(screen, [0, 30])
            pygame.display.flip()
            time.sleep(0.4)



    # отображение персонажей
    weapon.render()
    hero.render()
    enemy.render()

    # отображение текста
    text = myFont.render("Skore: ", 1, [255, 0, 0])
    n = myFont.render(str(counter), 1, [255, 0, 0])
    score.blit(text, [0, 0])
    score.blit(n, [120, 0])
    score.blit(myFont.render("Cartridges: " + str(weapon.n), 1, [255, 0, 0]), [200, 0])


    # отображение окна

    window.blit(score, [0, 0])
    window.blit(screen, [0, 40])
    pygame.display.flip()
    pygame.time.delay(5)

pygame.quit()