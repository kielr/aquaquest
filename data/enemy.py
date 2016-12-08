__author___ = "kiel.regusters"
import pygame as pg
from . import constants as c
from . import init, gamemanager
from itertools import cycle

class Enemy(pg.sprite.Sprite):
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
		self.HP = 100
		self.XPreward = 25
		self.isDead = False
		self.damageInvuln = False
		self.damageInvulnFrames = 30
		self.damageInvulnTimer = 0

	def SetUpForces(self):
		self.velX = 0
		self.velY = 0
		self.maxVelX = c.MAX_VEL_X
		self.maxVelY = c.MAX_VEL_Y
		self.gravity = c.GRAVITY
		self.accelX = c.ACCEL

	def Update(self):
		pass

	def CheckForDeath(self):
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
	def __init__(self, name):
		Enemy.__init__(self, name)
		self.turnAroundFrames = 120
		self.turnAroundCurrent = 0
		self.SetUpAnimations()
		self.velX = 2.5

	def SetUpAnimations(self):
		self.anims['idle-right'] = [0]
		self.anims['idle-left'] = [1]
		self.anims['death'] = [9]
		self.anims['invisible'] = [10]
		self.anims['walk-right'] = cycle([3, 4])
		self.anims['walk-left'] = cycle([6, 7])
		self.image = self.frames[self.anims['idle-right'][0]]
		self.rect = self.image.get_rect()

	def Update(self):
		if self.state == c.WALKING:
			self.Patrol()
		if self.state == c.DEAD:
			self.Death()
		self.Invulnerable()
		self.Animation()

	def Death(self):
		self.velY += self.gravity
		self.velX = 0
		self.frameIndex = self.anims['death'][0]

	def TakeDamage(self, damage):
		if self.damageInvuln == False:
			init.SFX['hurt'].play()
			self.damageInvuln = True
			self.HP -= damage
			if self.facingRight:
				self.velY -= 5
			else:
				self.velY -= 5

	def Invulnerable(self):
		if self.damageInvulnTimer == self.damageInvulnFrames:
			self.damageInvuln = False
			self.damageInvulnTimer = False
		else:
			self.damageInvulnTimer += 1

	def Patrol(self):
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