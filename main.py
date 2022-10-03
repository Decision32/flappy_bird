import pygame
import time
from random import randint

pygame.mixer.pre_init(44100, -16, 2, 256)
pygame.init()
pygame.mixer.init()

width, height = 800, 600 # размеры окна
fps = 60

window = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

pygame.display.set_caption('Flappy Bird by Oleg Mishin') # наименование окна
pygame.display.set_icon(pygame.image.load('images/favicon.ico')) # иконка игры

font1 = pygame.font.Font(None, 35)
font2 = pygame.font.Font(None, 40)

imgbg = pygame.image.load('images/bg.png')
imgbird = pygame.image.load('images/spr_b3_strip4.png')
imgPT = pygame.image.load('images/spr_block.png')
imgPB = pygame.image.load('images/pipe-red.png')

pygame.mixer.music.load('sounds/phon.mp3')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

sndFall = pygame.mixer.Sound('sounds/audio_hit.wav')
sndPoint = pygame.mixer.Sound('sounds/point.wav')
sndWing = pygame.mixer.Sound('sounds/sfx_wing.ogg')
sndWon = pygame.mixer.Sound('sounds/game-won.wav')
pygame.mixer.set_num_channels(7)

py, sy, ay = height // 2, 0, 0
player = pygame.Rect(width // 3, py, 34, 24)
frame = 0

state = 'start'
timer = 10

pipes = []
bges = []
pipesScores = []

pipeSpeed = 3
piperandSize = 200
piperandPos = height // 2

bges.append(pygame.Rect(0, 0, 841, 600))

lives = 3
scores = 0
startsnd = 0

play = True
while play:
     for event in pygame.event.get():
          if event.type == pygame.quit:
              play = False
     press = pygame.mouse.get_pressed()
     keys = pygame.key.get_pressed()
     click = press[0] or keys[pygame.K_SPACE]
     if timer > 0:
         timer -= 1
     frame = (frame + 0.2) % 4
     for i in range(len(bges)-1, -1, -1):
         bg = bges[i]
         bg.x -= pipeSpeed // 2
         if bg.right < 0:
              bges.remove(bg)
         if bges[-1].right <= width:
             bges.append(pygame.Rect(bges[-1].right, 0, 841, 600))
     for i in range(len(pipes)-1, -1, -1):
         pipe = pipes[i]
         pipe.x -= pipeSpeed
         if pipe.right < 0:
              pipes.remove(pipe)
              if pipe in pipesScores:
                  pipesScores.remove(pipe)
     if state == 'start':
         if click and not timer and not len(pipes):
             state = 'play'
         py += (height // 2 - py) * 0.1
         player.y = py
     elif state == 'play':
         if click:
             ay = -2
             if time.time() - startsnd > 0.3: #задержка для воспроизведения звука взмаха крыльев
                startsnd = time.time()
                pygame.mixer.find_channel(4).play(sndWing)
         else:
             ay = 0
         py += sy
         sy = (sy + ay + 1) * 0.98
         player.y = py
         if not len(pipes) or pipes[len(pipes)-1].x <width -200:
             pipes.append(pygame.Rect(width, 0, 52, piperandPos - piperandSize//2))
             pipes.append(pygame.Rect(width, piperandPos + piperandSize//2, 52, height - piperandPos - piperandSize//2))
             piperandPos += randint(-100, 100)
             if piperandPos < piperandSize:
                 piperandPos = piperandSize
             elif piperandPos > height - piperandSize:
                 piperandPos = height - piperandSize
         if player.top < 0 or player.bottom > height:
             state = 'fall'
         for pipe in pipes:
             if player.colliderect(pipe):
                 state = 'fall'
             if pipe.right < player.left and pipe not in pipesScores:
                 pipesScores.append(pipe)
                 scores += 0.5
                 pygame.mixer.find_channel(3).play(sndPoint)
                 pipeSpeed = 3 + scores // 25
     elif state == 'fall': # при падении
         pygame.mixer.find_channel(2).play(sndFall)
         sy, ay = 0, 0
         piperandPos = height // 2

         lives -= 1
         if lives:
             state = 'start'
             timer = 60
         else: # при проигрыше
             state = 'game over'
             timer = 180
     else:
         py += sy
         sy = (sy + ay + 1) * 0.98
         player.y = py

         if not timer:
             play = False
# отрисовка
     for bg in bges:
         window.blit(imgbg, bg)
     for pipe in pipes:
         if not pipe.y:
            rect = imgPT.get_rect(bottomleft = pipe.bottomleft)
            window.blit(imgPT, rect)
         else:
             rect = imgPB.get_rect(topleft=pipe.topleft)
             window.blit(imgPB, rect)
     image = imgbird.subsurface(34 * int(frame), 0, 34, 24)
     image = pygame.transform.rotate(image, -sy * 2)
     window.blit(image, player)

     text = font1.render('Очки: ' + str(int(scores)), 0, pygame.Color ('black'))
     window.blit(text, (10, 10))

     text = font2.render('Жизни: ' + str(lives), 0, pygame.Color('red'))
     window.blit(text, (10, height -40))

     pygame.display.update()
     clock.tick(fps)

pygame.quit()
