"""
This module contains the Menu state class for the game.
"""

__author__ = "kiel.regusters"

import pygame as pg
from .. import constants as c
from .. import state
from .. import init
from .. import utility
from .. import soundmanager
from .. import debug

class Menu(state.State):
	"""
	This is the class for the main menu state. This is where the user will choose what the program do.
	"""
	def __init__(self):
		state.State.__init__(self)
		self.StartUp(0.0)

	def StartUp(self, currentTime):
		"""
		The initial function called on every state. Sets up overhead info, soundmanager, and graphics if necessary
		"""
		self.overhead = utility.Overhead(c.MAIN_MENU)
		self.soundManager = soundmanager.Sound(self.overhead)
		self.titlescreen = init.GRAPHICS['title']
		self.SetupCursor()

	def SetupCursor(self):
		"""
		Sets up the cursor sprite and initializees its state for later.
		"""
		self.cursor = pg.sprite.Sprite()
		dest = (220, 275)

		self.cursor.image, self.cursor.rect = self.GetImage(0, 0, 16, 16, dest, init.GRAPHICS['cursor'])
		self.cursor.image.set_colorkey((255,0,255))
		self.cursor.state = c.PLAY

	def GetImage(self, x, y, width, height, dest, spritesheet):
		"""
		Gets the image of the cursor and scales it up.
		"""
		image = pg.Surface([width, height])
		rect = image.get_rect()

		image.blit(spritesheet, (0, 0), (x, y, width, height))

		image = pg.transform.scale(image, (int(rect.width*3), (int(rect.width*3))))
		rect = image.get_rect()
		rect.x = dest[0]
		rect.y = dest[1]

		return (image, rect)
	#
	def UpdateCursor(self, keys, events):
		"""
		Called every frame and listens for user input to move the cursor around.
		"""
		positions = [275, 325, 435, 375]
		input_list = [pg.K_SPACE, pg.K_RETURN, pg.K_e, pg.K_f]
		for event in events:
			if event.type == pg.KEYDOWN:
				if self.cursor.state == c.PLAY:
					if keys[pg.K_s]:
						self.soundManager.sfx['cursor_move'].play()
						self.cursor.rect.y = positions[1]
						self.cursor.state = c.LOAD
					elif keys[pg.K_w]:
						self.soundManager.sfx['cursor_move'].play()
						self.cursor.rect.y = positions[2]
						self.cursor.state = c.QUIT
					for input in input_list:
						if keys[input]:
							self.soundManager.sfx['cursor_select'].play()
							debug.debug("Stopping music")
							self.soundManager.StopBGM()
							debug.debug("Play selected.")
							debug.debug("Set the next state to a load screen")
							self.done = True
							self.next = c.LOAD_SCREEN
							pg.time.wait(1000)
				elif self.cursor.state == c.OPTIONS:
					if keys[pg.K_s]:
						self.soundManager.sfx['cursor_move'].play()
						self.cursor.rect.y = positions[2]
						self.cursor.state = c.QUIT
					elif keys[pg.K_w]:
						self.soundManager.sfx['cursor_move'].play()
						self.cursor.rect.y = positions[1]
						self.cursor.state = c.LOAD
					for input in input_list:
						if keys[input]:
							debug.debug("Stopping music")
							self.soundManager.sfx['cursor_select'].play()
							debug.debug("Options selected.")
							debug.debug("Set the next state to options")
							self.done = True
							self.next = c.OPTIONS
				elif self.cursor.state == c.LOAD:
					if keys[pg.K_s]:
						self.soundManager.sfx['cursor_move'].play()
						self.cursor.rect.y = positions[3]
						self.cursor.state = c.OPTIONS
					elif keys[pg.K_w]:
						self.soundManager.sfx['cursor_move'].play()
						self.cursor.rect.y = positions[0]
						self.cursor.state = c.PLAY
					for input in input_list:
						if keys[input]:
							debug.debug("Stopping music")
							self.soundManager.sfx['cursor_select'].play()
							debug.debug("Continue selected.")
							debug.debug("Set the next state to a load screen")
							self.done = True
							self.next = c.CONTINUE
				else:
					if keys[pg.K_s]:
						self.soundManager.sfx['cursor_move'].play()
						self.cursor.rect.y = positions[0]
						self.cursor.state = c.PLAY
					elif keys[pg.K_w]:
						self.soundManager.sfx['cursor_move'].play()
						self.cursor.rect.y = positions[3]
						self.cursor.state = c.OPTIONS
					for input in input_list:
						if keys[input]:
							self.soundManager.sfx['cursor_select_quit'].play()
							debug.debug("Player quit.")
							pg.time.wait(1000)
							self.soundManager.StopBGM()
							self.quit = True
							self.done = True



	def Update(self, surface, keys, currentTime, events):
		""" Updates the state every tick """
		self.UpdateCursor(keys, events)
		surface.blit(self.titlescreen, (0,0))
		surface.blit(self.cursor.image, self.cursor.rect)