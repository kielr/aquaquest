__author__ = "kiel.regusters"

"""
Module for a camera object that lets us change what the viewport sees.
"""
from . import init
import pygame as pg
class Camera(object):
	"""
	Very important class. Ensures that the player an always see the character.
	"""

	def __init__(self):
		self.viewport = init.SCREEN.get_rect()
		self.x = self.viewport.x
		self.y = self.viewport.y
		self.orgX = self.viewport.centerx
		self.orgY = self.viewport.centery
	def __str__(self):
		return "cameraX: {}, cameraY: {}, orgX: {}, orgY: {}".format(self.x, self.y, self.orgX, self.orgY)

	#def EnforceLimit(self):
	#	if self.limitRect != None:
	#		if self.right >= self.limitRect.right:
	#			self.x = self.limitRect.left
	#			self.orgX -= 1

	def LookAt(self, vector):
		"""
		Sets the camera to the provided (x,y) format vector.
		"""
		self.x = int(vector[0] - self.viewport.width / 2)
		self.y = int(vector[1] - self.viewport.height / 2)
		self.orgX = int(self.x + self.viewport.width / 2)
		self.orgY = int(self.y + self.viewport.height / 2)

	def LookAtX(self, x):
		"""
		Sets the camera's x coordinate to the provided x parameter.
		"""
		self.x = int(x - self.viewport.width / 2)
		self.orgX = int(self.x + self.viewport.width / 2)

	def LookAtY(self, y):
		"""
		Sets the camera's y coordinate to the provided x parameter.
		"""
		self.y = int(y - self.viewport.width / 2)
		self.orgY = int(self.y + self.viewport.width / 2)


	def Move(self, x, y):
		"""
		@param x: x-axis amount to move
		@param y: y-axis amount to move

		Moves the camera.
		"""
		self.x += x
		self.y += y
		self.orgX += x
		self.orgY += y
		#self.EnforceLimit()