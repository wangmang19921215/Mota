import sys
import pygame
import time
import json
from enum import Enum

icons = {
	"npc_0" : "resources/NPC/仙女 0.png",
	"npc_1" : "resources/NPC/老人 0.png",
	"npc_2" : "resources/NPC/商人 0.png",
	"npc_3" : "resources/NPC/盜賊 0.png"
}

class o_type(Enum):
	scene 	= -1
	ground 	= 0
	wall 	= 1
	monster = 2
	npc 	= 3

	up_floor 	= 4
	down_floor 	= 5

	door = 6
	barrier = 7

class d_type(Enum):
	yellow = 0
	blue   = 1
	red    = 2
	magic  = 3

class npc_type(Enum):
	fairy	 = 0
	trader   = 1
	old_man  = 2
	thief    = 3

parameter = {"max_level":0}

parameter['level'] 		= 1
parameter['health'] 	= 1000
parameter['attack'] 	= 10
parameter['defence'] 	= 10
parameter['agility'] 	= 1
parameter['money'] 		= 0

parameter['0_key']  = 1
parameter['1_key']  = 1
parameter['2_key']  = 0

class text_object():
	def __init__(self, screen, text, location):
		self.text = text
		self.location = location
		self.screen = screen
	def blitme(self):
		self.screen.blit(self.text, (self.location[0] * 48 + 336, self.location[1] * 48 + 96))

class conversation():
	def __init__(self, screen):
		self.in_conversation = False
		self.screen = screen
		self.objects = []

	def print_word(self, name, text, path = ""):
		self.in_conversation = True
		self.objects.append(object(self.screen, "resources/字/msg_box.png", 13, 15, o_type = o_type.scene, multiple = 1))

		if path != "":
			self.objects.append(object(self.screen, icons[path], 1.75, 11.25, o_type = o_type.scene, multiple = 1.5))

		font = pygame.font.Font("resources/GenRyuMinTW_Regular.ttf", 32)
		self.objects.append(text_object(self.screen, font.render(name , True , (255,255,255)), (2, 9.5)))
		font = pygame.font.Font("resources/GenRyuMinTW_Regular.ttf", 20)
		self.objects.append(text_object(self.screen, font.render(text , True , (255,255,255)), (1, 10.5)))

		font = pygame.font.Font("resources/GenRyuMinTW_Regular.ttf", 14)
		self.objects.append(text_object(self.screen, font.render("按任意鍵退出" , True , (255,255,255)), (11, 11.5)))

	def end_conversation(self):
		self.in_conversation = False

def cost(item, amount):
	if parameter[item] >= amount:
		parameter[item] -= amount
		return True
	return False

class object():
	def __init__(self, screen, path, x , y,dynamic = False, o_type = o_type.ground, multiple = 1.5, arg = {}, npc_script = None):
		self.screen = screen

		if path != "":
			self.visible = True
			self.dynamic = dynamic
			if dynamic:
				self.counter = 0
				self.path = path
				image = pygame.image.load(path % 0)
				rect = image.get_rect()
				image = pygame.transform.scale(image, (int(rect.width * multiple), int(rect.height * multiple)))
				self.rect = image.get_rect()
			else:
				self.image = pygame.image.load(path)
				self.rect = self.image.get_rect()
				self.image = pygame.transform.scale(self.image, (int(self.rect.width * multiple), int(self.rect.height * multiple)))
				self.rect = self.image.get_rect()
		else:
			self.visible = False

		self.o_type = o_type

		self.location = [x,y]

		self.npc_script = npc_script

		self.init2(arg)

	def init2(self, arg):
		pass

	def trigger(self):
		if self.o_type == o_type.wall:
			return False
		return True

	def blitme(self):
		if self.visible:
			self.rect.centerx = self.location[0] * 48 + 336 - self.rect.width / 2
			self.rect.bottom = self.location[1] * 48 + 96 - self.rect.height
			if self.dynamic:
				image = pygame.transform.scale(pygame.image.load(self.path % self.counter),(self.rect.width, self.rect.height))

				self.screen.blit(image, self.rect)

				self.counter += 1
				if self.counter == 4:
					self.counter = 0
			else:

				self.screen.blit(self.image, self.rect)


class npc(object):
	def init2(self, arg):
		global conversation_control

		self.npc_script.conversation_control = conversation_control

		self.name = arg["name"]
		if self.npc_script != None:
			self.npc_script.__init__(self.npc_script, arg)

	def trigger(self):
		if self.npc_script != None:
			self.npc_script.trigger(self.npc_script)
			return False

class door(object):
	def init2(self, parameter):
		self.d_type = parameter['d_type']
		self.parameter = parameter
		self.is_open = False
	def trigger(self):
		if not self.is_open:
			if not self.d_type == 3:
				if cost(str(self.d_type) + "_key", 1):
					self.is_open = True
					self.count   = 0
					return False
			else:
				return magic_door()
		else:
			return not self.visible

	def magic_door():
		pass

	def blitme(self):
		if self.visible and not self.is_open:
			self.rect.centerx = self.location[0] * 48 + 336 - self.rect.width / 2
			self.rect.bottom = self.location[1] * 48 + 96 - self.rect.height

			self.screen.blit(self.image, self.rect)
		elif self.visible:
			self.count += 1
			if self.count == 4:
				self.visible = False
				return
			path = "resources/地形/門/" + ["黃","藍","紅","魔法"][self.d_type] + " %s.png" % self.count
			self.image = pygame.image.load(path)
			self.rect = self.image.get_rect()
			self.image = pygame.transform.scale(self.image, (int(self.rect.width * 1.5), int(self.rect.height * 1.5)))
			self.rect = self.image.get_rect()

			self.rect.centerx = self.location[0] * 48 + 336 - self.rect.width / 2
			self.rect.bottom = self.location[1] * 48 + 96 - self.rect.height

			self.screen.blit(self.image, self.rect)

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
				elif self.scene[i - 1][j - 1] == 2:
					self.objects.append(object(screen, "resources/地形/wall 2.png", j, i, o_type = o_type.wall))
				elif self.scene[i - 1][j - 1] == 3:
					self.objects.append(object(screen, "resources/地形/wall 3.png", j, i, o_type = o_type.wall))
				elif self.scene[i - 1][j - 1] == 4:
					self.down_floor = [j, i]
					if not data['config']['prev_floor'] == None:
						self.objects.append(object(screen, "resources/地形/down_floor.png", j, i, o_type = o_type.down_floor))
				elif self.scene[i - 1][j - 1] == 5:
					self.up_floor = [j, i]
					if not data['config']['next_floor'] == None:
						self.objects.append(object(screen, "resources/地形/up_floor.png", j, i, o_type = o_type.up_floor))
				elif type(self.scene[i - 1][j - 1]) == dict:
					module = __import__("scripts." + self.scene[i - 1][j - 1]['program'])
					exec("global NPC; NPC = module." + self.scene[i - 1][j - 1]['program'] + ".NPC")
					path = "resources/NPC/" + ["仙女", "老人", "商人", "盜賊"][self.scene[i - 1][j - 1]["npc_type"]] + " %s.png"

					self.objects.append(npc(screen, path , j, i,dynamic = True, o_type = o_type.npc, arg = self.scene[i - 1][j - 1], npc_script = NPC))

				elif 62 >= self.scene[i - 1][j - 1] >= 60:
					self.objects.append(door(screen, "resources/地形/門/%s 0.png" % (["黃","藍","紅"][self.scene[i - 1][j - 1] - 60]), j, i, o_type = o_type.door, arg = {"d_type": self.scene[i - 1][j - 1] - 60}))


	def blitme(self):
		for i in self.objects:
			i.blitme()


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

		self.location = [1,1]
		self.speed = 3

	def blitme(self):
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
				if not i.trigger():
					return
				

		self.location[0] += self.vector[0] 
		self.location[1] +=  self.vector[1] 


def produce_number(screen, number,x ,y):
	c = []
	for i,j in enumerate(number):
		c.append(object(screen, "resources/字/%s.png" % j, x + 0.5 * i, y - 0.025, o_type = o_type.scene, multiple = 0.22))
	return c

def check_events(player, objs, conversation_control):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		if not conversation_control.in_conversation:
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
		else:
			player.vector = [0, 0, player.vector[2]]
			if event.type == pygame.KEYDOWN:
				conversation_control.end_conversation()

	player.move(objs)


def update_screen(screen, objects):
	screen.fill((30,30,30))
	for i in objects:
		i.blitme()
	pygame.display.flip()


pygame.init()
screen  = pygame.display.set_mode((int(576 * 1.5 + 144), int(480 * 1.5)))

conversation_control = conversation(screen)

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
	check_events(warrior, scenes + this_floor.objects, conversation_control)
	information = (produce_number(screen, str(parameter['level']), -2.1, 1) + 
		   produce_number(screen, str(parameter['health']), -3, 2) + 
		   produce_number(screen, str(parameter['attack']), -3, 3) + 
		   produce_number(screen, str(parameter['defence']), -3, 4) + 
		   produce_number(screen, str(parameter['agility']), -3, 5) +
		   produce_number(screen, str(parameter['0_key']), -3, 8.5) +
		   produce_number(screen, str(parameter['1_key']), -3, 9.5) +
		   produce_number(screen, str(parameter['2_key']), -3, 10.5) +
		   produce_number(screen, str(parameter['money']), -3, 11.5))

	update_screen(screen, grounds + information + scenes + [this_floor, warrior] + (conversation_control.objects if conversation_control.in_conversation else []))
	time.sleep(0.085)
