__author__ = "kiel.regusters"
import pygame as pg
import os
from .. import state
from .. libs import pytmx
from .. libs import util_pygame
from .. import soundmanager
from .. import utility
from .. import constants as c
from .. import debug
from .. import init
from .. import camera
from .. import player

class World(state.State):
	""" 
	This class holds the TMX map and handles collision between entities inside the map.
	It will also probably handle things like checkpoint and file IO for saving.
	"""
	def __init__(self):
		state.State.__init__(self)

	def StartUp(self, currentTime):
		# The player got here from PLAY, so it's the first level.
		debug.debug("Getting TMX file...")
		self.tiledMap = util_pygame.load_pygame("resources/maps/level1.tmx")
		self.levelSurface = pg.Surface((int(c.TILE_SIZE * self.tiledMap.width * c.ZOOM), 
								  int(c.TILE_SIZE * self.tiledMap.height * c.ZOOM))).convert()
		self.levelRect = self.levelSurface.get_rect()
		debug.debug("Done")
		debug.debug("Spawning Player")
		self.overhead = utility.Overhead(c.LEVEL1)
		self.soundManager = soundmanager.Sound(self.overhead)
		self.camera = camera.Camera()
		self.state = c.UNPAUSE
		self.camera.limitRect = self.levelRect
		self.SpawnPlayer()
		self.SetUpSpriteGroups()
		#Draw to Level surface
		self.DrawLevel()

	def SetUpSpriteGroups(self):
		self.playerGroup = pg.sprite.Group(self.player)
		self.SetUpSolidGroup()

	def SetUpSolidGroup(self):
		self.levelGroup = pg.sprite.Group()
		for layer in self.tiledMap.layers:
			if "Solid" in layer.name:
				for x,y,image in layer.tiles():
					newSprite = pg.sprite.Sprite()
					newSprite.rect = image.get_rect()
					newSprite.rect[0] = x * 16 * c.ZOOM - self.camera.x
					newSprite.rect[1] = y * 16 * c.ZOOM - self.camera.y
					newSprite.rect[2] *= c.ZOOM
					newSprite.rect[3] *= c.ZOOM
					self.levelGroup.add(newSprite)

	def SpawnPlayer(self):
		# Find where player should spawn
		playerSpawnObject = self.tiledMap.get_object_by_name("playerSpawn")
		self.playerX = playerSpawnObject.x
		self.playerY = playerSpawnObject.y
		self.player = player.Player()
		self.player.rect.x = self.playerX * c.ZOOM - self.camera.x
		self.player.rect.y = self.playerY * c.ZOOM - self.camera.y
		self.player.relX = self.playerX * c.ZOOM
		self.player.relY = self.playerY * c.ZOOM


	def Update(self, surface, keys, currentTime, events):

		# Handle States
		self.HandleStates(keys, events)

		# Draw Everything
		self.DrawEverything(surface)

		# Update Sound
		self.soundManager.Update()

	def HandleStates(self, keys, events):
		if self.state == c.UNPAUSE:
			self.UpdateAllSprites(keys, events)

	def UpdateAllSprites(self, keys, events):
		self.player.Update(keys, events)
		self.MovePlayerX()
		self.CheckPlayerXLevelCollisions()
		self.UpdateCameraX()
		self.MovePlayerY()
		self.CheckPlayerYLevelCollisions()
		self.UpdateCameraY()

	def MovePlayerX(self):
		self.player.relX += self.player.velX
		self.player.rect.x = self.player.relX - self.camera.x
		
	def CheckPlayerXLevelCollisions(self):
		tile = pg.sprite.spritecollideany(self.player, self.levelGroup)

		if tile:
			self.ResolvePlayerXLevelCollisions(tile)

	def CheckPlayerYLevelCollisions(self):
		tile = pg.sprite.spritecollideany(self.player, self.levelGroup)

		if tile:
			self.ResolvePlayerYLevelCollisions(tile)
			self.player.allowJump = True

	def ResolvePlayerXLevelCollisions(self, collider):
		if self.player.velX > 0: # Going right
			intersectDepth = collider.rect.left - self.player.rect.right
			if intersectDepth < (-16*3):
				return

			# Correct the position
			self.player.relX += intersectDepth
			self.player.rect.x = self.player.relX - self.camera.x

		elif self.player.velX < 0: # Going left
			intersectDepth = collider.rect.right - self.player.rect.left
			if intersectDepth > 16*3:
				return

			# Correct the position
			self.player.relX += intersectDepth
			self.player.rect.x = self.player.relX - self.camera.x


	def ResolvePlayerYLevelCollisions(self, collider):
		if self.player.velY > 0: # Going Down
			intersectDepth = collider.rect.top - self.player.rect.bottom
			if intersectDepth < (-16*3):
				return

			# Correct the position
			self.player.relY += intersectDepth
			self.player.rect.y = self.player.relY - self.camera.y
			self.player.velY = 0

		elif self.player.velY < 0: # Going Up
			intersectDepth = collider.rect.bottom - self.player.rect.top
			if intersectDepth > 16*3:
				return

			# Correct the position
			self.player.relY += intersectDepth
			self.player.rect.y = self.player.relY - self.camera.y
			self.player.velY = 0

	def MovePlayerY(self):
		self.player.relY += self.player.velY
		self.player.rect.y = self.player.relY - self.camera.y
	
	def UpdateCameraX(self):
		# Look at the player
		if self.player.facingRight:
			self.camera.LookAtX(self.player.relX)
		else:
			self.camera.LookAtX(self.player.relX)
		third = self.camera.viewport.x + self.camera.viewport.w//3
		third_right = third * 2

		if self.player.rect.centerx >= third_right:
			self.camera.Move(self.player.velX,0)
		if self.player.rect.centerx <= third and self.player.velX <= 0:
			self.camera.Move(self.player.velX, 0)

	def UpdateCameraY(self):
		# Look at the player
		if self.player.facingRight:
			self.camera.LookAtY(self.player.relY + 75)
		else:
			self.camera.LookAtY(self.player.relY + 75)
		#half = self.camera.viewport.y + self.camera.viewport.h//2
		#third = self.camera.viewport.y + self.camera.viewport.h//3
		#third_right = third * 2

		#if self.player.rect.centery >= half:
		#	self.camera.Move(0,self.player.velY)
		#if self.player.rect.centery <= third_right and self.player.velY <= 0:
		#	self.camera.Move(0, self.player.velY)

	def DrawLevel(self):
		self.levelSurface.fill(c.BLACK)
		for layer in self.tiledMap.layers:
			if "Object" not in str(type(layer)):
				for x,y,image in layer.tiles():
					rect = image.get_rect()
					self.levelSurface.blit(pg.transform.scale(image, (int(rect.width*3), 
												(int(rect.width*3)))), 
												[c.TILE_SIZE * c.ZOOM * x, c.TILE_SIZE * c.ZOOM * y])


	def DrawEverything(self, surface):
		self.SetUpSolidGroup()
		#Draw player

		# Draw to the surface
		surface.blit(self.levelSurface, (0,0), [0 + self.camera.x, 0+self.camera.y, self.camera.viewport.width, self.camera.viewport.height])
		# Draw player
		self.playerGroup.draw(surface)
		# Draw weapon if active
		if self.player.meleeActive:
			if self.player.facingRight:
				surface.blit(self.player.weaponImage, [self.player.rect.x + 45, self.player.rect.y - 25, self.player.rect.w, self.player.rect.h])
			else:
				surface.blit(pg.transform.flip(self.player.weaponImage, True, False), 
				 [self.player.rect.x - 95, self.player.rect.y - 25, self.player.rect.w, self.player.rect.h])


		if debug.DEBUG_DRAW:
			pg.draw.rect(surface, (255, 0, 0), self.player.rect)
			for sprites in self.levelGroup.sprites():
				pg.draw.rect(surface, (255,0,0), sprites.rect)