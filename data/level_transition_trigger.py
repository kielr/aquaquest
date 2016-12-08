"""
Module containing the trigger class. This class causes the level transition if the player steps into it.
"""

__author__ = "kiel.regusters"

import pygame as pg
import constants as c
import init

class Trigger(pg.sprite.Sprite):
	"""
	Causes the level transition if the player steps on the trigger. No graphics will be needed because it will be
	invisible to the player.
	"""
	def __init__(self, x, y):
		pg.sprite.Sprite.__init__(self)
		self.relX = x
		self.relY = y
		self.image = pg.Surface((50,50))
		self.rect = pg.Rect([x, y, 16 * c.ZOOM, 32 * c.ZOOM])