class Script():
	def trigger(self):
		self.conversation(self.screen, ["如果你想知道究竟要往哪裡走的話，","這個圖片會給你答案"], color = (255,255,255,255), type = 1)
		self.print_image(self.screen, "resources/hints/hint1.png")