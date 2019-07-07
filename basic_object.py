import basic_enum

class object():
	def __init__(self, screen, path, x , y, o_type = basic_enum.o_type.ground, multiple = 1.5, parameter = {}):
		self.screen = screen

		self.image = pygame.image.load(path)
		self.rect = self.image.get_rect()
		self.image = pygame.transform.scale(self.image, (int(self.rect.width * multiple), int(self.rect.height * multiple)))
		self.rect = self.image.get_rect()

		self.visible = True
		self.o_type = o_type

		self.location = [x,y]

		self.__init__2(parameter)

	def __init__2(self, parameter):
		pass

	def trigger(self):
		if self.o_type == basic_enum.o_type.wall:
			return False

	def blitme(self):

		if self.visible:
			self.rect.centerx = self.location[0] * 48 + 336 - self.rect.width / 2
			self.rect.bottom = self.location[1] * 48 + 96 - self.rect.height

			self.screen.blit(self.image, self.rect)

class door(object):
	def __init__2(self, parameter):
		self.d_type = parameter['d_type']
		self.parameter = parameter
		self.is_open = False

	def trigger(self):
		if not self.is_open:
			if not self.d_type == 3:
				if cost(self.d_type + "_key"):
					self.is_open = True
					self.count   = 0
					return True
			else:
				return magic_door()
		else:
			return True

	def magic_door():
		pass

	def blitme(self):
		if self.visible and not self.is_open:
			self.rect.centerx = self.location[0] * 48 + 336 - self.rect.width / 2
			self.rect.bottom = self.location[1] * 48 + 96 - self.rect.height

			self.screen.blit(self.image, self.rect)
		elif self.visible:
			self.count += 1
			path = "resources/地形/門/" + ["黃","藍","紅","魔法"][self.d_type] + " %s.png" % self.count
			self.image = pygame.image.load(path)
			self.rect = self.image.get_rect()
			self.image = pygame.transform.scale(self.image, (int(self.rect.width * multiple), int(self.rect.height * multiple)))
			self.rect = self.image.get_rect()

			self.screen.blit(self.image, self.rect)
			if self.count == 3:
				self.visible = False