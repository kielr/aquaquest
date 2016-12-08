__author__ = "kiel.regusters"
"""
This module contains utility functions for loading content into the game.
"""
import pygame as pg
import os
import sys
sys.path.append(os.path.join("resources", "graphics"))
sys.path.append(os.path.join("resources", "music"))
sys.path.append(os.path.join("resources", "sfx"))
sys.path.append(os.path.join("resources", "tilesets"))
sys.path.append(os.path.join("resources", "maps"))

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

def load_all_music(directory, acccept=('.wav', '.mp3', '.ogg', '.mdi')):
	songs = {}
	for song in os.listdir(directory):
		name,ext = os.path.splitext(song)
		if ext.lower() in acccept:
			songs[name] = os.path.join(directory, song)
	return songs

def load_all_sfx(directory, accept=('.wav', '.mp3', '.ogg', '.mdi')):
	effects = {}
	for sfx in os.listdir(directory):
		name, ext = os.path.splitext(sfx)
		if ext.lower() in accept:
			effects[name] = pg.mixer.Sound(os.path.join(directory, sfx))
	return effects
