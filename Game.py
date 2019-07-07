import sys
import pygame
import time
import json
from enum import Enum

parameter = {"max_level":0}

parameter['level'] 		= 1
parameter['health'] 	= 1000
parameter['attack'] 	= 10
parameter['defence'] 	= 10
parameter['agility'] 	= 1
parameter['money'] 		= 0

parameter['yellow_key']  = 1
parameter['blue_key']  = 0
parameter['red_key']  = 0

class o_type(Enum):
	scene 	= -1
	ground 	= 0
	wall 	= 1
	monster = 2
	npc 	= 3

	up_floor 	= 4
	down_floor 	= 5

class floor():
	def __init__(self, screen, path):
		data = open(path)
		data = json.load(data)
		
		self.name  = data["name"]
		self.scene = data["scene"]
		self.allow_teleport = data['config']['allow_teleport']
		self.objects 	= []
		self.up_floor   = [0, 0]
		self.down_floor = [0, 0]

		for i in range(1,14):
			for j in range(1,14):
				if self.scene[i - 1][j - 1] == 1:
					self.objects.append(object(screen, "resources/地形/wall.png", j, i, o_type = o_type.wall))
				elif self.scene[i - 1][j - 1] == 4:
					self.down_floor = [j, i]
					if not data['config']['is_lowest']:
						self.objects.append(object(screen, "resources/地形/down_floor.png", j, i, o_type = o_type.down_floor))
				elif self.scene[i - 1][j - 1] == 5:
					self.up_floor = [j, i]
					if not data['config']['is_highest']:
						self.objects.append(object(screen, "resources/地形/up_floor.png", j, i, o_type = o_type.up_floor))


	def blitme(self):
		for i in self.objects:
			i.blitme()

def produce_number(screen, number,x ,y):
	c = []
	for i,j in enumerate(number):
		c.append(object(screen, "resources/字/%s.png" % j, x + 0.5 * i, y - 0.025, o_type = o_type.scene, multiple = 0.22))
	return c

class object():
	def __init__(self, screen, path, x , y, o_type = o_type.ground, multiple = 1.5):
		self.screen = screen

		self.image = pygame.image.load(path)
		self.rect = self.image.get_rect()
		self.image = pygame.transform.scale(self.image, (int(self.rect.width * multiple), int(self.rect.height * multiple)))
		self.rect = self.image.get_rect()

		self.visible = True
		self.o_type = o_type

		self.location = [x,y]

	def trigger(self):
		if self.o_type == o_type.wall:
			return True

	def blitme(self):

		if self.visible:
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

	def move(self, objs):
		if self.vector[:2] != [0,0]:
			self.counter += 1
			if self.counter == 4:
				self.counter = 0
		for i in objs:
			if i.location == [self.location[0] + self.vector[0], self.location[1] + self.vector[1]]:
				if i.trigger():
					return
				

		self.location[0] += self.vector[0] 
		self.location[1] +=  self.vector[1] 


def check_events(player, objs):
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
	player.move(objs)


def update_screen(screen, objects):
	screen.fill((30,30,30))
	for i in objects:
		i.blitme()
	pygame.display.flip()

def run_game():
	pygame.init()

	screen  = pygame.display.set_mode((int(576 * 1.5 + 144), int(480 * 1.5)))

	grounds 	= []
	scenes 		= []

	for i in range(-6,0):
		scenes.append(object(screen, "resources/地形/wall 3.png", i,  0, o_type = o_type.scene))
		scenes.append(object(screen, "resources/地形/wall 3.png", i, 14, o_type = o_type.scene))
		scenes.append(object(screen, "resources/地形/wall 3.png", i, 7, o_type = o_type.scene))

	for i in range(15):
		scenes.append(object(screen, "resources/地形/wall 3.png", i,  0, o_type = o_type.wall))
		scenes.append(object(screen, "resources/地形/wall 3.png", i, 14, o_type = o_type.wall))
		scenes.append(object(screen, "resources/地形/wall 3.png", 0,  i, o_type = o_type.wall))
		scenes.append(object(screen, "resources/地形/wall 3.png", 14, i, o_type = o_type.wall))
		scenes.append(object(screen, "resources/地形/wall 3.png", -6, i, o_type = o_type.scene))

	scenes.append(object(screen, "resources/勇者/down 0.png", -4.5, 1.25, o_type = o_type.scene))
	scenes.append(object(screen, "resources/字/等级.png", -2.5, 0.75, o_type = o_type.scene,multiple = 1.2))

	scenes.append(object(screen, "resources/字/体力.png", -3.5, 2, o_type = o_type.scene))
	scenes.append(object(screen, "resources/字/攻击.png", -3.5, 3, o_type = o_type.scene))
	scenes.append(object(screen, "resources/字/防御.png", -3.5, 4, o_type = o_type.scene))
	scenes.append(object(screen, "resources/字/敏捷.png", -3.5, 5, o_type = o_type.scene))
	scenes.append(object(screen, "resources/道具/16.png", -4.5, 9, o_type = o_type.scene))
	scenes.append(object(screen, "resources/道具/17.png", -4.5, 10, o_type = o_type.scene))
	scenes.append(object(screen, "resources/道具/18.png", -4.5, 11, o_type = o_type.scene))
	scenes.append(object(screen, "resources/道具/31.png", -4.6, 12, o_type = o_type.scene))


	for i in range(-6,15):
		for j in range(0,15):
			grounds.append(object(screen, "resources/地形/ground.png", i, j, o_type = o_type.ground))

	warrior = player(screen)
	pygame.display.set_caption("Mota")

	this_floor = floor(screen, "floor/demo.json")
	warrior.location = this_floor.down_floor
	while True:
		check_events(warrior, scenes + this_floor.objects)
		information = (produce_number(screen, str(level), -2.1, 1) + 
			   produce_number(screen, str(parameter['health']), -3, 2) + 
			   produce_number(screen, str(parameter['attack']), -3, 3) + 
			   produce_number(screen, str(parameter['defence']), -3, 4) + 
			   produce_number(screen, str(parameter['agility']), -3, 5) +
			   produce_number(screen, str(parameter['yellow_key']), -3, 8.5) +
			   produce_number(screen, str(parameter['blue_key']), -3, 9.5) +
			   produce_number(screen, str(parameter['red_key']), -3, 10.5) +
			   produce_number(screen, str(parameter['money']), -3, 11.5))

		update_screen(screen, grounds + information + scenes + [this_floor, warrior])
		time.sleep(0.10)

run_game()