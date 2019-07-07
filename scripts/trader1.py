class NPC():
	def __init__(self, arg):
		self.count = 0
	def trigger(self):
		if self.count <= 3:
			self.conversation_control.print_word("商人","又有人來送死了！不知道你能活多久。嘻嘻嘻嘻！", 'npc_2')
		elif self.count <= 5:
			self.conversation_control.print_word("商人","不知道你能活多久。嘻嘻嘻嘻！", 'npc_2')
		else:
			self.conversation_control.print_word("商人","我先離開了！", 'npc_2')
			self.status.visible = False
			self.status.valid = False
		self.count += 1
		self.conversation_control.print_word("勇者","這裡怪怪的！", 'player')
		if self.count <= 5:
			self.conversation_control.print_word("商人","但是有利可圖，嘻嘻！", 'npc_2')