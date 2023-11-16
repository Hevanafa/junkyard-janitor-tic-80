# title:   Junkyard Janitor
# author:  Hevanafa
# desc: 16-11-2023
# license: MIT License
# version: 0.1
# script:  python

# Comment this on release
from typings import btn, cls, spr

from math import atan2, pi as PI, sin, cos
from random import random as rand, randint

def getDist(x1, x2, y1, y2):
	return (x2 - x1) ** 2 + (y2 - y1) ** 2

def getShootingAngle(dx: float, dy: float) -> float:
	return atan2(dy, dx) + PI / 2


sw = 240
sh = 136

b_top = 20
b_left = 10
b_right = 230
b_bottom = 116

px = 120.0
py = 110.0
capacity = 0

class Garbage:
	def __init__(self):
		self.cx = 0.0
		self.cy = 0.0
		self.vx = 0.0
		self.vy = 0.0

garbage_list: list[Garbage] = []


for a in range(1, 11):
	g = Garbage()
	g.cx = randint(b_left, b_right)
	g.cy = randint(b_top, b_bottom)
	garbage_list.append(g)


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
	
	if py < b_top: py = b_top
	if py > b_bottom: py = b_bottom

	if px < b_left: px = b_left
	if px > b_right: px = b_right


	for g in garbage_list:
		g.cx += g.vx
		g.cy += g.vy

		if getDist(g.cx, px, g.cy, py) < 900:  # 30 pixels
			rads = getShootingAngle(px - g.cx, py - g.cy)
			g.vx = sin(rads)
			g.vy = -cos(rads)
		elif getDist(g.cx, px, g.cy, py) < 64:  # 8 pixels
			capacity += 1
			garbage_list.remove(g)


	cls(0)

	# garbage truck
	spr(40, (sw - 16) // 2, sh - 17, 0, w=2, h=2)

	# render all garbage
	for g in garbage_list:
		spr(19, int(g.cx - 4), int(g.cy - 4), 0)

	# player sprite
	spr(36, int(px) - 8, int(py - 8), 0, w=2, h=2)

