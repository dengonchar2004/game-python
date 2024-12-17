import pygame
from random import randint
pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60

window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
imPT = pygame.image.load('pygamgr/pipe_top.png')
imPB = pygame.image.load('pygamgr/pipe_bottom.png')
pygame.display.set_caption('Space craft')
pygame.display.set_icon(pygame.image.load('pygamgr/NLa-Photoroom.png'))

font1 = pygame.font.Font(None, 35)
font2 = pygame.font.Font(None, 80)

im = pygame.image.load('pygamgr/found.png')
imNLO = pygame.image.load('pygamgr/NLOgg.png')
pygame.mixer.music.load('pygamgr/mmp.mp3')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)
varFall = pygame.mixer.Sound('pygamgr/crash.mp3')

py, sy, ay = HEIGHT // 2, 0, 0
player = pygame.Rect(WIDTH // 3, py, 90, 37)
frame = 0

state = 'start'
timer = 20

pipes = []
city = []
pipeScores = []

pipeSpeed = 3
pipeGateS = 230
pipeGateP = HEIGHT // 2

city.append(pygame.Rect(0, 0, 800, 600))

lives = 3
scores = 0


play = True
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False


    
            
    press = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()
    click = press[0] or keys[pygame.K_SPACE]
    if timer > 0:
        timer -= 1
        
    frame = (frame + 0.2) % 4
    pipeSpeed = 3 + scores // 100

    for i in range(len(city)-1, -1, -1):
        ci = city[i]
        ci.x -= pipeSpeed // 2
        
        if ci.right < 0:
             city.remove(ci)

             
        if city[len(city)-1].right <= WIDTH:
            city.append(pygame.Rect(city[len(city)-1].right, 0, 800, 600))
        
    for i in range(len(pipes)-1, -1, -1):
        pipe = pipes[i]
        pipe.x -= pipeSpeed

        if pipe.right < 0:
            pipes.remove (pipe)
            if pipe in pipeScores:
                pipeScores.remove (pipe)

            
    
    if state == 'start':
        if click and timer == 0 and len(pipes) == 0:
           state = 'play'
           
        py += (HEIGHT // 2 - py) * 0.1
        player.y = py
    elif state == 'play':
        if click:
            ay = -2
        else:
            ay = 0
            
        py += sy
        sy = (sy + ay + 1) * 0.98
        player.y = py

        if len (pipes) == 0 or pipes[len(pipes)-1].x < WIDTH - 200:
            pipes.append (pygame.Rect(WIDTH, 0, 50, pipeGateP - pipeGateS // 2))
            pipes.append (pygame.Rect(WIDTH, pipeGateP + pipeGateS // 2 , 50, HEIGHT - pipeGateP + pipeGateS // 2))
            pipeGateP += randint (-100, 100)
            if pipeGateP < pipeGateS:
                pipeGateP = pipeGateS
            elif pipeGateP > HEIGHT - pipeGateS:
                pipeGateP = HEIGHT - pipeGateS
                 

        if player.top < 0 or player.bottom > HEIGHT:
            state = 'fall'
        for pipe in pipes:
            if player. colliderect (pipe):
                state = 'fall'

            if pipe.right < player.left and pipe not in pipeScores:
                pipeScores.append (pipe)
                scores += 5
                
    elif state == 'fall':
        varFall.play()
        sy, ay = 0, 0
        pipeGateP = HEIGHT // 2
        state = 'start'
        timer = 50

        lives -= 1
        if lives > 0:
            state = 'start'
            timer = 50
        else:
            state = 'game over'
            timer = 100
    else:
        py += sy
        sy = (sy + ay + 1) * 0.98
        player.y = py
        if timer == 0:
            play = False


   
    for ci in city:
        window.blit(im, ci)
    for pipe in pipes:
        pygame.draw.rect(window, pygame.Color('grey'), pipe)
        if pipe.y == 0:
            rect = imPT.get_rect(bottomleft = pipe.bottomleft)
            window.blit(imPT, rect)
        else:
            rect = imPB.get_rect(topleft = pipe.topleft)
            window.blit(imPB, rect)
        
    NLO = imNLO.subsurface(0, 0, 90, 37)
    window.blit(NLO, player)
    
    window.blit(imNLO,player)
    text = font1.render('Очки: ' + str(scores), 0, pygame.Color('white'))
    window.blit(text, (10, 10))

    text = font2.render('Жизни: ' + str(lives), 0, pygame.Color('white'))
    window.blit(text, (10, HEIGHT - 60))
    
    

    
    pygame.display.update()
    clock.tick (FPS)

pygame.quit()   
