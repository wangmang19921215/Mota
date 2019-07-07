class NPC():
	def __init__(self, arg):
		self.not_talk = True

	def trigger(self):
		if self.not_talk:
			print("你好")
			self.not_talk = False