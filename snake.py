import pygame
import time
import random

pygame.init() # initialise the pygame module

# rgb color
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,155,0)

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height)) # make screen of game
pygame.display.set_caption("Slither") # st the caption of game
icon = pygame.image.load('apple.png')
pygame.display.set_icon(icon)

img = pygame.image.load('snake_head.png')
appleimg = pygame.image.load('apple.png')

# pygame.display.flip() # it will flip(update) whole surface
# pygame.display.update() # it will update some thing in screen if we pass parameter otherwise update entire surface will be updated

clock = pygame.time.Clock() # to insert some delay for FPS
AppleThickness = 30
block_size = 20
FPS = 30
direction = "right"
smallfont = pygame.font.SysFont("comicsansms", 25) # it is the size of font of our system
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 80)

def pause():
    paused = True
    message_to_screen("Paused", black, -100, "large")
    message_to_screen("Press c to continue or q to quit", black, 25, "small")
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                quit()
            if (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_c):
                    paused = False
                elif (event.key == pygame.K_q):
                    pygame.quit()
                    quit()
        # gameDisplay.fill(white)
        clock.tick(5)

def score(score):
    text = smallfont.render("Score: "+str(score), True, black)
    gameDisplay.blit(text, [0,0])

def randAppleGen():
    randAppleX = round((random.randrange(0,display_width-AppleThickness))/block_size)*block_size
    randAppleY = round((random.randrange(0,display_height-AppleThickness))/block_size)*block_size
    return randAppleX, randAppleY

def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        
        gameDisplay.fill(white)
        message_to_screen("Welcom to Slither", green, -100, "large")
        message_to_screen("The objective of game is to eat red apples", black, -30, "small")
        message_to_screen("The more apple you eat, the longer you get", black, 10, "small")
        message_to_screen("If you run into yourself or the edges, you die", black, 50, "small")
        message_to_screen("Press C to play, P to pause or Q to quit", black, 180, "small")
        pygame.display.update()
        clock.tick(15)
        
def snake(block_size,snakelist):
    if (direction == "right"):
        head = pygame.transform.rotate(img, 270)
    if (direction == "left"):
        head = pygame.transform.rotate(img, 90)
    if (direction == "up"):
        head = pygame.transform.rotate(img, 0) # rotation of image
    if (direction == "down"):
        head = pygame.transform.rotate(img, 180)
    
    gameDisplay.blit(head, (snakelist[-1][0],snakelist[-1][1]))
    for XnY in snakelist[:-1]:
        pygame.draw.rect(gameDisplay, green, [XnY[0],XnY[1],block_size,block_size]) # draw the rectangle

def text_objects(text, color, size):
    if (size == "small"):
        textSurface = smallfont.render(text, True, color)
    elif (size == "medium"):
        textSurface = medfont.render(text, True, color)
    elif (size == "large"):
        textSurface = largefont.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_to_screen(msg, color, y_displace=0, size="small"):
    textSurf, textRect = text_objects(msg, color, size)
    # screen_text = font.render(msg, True, color)
    # gameDisplay.blit(screen_text, [display_width/2, display_height/2])
    textRect.center = (display_width/2),(display_height/2)+y_displace
    gameDisplay.blit(textSurf, textRect)

# game loop
def gameLoop():
    global direction
    direction = "right"
    gameExit = False
    gameOver = False
    lead_x = display_width/2
    lead_y = display_height/2
    lead_x_change = 10
    lead_y_change = 0
    snakeList = []
    snakeLength = 1
    randAppleX, randAppleY = randAppleGen()
    while not gameExit:
        if gameOver == True:
            message_to_screen("Game over", red, y_displace=-50, size="large")
            message_to_screen("Press C to play again and Q to quit", black, 50, size="medium")
            pygame.display.update()
        
        while gameOver == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOver = False
                    gameExit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()
            
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                gameExit = True
            if (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_LEFT):
                    direction = "left"
                    lead_x_change = -block_size
                    lead_y_change = 0
                elif (event.key == pygame.K_RIGHT):
                    direction = "right"
                    lead_x_change = block_size
                    lead_y_change = 0
                elif (event.key == pygame.K_UP):
                    direction = "up"
                    lead_x_change = 0
                    lead_y_change = -block_size
                elif (event.key == pygame.K_DOWN):
                    direction = "down"
                    lead_x_change = 0
                    lead_y_change = block_size
                elif (event.key == pygame.K_p):
                    pause()
            

        if (lead_x >= display_width or lead_x < 0 or lead_y < 0 or lead_y >= display_height):
            gameOver = True

        lead_x += lead_x_change
        lead_y += lead_y_change
        
        gameDisplay.fill(white) # change the background to white
        # pygame.draw.rect(gameDisplay, red, [randAppleX, randAppleY, AppleThickness, AppleThickness]) # draw the appl
        gameDisplay.blit(appleimg, (randAppleX, randAppleY))
        
        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)
        if (len(snakeList) > snakeLength):
            del snakeList[0]
        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                gameOver = True
            
        snake(block_size, snakeList)
        score(snakeLength-1)
        # gameDisplay.fill(red, rect=[200,200,50,50])
        pygame.display.update()
        # if (lead_x == randAppleX and lead_y == randAppleY):
            # randAppleX = round((random.randrange(0,display_width-block_size))/block_size)*block_size
            # randAppleY = round((random.randrange(0,display_height-block_size))/block_size)*block_size
            # snakeLength += 1
        # if (lead_x >= randAppleX and lead_x <= randAppleX+AppleThickness):
            # if (lead_y >= randAppleY and lead_y <= randAppleY+AppleThickness):
                # randAppleX = round((random.randrange(0,display_width-block_size))/block_size)*block_size
                # randAppleY = round((random.randrange(0,display_height-block_size))/block_size)*block_size
                # snakeLength += 1
        if (lead_x > randAppleX and lead_x < randAppleX+AppleThickness) or (lead_x+block_size > randAppleX and lead_x+block_size < randAppleX+AppleThickness):
            if (lead_y > randAppleY and lead_y < randAppleY+AppleThickness) or (lead_y+block_size > randAppleY and lead_y+block_size < randAppleY+AppleThickness):
                randAppleX, randAppleY = randAppleGen()
                snakeLength += 1
            
        clock.tick(FPS) # setting 30 FPS
    pygame.quit() # quit the pygame
    quit() # exit out of python

game_intro()
gameLoop()
