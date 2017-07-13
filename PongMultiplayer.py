#By: Jorge Santos
#Let paddle 1 and 2 be key controlled

import pygame, sys
from pygame.locals import*

#Number of frames per second
#Change this number to speed up or slow down your game
FPS = 70
INCREASESPEED = 5

#Global Variables to be used through our prgogram
WINDOWWIDTH = 780
WINDOWHEIGHT = 360
LINETHICKNESS = 10
PADDLESIZE = int(WINDOWHEIGHT / 6)
PADDLEOFFSET = 40

BLACK   = (0  ,0  ,0  )
WHITE   = (255,255,255)
GRASS   = (0, 128,0 )

def drawArena():
    DISPLAYSURF.fill(GRASS)
    pygame.draw.rect(DISPLAYSURF, WHITE, ((0,0),(WINDOWWIDTH,WINDOWHEIGHT)), int(LINETHICKNESS*2))
    pygame.draw.circle(DISPLAYSURF, WHITE, (int(WINDOWWIDTH/2), int(WINDOWHEIGHT/2)), int(WINDOWWIDTH/8),int(LINETHICKNESS/4))
    pygame.draw.line(DISPLAYSURF, WHITE, ((WINDOWWIDTH/2),0),((WINDOWWIDTH/2),WINDOWHEIGHT), int(LINETHICKNESS/4))


def drawPaddle(paddle):
    if paddle.bottom > WINDOWHEIGHT - LINETHICKNESS:
        paddle.bottom = WINDOWHEIGHT - LINETHICKNESS
    elif paddle.top < LINETHICKNESS:
        paddle.top = LINETHICKNESS
    pygame.draw.rect(DISPLAYSURF, WHITE, paddle)

def drawBall(ball):
    pygame.draw.rect(DISPLAYSURF, WHITE, ball)

#moves the ball returns new position
def moveBall(ball, ballDirX, ballDirY):
    ball.x += (ballDirX * INCREASESPEED)
    ball.y += (ballDirY * INCREASESPEED)
    return ball

#Checks for a collision with a wall, and 'bounces' ball off it.
#Returns new direction
def checkEdgeCollision(ball, ballDirX, ballDirY):
    if (
       ball.top == (LINETHICKNESS) or
       ball.bottom == (WINDOWHEIGHT - LINETHICKNESS)
       ):
        ballDirY = ballDirY * -1
    if (
        ball.left == (LINETHICKNESS) or
        ball.right == (WINDOWWIDTH - LINETHICKNESS)
        ):
        ballDirX = ballDirX * -1
    #return a tuple to be unpacked and assigned on the other side
    return ballDirX, ballDirY

def checkHitBall(ball, paddle1, paddle2, ballDirX):
    if (
        ballDirX == -1 and paddle1.right == ball.left and
        paddle1.top < ball.top and paddle1.bottom > ball.bottom
        ):
        return -1
    elif (
        ballDirX == 1 and paddle2.left == ball.right and
        paddle2.top < ball.top and paddle2.bottom > ball.bottom
        ):
        return -1
    else: return 1

def checkPointScored(paddle1, ball, score, ballDirX):
    #reset points if left wall is hit
    if ball.left == LINETHICKNESS:
        return 0
    #1 point for hitting the ball
    elif (
        ballDirX == -1 and paddle1.right == ball.left
        and paddle1.top < ball.top and paddle1.bottom > ball.bottom
        ):
        score += 1
        return score
    #5 points for beating the other paddle
    elif ball.right == WINDOWWIDTH - LINETHICKNESS:
        score += 5
        return score 
    #if no points scored, return score unchanged
    else: return score

def displayScore(score):
    resultSurf = BASICFONT.render('Score = %s' %(score), True, WHITE)
    resultRect = resultSurf.get_rect()
    resultRect.topleft = (WINDOWWIDTH -150, 25)
    DISPLAYSURF.blit(resultSurf, resultRect)
def checkHighScore(score, highScore):
    if highScore >= score:
        return highScore
    elif highScore < score:
        highScore == score
        return score
def displayHighScore(highScore):
    resultSurf = BASICFONT.render('High Score = %s' %(highScore), True, WHITE)
    resultRect = resultSurf.get_rect()
    resultRect.topleft = (50, 25)
    DISPLAYSURF.blit(resultSurf, resultRect)

#Main function
def main():
    PADDLESPEED1 = 0
    PADDLESPEED2 = 0
    pygame.init()
    global DISPLAYSURF
    ##Font information
    global BASICFONT, BASICFONTSIZE
    BASICFONTSIZE = 20
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    pygame.display.set_caption('Pong') 

    #Initiate variable and set
    ballX = WINDOWWIDTH/2 - LINETHICKNESS/2
    ballY = WINDOWHEIGHT/2 - LINETHICKNESS/2

    playerOnePosition = (WINDOWHEIGHT - PADDLESIZE) /2
    playerTwoPosition = (WINDOWHEIGHT - PADDLESIZE) /2

    score = 0
    highScore = 0

    paddle1 = pygame.Rect(PADDLEOFFSET,playerOnePosition, LINETHICKNESS,PADDLESIZE)
    paddle2 = pygame.Rect(WINDOWWIDTH - PADDLEOFFSET - LINETHICKNESS, playerTwoPosition, LINETHICKNESS,PADDLESIZE)
    ball = pygame.Rect(ballX, ballY, LINETHICKNESS, LINETHICKNESS)
    ballDirY = -1
    ballDirX = -1

    drawArena()
    drawPaddle(paddle1)
    drawPaddle(paddle2)
    drawBall(ball)


    pygame.mouse.set_visible(0) # make cursor invisible

    while True:  #main game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_w:
                    PADDLESPEED1 = -5
                if event.key == K_s:
                    PADDLESPEED1 = 5
                if event.key == K_o:
                    PADDLESPEED2 = -5
                if event.key == K_l:
                    PADDLESPEED2 = 5
            if event.type == KEYUP:
                if event.key == K_w or event.key == K_s:
                    PADDLESPEED1 = 0
                if event.key == K_o or event.key == K_l:
                    PADDLESPEED2 = 0
                    
        
        #Drawws the starting position of the Arena
        drawArena()
        drawPaddle(paddle1)
        drawPaddle(paddle2)
        drawBall(ball)
        
        #right after you draw the ball and right before you
        #update the display makke sure to move the ball by a factor of
        #ballDirX, ballDirY
        ball = moveBall(ball, ballDirX, ballDirY)
        ballDirX, ballDirY = checkEdgeCollision(ball, ballDirX, ballDirY)
        highScore = checkHighScore(score, highScore)
        score = checkPointScored(paddle1, ball, score, ballDirX)
        ballDirX = ballDirX * checkHitBall(ball, paddle1, paddle2, ballDirX)
        paddle1.y += PADDLESPEED1
        paddle2.y += PADDLESPEED2

        displayScore(score)
        displayHighScore(highScore)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__=='__main__':
    main()
