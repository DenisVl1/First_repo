import random
import pygame

from pygame.constants import QUIT,K_DOWN,K_UP,K_LEFT,K_RIGHT
pygame.init()
FPS = pygame.time.Clock()
HEIGHT = 800
WIDTH = 1200

FONT = pygame.font.SysFont('Verdana', 20)
COLOR_WHITE = (255, 255, 255)
COLOR_BLUE = (0, 0, 255)
COLOR_GREEN = (0, 255, 0)
COLOR_BLACK = (0, 0, 0)

BG=pygame.transform.scale(pygame.image.load('background.png'),(WIDTH,HEIGHT))
bg_X1=0
bg_X2=BG.get_width()
bg_move = 3



main_display = pygame.display.set_mode((WIDTH, HEIGHT))

player=pygame.image.load('player.png').convert_alpha()
player_size=(100,40)

#player_rect = player.get_rect()

player_move_down=[0,4]
player_move_top=[0,-4]
player_move_right=[4,0]
player_move_left=[-4,0]
player_rect=pygame.Rect(0,300,*player_size)

def create_enemy():
    enemy=pygame.image.load('enemy.png').convert_alpha()
    enemy_size=enemy.get_size()
    enemy_rect=pygame.Rect(WIDTH,random.randint(enemy.get_height(),HEIGHT-enemy.get_height()),*enemy_size)
    enemy_move=[random.randint(-8,-4),0]
    return [enemy,enemy_rect,enemy_move]
def create_bonus():
    bonus=pygame.image.load('bonus.png').convert_alpha()
    bonus_size=bonus.get_size()
    bonus_rect=pygame.Rect(random.randint(bonus.get_width(),WIDTH-bonus.get_width()),0,*bonus_size)
    bonus_move=[0,random.randint(4,8)]
    return [bonus,bonus_rect,bonus_move]

CREATE_ENEMY=pygame.USEREVENT + 1 
pygame.time.set_timer(CREATE_ENEMY, 1500)
enemies=[]

CREATE_BONUS=pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 1000)
bonuses=[]
score = 0

playing = True
while playing:
    FPS.tick(150)
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type==CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type==CREATE_BONUS:
            bonuses.append(create_bonus())

   # main_display.fill(COLOR_BLACK)

    bg_X1-=bg_move
    bg_X2-=bg_move

    if bg_X1 < -BG.get_width():
        bg_X1=BG.get_width()
    if bg_X2 < -BG.get_width(): 
        bg_X2=BG.get_width()

    main_display.blit(BG,(bg_X1,0))
    main_display.blit(BG,(bg_X2,0))

    main_display.blit(player,player_rect)


    keys=pygame.key.get_pressed()
    if keys[K_DOWN] and player_rect.bottom<HEIGHT:
        player_rect=player_rect.move(player_move_down)
    if keys[K_UP] and player_rect.top>=0:
        player_rect=player_rect.move(player_move_top)
    if keys[K_LEFT] and player_rect.left>=0:
        player_rect=player_rect.move(player_move_left)
    if keys[K_RIGHT] and player_rect.left<=WIDTH:
        player_rect=player_rect.move(player_move_right)

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0],enemy[1])

        if player_rect.colliderect(enemy[1]):
          playing=False
            

    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0],bonus[1])
        
        if player_rect.colliderect(bonus[1]):
           bonuses.pop(bonuses.index(bonus))
           score+=1

    main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH-50,20))

   

    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].left <0:
            enemies.pop(enemies.index(enemy))
    for bonus in bonuses:
        if bonus[1].bottom > HEIGHT:
            bonuses.pop(bonuses.index(bonus))