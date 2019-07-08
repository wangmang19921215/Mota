import sys
import pygame
import time
import json
from random import random as rnd
from enum import Enum

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

	item = 8


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

icons = {
	"npc_0" : "resources/NPC/仙女 0.png",
	"npc_1" : "resources/NPC/老人 0.png",
	"npc_2" : "resources/NPC/商人 0.png",
	"npc_3" : "resources/NPC/盜賊 0.png",
	"player": "resources/勇者/down 0.png"
}

monsters = {}
monster = json.load(open("data/monsters_data.json"))
for i in monster['monster']:
	monsters[i['id']] = i

parameter = {"highest_floor": 0, "this_floor": 0}

floors = {}

parameter['level'] 		= 1
parameter['health'] 	= 1000
parameter['attack'] 	= 10
parameter['defence'] 	= 10
parameter['agility'] 	= 1
parameter['money'] 		= 0

parameter['0_key']  = 1
parameter['1_key']  = 1
parameter['2_key']  = 1


class text_object():
	def __init__(self, screen, text, location):
		self.text = text
		self.location = location
		self.screen = screen
	def blitme(self):
		self.screen.blit(self.text, (self.location[0] * 48 + 336, self.location[1] * 48 + 96))

class fight():
	def __init__(self, screen):
		self.screen = screen
		self.objects = []
		self.in_fighting = False

	def fight_with(self, monster):
		global this_floor, grounds, information, scenes,warrior
		self.in_fighting = True
		path, hp, atk, dfs, agl, name, money = monster.path, monster.health, monster.attack, monster.defence, monster.agility, monster.name, monster.money
		
		font = pygame.font.Font("resources/GenRyuMinTW_Regular.ttf", 24)
		
		counter = 0
		while self.in_fighting and ((hp > 0 and parameter['health'] > 0) or counter <= 3):
			self.objects = []

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				if event.type == pygame.KEYDOWN and event.key == ord("q"):
					self.quit()

			if counter == 3:
				if rnd() > (agl - parameter['agility'] / 3)/100:
					hp -= max(parameter['attack'] - dfs, 0)
					if rnd() < (parameter['agility'] - agl / 3)/100:
						hp -= max(parameter['attack'] - dfs, 0)
					hp = max(hp, 0)

			if counter == 6:
				if rnd() > (parameter['agility'] - agl / 3)/100:
					parameter['health'] -= max(atk - parameter['defence'], 0)
					if rnd() < (agl - parameter['agility'] / 3)/100:
						parameter['health'] -= max(atk - parameter['defence'], 0)
					parameter['health'] = max(parameter['health'], 0)
				counter = 0

			self.objects.append(object(self.screen, "resources/字/fgt_box.png", 13, 13, o_type = o_type.scene, multiple = 1))
			self.objects.append(object(self.screen, monster.path , 4, 6, dynamic = True, o_type = o_type.scene, multiple = 3))
			self.objects.append(object(self.screen, icons['player'], 11, 6, o_type = o_type.scene, multiple = 3))
			self.objects.append(text_object(self.screen, font.render(str(name) , True , (255,255,255)), (2, 1.3)))
			self.objects.append(text_object(self.screen, font.render(str("勇者") , True , (255,255,255)), (9.5, 1.3)))
			self.objects.append(text_object(self.screen, font.render("HP： " + str(hp) , True , (255,255,255)), (2, 4.5)))
			self.objects.append(text_object(self.screen, font.render("HP： " + str(parameter['health']) , True , (255,255,255)), (9, 4.5)))
			self.objects.append(text_object(self.screen, font.render("ATK： " + str(atk) , True , (255,255,255)), (2, 5.2)))
			self.objects.append(text_object(self.screen, font.render("ATK： " + str(parameter['attack']) , True , (255,255,255)), (9, 5.2)))
			self.objects.append(text_object(self.screen, font.render("DFS： " + str(dfs) , True , (255,255,255)), (2, 5.9)))
			self.objects.append(text_object(self.screen, font.render("DFS： " + str(parameter['defence']) , True , (255,255,255)), (9, 5.9)))


			update_screen(self.screen, grounds + information + scenes + [warrior] + self.objects + this_floor.objects)
			counter += 1
			time.sleep(0.075)
		self.objects = []
		if not self.in_fighting:
			return

		self.in_fighting = False
		if hp == 0:
			parameter['money'] += money
			monster.valid = False
			monster.visible = False
			return

		time.sleep(3)

		self.screen.fill((0,0,0))

		object(self.screen, "resources/字/loss.png", 8, 8, o_type = o_type.scene, multiple = 1).blitme()
		pygame.display.flip()
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()


	def quit(self):
		self.in_fighting = False
		self.objects = []

class conversation():
	def __init__(self, screen):
		self.in_conversation = False
		self.screen = screen
		self.objects = []
		self.queue = []
	def print_word(self, name, text, path = ""):
		if self.in_conversation:
			self.queue.append((name, text, path))
			return

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

		time.sleep(0.05)
	def end_conversation(self, key = -1):
		self.in_conversation = False

		if self.queue != []:
			arg = self.queue[0]
			del self.queue[0]
			self.print_word(arg[0], arg[1], arg[2])
		else:
			self.objects = []

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
			self.valid   = True
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


class monster(object):
	def init2(self, arg):
		global monsters
		monster_data = monsters[arg["m_type"]]
		self.name   = monster_data['name']
		self.health = monster_data["hp"]
		self.attack = monster_data["atk"]
		self.defence = monster_data["dfs"]
		self.agility = monster_data["agility"]
		self.money = monster_data["money"]

	def trigger(self):
		global fight_system, warrior
		warrior.vector = [0, 0, warrior.vector[2]]
		warrior.counter = 0

		fight_system.fight_with(self)


class npc(object):
	def init2(self, arg):
		global conversation_control

		self.npc_script.conversation_control = conversation_control

		self.name = arg["name"]
		if self.npc_script != None:
			self.npc_script.status = self
			self.npc_script.__init__(self.npc_script, arg)

	def trigger(self):
		if self.npc_script != None:
			global warrior
			warrior.vector = [0, 0, warrior.vector[2]]
			warrior.counter = 0

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
		data = json.load(open("data/" + path + ".json"))

		self.scene = data["scene"]
		self.config = data['config']
		self.this_floor = data['floor']
		self.objects 	= []
		self.up_floor   = (0, 0)
		self.down_floor = (0, 0)

		for i in range(1,14):
			for j in range(1,14):
				if self.scene[i - 1][j - 1] == 1:
					self.objects.append(object(screen, "resources/地形/wall.png", j, i, o_type = o_type.wall))

				elif self.scene[i - 1][j - 1] == 2:
					self.objects.append(object(screen, "resources/地形/wall 2.png", j, i, o_type = o_type.wall))

				elif self.scene[i - 1][j - 1] == 3:
					self.objects.append(object(screen, "resources/地形/wall 3.png", j, i, o_type = o_type.wall))

				elif self.scene[i - 1][j - 1] == 4:
					self.down_floor = (j, i)
					if not data['config']['prev_floor'] == None:
						self.objects.append(object(screen, "resources/地形/down_floor.png", j, i, o_type = o_type.down_floor))

				elif self.scene[i - 1][j - 1] == 5:
					self.up_floor = (j, i)
					if not data['config']['next_floor'] == None:
						self.objects.append(object(screen, "resources/地形/up_floor.png", j, i, o_type = o_type.up_floor))

				elif type(self.scene[i - 1][j - 1]) == dict:
					module = __import__("scripts." + self.scene[i - 1][j - 1]['program'])
					exec("global NPC; NPC = module." + self.scene[i - 1][j - 1]['program'] + ".NPC")
					path = "resources/NPC/" + ["仙女", "老人", "商人", "盜賊"][self.scene[i - 1][j - 1]["npc_type"]] + " %s.png"

					self.objects.append(npc(screen, path , j, i,dynamic = True, o_type = o_type.npc, arg = self.scene[i - 1][j - 1], npc_script = NPC))

				elif 62 >= self.scene[i - 1][j - 1] >= 60:
					self.objects.append(door(screen, "resources/地形/門/%s 0.png" % (["黃","藍","紅"][self.scene[i - 1][j - 1] - 60]), j, i, o_type = o_type.door, arg = {"d_type": self.scene[i - 1][j - 1] - 60}))
				
				elif 71 >= self.scene[i - 1][j - 1] >= 70:
					self.objects.append(object(screen, "resources/地形/" + (["lava","star"][self.scene[i - 1][j - 1] - 70]) + " %s.png", j, i, dynamic = True, o_type = o_type.wall))
				
				elif 900 > self.scene[i - 1][j - 1] >= 800:
					self.objects.append(item(screen, "resources/道具/%s.png" % str(self.scene[i - 1][j - 1] - 800), j, i, o_type = o_type.item, arg = {'i_type': self.scene[i - 1][j - 1] - 800}))
				elif self.scene[i - 1][j - 1] >= 2000:
					self.objects.append(monster(screen, "resources/怪物/" + str(self.scene[i - 1][j - 1] % 1000) + ",%s.png", j, i, dynamic = True, o_type = o_type.monster, arg = {'m_type': self.scene[i - 1][j - 1] % 1000}))

	def blitme(self):
		for i in self.objects:
			i.blitme()

class item(object):
	def init2(self, arg):
		self.i_type = arg['i_type']

	def trigger(self):
		if self.i_type == 0:
			parameter['attack'] += 2
		if self.i_type == 1:
			parameter['defence'] += 2
		if self.i_type == 2:
			parameter['agility'] += 2
		if self.i_type == 4:
			parameter['health'] += 200
		if self.i_type == 5:
			parameter['health'] += 400
		if self.i_type == 15:
			parameter['health'] *= 2
		if self.i_type == 16:
			parameter['0_key'] += 1
		if self.i_type == 17:
			parameter['1_key'] += 1
		if self.i_type == 18:
			parameter['2_key'] += 1
		if self.i_type == 19:
			parameter['0_key'] += 1
			parameter['1_key'] += 1
			parameter['2_key'] += 1
		if self.i_type == 31:
			parameter['money'] += 300
		if self.i_type == 36:
			parameter['level'] += 1
			parameter['attack'] += 5
			parameter['defence'] += 3


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
		else:
			return

		for i in objs:
			if i.valid and i.location == [self.location[0] + self.vector[0], self.location[1] + self.vector[1]]:
				if i.o_type == o_type.up_floor:
					jump(self.screen, this_floor.config['next_floor'])
					return
				elif i.o_type == o_type.down_floor:
					jump(self.screen, this_floor.config['prev_floor'])
					return
				if not i.trigger():
					return

				
		self.location[0] += self.vector[0] 
		self.location[1] +=  self.vector[1] 
			


def jump(screen, destination):
	global warrior, parameter, this_floor
	warrior.vector = [0, 0, warrior.vector[2]]
	if destination > parameter['highest_floor']:
		parameter['highest_floor'] = destination
		floors[parameter["this_floor"]] = this_floor
		this_floor = floor(screen, str(destination))
		warrior.location = this_floor.down_floor
	else:
		floors[parameter["this_floor"]] = this_floor
		this_floor = floors[destination]
		if destination < parameter["this_floor"]:
			warrior.location = this_floor.up_floor
		else:
			warrior.location = this_floor.down_floor

	warrior.location = list(warrior.location)
	parameter["this_floor"] = destination

def produce_number(screen, number,x ,y):
	c = []
	for i,j in enumerate(number):
		c.append(object(screen, "resources/字/%s.png" % j, x + 0.5 * i, y - 0.025, o_type = o_type.scene, multiple = 0.22))
	return c

def check_events(player, objs, conversation_control, fight_system):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		if not conversation_control.in_conversation:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RIGHT:
					player.vector = [1, 0, 0]
				elif event.key == pygame.K_LEFT:
					player.vector = [-1,0, 1]
				if event.key == pygame.K_DOWN:
					player.vector = [0, 1, 2]
				elif event.key == pygame.K_UP:
					player.vector = [0,-1, 3]
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_RIGHT:
					player.vector = [0, player.vector[1], player.vector[2]]
				elif event.key == pygame.K_LEFT:
					player.vector = [0, player.vector[1], player.vector[2]]
				if event.key == pygame.K_DOWN:
					player.vector = [player.vector[0], 0, player.vector[2]]
				elif event.key == pygame.K_UP:
					player.vector = [player.vector[0], 0, player.vector[2]]
		else:
			if event.type == pygame.KEYDOWN:
				conversation_control.end_conversation()



	player.move(objs)


def update_screen(screen, objects):
	for i in objects:
		i.blitme()
	pygame.display.flip()


pygame.init()
screen  = pygame.display.set_mode((int(576 * 1.5 + 144), int(480 * 1.5)))

conversation_control = conversation(screen)
fight_system = fight(screen)

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

this_floor = floor(screen, "0")
warrior.location = list(this_floor.down_floor)
while True:
	check_events(warrior, scenes + this_floor.objects, conversation_control, fight_system)
	information = (produce_number(screen, str(parameter['level']), -2.1, 1) + 
		   produce_number(screen, str(parameter['health']), -3, 2) + 
		   produce_number(screen, str(parameter['attack']), -3, 3) + 
		   produce_number(screen, str(parameter['defence']), -3, 4) + 
		   produce_number(screen, str(parameter['agility']), -3, 5) +
		   produce_number(screen, str(parameter['0_key']), -3.5, 8.5) +
		   produce_number(screen, str(parameter['1_key']), -3.5, 9.5) +
		   produce_number(screen, str(parameter['2_key']), -3.5, 10.5) +
		   produce_number(screen, str(parameter['money']), -3.5, 11.5))

	update_screen(screen, grounds + information + scenes + [this_floor, warrior] + conversation_control.objects + fight_system.objects)
	time.sleep(0.075)
