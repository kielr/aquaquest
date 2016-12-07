__author___ = "kiel.regusters"
import pygame as pg
from . import constants as c
from . import init, gamemanager
from itertools import cycle

keybinding = {
	'left':pg.K_a,
	'right':pg.K_d,
	'jump':pg.K_SPACE,
	'melee':pg.K_e
}

class Player(pg.sprite.Sprite):
	def __init__(self, info):
		pg.sprite.Sprite.__init__(self)
		self.spriteSheet = init.GRAPHICS['character']
		self.anims = {}
		self.facingRight = True
		self.allowJump = True
		self.allowJumpPrev = self.allowJump
		self.state = c.IDLE
		self.attackState = c.NOTATTACKING
		self.frameIndex = 0
		self.switchIndex = 10
		self.switchCounter = 0
		self.relX = 0
		self.relY = 0
		self.info = info
		self.LoadFrames()
		self.SetUpAnimations()
		self.SetUpForces()
		self.SetUpMelee()
		self.SetUpWeapon()
		self.SetUpStats(self.info)

	def SetUpForces(self):
		self.velX = 0
		self.velY = 0
		self.maxVelX = c.MAX_VEL_X
		self.maxVelY = c.MAX_VEL_Y
		self.gravity = c.GRAVITY
		self.accelX = c.ACCEL

	def SetUpMelee(self):
		self.allowAttack = True
		self.meleeActive = False
		self.meleeCounter = 0
		self.meleeTime = 10

	def SetUpStats(self, info):
		self.HP = info["HP"]
		self.LVL = info["LVL"]
		self.STR = info["STR"]
		self.INT = info["INT"]
		self.DEX = info["DEX"]
		self.XP = info["XP"]
		self.SP = info["SP"]
		self.skillPointState = c.LEVEL_AVAILABLE
		self.canLevelUp = True
		self.canSpendSkills = True
		self.canCast = True
		self.isDead = False
		self.damageInvuln = False
		self.damageInvulnFrames = 90
		self.damageInvulnTimer = 0

	def CheckForLevelUp(self):
		if self.XP >= 100 and self.canLevelUp == True:
			init.SFX['lvlup'].play()
			self.LVL += 1
			if self.LVL == c.LEVEL_CAP:
				self.canLevelUp = False
			self.SP += 1
			if self.LVL != c.LEVEL_CAP:
				self.XP = 0
		elif self.canLevelUp == False:
			self.XP = 100
		if self.SP > 0:
			self.canSpendSkills = True
		else:
			self.canSpendSkills = False

	def CheckForDeath(self):
		if(self.HP <= 0):
			self.isDead = True
			self.allowAttack = False
			self.allowJump = False
			self.canCast = False
			self.state = c.DEAD
		elif(self.HP >= 100):
			self.HP = 100

	def SetUpWeapon(self):
		self.weaponImage = init.GRAPHICS['weapon']
		self.weaponImage.set_colorkey((255, 0, 255))
		self.weaponRect = self.weaponImage.get_rect()
		self.weaponImage = pg.transform.scale(self.weaponImage,
							  (int(self.weaponRect.width * c.ZOOM * 2), int(self.weaponRect.height * c.ZOOM * 2)))
		self.weaponHbox = pg.Rect(0, 0, 24 * c.ZOOM, 2 * c.ZOOM)

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
		self.anims['death'] = [9]
		self.anims['invisible'] = [10]
		self.anims['walk-right'] = cycle([3, 4])
		self.anims['walk-left'] = cycle([6, 7])
		self.image = self.frames[self.anims['idle-right'][0]]
		self.rect = self.image.get_rect()
		
	def Update(self, keys, events):
		self.HandleState(keys, events)
		self.Animation()
		self.CheckForLevelUp()
		self.CheckForDeath()
		self.UpdateInfo()
		if self.damageInvuln:
			self.Invulnerable()

	def UpdateInfo(self):
		if self.HP < 0:
			self.HP = 0
		self.info["HP"] = self.HP
		self.info["LVL"] = self.LVL
		self.info["STR"] = self.STR
		self.info["INT"] = self.INT
		self.info["DEX"] = self.DEX
		self.info["XP"] = self.XP
		self.info["SP"] = self.SP

	def TakeDamage(self, damage):
		if self.damageInvuln == False:
			init.SFX['hurt'].play()
			self.damageInvuln = True
			self.HP -= damage


	def Invulnerable(self):
		if self.damageInvulnTimer == self.damageInvulnFrames:
			self.damageInvuln = False
			self.damageInvulnTimer = False
		else:
			self.damageInvulnTimer += 1
	def HandleState(self, keys, events):
		if self.state == c.IDLE:
			self.Idle(keys,events)
		elif self.state == c.WALKING:
			self.Walking(keys, events)
		elif self.state == c.JUMP:
			self.Jumping(keys, events)
		elif self.state == c.DOUBLEJUMP:
			self.DoubleJump(keys, events)
		elif self.state == c.DEAD:
			self.Death()
		if self.attackState == c.ATTACKING:
			self.Attacking()
		if self.canSpendSkills:
			self.HandleSkillUp(keys, events)

	def HandleSkillUp(self, keys, events):
		for event in events:
			if event.type == pg.KEYDOWN and self.canSpendSkills:
				if keys[pg.K_1]:
					if self.STR < 9:
						init.SFX['skillup'].play()
						self.STR += 1
						self.SP -= 1
					else:
						init.SFX['fail'].play()
				elif keys[pg.K_2]:
					if self.DEX < 9:
						init.SFX['skillup'].play()
						self.DEX += 1
						self.SP -= 1
					else:
						init.SFX['fail'].play()
				elif keys[pg.K_3]:
					if self.INT < 9:
						init.SFX['skillup'].play()
						self.INT += 1
						self.SP -= 1
					else:
						init.SFX['fail'].play()

	def Death(self):
		self.velY += self.gravity
		self.velX = 0
		self.frameIndex = self.anims['death'][0]

	def Idle(self, keys, events):
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
		else:
			self.state = c.IDLE

		for event in events:
			if event.type == pg.KEYDOWN and self.allowJump:
				if keys[keybinding['jump']]:
					self.state = c.JUMP
					self.velY = c.JUMP_VEL
					init.SFX['jump'].play()
			if event.type == pg.KEYDOWN and self.allowAttack:
				if keys[keybinding['melee']]:
					self.attackState = c.ATTACKING
					init.SFX['attack'].play()

	def Walking(self, keys, events):
		self.velY += self.gravity

		if(self.switchCounter == self.switchIndex):
			if self.facingRight:
				if self.allowJump:
					self.frameIndex = next(self.anims['walk-right'])
					init.SFX['footstep'].play()
				self.switchCounter = 0
			else:
				if self.allowJump:
					self.frameIndex = next(self.anims['walk-left'])
					init.SFX['footstep'].play()
				self.switchCounter = 0
		else:
			self.switchCounter += 1
		if keys[keybinding['left']]:
			self.facingRight = False
			self.accelX = c.ACCEL + (self.DEX / 2)
			if self.velX > (-self.maxVelX - self.DEX / 2):
				self.velX -= self.accelX
			elif self.velX <= (-self.maxVelX - self.DEX / 2):
				self.velX = -self.maxVelX - self.DEX / 2
		elif keys[keybinding['right']]:
			self.facingRight = True
			self.accelX = c.ACCEL + (self.DEX / 2)
			if self.velX < self.maxVelX + self.DEX / 2:
				self.velX += self.accelX
			elif self.velX > self.maxVelX + self.DEX / 2:
				self.velX = self.maxVelX + self.DEX / 2
		else:
			self.switchCounter = 0
			self.state = c.IDLE
			if self.facingRight:
				self.frameIndex = self.anims['idle-right'][0]
			else:
				self.frameIndex = self.anims['idle-left'][0]
		for event in events:
			if event.type == pg.KEYDOWN and self.allowJump:
				if keys[keybinding['jump']]:
					self.state = c.JUMP
					self.velY = c.JUMP_VEL
					init.SFX['jump'].play()
			if event.type == pg.KEYDOWN and self.allowAttack:
				if keys[keybinding['melee']]:
					self.attackState = c.ATTACKING
					init.SFX['attack'].play()

	def Jumping(self, keys, events):
		self.allowJump = False
		self.gravity = c.JUMP_GRAVITY
		self.velY += self.gravity
		self.velY += -0.2

		if(self.velY > 1 and self.velY < self.maxVelY):
			self.state = c.WALKING
			self.gravity = c.GRAVITY

		if keys[keybinding['left']] and self.state == c.JUMP:
			if self.velX > (self.maxVelX * -1 - self.DEX / 2):
				self.velX -= self.accelX + self.DEX / 2
			elif self.velX < (self.maxVelX * -1 - self.DEX / 2):
				self.velX = self.maxVelX * -1 - self.DEX / 2
		if keys[keybinding['right']] and self.state == c.JUMP:
			if self.velX < self.maxVelX + self.DEX / 2 :
				self.velX += self.accelX + self.DEX / 2 
			elif self.velX > self.maxVelX + self.DEX / 2 :
				self.velX = self.maxVelX + self.DEX / 2  

		for event in events:
			if event.type == pg.KEYDOWN:
				if keys[keybinding['jump']]:
					self.state = c.DOUBLEJUMP
					self.velY = c.DOUBLE_JUMP_VEL
					init.SFX['doublejump'].play()
			if event.type == pg.KEYDOWN and self.allowAttack:
				if keys[keybinding['melee']]:
					self.attackState = c.ATTACKING
					init.SFX['attack'].play()
	
	def DoubleJump(self, keys, events):
		self.gravity = c.JUMP_GRAVITY
		self.velY += self.gravity
		self.velY += -0.2
		if(self.velY > 0 and self.velY < self.maxVelY):
			self.state = c.WALKING
			self.gravity = c.GRAVITY

		if keys[keybinding['left']] and self.state == c.DOUBLEJUMP:
			if self.velX > (self.maxVelX * -1 - self.DEX / 2):
				self.velX -= self.accelX + self.DEX / 2
			elif self.velX < (self.maxVelX * -1 - self.DEX / 2):
				self.velX = self.maxVelX * -1 - self.DEX / 2
		if keys[keybinding['right']] and self.state == c.DOUBLEJUMP:
			if self.velX < self.maxVelX + self.DEX / 2 :
				self.velX += self.accelX + self.DEX / 2 
			elif self.velX > self.maxVelX + self.DEX / 2 :
				self.velX = self.maxVelX + self.DEX / 2

		for event in events:
			if event.type == pg.KEYDOWN and self.allowAttack:
				if keys[keybinding['melee']]:
					self.attackState = c.ATTACKING
					init.SFX['attack'].play()

	def Attacking(self):
		self.meleeActive = True
		self.allowAttack = False
		if self.meleeCounter == self.meleeTime:
			self.meleeActive = False
			self.allowAttack = True
			self.attackState = c.NOTATTACKING
			self.meleeCounter = 0
		else:
			self.meleeCounter += 1


	def Animation(self):
		if self.damageInvuln == False or self.isDead:
			self.image = self.frames[self.frameIndex]
		else:
			if self.damageInvulnTimer % 4 == 0:
				self.image = self.frames[self.frameIndex]
			else:
				self.image = self.frames[self.anims["invisible"][0]]