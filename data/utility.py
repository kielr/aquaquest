__author__ = "kiel.regusters"
""" This module contains the Overhead class, and a class for writing text."""
import pygame as pg
from . import init
from . import constants as c

class Character(pg.sprite.Sprite):
	def __init__(self, image):
		super(Character, self).__init__()
		self.image = image
		self.rect = self.image.get_rect()

class Overhead(object):
	""" The Overhead class keeps track of certain information. """
	def __init__(self, state):
		self.state = state
		self.spriteSheet = init.GRAPHICS['font']
		self.levelUpImage = init.GRAPHICS['levelupscreen']
		self.CreateImageList()
		self.CreateLifeLabel()
		self.CreateLVLLabel()
		self.CreateSTRLabel()
		self.CreateDEXLabel()
		self.CreateINTLabel()
		self.CreateOrangeNumbers()
		self.CreateTanNumbers()
		self.CreateBlueNumbers()
		self.CreateGreenNumbers()
		self.info = None

	def CreateOrangeNumbers(self):
		"""
		Set up the dictionary containing orange font numbers.
		"""
		self.orangeDict = {}
		count = 0
		for i in range(21, 32):
			self.orangeDict[count] = self.frames[i]
			count += 1

	def CreateTanNumbers(self):
		"""
		Set up the dictionary containing tan font numbers.
		"""
		self.tanDict = {}
		count = 0
		for i in range(405, 416):
			self.tanDict[count] = self.frames[i]
			count += 1

	def CreateBlueNumbers(self):
		"""
		Set up the dictionary containing blue font numbers.
		"""
		self.blueDict = {}
		count = 0
		for i in range(213, 224):
			self.blueDict[count] = self.frames[i]
			count += 1

	def CreateGreenNumbers(self):
		"""
		Set up the dictionary containing green font numbers.
		"""
		self.greenDict = {}
		count = 0
		for i in range(341, 352):
			self.greenDict[count] = self.frames[i]
			count += 1

	def CreateImageList(self):
		"""
		Load all of the frames we need from our font spritesheet.
		"""
		spriteSheetRect = self.spriteSheet.get_rect()
		tileWidth = int(spriteSheetRect.width / 16)
		tileHeight = int(spriteSheetRect.height / 16)
		self.frames = []
		for j in range(tileHeight):
			for i in range(tileWidth):
				newSurface = pg.Surface((c.TILE_SIZE, c.TILE_SIZE))
				newSurface.blit(self.spriteSheet, (0,0), (i * c.TILE_SIZE, j* c.TILE_SIZE,c.TILE_SIZE, c.TILE_SIZE))
				newSurface.set_colorkey((128, 0, 128))
				rect = newSurface.get_rect()
				newSurface = pg.transform.scale(newSurface,
							  (int(rect.width * 2), int(rect.height * 2)))
				self.frames.append(newSurface)

		self.blitLevelUp = pg.Surface((800, 600))
		self.blitLevelUp.set_colorkey((128, 0, 128))
		self.blitLevelUp.blit(self.levelUpImage, (0,0))

	def CreateLifeLabel(self):
		"""
		Create the life text that will be shown on the UI.
		"""
		letters = [self.frames[43], self.frames[40], self.frames[37], self.frames[36]]
		self.lifeLabel = pg.Surface((64 * 3,16 * 3))
		i = 0
		self.lifeLabel.fill(c.BLACK)
		self.lifeLabel.set_colorkey(c.BLACK)
		for letter in letters:
			self.lifeLabel.blit(letter, (i, 0))
			i += 16 * 2

	def CreateLVLLabel(self):
		"""
		Create the LVL text that will be shown on the UI.
		"""
		letters = [self.frames[43], self.frames[53], self.frames[43]]
		self.lvlLabel = pg.Surface((64 * 3,16 * 3))
		i = 0
		self.lvlLabel.fill(c.BLACK)
		self.lvlLabel.set_colorkey(c.BLACK)
		for letter in letters:
			self.lvlLabel.blit(letter, (i, 0))
			i += 16 * 2

	def CreateSTRLabel(self):
		"""
		Create the STR text that will be shown on the UI.
		"""
		letters = [self.frames[434], self.frames[435], self.frames[433]]
		self.STRLabel = pg.Surface((64 * 3,16 * 3))
		i = 0
		self.STRLabel.fill(c.BLACK)
		self.STRLabel.set_colorkey(c.BLACK)
		for letter in letters:
			self.STRLabel.blit(letter, (i, 0))
			i += 16 * 2

	def CreateDEXLabel(self):
		"""
		Create the DEX text that will be shown on the UI.
		"""
		letters = [self.frames[355], self.frames[356], self.frames[375]]
		self.DEXLabel = pg.Surface((64 * 3,16 * 3))
		i = 0
		self.DEXLabel.fill(c.BLACK)
		self.DEXLabel.set_colorkey(c.BLACK)
		for letter in letters:
			self.DEXLabel.blit(letter, (i, 0))
			i += 16 * 2

	def CreateINTLabel(self):
		"""
		Create the INT text that will be shown on the UI.
		"""
		letters = [self.frames[232], self.frames[237], self.frames[243]]
		self.INTLabel = pg.Surface((64 * 3,16 * 3))
		i = 0
		self.INTLabel.fill(c.BLACK)
		self.INTLabel.set_colorkey(c.BLACK)
		for letter in letters:
			self.INTLabel.blit(letter, (i, 0))
			i += 16 * 2

	def Update(self, info):
		"""
		Called every frame, update the player persistant info.
		"""
		self.UpdateInfo(info)

	def UpdateInfo(self, info):
		"""
		Do the actual updating.
		"""
		self.info = info

	def draw(self, surface):
		"""
		This method draws the game UI
		"""
		# Draw level screen
		if self.info['SP'] != 0:
			surface.blit(self.blitLevelUp, (0,0))
		# Draw LVL
		surface.blit(self.lvlLabel, (175,5))
		# Draw LVL Total
		if self.info['LVL'] < 10:
			surface.blit(self.orangeDict[self.info['LVL']], (202, 35))
		else:
			surface.blit(self.orangeDict[self.info['LVL'] // 10], (202, 35))
			surface.blit(self.orangeDict[self.info['LVL'] % 10], (234, 35))


		# Draw STR
		surface.blit(self.STRLabel, (286,5))

		# Drw STR Total
		surface.blit(self.tanDict[self.info['STR']], (318, 35))

		# Draw DEX
		surface.blit(self.DEXLabel, (397,5))

		# Drw DEX Total
		surface.blit(self.greenDict[self.info['DEX']], (434, 35))

		# Draw INT
		surface.blit(self.INTLabel, (508,5))

		# Drw INT Total
		surface.blit(self.blueDict[self.info['INT']], (550, 35))

		# Draw XP Bar back
		pg.draw.rect(surface, c.BLACK, [5, 53, 100 * 1.2, 16])

		if self.info['XP'] !=0:
			pg.draw.rect(surface, (233, 233, 0), [5, 53, self.info['XP'] * 1.2, 16])

		# Draw Life
		surface.blit(self.lifeLabel, (5,5))
		# Draw Life Bar
		pg.draw.rect(surface, (255, 0, 0), [5, 37, 100 * 1.2, 16])
		if self.info['HP'] != 0:
			pg.draw.rect(surface, (0, 200, 0), [5, 37, self.info['HP'] * 1.2, 16])
