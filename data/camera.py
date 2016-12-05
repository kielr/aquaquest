__author__ = "kiel.regusters"

"""
Module for a camera object that lets us change what the viewport sees.
"""
from . import init
import pygame as pg
class Camera(object):
	def __init__(self):
		self.viewport = init.SCREEN.get_rect()
		self.x = self.viewport.x
		self.y = self.viewport.y
		self.right = self.x + self.viewport.width
		self.bottom = self.y + self.viewport.height
		self.left = self.x
		self.top = self.y
		self.orgX = self.viewport.centerx
		self.orgY = self.viewport.centery
		self.limitRect = None
	def __str__(self):
		return "cameraX: {}, cameraY: {}, orgX: {}, orgY: {}".format(self.x, self.y, self.orgX, self.orgY)

	#def EnforceLimit(self):
	#	if self.limitRect != None:
	#		if self.right >= self.limitRect.right:
	#			self.x = self.limitRect.left
	#			self.orgX -= 1

	def LookAt(self, vector):
		self.x = int(vector[0] - self.viewport.width / 2)
		self.y = int(vector[1] - self.viewport.height / 2)
		self.orgX = int(self.x + self.viewport.width / 2)
		self.orgY = int(self.y + self.viewport.height / 2)

	def LookAtX(self, x):
		self.x = int(x - self.viewport.width / 2)
		self.orgX = int(self.x + self.viewport.width / 2)

	def LookAtY(self, y):
		self.y = int(y - self.viewport.width / 2)
		self.orgY = int(self.y + self.viewport.width / 2)


	def LerpLookAt(self, vector, t):
		frompos = pg.math.Vector2(self.x, self.y)
		target = pg.math.Vector2(vector[0] - self.viewport.width / 2, vector[1] - self.viewport.height / 2)
		lerpTarget = pg.math.Vector2.lerp(frompos, target, t)

		self.x = int(lerpTarget.x)
		self.y = int(lerpTarget.y)
		self.orgX = int(self.x + self.viewport.width / 2)
		self.orgY = int(self.y + self.viewport.height / 2)


	def Move(self, x, y):
		self.x += x
		self.y += y
		self.orgX += x
		self.orgY += y
		#self.EnforceLimit()