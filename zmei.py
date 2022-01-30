
import pygame, time, random

pygame.init()

pygame.mixer.music.load('slugfest-2.wav')
pygame.mixer.music.play(-1)
# добавление змейки
def snake(headname, bodyname, snakeList, snakeHead, lead_x, lead_y):
    for XnY in snakeList:
        gameDisplay.blit(pygame.image.load(bodyname),(XnY[0],XnY[1]))
        gameDisplay.blit(pygame.image.load(headname),(lead_x,lead_y))
# окошко
def message_to_screen(msg,color,x,y):
    screen_text = font.render(msg, True, color)
    gameDisplay.blit(screen_text, [x,y])

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)

display_width = 600
display_height = 600
block_size = 40
# счёт
font = pygame.font.SysFont(None, 32)
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Snake")

gameExit = False

lead_x = (display_width-40)/2
lead_y = (display_height-40)/2
lead_x_change = 0
lead_y_change = 0

snakeList = []
snakeLength = 1
score = 0

appleX = round(random.randrange(block_size, display_width-block_size)/block_size)*block_size
appleY = round(random.randrange(block_size, display_height-block_size)/block_size)*block_size

while not gameExit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                lead_x_change = -block_size
                lead_y_change = 0
            elif event.key == pygame.K_RIGHT:
                lead_x_change = block_size
                lead_y_change = 0
            elif event.key == pygame.K_DOWN:
                lead_y_change = block_size
                lead_x_change = 0
            elif event.key == pygame.K_UP:
                lead_y_change = -block_size
                lead_x_change = 0

    if lead_x >= display_width-block_size or lead_x <0 or lead_y >= display_height-block_size or lead_y <0:
        gameDisplay.fill(white)
        message_to_screen(''.join(["Game over! Score: ",str(score)]), white, 200,260)
        pygame.display.update()
        time.sleep(2)
        gameExit = True

    # движение змейки
    lead_x += lead_x_change
    lead_y += lead_y_change
    snakeHead = [lead_x, lead_y]
    snakeList.append(snakeHead)
    if len(snakeList) > snakeLength:
        del snakeList[0]

    # столкновение змейки с самой собой
    for eachSegment in snakeList[:-1]:
        if eachSegment == snakeHead:
            gameDisplay.blit(pygame.image.load('bg.jpg'), (0, 0))
            message_to_screen(''.join(["Game over! Score: ",str(score)]), white, 200,260)
            pygame.display.update()
            time.sleep(2)
            gameExit = True

    # столкновение с ЯБЛОКОМ
    if lead_x == appleX and lead_y == appleY:
        appleX = round(random.randrange(block_size, display_width-block_size)/block_size)*block_size
        appleY = round(random.randrange(block_size, display_height-block_size)/block_size)*block_size
        snakeLength += 1
        score += 1
    
    # фон
    gameDisplay.blit(pygame.image.load('bg.png'), (0, 0))
    # отображение количества очков
    message_to_screen(''.join(["Score: ",str(score)]), white, 10,10)
    # отображение яблока
    gameDisplay.blit(pygame.image.load('apple.png'),(appleX, appleY))
    # отображение змейки
    snake('head.png', 'body.png', snakeList, snakeHead, lead_x, lead_y)
    pygame.display.update()
    pygame.time.delay(150)

pygame.quit()