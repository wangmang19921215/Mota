class Script():
	def trigger(self):
		a = 0
		while not ord("0") <= a <= ord("9"):
			a = self.print_image(self.screen, "resources/hints/hint2.png",fullscreen = True, imd_p = False)
			a = a.show()
		if a != ord('5'):
			self.die()
		return True