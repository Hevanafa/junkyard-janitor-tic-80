# title:   Junkyard Janitor
# author:  Hevanafa
# desc: 16-11-2023
# license: MIT License
# version: 0.1
# script:  python

# Comment this on release
from typings import btn, circ, circb, cls, spr

from math import atan2, pi as PI, sin, cos
from random import random as rand, randint

def getDist(x1, x2, y1, y2):
	return (x2 - x1) ** 2 + (y2 - y1) ** 2

def getShootingAngle(dx: float, dy: float) -> float:
	return atan2(dy, dx) + PI / 2

def seconds2frames(sec: float):
	return int(sec * 60)

sw = 240
sh = 136

b_top = 20
b_left = 10
b_right = 230
b_bottom = 116

px = 120.0
py = 110.0
capacity = 0

gt_x = sw // 2
gt_y = sh - 17

class Vector:
	def __init__(self):
		self.cx = 0.0
		self.cy = 0.0
		self.vx = 0.0
		self.vy = 0.0


class Garbage(Vector):
	pass
	# def __init__(self):
	# 	super().__init__()

class Particle(Vector):
	def __init__(self, colour: int):
		super().__init__()
		self.colour = colour
		self.ttl = 0

garbage_list: list[Garbage] = []
particle_list: list[Particle] = []

def emitParticles(x: int, y: int, colour: int):
	for _ in range(1, 10):
		p = Particle(colour)
		p.cx = x
		p.cy = y
		p.vx = rand() - 0.5
		p.vy = rand() - 0.5
		p.ttl = seconds2frames(0.5 + rand())
		particle_list.append(p)


for a in range(1, 11):
	g = Garbage()
	g.cx = randint(b_left, b_right)
	g.cy = randint(b_top, b_bottom)
	garbage_list.append(g)


def TIC():
	global px, py, capacity

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

	if capacity > 0 and getDist(gt_x, px, gt_y, py) <= 400:
		capacity = 0
		emitParticles(gt_x, gt_y, 7)


	for g in garbage_list:
		g.cx += g.vx
		g.cy += g.vy

		if capacity >= 5:
			continue

		if getDist(g.cx, px, g.cy, py) < 900:  # 30 pixels
			rads = getShootingAngle(px - g.cx, py - g.cy)
			g.vx = sin(rads) * 1.5
			g.vy = -cos(rads) * 1.5

		if getDist(g.cx, px, g.cy, py) < 64:  # 8 pixels
			capacity += 1
			emitParticles(g.cx, g.cy, 7)
			garbage_list.remove(g)

	for p in particle_list:
		p.cx += p.vx
		p.cy += p.vy
		p.ttl -= 1

		if p in particle_list and p.ttl <= 0:
			particle_list.remove(p)


	cls(0)

	# garbage truck
	circb(gt_x, gt_y, 20, 12)
	spr(40, gt_x - 8, gt_y - 8, 0, w=2, h=2)

	# garbage
	for g in garbage_list:
		spr(19, int(g.cx - 4), int(g.cy - 4), 0)

	if capacity > 0:
		spr(5, int(px) - 16, int(py - 8), 0)
	
	# player sprite
	spr(36, int(px) - 8, int(py - 8), 0, w=2, h=2)

	# particles
	for p in particle_list:
		circ(int(p.cx), int(p.cy), 1, 7)

