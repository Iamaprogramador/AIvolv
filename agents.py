#!/usr/bin/python3

from random import *
from brain import *

class agent():
	def __init__(self, id, x, y):
		self.x = x
		self.y = y
		self.team = randint(0, 2)
		self.id = id
		self.brain = brain(15, 10, 2)
		self.energy = 500
