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
from .. import player, fireball, checkpoint, level_transition_trigger
from .. import enemy

class World(state.State):
	""" 
	This class holds the TMX map and handles collision between entities inside the map.
	It will also probably handle things like checkpoint and file IO for saving.
	"""
	def __init__(self):
		state.State.__init__(self)
		self.checkpointDict = {}
		self.playerCheckDict = {}
		self.playerIsDead = False
		self.waitCount = 0
		self.waitTime = 120

	def StartUp(self, currentTime):
		# The player got here from PLAY, so it's the first level.
		self.currentTime = currentTime
		debug.debug("Getting TMX file...")
		self.tiledMap = util_pygame.load_pygame("resources/maps/level1.tmx")
		self.levelstate = "level1"
		self.levelSurface = pg.Surface((int(c.TILE_SIZE * self.tiledMap.width * c.ZOOM), 
								  int(c.TILE_SIZE * self.tiledMap.height * c.ZOOM))).convert()
		self.levelRect = self.levelSurface.get_rect()
		debug.debug("Done")
		debug.debug("Spawning Player")
		self.overhead = utility.Overhead(c.LEVEL1)
		self.soundManager = soundmanager.Sound(self.overhead)
		self.camera = camera.Camera()
		self.state = c.UNPAUSE
		self.SpawnPlayer()
		self.playerGroup = pg.sprite.Group(self.player)
		self.SetUpSpriteGroups()
		#Draw to Level surface
		self.DrawLevel()

	def Transition(self, level):
		debug.debug("Transition level to {}".format(level))
		debug.debug("Getting TMX file...")
		self.tiledMap = util_pygame.load_pygame("resources/maps/" + level + ".tmx")
		self.levelstate = level
		self.levelSurface = pg.Surface((int(c.TILE_SIZE * self.tiledMap.width * c.ZOOM), 
								  int(c.TILE_SIZE * self.tiledMap.height * c.ZOOM))).convert()
		self.levelRect = self.levelSurface.get_rect()
		self.overhead = utility.Overhead(level)
		self.overhead.info = self.player.info
		self.soundManager = soundmanager.Sound(self.overhead)
		self.TransitionPlayer(level)
		self.SetUpSpriteGroups()
		self.DrawLevel()

	def Continue(self, currentTime, game_info):
		"""
		Method that is called whenever the user is continuing from checkpoint
		"""
		debug.debug("Getting TMX file...")
		self.tiledMap = util_pygame.load_pygame("resources/maps/" + game_info["level"] + ".tmx")
		self.levelSurface = pg.Surface((int(c.TILE_SIZE * self.tiledMap.width * c.ZOOM), 
								  int(c.TILE_SIZE * self.tiledMap.height * c.ZOOM))).convert()
		self.levelRect = self.levelSurface.get_rect()
		debug.debug("Done")
		debug.debug("Spawning Player")
		self.overhead = utility.Overhead(game_info['level'])
		self.soundManager = soundmanager.Sound(self.overhead)
		self.camera = camera.Camera()
		self.state = c.UNPAUSE
		self.levelstate = game_info["level"]
		self.SetUpSpriteGroups()
		self.SpawnPlayerContinue(self.checkpointDict[game_info['checkpoint']].x, self.checkpointDict[game_info['checkpoint']].y, game_info)
		self.playerGroup = pg.sprite.Group(self.player)
		#Draw to Level surface
		self.DrawLevel()

	def SetUpSpriteGroups(self):
		"""
		This method sets up all the sprite groups that will be used by the world.
		"""
		self.fireballGroup = pg.sprite.Group()
		self.checkpointGroup = pg.sprite.Group()
		self.levelTriggerGroup = pg.sprite.Group()
		self.enemyGroup = pg.sprite.Group()
		i = 1

		for checkpointObject in self.tiledMap.get_layer_by_name("checkpoints"):
			newCheckpoint = checkpoint.Checkpoint(checkpointObject.x * c.ZOOM, checkpointObject.y * c.ZOOM)
			self.checkpointGroup.add(newCheckpoint)
			self.checkpointDict[i] = checkpointObject
			self.playerCheckDict[newCheckpoint] = i
			i += 1

		for triggerObject in self.tiledMap.get_layer_by_name("trigger"):
			newTrigger = level_transition_trigger.Trigger(triggerObject.x * c.ZOOM, triggerObject.y * c.ZOOM)
			newTrigger.name = triggerObject.name
			self.levelTriggerGroup.add(newTrigger)

		for enemies in self.tiledMap.get_layer_by_name("enemy"):
			if "zombie" in enemies.name:
				newEnemy = enemy.Zombie(enemies.name)
				newEnemy.relX = enemies.x * c.ZOOM
				newEnemy.relY = enemies.y * c.ZOOM
				self.enemyGroup.add(newEnemy)
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

	def TransitionPlayer(self, level):
		playerSpawnObject = self.tiledMap.get_object_by_name("playerSpawn")
		self.playerX = playerSpawnObject.x
		self.playerY = playerSpawnObject.y
		self.camera.LookAt((self.playerX*c.ZOOM, self.playerY*c.ZOOM))
		self.player.rect.x = self.playerX * c.ZOOM - self.camera.x
		self.player.rect.y = self.playerY * c.ZOOM - self.camera.y
		self.player.relX = self.playerX * c.ZOOM
		self.player.relY = self.playerY * c.ZOOM
		self.player.info['level'] = "level2"

	def SpawnPlayer(self):
		# Find where player should spawn
		playerSpawnObject = self.tiledMap.get_object_by_name("playerSpawn")
		self.playerX = playerSpawnObject.x
		self.playerY = playerSpawnObject.y
		newGameInfo = { "HP": 100, 
				"LVL": 1,
				"STR": 0,
				"DEX": 0,
				"INT": 0,
				"XP": 0,
			    "SP": 1,
				"level": "level1", 
				"checkpoint": None }
		self.player = player.Player(newGameInfo)
		self.player.rect.x = self.playerX * c.ZOOM - self.camera.x
		self.player.rect.y = self.playerY * c.ZOOM - self.camera.y
		self.player.relX = self.playerX * c.ZOOM
		self.player.relY = self.playerY * c.ZOOM

	def SpawnPlayerContinue(self, x, y, game_info):
		self.playerX = x
		self.playerY = y
		self.camera.LookAt((self.playerX*c.ZOOM, self.playerY*c.ZOOM))
		self.player = player.Player(game_info)
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
		# Cheats for dev and grader
		for event in events:
			if event.type == pg.QUIT:
				debug.debug("Player quitting...")
				self.done = True
				self.quit = True
			if event.type == pg.KEYDOWN:
				if keys[pg.K_ESCAPE]:
					self.done = True
					self.next = c.MAIN_MENU
				if keys[pg.K_q] and self.player.canCast:
					init.SFX['fireball'].play()
					newFireball = fireball.Fireball(self.player.relX, self.player.relY, self.player.facingRight)
					self.fireballGroup.add(newFireball)
				if keys[pg.K_F2]:
					self.player.TakeDamage(50)
				if keys[pg.K_F3]:
					self.player.HP += 50
		if keys[pg.K_F4]:
			self.player.XP += 10

		if self.state == c.UNPAUSE:
			self.UpdateAllSprites(keys, events)

	def UpdateAllSprites(self, keys, events):

		# Update Player
		self.CheckPlayerDeath()
		self.player.Update(keys, events)
		self.MovePlayerX()
		self.CheckPlayerXLevelCollisions()
		self.MovePlayerY()
		self.CheckPlayerYLevelCollisions()
		self.CheckEnemyYLevelCollisions()

		self.CheckEnemyPlayerCollision()

		self.overhead.Update(self.player.info)
		
		# Update Enemies
		for enemies in self.enemyGroup.sprites():
			enemies.Update()

		self.MoveEnemiesX()
		self.MoveEnemiesY()

		# Update Camera
		self.UpdateCameraX()
		self.UpdateCameraY()


		# Enemies
		self.CheckEnemySwordCollisions()
		self.CheckEnemyFireballCollisions()


		# Fireball
		self.MoveFireball()

		# Checkpoints
		self.CheckPlayerCheckpointCollisions()
		self.MoveCheckpoint()

		# Triggers
		self.CheckTriggerCollision()
		self.MoveTriggers()

	def MoveEnemiesX(self):
		for enemy in self.enemyGroup.sprites():
			enemy.relX += enemy.velX
			enemy.rect.x = enemy.relX - self.camera.x

	def MoveEnemiesY(self):
		for enemy in self.enemyGroup.sprites():
			enemy.relY += enemy.velY
			enemy.rect.y = enemy.relY - self.camera.y

	def MoveCheckpoint(self):
		for checkpoint in self.checkpointGroup.sprites():
			checkpoint.Update()
			checkpoint.rect.x = checkpoint.relX - self.camera.x
			checkpoint.rect.y = checkpoint.relY - self.camera.y

	def MoveTriggers(self):
		for trigger in self.levelTriggerGroup.sprites():
			trigger.rect.x = trigger.relX - self.camera.x
			trigger.rect.y = trigger.relY - self.camera.y

	def MoveFireball(self):
		for fireball in self.fireballGroup.sprites():
			fireball.Lifetime()
			if fireball.life <= (0 - self.player.INT * 1.5):
				self.fireballGroup.remove(fireball)
				continue
			if fireball.facingRight:
				fireball.velX += fireball.accelX + self.player.INT / 10
				fireball.relX += fireball.velX
			else:
				fireball.velX -= fireball.accelX + self.player.INT / 10
				fireball.relX += fireball.velX
			fireball.rect.x = fireball.relX - self.camera.x
			fireball.rect.y = fireball.relY - self.camera.y
			fireball.hurtbox[0] = fireball.rect.x
			fireball.hurtbox[1] = fireball.rect.y
	
	def CheckPlayerDeath(self):
		if self.player.isDead and self.playerIsDead == False:
			debug.debug("Player death.")
			self.playerIsDead = True
			init.SFX["death"].play()
			self.soundManager.StopBGM()
		elif self.playerIsDead:
			if self.waitCount == self.waitTime:
				self.waitCount = 0
				self.playerIsDead = False
				self.done = True
				self.next = c.MAIN_MENU
			self.waitCount += 1

	def CheckTriggerCollision(self):
		trigger = pg.sprite.spritecollideany(self.player, self.levelTriggerGroup)

		if trigger:
			self.Transition(trigger.name)

	def CheckPlayerCheckpointCollisions(self):
		checkpointSprite = pg.sprite.spritecollideany(self.player, self.checkpointGroup)

		if checkpointSprite:
			if checkpointSprite.got == False and self.player.isDead == False:
				checkpointSprite.got = True
				init.SFX['checkpointget'].play()
				self.player.info['checkpoint'] = self.playerCheckDict[checkpointSprite]
				f = open("save", "w")
				for key in self.player.info.keys():
					f.write("{} {}\n".format(key, self.player.info[key]))

	def CheckPlayerXLevelCollisions(self):
		tile = pg.sprite.spritecollideany(self.player, self.levelGroup)

		if tile:
			self.ResolveXLevelCollisions(self.player, tile)

	def CheckPlayerYLevelCollisions(self):
		tile = pg.sprite.spritecollideany(self.player, self.levelGroup)

		if tile:
			self.ResolveYLevelCollisions(self.player, tile)
			self.player.allowJump = True

	def CheckEnemyYLevelCollisions(self):
		for enemies in self.enemyGroup.sprites():
			tile = pg.sprite.spritecollideany(enemies, self.levelGroup)

			if tile:
				self.ResolveYLevelCollisions(enemies, tile)

	def CheckEnemySwordCollisions(self):
		if self.player.attackState == c.ATTACKING:
			for enemies in self.enemyGroup.sprites():
				if enemies.rect.colliderect(self.player.weaponHbox) and enemies.isDead == False:
					enemies.TakeDamage(50 + self.player.STR * 10)
					enemies.CheckForDeath()
					if enemies.isDead:
						self.player.XP += 25

	def CheckEnemyFireballCollisions(self):
		for enemies in self.enemyGroup.sprites():
			fireball = pg.sprite.spritecollideany(enemies, self.fireballGroup)

			if fireball and enemies.isDead == False:
				enemies.TakeDamage(15 + self.player.INT * 2)
				enemies.CheckForDeath()
				if enemies.isDead:
					self.player.XP += 25
	
	def CheckEnemyPlayerCollision(self):
		zombie = pg.sprite.spritecollideany(self.player, self.enemyGroup)
		if zombie and zombie.isDead == False:
			self.player.TakeDamage(25)

	def ResolveXLevelCollisions(self, entity, collider):
		if entity.velX > 0: # Going right
			intersectDepth = collider.rect.left - self.player.rect.right
			if intersectDepth < (-16*3):
				return

			# Correct the position
			entity.relX += intersectDepth
			entity.rect.x = entity.relX - self.camera.x

		elif entity.velX < 0: # Going left
			intersectDepth = collider.rect.right - self.player.rect.left
			if intersectDepth > 16*3:
				return

			# Correct the position
			entity.relX += intersectDepth
			entity.rect.x = entity.relX - self.camera.x

	def ResolveYLevelCollisions(self, entity, collider):
		if entity.velY > 0: # Going Down
			intersectDepth = collider.rect.top - entity.rect.bottom
			if intersectDepth < (-16*3):
				return

			# Correct the position
			entity.relY += intersectDepth
			entity.rect.y = entity.relY - self.camera.y
			entity.velY = 0

		elif self.player.velY < 0: # Going Up
			intersectDepth = collider.rect.bottom - entity.rect.top
			if intersectDepth > 16*3:
				return

			# Correct the position
			entity.relY += intersectDepth
			entity.rect.y = entity.relY - self.camera.y
			entity.velY = 0

	def MovePlayerX(self):
		self.player.relX += self.player.velX
		self.player.rect.x = self.player.relX - self.camera.x
		if self.player.facingRight:
			self.player.weaponHbox.x = self.player.rect.x + 50
		else:
			self.player.weaponHbox.x = self.player.rect.x - 71
	
	def MovePlayerY(self):
		self.player.relY += self.player.velY
		self.player.rect.y = self.player.relY - self.camera.y
		self.player.weaponHbox.y = self.player.rect.y + 22
	
	def UpdateCameraX(self):
		# Look at the player
		#self.camera.LookAtX(self.player.relx)

		third = self.camera.viewport.x + self.camera.viewport.w//3
		third2 = third * 2

		if self.player.velX < 0 and self.player.rect.centerx <= third:
			self.camera.Move(self.player.velX, 0)
		elif self.player.velX > 0 and self.player.rect.centerx >= third2:
			self.camera.Move(self.player.velX, 0)

	def UpdateCameraY(self):
		# Look at the player
		self.camera.LookAtY(self.player.relY + 75)

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
		# Draw Enemies
		self.enemyGroup.draw(surface)

		# Draw player
		self.playerGroup.draw(surface)

		# Draw fireball
		self.fireballGroup.draw(surface)
		
		# Draw Checkpoints
		self.checkpointGroup.draw(surface)
		
		# Draw weapon if active
		if self.player.meleeActive:
			if self.player.facingRight:
				surface.blit(self.player.weaponImage, [self.player.rect.x + 45, self.player.rect.y - 25, self.player.rect.w, self.player.rect.h])
			else:
				surface.blit(pg.transform.flip(self.player.weaponImage, True, False), 
				 [self.player.rect.x - 95, self.player.rect.y - 25, self.player.rect.w, self.player.rect.h])

		


		# Draw overhead info
		self.overhead.draw(surface)
		if debug.DEBUG_DRAW:
			pg.draw.rect(surface, (255, 0, 0), self.player.rect)
			for sprites in self.levelGroup.sprites():
				pg.draw.rect(surface, (255,0,0), sprites.rect)

			for fireball in self.fireballGroup.sprites():
				pg.draw.rect(surface, (0,0,255), fireball.rect)

			for checkpoint in self.checkpointGroup.sprites():
				pg.draw.rect(surface, (0,255,0), checkpoint.rect)

			for trigger in self.levelTriggerGroup.sprites():
				pg.draw.rect(surface, (0, 255, 255), trigger.rect)

			for enemy in self.enemyGroup.sprites():
				pg.draw.rect(surface, (200, 20, 20), enemy.rect)
			
			if self.player.attackState == c.ATTACKING:
				if self.player.facingRight:
					pg.draw.rect(surface, (255,0,0), self.player.weaponHbox)
				else:
					pg.draw.rect(surface, (255,0,0), self.player.weaponHbox)