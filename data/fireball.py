"""
Module that contains the fireball used by the player.
"""

__author__ = "kiel.regusters"
import pygame as pg
from . import constants as c
from . import init, gamemanager

class Fireball(pg.sprite.Sprite):
	def __init__(self, relX, relY, facingRight):
		"""
		@param facingRight: the players facingRight state at the time of casting
		@param relX: player's x position relative to the level
		@param relY: player's y position relative to the level
		"""
		pg.sprite.Sprite.__init__(self)
		self.sprite = init.GRAPHICS['fireball'].convert_alpha()
		self.relX = relX
		self.relY = relY
		self.facingRight = facingRight
		self.life = 30
		self.LoadImage()
		self.SetUpForces()

	def LoadImage(self):
		"""
		Method to load the graphics for the fireball.
		"""
		blitBall = pg.Surface((16, 16))
		blitBall.set_colorkey((255, 0, 255))
		blitBall.blit(self.sprite, (0,0))
		rect = blitBall.get_rect()
		self.image = pg.transform.scale(blitBall,(int(rect.width * 3), int(rect.height * 3)))
		if self.facingRight == False:
			self.image = pg.transform.flip(self.image, True, False)
		self.rect = self.image.get_rect()
		self.hurtbox = [self.relX, self.relY, 50, 25]
		self.rect = pg.Rect(self.hurtbox)

	def Lifetime(self):
		"""
		How decrement the fireball's life span.
		"""
		self.life -= 1

	def SetUpForces(self):
		"""
		Set up the forces used to move the fireball.
		"""
		self.velX = 0
		self.accelX = 0.5
