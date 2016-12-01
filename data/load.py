"""
This module contains utility functions for loading content into the game.
"""
import pygame as pg
import os



def load_all_gfx(directory, accept=(".png", ".jpg", ".bmp")):
	gfx = {}
	for tileset in os.listdir(directory):
		name, ext = os.path.splitext(tileset)
		if ext.lower() in accept:
			img = pg.image.load(os.path.join(directory, tileset))
			if img.get_alpha():
				img = img.convert_alpha()
			else:
				continue
			gfx[name] = img
	return gfx