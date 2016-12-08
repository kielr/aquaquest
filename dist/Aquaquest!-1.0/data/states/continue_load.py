"""
Module that holds the LoadScreen state class.
"""

__author__ = "kiel.regusters"

import sys
sys.path.append("..")
import pygame as pg
from .. import state
from .. import constants as c
from .. import utility
from .. import init
from .. import debug

class Continue(state.State):
	"""
	This class handles the loading screen animation. It doesn't actually do the loading, it is only for show.
	Slightly different from the loading state in that self.next is set to c.LOADMAP to let the gamemanager know to load
	a save file instead of a new game.

	>>> Continue()
	<__main__.Continue object at ...>
	"""
	def __init__(self):
		state.State.__init__(self)

	def StartUp(self, currentTime):
		"""
		The initial function called on every state. Sets up overhead info, soundmanager, and graphics if necessary
		"""
		self.startTime = currentTime
		self.next = c.LOADMAP
		self.overhead = utility.Overhead(c.LOAD_SCREEN)
		self.loadScreen = init.GRAPHICS['load']
		self.i = 0;

	def Update(self, surface, keys, currentTime, events):
		""" Simulate the loading of a retro game """
		if (currentTime - self.startTime) < 1400:
			surface.blit(self.loadScreen, (0,0))
			surface.fill((23, 19, 45), [220, 310, self.i, 40])
			if self.i < 370:
				self.i += 5
		else:
			debug.debug("Loading done, go to the map state.")
			self.done = True
