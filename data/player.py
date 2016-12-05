import pygame as pg
from . import constants as c
from . import init, gamemanager
from itertools import cycle

keybinding = {
	'left':pg.K_a,
	'right':pg.K_d,
	'jump':pg.K_SPACE
}

class Player(pg.sprite.Sprite):
	def __init__(self):
		pg.sprite.Sprite.__init__(self)
		self.spriteSheet = init.GRAPHICS['character']
		self.anims = {}
		self.velX = 0
		self.velY = 0
		self.maxVelX = c.MAX_VEL_X
		self.maxVelY = c.MAX_VEL_Y
		self.gravity = c.GRAVITY
		self.accelX = c.ACCEL
		self.LoadFrames()
		self.SetUpAnimations()
		self.image = self.frames[self.anims['idle-right'][0]]
		self.rect = self.image.get_rect()
		self.facingRight = True
		self.allowJump = True
		self.state = c.IDLE
		self.frameIndex = 0
		self.switchIndex = 10
		self.switchCounter = 0
		self.relX = 0
		self.relY = 0

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
		self.anims['idle-right'] = [0]
		self.anims['idle-left'] = [1]
		self.anims['walk-right'] = cycle([3, 4])
		self.anims['walk-left'] = cycle([6, 7])

	def Update(self, keys, events):
		self.HandleState(keys, events)
		self.Animation()
	
	def HandleState(self, keys, events):
		if self.state == c.IDLE:
			self.Idle(keys)
		elif self.state == c.WALKING:
			self.Walking(keys)
		elif self.state == c.JUMP:
			self.Jumping(keys, events)
		elif self.state == c.DOUBLEJUMP:
			self.DoubleJump(keys)

	def Idle(self, keys):
		"""
		Called when the player is no longer walking, or called by default
		"""
		self.velX = 0
		self.velY += self.gravity
		if keys[keybinding['left']]:
			self.facingRight = False
			self.frameIndex = next(self.anims['walk-left'])
			self.state = c.WALKING
		elif keys[keybinding['right']]:
			self.facingRight = True
			self.frameIndex = next(self.anims['walk-right'])
			self.state = c.WALKING
		elif keys[keybinding['jump']] and self.allowJump:
			self.state = c.JUMP
			init.SFX['jump'].play()
			self.velY = c.JUMP_VEL
		else:
			self.state = c.IDLE

	def Walking(self, keys):
		self.velY += self.gravity

		if(self.switchCounter == self.switchIndex):
			if self.facingRight:
				self.frameIndex = next(self.anims['walk-right'])
				init.SFX['footstep'].play()
				self.switchCounter = 0
			else:
				self.frameIndex = next(self.anims['walk-left'])
				init.SFX['footstep'].play()
				self.switchCounter = 0
		else:
			self.switchCounter += 1
		if keys[keybinding['left']]:
			self.facingRight = False
			self.accelX = c.ACCEL
			if self.velX > (self.maxVelX * -1):
				self.velX -= self.accelX
			elif self.velX < (self.maxVelX * -1):
				self.velX += self.accelX
		elif keys[keybinding['right']]:
			self.facingRight = True
			self.accelX = c.ACCEL
			if self.velX < self.maxVelX:
				self.velX += self.accelX
			elif self.velX > self.maxVelX:
				self.velX -= self.accelX
		else:
			self.switchCounter = 0
			self.state = c.IDLE
			if self.facingRight:
				self.frameIndex = self.anims['idle-right'][0]
			else:
				self.frameIndex = self.anims['idle-left'][0]
		if keys[keybinding['jump']] and self.allowJump:
			self.state = c.JUMP
			init.SFX['jump'].play()
			self.velY = c.JUMP_VEL

	def Jumping(self, keys, events):
		self.allowJump = False
		self.gravity = c.JUMP_GRAVITY
		self.velY += self.gravity

		if(self.velY > 0 and self.velY < self.maxVelY):
			self.state = c.WALKING
			self.gravity = c.GRAVITY

		if keys[keybinding['left']] and self.state == c.JUMP:
			if self.velX > (self.maxVelX * -1):
				self.velX -= self.accelX
			elif self.velX < (self.maxVelX * -1):
				self.velX += self.accelX
		if keys[keybinding['right']] and self.state == c.JUMP:
			if self.velX < self.maxVelX:
				self.velX += self.accelX
			elif self.velX > self.maxVelX:
				self.velX -= self.accelX

		for event in events:
			if event.type == pg.KEYDOWN:
				if keys[keybinding['jump']]:
					self.state = c.DOUBLEJUMP
					self.velY = c.DOUBLE_JUMP_VEL
					init.SFX['doublejump'].play()
	
	def DoubleJump(self, keys):
		self.gravity = c.JUMP_GRAVITY
		self.velY += self.gravity

		if(self.velY > 0 and self.velY < self.maxVelY):
			self.state = c.WALKING
			self.gravity = c.GRAVITY

		if keys[keybinding['left']] and self.state == c.DOUBLEJUMP:
			if self.velX > (self.maxVelX * -1):
				self.velX -= self.accelX
			elif self.velX < (self.maxVelX * -1):
				self.velX += self.accelX
		if keys[keybinding['right']] and self.state == c.DOUBLEJUMP:
			if self.velX < self.maxVelX:
				self.velX += self.accelX
			elif self.velX > self.maxVelX:
				self.velX -= self.accelX

	def Animation(self):
		self.image = self.frames[self.frameIndex]