"""
This module contains the information needed to create working enemies.
"""

__author___ = "kiel.regusters"
import pygame as pg
from . import constants as c
from . import init, gamemanager
from itertools import cycle

class Enemy(pg.sprite.Sprite):
	"""
	The base enemy class. If you want to make a new enemy type you can just inherit from this and change a few things.
	"""
	def __init__(self, name):
		pg.sprite.Sprite.__init__(self)
		self.spriteSheet = init.GRAPHICS[name]
		self.anims = {}
		self.state = c.WALKING
		self.frameIndex = 0
		self.switchIndex = 10
		self.switchCounter = 0
		self.facingRight = True
		self.relX = 0
		self.relY = 0
		self.LoadFrames()
		self.SetUpForces()
		self.SetUpStats()

	def LoadFrames(self):
		"""
		Loads the frames for the enemy animations.
		"""
		spriteSheetRect = self.spriteSheet.get_rect()
		tileWidth = int(spriteSheetRect.width / 16)
		tileHeight = int(spriteSheetRect.height / 16)
		self.frames = []
		for j in range(tileHeight):
			for i in range(tileWidth):
				newSurface = pg.Surface((c.TILE_SIZE, c.TILE_SIZE))
				newSurface.blit(self.spriteSheet, (0,0), (i * c.TILE_SIZE, j* c.TILE_SIZE,c.TILE_SIZE, c.TILE_SIZE))
				newSurface.set_colorkey((255, 0, 255))
				rect = newSurface.get_rect()
				newSurface = pg.transform.scale(newSurface,
							  (int(rect.width * c.ZOOM), int(rect.height * c.ZOOM)))
				self.frames.append(newSurface)

	def SetUpAnimations(self):
		pass

	def SetUpStats(self):
		"""
		Sets up the various stats for the enemy
		"""
		self.HP = 100
		self.XPreward = 25
		self.isDead = False
		self.damageInvuln = False
		self.damageInvulnFrames = 30
		self.damageInvulnTimer = 0

	def SetUpForces(self):
		"""
		Sets up the forces akin to the way the player's forces are set up.
		"""
		self.velX = 0
		self.velY = 0
		self.maxVelX = c.MAX_VEL_X
		self.maxVelY = c.MAX_VEL_Y
		self.gravity = c.GRAVITY
		self.accelX = c.ACCEL

	def Update(self):
		"""
		Main update, it does nothing in this base class. It must be overriden.
		"""
		pass

	def CheckForDeath(self):
		"""
		Check for the death of the enemy. If the health reaches 0 or below then set the state to dead.
		"""
		if(self.HP <= 0):
			self.isDead = True
			self.state = c.DEAD
		elif(self.HP >= 100):
			self.HP = 100

	def Animation(self):
		if self.damageInvuln == False or self.isDead:
			self.image = self.frames[self.frameIndex]
		else:
			if self.damageInvulnTimer % 4 == 0:
				self.image = self.frames[self.frameIndex]
			else:
				self.image = self.frames[self.anims["invisible"][0]]

class Zombie(Enemy):
	"""
	The main enemy used in the game
	"""
	def __init__(self, name):
		"""
		@param name: used to determine what graphics to load for the enemy. THis makes it easier to add enemies in later for enemies whose assets are made.
		"""
		Enemy.__init__(self, name)
		self.turnAroundFrames = 120
		self.turnAroundCurrent = 0
		self.SetUpAnimations()
		self.velX = 2.5

	def SetUpAnimations(self):
		"""
		set up all the animations for the zombie
		"""
		self.anims['idle-right'] = [0]
		self.anims['idle-left'] = [1]
		self.anims['death'] = [9]
		self.anims['invisible'] = [10]
		self.anims['walk-right'] = cycle([3, 4])
		self.anims['walk-left'] = cycle([6, 7])
		self.image = self.frames[self.anims['idle-right'][0]]
		self.rect = self.image.get_rect()

	def Update(self):
		"""
		Main update loop for the zombie. Do different things dependent on the state.
		"""
		if self.state == c.WALKING:
			self.Patrol()
		if self.state == c.DEAD:
			self.Death()
		self.Invulnerable()
		self.Animation()

	def Death(self):
		"""
		Function called if this zombie is dead. Set the frame to the death frame and apply gravity.
		"""
		self.velY += self.gravity
		self.velX = 0
		self.frameIndex = self.anims['death'][0]

	def TakeDamage(self, damage):
		"""
		Method called by the world when it decides that the zombie needs to take damage.
		"""
		if self.damageInvuln == False:
			init.SFX['hurt'].play()
			self.damageInvuln = True
			self.HP -= damage
			if self.facingRight:
				self.velY -= 5
			else:
				self.velY -= 5

	def Invulnerable(self):
		"""
		Method called to check and apply invulnerability of we've taken damage recently.
		"""
		if self.damageInvulnTimer == self.damageInvulnFrames:
			self.damageInvuln = False
			self.damageInvulnTimer = False
		else:
			self.damageInvulnTimer += 1

	def Patrol(self):
		"""
		Default state of the zombie. Walk bak and forth and make sure to change our sprite based on direction.
		"""
		self.velY += self.gravity

		if(self.switchCounter == self.switchIndex):
			if self.facingRight:
				self.frameIndex = next(self.anims['walk-right'])
				self.switchCounter = 0
			else:
				self.frameIndex = next(self.anims['walk-left'])
				self.switchCounter = 0
		else:
			self.switchCounter += 1

		if self.turnAroundCurrent == self.turnAroundFrames:
			self.facingRight = False if self.facingRight == True else True
			if self.facingRight:
				self.velX = 2.5
			else:
				self.velX = -2.5
			self.turnAroundCurrent = 0
		else:
			self.turnAroundCurrent += 1