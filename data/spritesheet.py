__author__ = "kiel.regusters"
"""
Module that contains classes that make it easy to draw the map, and its characters/animations.
"""

import pygame as pg
from . import init

class TextureAtlas(object):
	""" Class that will contain a dictionary of every frame of a tileset/spritesheet """
	def __init__(self, tileSizeX, tileSizeY, tileset):
		self.tileSizeX = tileSizeX
		self.tileSizeY = tileSizeY
		self.tileset = tileset
		self.tilesetSize = tileset.get_size()
		self.tileCount = int((self.tilesetSize[0] * self.tilesetSize[1]) / (tileSizeX * tileSizeY))
		self.tileDict = {} # tile dict that will contain gid : subsurface
		# Create subsurfaces
		i, j = 0, 0
		gid = 1
		while i < self.tilesetSize[0]:
			j = 0
			while j < self.tilesetSize[1]:
				self.tileDict[gid] = tileset.subsurface([i, j, self.tileSizeX, self.tileSizeY])
				gid += 1
				j += self.tileSizeX
			i += self.tileSizeY

		print("done")