import sys
import pygame
import time
from enum import Enum

level   = 1
health  = 1000
attack  = 10
defence = 10
agility = 1

def produce_number(screen, number,x ,y):
	c = []
	for i,j in enumerate(number):
		c.append(object(screen, "resources/字/%s.png" % j, x + 0.5 * i, y - 0.025, o_type = o_type.scene, multiple = 0.22))
	return c

class o_type(Enum):
	scene 	= -1
	ground 	= 0
	wall 	= 1
	monster = 2

class object():
	def __init__(self, screen, path, x , y, o_type = o_type.ground, multiple = 1.5):
		self.screen = screen

		self.image = pygame.image.load(path)
		self.rect = self.image.get_rect()
		self.image = pygame.transform.scale(self.image, (int(self.rect.width * multiple), int(self.rect.height * multiple)))
		self.rect = self.image.get_rect()

		self.visible = True
		self.type = o_type

		self.location = [x,y]

	def trigger(self):
		pass

	def blitme(self):

		self.rect.centerx = self.location[0] * 48 + 336 - self.rect.width / 2
		self.rect.bottom = self.location[1] * 48 + 96 - self.rect.height

		self.screen.blit(self.image, self.rect)

class player(object):
	def __init__(self, screen):
		self.screen = screen

		self.counter = 0
		self.images = [[],[],[],[]]
		for i in range(4):
			self.images[0].append(pygame.transform.scale(pygame.image.load('resources/勇者/right %s.png' % i), (48, 48)))
			self.images[1].append(pygame.transform.scale(pygame.image.load('resources/勇者/left %s.png' % i), (48, 48)))
			self.images[2].append(pygame.transform.scale(pygame.image.load('resources/勇者/down %s.png' % i), (48, 48)))
			self.images[3].append(pygame.transform.scale(pygame.image.load('resources/勇者/up %s.png' % i), (48, 48)))
		self.rect = self.images[0][0].get_rect()
		self.vector = [0,0,2]
		#put spaceship on the bottom of window

		self.location = [1,1]
		self.speed = 3

	def blitme(self):
		#buld the spaceship at the specific location

		self.rect.centerx = self.location[0] * 48 + 336 - self.rect.width/2
		self.rect.bottom = self.location[1] * 48 + 96 - self.rect.height

		self.screen.blit(self.images[self.vector[2]][self.counter], self.rect)

	def move(self, walls, monsters, items):
		if self.vector[:2] != [0,0]:
			self.counter += 1
			if self.counter == 4:
				self.counter = 0
		for i in walls:
			if i.location == [self.location[0] + self.vector[0], self.location[1] + self.vector[1]]:
				i.trigger()
				return

		self.location[0] += self.vector[0] 
		self.location[1] +=  self.vector[1] 


def check_events(player, walls, monsters, items):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RIGHT:
				player.vector = [1, 0, 0]
			elif event.key == pygame.K_LEFT:
				player.vector = [-1,0, 1]
			elif event.key == pygame.K_DOWN:
				player.vector = [0, 1, 2]
			elif event.key == pygame.K_UP:
				player.vector = [0,-1, 3]
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_RIGHT:
				player.vector = [0, player.vector[1], player.vector[2]]
			elif event.key == pygame.K_LEFT:
				player.vector = [0, player.vector[1], player.vector[2]]
			elif event.key == pygame.K_DOWN:
				player.vector = [player.vector[0], 0, player.vector[2]]
			elif event.key == pygame.K_UP:
				player.vector = [player.vector[0], 0, player.vector[2]]
	player.move(walls, monsters, items)


def update_screen(screen, objects):
	screen.fill((30,30,30))
	for i in objects:
		i.blitme()
	pygame.display.flip()

def run_game():
	pygame.init()

	screen  = pygame.display.set_mode((int(576 * 1.5 + 96), int(448 * 1.5)))

	scenes 		= []
	walls		= []
	grounds 	= []
	monsters	= []
	items 		= []

	for i in range(-6,0):
		scenes.append(object(screen, "resources/地形/wall 3.png", i,  0, o_type = o_type.scene))
		scenes.append(object(screen, "resources/地形/wall 3.png", i, 13, o_type = o_type.scene))
		scenes.append(object(screen, "resources/地形/wall 3.png", i, 8, o_type = o_type.scene))

	for i in range(14):
		walls.append(object(screen, "resources/地形/wall 3.png", i,  0, o_type = o_type.wall))
		walls.append(object(screen, "resources/地形/wall 3.png", i, 13, o_type = o_type.wall))
		walls.append(object(screen, "resources/地形/wall 3.png", 0,  i, o_type = o_type.wall))
		walls.append(object(screen, "resources/地形/wall 3.png", 13, i, o_type = o_type.wall))
		scenes.append(object(screen, "resources/地形/wall 3.png", -6, i, o_type = o_type.scene))

	scenes.append(object(screen, "resources/勇者/down 0.png", -4.5, 2, o_type = o_type.scene))
	scenes.append(object(screen, "resources/字/等级.png", -2.5, 1.25, o_type = o_type.scene,multiple = 1.2))

	scenes.append(object(screen, "resources/字/体力.png", -3.5, 3, o_type = o_type.scene))
	scenes.append(object(screen, "resources/字/攻击.png", -3.5, 4, o_type = o_type.scene))
	scenes.append(object(screen, "resources/字/防御.png", -3.5, 5, o_type = o_type.scene))
	scenes.append(object(screen, "resources/字/敏捷.png", -3.5, 6, o_type = o_type.scene))


	for i in range(-6,13):
		for j in range(0,13):
			grounds.append(object(screen, "resources/地形/ground.png", i, j, o_type = o_type.ground))

	warrior = player(screen)
	pygame.display.set_caption("Mota")

	while True:
		check_events(warrior, walls, monsters, items)
		information = (produce_number(screen, str(level), -2.1, 1.5) + 
			   produce_number(screen, str(health), -3, 3) + 
			   produce_number(screen, str(attack), -3, 4) + 
			   produce_number(screen, str(defence), -3, 5) + 
			   produce_number(screen, str(agility), -3, 6))

		update_screen(screen, grounds + information + scenes + walls + items + monsters + [warrior])
		time.sleep(0.10)

run_game()