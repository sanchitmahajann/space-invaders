import pygame
import random
import math
from pygame import mixer

pygame.init()

win = pygame.display.set_mode((800, 600))

pygame.display.set_caption('Space Invaders by Sanchit')
bgimage = pygame.image.load('background.jpg')
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

mixer.music.load('background.wav')
mixer.music.play(-1)
#Player
player_img = pygame.image.load('space-invaders-spaceship.png')
playerx = 368
playery = 500
playerx_change = 0

#Enemy
enemy_img = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []
enemycount = 6

for i in range(enemycount):
	enemy_img.append(pygame.image.load('alien-3.png'))
	enemyx.append(random.randint(0, 736))
	enemyy.append(random.randint(25, 125))
	enemyx_change.append(3)
	enemyy_change.append(40)

#Bullet
bullet_img = pygame.image.load('laser.png')
bulletx = 0
bullety = 480
bullety_change = 10
bullet_state = 'ready'

score_value = 0
font = pygame.font.Font('CaviarDreams.ttf', 32)
textx = 10
texty = 10

gameover_font = pygame.font.Font('CaviarDreams_Bold.ttf', 70)

def gameover_txt():
	gameover_text = gameover_font.render("GAME OVER", True, (255, 0, 0))
	win.blit(gameover_text, (200, 200))


def showscore(x, y):
	score = font.render('Score: ' + str(score_value), True, (255, 255, 255))
	win.blit(score, (x, y))

def player(x, y):
	win.blit(player_img, (x, y))

def enemy(x, y, i):
	win.blit(enemy_img[i], (x, y))

def fire(x, y):
	global bullet_state
	bullet_state = 'fire'
	win.blit(bullet_img, (x + 30, y + 10))

def cancollide(enemyx, enemyy, bulletx, bullety):
	distance = math.hypot(enemyx - bulletx, enemyy - bullety)
	if distance < 27:
		return True
	else:
		return False

# Game Loop
run = True
while run:
	win.fill((0, 0, 0))
	win.blit(bgimage, (0,0))
	

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.KEYDOWN:
			if event.key == ord('a'):
				playerx_change = -4
			if event.key == ord('d'):
				playerx_change = 4
			if event.key == pygame.K_SPACE:
				if bullet_state == 'ready':
					bullet_sound = mixer.Sound('shoot.wav')
					bullet_sound.play()
					bulletx = playerx
					fire(playerx, bullety)


		if event.type == pygame.KEYUP:
			if event.key == ord('a') or event.key == ord('d'):
				playerx_change = 0

	playerx += playerx_change
	
	if playerx <= 0:
		playerx = 0
	elif playerx >= 736:
		playerx = 736

	for i in range(enemycount):
		if enemyy[i] > 400:
			for j in range(enemycount):
				enemyy[j] = 2000
			gameover_txt()
			break


		enemyx[i] += enemyx_change[i]
		if enemyx[i] <= 0:
			enemyx_change[i] = 3
			enemyy[i] += enemyy_change[i]
		elif enemyx[i] >= 736:
			enemyx_change[i] = -3
			enemyy[i] += enemyy_change[i]

		collision = cancollide(enemyx[i], enemyy[i], bulletx, bullety)
		if collision:
			explosion_sound = mixer.Sound('explosion.wav')
			explosion_sound.play()
			bullety = 480
			bullet_state = 'ready'
			score_value += 1

			if score_value > 40:
				enemycount += 1
			
			enemyx[i] = random.randint(0, 736)
			enemyy[i]= random.randint(25, 125)

		enemy(enemyx[i], enemyy[i], i)

	#Bullet Movement
	if bullety <= 0:
		bullety = 480
		bullet_state = 'ready'

	if bullet_state is 'fire':
		fire(bulletx, bullety)
		bullety -= bullety_change


	player(playerx, playery)
	showscore(textx, texty)
	pygame.display.update()