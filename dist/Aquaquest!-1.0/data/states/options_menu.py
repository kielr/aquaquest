"""
This Module contains the Options state class.
"""

__author__ = "kiel.regusters"

import sys
sys.path.append("..")
import pygame as pg
from .. import constants as c
from .. import state
from .. import init
from .. import utility
from .. import soundmanager
from .. import debug

class Options(state.State):
	"""
	This is the class for the main menu state. This is where the user will choose what to change in options.

	>>> Options()
	<__main__.Options object at ...>
	"""
	def __init__(self):
		state.State.__init__(self)
		self.StartUp(0.0)

	def StartUp(self, currentTime):
		"""
		Called everytime we switch to this state
		"""
		self.overhead = utility.Overhead(c.MAIN_MENU)
		self.soundManager = soundmanager.Sound(self.overhead)
		self.titlescreen = init.GRAPHICS['options']
		self.SetupCursor()

	def SetupCursor(self):
		"""
		Same as the main menu cursor set up, slightly different initial position
		"""
		self.cursor = pg.sprite.Sprite()
		dest = (40, 60)

		self.cursor.image, self.cursor.rect = self.GetImage(0, 0, 16, 16, dest, init.GRAPHICS['cursor'])
		self.cursor.image.set_colorkey((255,0,255))
		self.cursor.state = c.MUSIC_MUTE

	def GetImage(self, x, y, width, height, dest, spritesheet):
		"""
		@param x: the width of the image
		@param y: the height of the image
		@param dest: where to blit the sprite
		@param spritesheet: the original image
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
		positions = [60, 140]
		input_list = [pg.K_SPACE, pg.K_RETURN, pg.K_e, pg.K_f]
		for event in events:
			if event.type == pg.KEYDOWN:
				if self.cursor.state == c.MUSIC_MUTE:
					if keys[pg.K_s]:
						self.soundManager.sfx['cursor_move'].play()
						self.cursor.rect.y = positions[1]
						self.cursor.state = c.BACK
					elif keys[pg.K_w]:
						self.soundManager.sfx['cursor_move'].play()
						self.cursor.rect.y = positions[1]
						self.cursor.state = c.BACK
					for input in input_list:
						if keys[input]:
							if c.MUTE == False:
								c.MUTE = True
								self.soundManager.sfx['cursor_select_quit'].play()
								debug.debug("Mute selected.")
								debug.debug("Stopping music")
								self.soundManager.StopBGM()
							else:
								c.MUTE = False
								self.soundManager.sfx['cursor_select'].play()
								debug.debug("Unmute selected.")
								debug.debug("Starting music")
								self.soundManager.MixerStartup()

				else:
					if keys[pg.K_s]:
						self.soundManager.sfx['cursor_move'].play()
						self.cursor.rect.y = positions[0]
						self.cursor.state = c.MUSIC_MUTE
					elif keys[pg.K_w]:
						self.soundManager.sfx['cursor_move'].play()
						self.cursor.rect.y = positions[0]
						self.cursor.state = c.MUSIC_MUTE
					for input in input_list:
						if keys[input]:
							self.soundManager.sfx['cursor_select'].play()
							debug.debug("Back Selected")
							debug.debug("Going back to main menu")
							self.done = True
							self.next = c.MAIN_MENU



	def Update(self, surface, keys, currentTime, events):
		""" Updates the state every tick """
		self.UpdateCursor(keys, events)
		surface.blit(self.titlescreen, (0,0))
		surface.blit(self.cursor.image, self.cursor.rect)
