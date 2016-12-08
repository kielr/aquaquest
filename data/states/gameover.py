"""
Module that holds the Gameover state class.
"""

__author__ = "kiel.regusters"


import pygame as pg
from .. import state
from .. import constants as c
from .. import utility
from .. import init
from .. import debug
from .. import soundmanager

class GameOver(state.State):
	"""
	This class handles the gameover screen state of the game
	"""
	def __init__(self):
		state.State.__init__(self)
	
	def StartUp(self, currentTime):
		"""
		The initial function called on every state. Sets up overhead info, soundmanager, and graphics if necessary
		"""
		self.startTime = currentTime
		self.next = c.MAIN_MENU
		self.overhead = utility.Overhead(c.GAMEOVER)
		self.soundManager = soundmanager.Sound(self.overhead)
		self.loadScreen = init.GRAPHICS['gameover']

	def Update(self, surface, keys, currentTime, events):
		""" Listen for escape keys to the main menu """
		for event in events:
			if event.type == pg.KEYDOWN:
				if keys[pg.K_ESCAPE]:
					self.done = True
					self.next = c.MAIN_MENU
		surface.blit(self.loadScreen, (0,0))