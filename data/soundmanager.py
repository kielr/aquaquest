__author__ = "kiel.regusters"

"""
Module that handles sound and bgm based off of the state of the game.
"""

import pygame as pg
from . import init
from . import constants as c
from . import utility

class Sound(object):
	"""
	Sound manager that handles the playing of music.
	"""
	def __init__(self, overhead=None):
		self.music_dict = init.BGM
		self.sfx = init.SFX
		self.overhead = overhead
		if overhead != None:
			self.MixerStartup()


	def MixerStartup(self):
		""" Plays the correct BGM depending on the state of the game. """
		if self.overhead.state == c.MAIN_MENU:
			try:
				pg.mixer.music.load(self.music_dict['title'])
				pg.mixer.music.set_volume(0.5)
				pg.mixer.music.play(loops=-1)
				self.state = c.s_MENU
			except(KeyError):
				print("ERROR: title music not found!")
		elif self.overhead.state == c.LEVEL1:
			try:
				pg.mixer.music.load(self.music_dict['level1'])
				pg.mixer.music.set_volume(0.5)
				pg.mixer.music.play(loops=-1)
				self.state = c.NORMAL
			except(KeyError):
				print("ERROR: level music not found!")
	def StopBGM(self):
		""" Simply stops all playback for music when called. """
		pg.mixer.music.stop()

	def Update(self):
		pass