import time
class Script():
	def trigger(self):
		self.conversation(self.screen, ["", "按下任意鍵開始播放動畫！"], color = (255,255,255,255), type = 1)
		self.animation(self.screen, "resources/animation/parking_lot/parking_lot %s.png", 11).show()
		time.sleep(0.3)
		self.conversation(self.screen, ["有一位夫妻駕著一輛車，非常緊急的飆到某一個地方。","到了之後先生趕緊下車，離開了一回。","當他回來的時候發現他老婆已經去世，車子裡面多了一個人。"], color = (255,255,255,255), type = 1)

		self.conversation(self.screen, ["請去這位夫婦原本是要駕車去的地點，而答案在左邊。"], color = (255,255,255,255), type = 1)