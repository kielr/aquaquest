__author__ = "kiel.regusters"

"""
Module that handles sound and bgm based off of the state of the game.
"""

import pygame as pg
from . import init
from . import constants as c
from . import utility

class Sound(object):
	def __init__(self, overhead):
		self.music_dict = init.BGM
		self.sfx = init.SFX
		self.overhead = overhead
		self.MixerStartup()

	def MixerStartup(self):
		""" Plays the correct BGM depending on the state of the game. """
		if self.overhead.state == c.MAIN_MENU:
			pg.mixer.music.load(self.music_dict['title'])
			pg.mixer.music.set_volume(0.5)
			pg.mixer.music.play()

	def StopBGM(self):
		""" Simply stops all playback for music when called. """
		pg.mixer.music.stop()