#!/usr/bin/python3

from random import *

class brain:
	def __init__(self, inputs, middle, outputs):
		self.inputs = inputs
		self.outputs = outputs
		self.middle = middle
		self.weights1 = [[2*random()-1 for j in range(inputs)] for i in range(middle)]
		self.weights2 = [[2*random()-1 for j in range(middle)] for i in range(outputs)]
	def feedforward(self, inputs):
		middlelayer = [0] * self.middle
		for i in range(self.middle):
			for j in range(self.inputs):
				middlelayer[i] += inputs[j] * self.weights1[i][j]
		middlelayer = [sigmoid(x) for x in range(self.middle)]
		outputlayer = [0] * self.outputs
		for i in range(self.outputs):
			for j in range(self.middle):
				outputlayer[i] += middlelayer[j] * self.weights2[i][j]
		outputlayer = [sigmoid(x) for x in outputlayer]
		return outputlayer
	def mutate(self, rate):
		for i in range(self.middle):
			for j in range(self.inputs):
				self.weights1[i][j] += uniform(-rate, rate)
		for i in range(self.outputs):
			for j in range(self.middle):
				self.weights2[i][j] += uniform(-rate, rate)

def sigmoid(x):
	return 1/(1+pow(2.71828, -x))
