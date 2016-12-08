__author__ = "kiel.regusters"

"""
This module contains the Checkpoint trigger class to be used with pytmx.
"""

import pygame as pg
import constants as c
import init

class Checkpoint(pg.sprite.Sprite):
	"""
	This class contains two frames. A frame for when the character hasn't collided, and a frame for when they have.
	"""
	def __init__(self, x, y):
		pg.sprite.Sprite.__init__(self)
		self.spritenormal = init.GRAPHICS['checkpoint'].convert_alpha()
		self.spritegot = init.GRAPHICS['checkpointgot'].convert_alpha()
		self.relX = x
		self.relY = y
		self.SetUpImages()
		self.got = False

	def SetUpImages(self):
		"""
		Sets up both of the frames used for both states of the checkpoint.
		"""
		blitCheck = pg.Surface((16, 16))
		blitCheck.set_colorkey((255, 0, 255))
		blitCheck.blit(self.spritenormal, (0,0))

		blitCheckGot = pg.Surface((16, 16))
		blitCheckGot.set_colorkey((255, 0, 255))
		blitCheckGot.blit(self.spritegot, (0,0))

		rect = blitCheck.get_rect()
		self.frame1 = pg.transform.scale(blitCheck,(int(rect.width * 3), int(rect.height * 3)))
		self.frame2 = pg.transform.scale(blitCheckGot,(int(rect.width * 3), int(rect.height * 3)))

		self.image = self.frame1
		self.rect = self.image.get_rect()
		self.rect.x = 0
		self.rect.y = 0

	def Update(self):
		"""
		Listens for the got flag to be true otherwise, do nothing.
		"""
		if self.got == True:
			self.image = self.frame2
		else:
			pass