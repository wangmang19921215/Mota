class NPC():
	def __init__(self, arg):
		self.count = 0
	def trigger(self):
		key = self.conversation_control.print_word("商人","我有一顆紅寶石，你要嗎？賣你 2 塊錢", 'npc_2', prompt = "（Ｙ／Ｎ）", keys = [ord('y'), ord('n')])

		if key == ord('y') and self.status.cost("money", 2):
			self.status.cost("attack", -2)
			self.status.valid = False
			self.status.visible = False