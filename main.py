import sys
import pygame
from enum import Enum
import time
import json
from math import ceil

class obj_type(Enum):
	ground = 0
	wall = 1
	sign = 2
	npc = 3
	teleport = 4

class print_image():
	def __init__(self, screen, path, imd_p = True, fullscreen = False, prompt = "（任意鍵繼續）"):
		self.screen = screen
		self.objects = []
		if not fullscreen:
			self.objects.append(object(self.screen, "resources/box/msg_box.png", obj_type.sign, 0, 1, multiple = 2))
			self.objects.append(object(self.screen, path , obj_type.sign, 0, 1.25, multiple = 2))
			self.objects.append(text_object(self.screen, prompt, (10 , 11), (0, 0, 0, 255), 24))
		else:
			self.objects.append(object(self.screen, path , obj_type.sign, 0, 0, multiple = 2))
		if imd_p:
			self.show()

	def show(self):
		while True:
			self.screen.fill((255, 255, 255))

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				if event.type == pygame.KEYDOWN:
					return event.key

			for i in self.objects:
				i.blitme()

			pygame.display.flip()
			time.sleep(0.075)


class conversation():
	def __init__(self, screen, text, color = (0, 0, 0, 255), font_size = 24, type = 0, prompt = "（任意鍵繼續）",imd_p = True):
		self.screen = screen
		self.objects = []
		self.type = type
		if type == 0:
			self.objects.append(object(self.screen, "resources/box/msg_box.png", obj_type.sign, 0, 1, multiple = 2))
			self.objects.append(text_object(self.screen, prompt, (10 , 12.25), color, 24))
			for i,j in enumerate(text):
				self.objects.append(text_object(self.screen, j, (0.5 , 1.5 + i), color, font_size))
		else:
			self.objects.append(object(self.screen, "resources/box/msg_box 2.png", obj_type.sign, 0, 10, multiple = 2))
			self.objects.append(text_object(self.screen, prompt, (10 , 12.25), color, 24))
			for i,j in enumerate(text):
				self.objects.append(text_object(self.screen, j, (0.5 , 10.5 + i), color, font_size))
	
		if imd_p:
			self.show()
		
	def show(self):
		global this_scene, Jeff
		while True:
			self.screen.fill((255, 255, 255))
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				if event.type == pygame.KEYDOWN:
					return event.key
					
			if self.type == 0:
				for i in self.objects:
					i.blitme()
			else:
				for i in this_scene.objects + [Jeff] + self.objects:
					i.blitme()

		
			pygame.display.flip()
			time.sleep(0.075)

class text_object():
	def __init__(self, screen, text, location, color, font_size = 32):
		font = pygame.font.Font("resources/GenRyuMinTW_Regular.ttf", font_size)
		self.text = font.render(str(text) , True , color)
		self.location = location
		self.screen = screen

	def blitme(self):
		self.screen.blit(self.text, ((64) * self.location[0], (64) * self.location[1]))

class object():
	def __init__(self, screen, path, obj_type, x, y, dynamic = False, script = None, arg = {}, multiple = 2, sound = ""):
		self.screen = screen

		if dynamic:
			image = pygame.image.load(path % '0')
			self.path = path
			self.rect = self.image.get_rect()
			self.counter = 0
		else:
			self.image = pygame.image.load(path)
			self.rect = self.image.get_rect()
			self.image = pygame.transform.scale(self.image, (int(self.rect.width * multiple), int(self.rect.height * multiple)))
			self.rect = self.image.get_rect()

		self.multiple = multiple
		self.script = script
		self.type = obj_type
		self.dynamic = dynamic
		self.location = [x, y]
		self.sound = sound

		self.init2(arg)

	def init2(self, arg):
		pass

	def blitme(self):
		self.rect.centerx = (32 * self.multiple) * self.location[0] + self.rect.width  /  2
		self.rect.bottom  = (32 * self.multiple) * self.location[1] + self.rect.height
		
		if self.dynamic:
			image = pygame.transform.scale(pygame.image.load(path % self.counter), self.rect)

			self.screen.blit(self.image, self.rect)

			self.counter += 1
			if self.counter == 6:
				self.counter = 0
		else:
			self.screen.blit(self.image, self.rect)

	def trigger(self):
		if self.sound != "":
			play_audio(self.sound)
		if self.script != None:
			self.script.trigger(self.script)
		if self.type == obj_type.wall:
			return False
		return True

class animation():
	def __init__(self, screen, path, frames):
		self.screen = screen
		self.path = path
		self.frames = frames
		self.counter = 0

	def show(self):
		while self.counter < self.frames:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

			image = pygame.transform.scale(pygame.image.load(self.path % self.counter),(832, 832))

			self.screen.blit(image, (0, 0))
			pygame.display.flip()
			self.counter += 1
			time.sleep(0.075)

class telepoint(object):
	def __init__(self, arg, x, y):
		self.init2(arg)
		self.location = [x, y]

	def init2(self, arg):
		self.destination = [arg['destination'], arg['new_location']]

	def trigger(self):
		jump(self.destination[0],self.destination[1])

	def blitme(self):
		pass

class player(object):
	def __init__(self, screen, x , y):
		self.screen = screen
		self.images = []
		
		self.images.append('resources/Jeff/right %s.png')
		self.images.append('resources/Jeff/left %s.png')
		self.images.append('resources/Jeff/up %s.png')
		self.images.append('resources/Jeff/down %s.png')

		self.counter =  0

		image = pygame.transform.scale(pygame.image.load(self.images[0] % '0'), (64, 64))
		
		self.rect = image.get_rect()
		self.vector = [0, 0, 2]

		self.location = [x, y]

	def blitme(self):
		self.rect.centerx = 64 * self.location[0] + self.rect.width /  2
		self.rect.bottom  = 64 * self.location[1] + self.rect.height

		image = pygame.transform.scale(pygame.image.load(self.images[self.vector[2]] % self.counter), ((64, 64)))

		self.screen.blit(image, self.rect)

	def move(self, objs = []):
		if self.vector[:2] == [0,0]:
			return
		else:
			self.counter += 1
			if self.counter == 4:
				self.counter = 1
		if not (0 <= self.location[0] + self.vector[0] <= 12 and 0 <= self.location[1] + self.vector[1] <= 12):
			return

		for i in objs:
			if i.location == [int(self.location[0] + self.vector[0]), ceil(self.location[1] + self.vector[1])] or i.location == [ceil(self.location[0] + self.vector[0]), int(self.location[1] + self.vector[1])] or i.location == [ceil(self.location[0] + self.vector[0]), ceil(self.location[1] + self.vector[1])] or i.location == [int(self.location[0] + self.vector[0]), int(self.location[1] + self.vector[1])]:
				if not i.trigger():
					self.vector[0] = 0
					self.vector[1] = 0
					return

		play_audio("walk")
		self.location[0] += self.vector[0]
		self.location[1] += self.vector[1]


def check_events(player, objs):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RIGHT:
				player.vector = [0.5, 0, 0]
			if event.key == pygame.K_LEFT:
				player.vector = [-0.5,0, 1]
			if event.key == pygame.K_UP:
				player.vector = [0,-0.5, 2]
			if event.key == pygame.K_DOWN:
				player.vector = [0, 0.5, 3]
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
				player.vector[0] = 0
			if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
				player.vector[1] = 0

	player.move(objs)


def update_screen(screen, objects):
	screen.fill((255, 255, 255))
	for i in objects:
		i.blitme()

	pygame.display.flip()

class sign(object):
	def init2(self, arg):
		self.text = arg["msg"]
	def trigger(self):
		conversation(self.screen, self.text,color = (255,255,255,255), type = 1)
class scene():
	def __init__(self, screen, data):
		scene = data['scene']
		self.objects = []
		self.screen = screen

		for i in range(len(scene)):
			for j in range(len(scene[1])):
				if type(scene[i][j]) == int or type(scene[i][j]) == float:
					if scene[i][j] == -1:
						self.objects.append(endGame(j, i))
					elif 0 <= scene[i][j] < 10:
						blk_type = obj_type.ground
					elif 10 <= scene[i][j] < 35: 
						blk_type = obj_type.wall

					if scene[i][j] >= 0:
						self.objects.append(object(self.screen, "resources/material/%s.png" % scene[i][j], blk_type, j, i, dynamic = False))

				elif type(scene[i][j]) == list:
						for img in scene[i][j]:
							
							if type(img) == int or type(img) == float:
								if img == -1:
									self.objects.append(endGame(j, i))
								elif 0 <= img < 10:
									blk_type = obj_type.ground
								elif 10 <= img < 35: 
									blk_type = obj_type.wall

								if img >= 0:
									self.objects.append(object(self.screen, "resources/material/%s.png" % img, blk_type, j, i, dynamic = False))
							elif type(img) == dict:
								if img['obj_type'] == obj_type.npc.value:
									program = img['program']
									exec("global SCRIPT; SCRIPT = __import__('script." + program + "')." + program + ".Script()")

									self.objects.append(npc(self.screen, "resources/material/%s.png" % img['blk_type'], img['obj_type'], j, i, dynamic = False, script = SCRIPT))
								elif img['obj_type'] == obj_type.sign.value:
									self.objects.append(sign(self.screen, "resources/material/%s.png" % img['blk_type'], img['obj_type'], j, i,arg = {'msg': img['msg']}, dynamic = False))

								elif img['obj_type'] == obj_type.teleport.value:
									if 'sound' in img:
										self.objects.append(object(self.screen, "resources/material/%s.png" % img['blk_type'], img['obj_type'], j, i, dynamic = False, sound = img['sound']))
									else:

										self.objects.append(object(self.screen, "resources/material/%s.png" % img['blk_type'], img['obj_type'], j, i, dynamic = False))

									self.objects.append(telepoint(img, j, i))

				elif scene[i][j]['obj_type'] == obj_type.teleport.value:

					self.objects.append(object(self.screen, "resources/material/%s.png" % scene[i][j]['blk_type'], scene[i][j]['obj_type'], j, i, dynamic = False))

					self.objects.append(telepoint(scene[i][j], j, i))

				elif type(scene[i][j]) == dict:
					if scene[i][j]['obj_type'] == obj_type.npc.value:
						program = scene[i][j]['program']
						exec("global SCRIPT; SCRIPT = __import__('script." + program + "')." + program + ".Script()")

						self.objects.append(npc(self.screen, "resources/material/%s.png" % scene[i][j]['blk_type'], scene[i][j]['obj_type'], j, i, dynamic = False, script = SCRIPT))
					elif scene[i][j]['obj_type'] == obj_type.teleport.value:
						self.objects.append(object(self.screen, "resources/material/%s.png" % scene[i][j]['blk_type'], scene[i][j]['obj_type'], j, i, dynamic = False))
						self.objects.append(telepoint(img, j, i))
					elif scene[i][j]['obj_type'] == obj_type.sign.value:
						self.objects.append(sign(self.screen, "resources/material/%s.png" % scene[i][j]['blk_type'], scene[i][j]['obj_type'], j, i, arg = {'msg': scene[i][j]['msg']}, dynamic = False))


		if data['background'] != None:
			self.objects.append(object(self.screen, "resources/background/%s.png" % data['background'], 0, 0, 0, dynamic = False))

	def blitme(self):
		for i in self.objects:
			i.blitme()

class endGame(object):
	def __init__(self, x, y):
		self.location = [x, y]
	def trigger(self):
		global keepGame
		keepGame = False
		return
	def blitme(self):
		pass

class npc(object):
	def init2(self, arg):
		if self.script != None:
			self.script.conversation = conversation
			self.script.print_image = print_image
			self.script.animation = animation
			self.script.screen = self.screen
			self.script.die = die
			self.script.won = won
	def trigger(self):
		return self.script.trigger()

def die():
	global keepGame
	keepGame = False
def won():
	global keepGame, ifWon
	keepGame = False
	ifWon = True
def jump(destination, new_location):
	global this_scene
	this_scene = scenes[destination]
	Jeff.location = new_location.copy()

def play_audio(path):
	if pygame.mixer.music.get_busy():
		pygame.mixer.music.stop()

	audio_player = pygame.mixer.music
	audio_player.load("resources/sound/" + path + ".mp3")
	audio_player.play()


dead_counter = 0

pygame.init()
screen = pygame.display.set_mode((832, 832))

conversation(screen, ["","","Finding Joe"], font_size = 132)

ifWon = False

def run_game():
	global scenes, screen, maps, this_scene, Jeff, keepGame, ifWon

	keepGame = True
	ifWon = False
	pygame.display.set_caption("Finding Joe")

	scenes = {}

	maps = json.load(open("data/maps.json"))

	for each_scene in maps['scenes']:
		scenes[each_scene['name']] = scene(screen, each_scene)

	this_scene = scenes[maps["default_scene"]]

	Jeff = player(screen, maps['default_location'][0], maps['default_location'][1])

	del maps

	conversation(screen, ["Jeff 起床時，發現他的狗狗 Joe 不見了！","於是他踏上了尋找狗狗之路！"], font_size = 32)

	while keepGame:
		check_events(Jeff, this_scene.objects)

		update_screen(screen, [this_scene, Jeff])

		time.sleep(0.075)

while True:
	play_audio("fuck_jeff")
	run_game()
	if ifWon:
		break
	conversation(screen, ["",""," Jeff 從惡夢中驚醒"], font_size = 72)
	dead_counter += 1
conversation(screen, ["",""," Jeff 從睡夢中驚醒"], font_size = 72)
conversation(screen, ["",""," 發現自己的狗 Joe 就在一旁的狗窩"], font_size = 36)
conversation(screen, ["END","恭喜你完成遊戲！"," Jeff 總共經歷了 %s 層夢中夢。" % str(dead_counter)], font_size = 36)