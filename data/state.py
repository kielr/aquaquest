__author__ = "kiel.regusters"
"""
This module contains the class for the main states used in the game.
"""

class State(object):
	def __init__(self):
		self.done = False
		self.quit = False
		self.next = None
		self.previous = None
	
	def Update(self, surface, keys, currentTime, events):
		""" Function called every tick. Update functions differ on the state so this method must be overwritten. """
		pass