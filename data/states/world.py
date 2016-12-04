__author__ = "kiel.regusters"
import pygame as pg
import os
from .. import state
from .. libs import pytmx
from .. libs import util_pygame
from .. import soundmanager
from .. import utility
from .. import constants as c
from .. import debug

class World(state.State):
	""" 
	This class holds the TMX map and handles collision between entities inside the map.
	It will also probably handle things like checkpoint and file IO for saving.
	"""
	def __init__(self):
		state.State.__init__(self)
	def StartUp(self, currentTime):
		# The player got here from PLAY, so it's the first level.
		debug.debug("Getting TMX file...")
		self.tiledMap = util_pygame.load_pygame("resources/maps/level1.tmx")
		debug.debug("Done")
		self.entities = []
		self.overhead = utility.Overhead(c.LEVEL1)
		self.soundManager = soundmanager.Sound(self.overhead)

	def Update(self, surface, keys, currentTime, events):
		pass