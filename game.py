# title:   Junkyard Janitor
# author:  Hevanafa
# desc: 16-11-2023
# license: MIT License
# version: 0.1
# script:  python

# Comment this on release
from typings import btn, cls, spr

sw = 240
sh = 136

px = 96.0
py = 24.0
capacity = 0

class Garbage:
	def __init__(self):
		self.cx = 0.0
		self.cy = 0.0
		self.vx = 0.0
		self.vy = 0.0

garbage_list: list[Garbage] = []


def TIC():
	global px, py

	if btn(0):
		py -= 1
	if btn(1):
		py += 1
	if btn(2):
		px -= 1
	if btn(3):
		px += 1

	cls(0)

	spr(36, int(px), int(py), 0, w=2, h=2)
