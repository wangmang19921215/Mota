class NPC():
	def __init__(self, arg):
		self.not_talk = True

	def trigger(self):
		self.conversation_control.print_word("商人","又有人來送死了！不知道你能活多久。嘻嘻嘻嘻！", 'npc_2')
		self.not_talk = False