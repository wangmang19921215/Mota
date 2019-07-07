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

class d_type(Enum):
	yellow = 0
	blue   = 1
	red    = 2
	magic  = 3