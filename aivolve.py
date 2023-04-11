#!/usr/bin/python3
'''version 1.0.0
author: iamaprogramador
officialrender: #2
rendername: 1.0.0d_testing_#003
notes: fixing rendering
data: na
see README for more info
'''
from math import *
from os import system
from random import random, randint
from time import time
from agents import agent
import cv2 as cv
import numpy as np

beginningtime = time()
system('rm *.png')
frames = 30000
width = 320
height = 240
agentnum = 500
agentsize = 16/2 #radius of the rendered agent
learning = .01 #amount by which the neural network mutates each tick
eatingefficiency = .8 #efficiency of an agent's metabolism when eating another agent
reach = 6**2 #distance at which an agent can kill another, squared
reproduction = 100 #energy at which an agent may reproduce
repelling = .01 #strength of the repelling force between two agents on the same team
s = 25 #chunksize
teamcolors = [(255,0,0), (0,255,0), (0,0,255)]

agents = []
for x in range(agentnum):
	agents.append(agent(x, randint(0, width), randint(0, height)))

for f in range(frames):
	#indexing the agents that are in each chunk
	index = [[[] for y in range(1+int(height/s))] for x in range(1+int(width/s))]
	for a in agents:
		if a.x > width or a.x < 0 or a.y > height or a.y < 0:
			agents.remove(a)
		else:
			index[int(a.x/s)][int(a.y/s)].append(a)
	#move the agents
	for a in agents:
		#create a list for the brain of the 5 nearest agents
		dists = []
		for xchunk in range(int(a.x/s)-1, int(a.x/s)+2):
			for ychunk in range(int(a.y/s)-1, int(a.y/s)+2):
				for obj in index[xchunk % (1+int(width/s))][ychunk % (1+int(height/s))]:
					dists.append((obj.x-a.x)**2 + (obj.y-a.y)**2)
		dists.sort()
		if len(dists) < 5:
			continue
		maxdist = dists[4]
		nearby = []
		for xchunk in range(int(a.x/s)-1, int(a.x/s)+2):
			for ychunk in range(int(a.y/s)-1, int(a.y/s)+2):
				for obj in index[xchunk % (1+int(width/s))][ychunk % (1+int(height/s))]:
					if ((obj.x-a.x)**2 + (obj.y-a.y)**2) <= maxdist:
						nearby.append(obj)
		del dists
		impulses = []
		for x in range(5):
			impulses.append(a.x - nearby[x].x)
			impulses.append(a.y - nearby[x].y)
			impulses.append(nearby[x].team/2)
			#brain impulses are, for each five, [x dist, y dist, team]
		movement = a.brain.feedforward(impulses)
		a.brain.mutate(learning)
		a.x += .25*movement[0]
		a.y += .25*movement[1]
		a.energy -= sum(movement)**2
		#so all the agents don't eventually starve, we need a constant influx of energy
		a.energy += .05
		for x in range(5):
			if a.team == nearby[x].team:
				#repel any teammates that get too close
				dist = .001 + (a.x - nearby[x].x)**2 + (a.y - nearby[x].y)**2
				strength = 1/(dist*repelling)
				nearby[x].x += (a.x - nearby[x].x)*strength
				nearby[x].y += (a.y - nearby[x].y)*strength
			if ((a.x - nearby[x].x)**2 + (a.y - nearby[x].y)**2) < reach and nearby[x].team != a.team:
				#kill the nearby agent and eat it
				if x in nearby:
					a.energy += nearby[x].energy * eatingefficiency
					agents.remove(nearby[x])
		#did I die of starvation?
		if a.energy < 0:
			agents.remove(a)
		#can I reproduce?
		if a.energy >= reproduction:
			newagent = a
			newagent.x += 6*random()-3
			newagent.y -= 6*random()-3
			newagent.energy = a.energy / 2
			a.energy *= .5
			agents.append(newagent)
	del index, nearby, impulses, movement
	#render and save the file
	img = img = np.zeros((height, width, 3), 'uint8')
	for a in agents:
		cv.rectangle(img, [int(a.x), int(a.y)], [int(a.x+agentsize), int(a.y+agentsize)], teamcolors[a.team], -1)
	cv.imwrite('%04d.png' % f, img)
	print('Done with img %d' % f)

system('rm nseorihf.mkv')
system('ffmpeg -v 24 -f image2 -framerate 30 -i %04d.png nseorihf.mkv')

system('cd ..;rm *.png')

print('Elapsed time: %11f' % (time()-beginningtime))

play = input('Play generated video? [Y/n]')
if play == 'Y' or play == 'y':
	system('mpv --fs nseorihf.mkv')
