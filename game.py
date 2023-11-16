# title:   Junkyard Janitor
# author:  Hevanafa
# desc: 16-11-2023
# license: MIT License
# version: 0.1
# script:  python

# Comment this on release
from typings import btn, circ, circb, cls, spr, print

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
p_frame = 0
p_face_right = True
p_cash = 0

volume = 0
"""carry capacity"""

max_volume = 5
"""max. carry capacity"""

p_suction_level = 1  # Garbage.min_level
p_volume_level = 1
p_range_level = 1


gt_x = sw // 2
"""Garbage truck X"""

gt_y = sh - 14
"""Garbage truck Y"""

class Vector:
	def __init__(self, cx = 0.0, cy = 0.0, vx = 0.0, vy = 0.0):
		self.cx = cx
		self.cy = cy
		self.vx = vx
		self.vy = vy


class Garbage(Vector):
	def __init__(self):
		super().__init__()
		self.activated = False
		self.min_level = 1

class Particle(Vector):
	def __init__(self, colour: int):
		super().__init__()
		self.colour = colour
		self.ttl = 0

last_points: list[Vector] = []

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


# default spawner
# for a in range(1, 11):
# 	g = Garbage()
# 	g.cx = randint(b_left, b_right)
# 	g.cy = randint(b_top, b_bottom)
# 	garbage_list.append(g)

# spawn in clusters
# Todo: upgrades: suction lv, capacity & range
for a in range(1, 25):
	g = Garbage()
	g.cx = 50 + sin(rand() * 2 * PI) * 20
	g.cy = 50 + cos(rand() * 2 * PI) * 20
	garbage_list.append(g)

	g = Garbage()
	g.cx = 190 + sin(rand() * 2 * PI) * 20
	g.cy = 50 + cos(rand() * 2 * PI) * 20
	garbage_list.append(g)

garbage_count = len(garbage_list)

def TIC():
	global p_frame, p_face_right, px, py, volume

	if btn(0):
		py -= 0.5
	if btn(1):
		py += 0.5

	if btn(2):
		px -= 0.5
		p_face_right = False
	if btn(3):
		px += 0.5
		p_face_right = True

	if len(last_points) == 0 or last_points[0].cx != px or last_points[0].cy != py:
		last_points.insert(0, Vector(px, py))

		if len(last_points) > 20:
			last_points.pop()
	
	if py < b_top: py = b_top
	if py > b_bottom: py = b_bottom

	if px < b_left: px = b_left
	if px > b_right: px = b_right

	p_frame += 1
	if p_frame >= 60:
		p_frame = 0

	# check garbage truck
	if volume > 0 and getDist(gt_x, px, gt_y, py) <= 400:
		volume = 0
		emitParticles(gt_x, gt_y, 7)


	for g in garbage_list:
		g.activated = getDist(g.cx, px, g.cy, py) < 725 and volume < max_volume  # 25 pixels

		if g.activated:
			g.cx += g.vx
			g.cy += g.vy

			rads = getShootingAngle(px - g.cx, py - g.cy)
			g.vx = sin(rads) * 1.5
			g.vy = -cos(rads) * 1.5

		if volume < max_volume and getDist(g.cx, px, g.cy, py) < 144:  # 12 pixels
			volume += 1
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

	if volume > 0:
		spr(5, int(last_points[-1].cx - 4), int(last_points[-1].cy - 4), 0)
	
	# player sprite
	spr(36 + p_frame // 30 * 2, int(px) - 8, int(py - 8), 0, w=2, h=2)
	# print(f"{p_frame}")

	# vacuum
	# Note: 0 is falsy
	# Ref: https://stackoverflow.com/questions/39983695
	spr(7, int(px) + (p_face_right and 6 or -14), int(py), 0, flip = 0 if p_face_right else 1)


	# particles
	for p in particle_list:
		circ(int(p.cx), int(p.cy), 1, 7)


	# HUD
	s = f"{ volume } / 5"
	w = print(s, y=-100, alt=True)
	spr(5, sw - w - 18, 2, 0)
	print(s, sw - w - 10, 4, volume >= max_volume and 8 or 7, alt=True)

	if volume == max_volume:
		print("FULL!", sw - 30, 12, 8)

	perc = (garbage_count - len(garbage_list)) / garbage_count
	print(f"{ round(perc * 100) }%", 10, 4, 7, alt=True)


