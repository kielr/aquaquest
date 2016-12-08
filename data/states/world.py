"""
This module contains the World state class and is where most of the game will be taking place
"""

__author__ = "kiel.regusters"

import sys
sys.path.append("..")
import pygame as pg
import state
from libs import pytmx
from libs import util_pygame
import soundmanager
import utility
import constants as c
import debug
import init
import camera
import player, fireball, checkpoint, level_transition_trigger
import enemy

class World(state.State):
	""" 
	This class holds the TMX map and handles collision between entities inside the map.
	It will also probably handle things like checkpoint and file IO for saving. It also
	has conversation with the player sprite class and all other entities inside of it.

	>>> World()
	<__main__.World object at ...>
	"""
	def __init__(self):
		state.State.__init__(self)
		self.checkpointDict = {}
		self.playerCheckDict = {}
		self.playerIsDead = False
		self.waitCount = 0
		self.waitTime = 120

	def StartUp(self, currentTime):
		"""
		Called for a new game, loads the map, and sets up all the enemy, checkpoint, and trigger groups
		"""
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
		"""
		Called when the current object is transitioning to a new level. Similar to start up, but we don't need to
		spawn the player, just move him.
		"""
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
		Gamemanager loads game_info for us and from that we can determine where to put the player and what
		stats to give him.
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
		self.noGameover = True
		try:
			self.gameoverObject = self.tiledMap.get_object_by_name("gameover")
			self.noGameover = False
		except:
			debug.debug("No gameover object found.")
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
		"""
		Sets up the level collidables so the player doesn't fall through.
		"""
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
		"""
		If the player reached the end of a level, we need to move him to the player spawn of the next.
		This is what the method does.
		"""
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
		"""
		This method is called if the player is starting a new game. Thus we create a newGameInfo dict and pass into a new player class.
		"""
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
		"""
		This method is called if the player selected the Continue option from the Main menu state class. game_info is loaded
		in the game manager and given to the world so that we can pull important persistant information that was saved to the file.
		"""
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
		"""
		Originally meant to handle multiple states of the game but there ended up being only one because pause was never
		implemented.
		"""
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
		"""
		This is where most of the magic of the game will happen.

		Handles the map collision for every entity, including weapon and magic collision.
		"""
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

		# Gameover
		if self.noGameover == False:
			self.CheckGameover()

	def CheckGameover(self):
		"""
		Checks to see if the player collided with the gameover object.
		"""
		if self.player.rect.colliderect([self.gameoverObject.x*c.ZOOM - self.camera.x, self.gameoverObject.y*c.ZOOM - self.camera.y,
								   self.gameoverObject.width*c.ZOOM, self.gameoverObject.height*c.ZOOM]):
			self.done = True
			self.next = c.GAMEOVER

	def MoveEnemiesX(self):
		"""
		Move all enemies on the x axis.
		"""
		for enemy in self.enemyGroup.sprites():
			enemy.relX += enemy.velX
			enemy.rect.x = enemy.relX - self.camera.x

	def MoveEnemiesY(self):
		"""
		Move all enemies on the y axis.
		"""
		for enemy in self.enemyGroup.sprites():
			enemy.relY += enemy.velY
			enemy.rect.y = enemy.relY - self.camera.y

	def MoveCheckpoint(self):
		"""
		Adjust the checkpoints based off the camera position.
		"""
		for checkpoint in self.checkpointGroup.sprites():
			checkpoint.Update()
			checkpoint.rect.x = checkpoint.relX - self.camera.x
			checkpoint.rect.y = checkpoint.relY - self.camera.y

	def MoveTriggers(self):
		"""
		Adjust the triggers based off the camera position.
		"""
		for trigger in self.levelTriggerGroup.sprites():
			trigger.rect.x = trigger.relX - self.camera.x
			trigger.rect.y = trigger.relY - self.camera.y

	def MoveFireball(self):
		"""
		Adjust the player spells based off the camera position.
		"""
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
		"""
		Listen for the player object telling us that the player is dead. If the player is dead
		then we will wait for a little bit and send the user back to the main menu.
		"""
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
		"""
		Check to see if the player is colliding with a trigger.
		"""
		trigger = pg.sprite.spritecollideany(self.player, self.levelTriggerGroup)

		if trigger:
			self.Transition(trigger.name)

	def CheckPlayerCheckpointCollisions(self):
		"""
		Check to see if the player has collided with a checkpoint, if they do, open a file for writing and save the
		persistant game info to the file.
		"""
		checkpointSprite = pg.sprite.spritecollideany(self.player, self.checkpointGroup)

		if checkpointSprite:
			if checkpointSprite.got == False and self.player.isDead == False:
				checkpointSprite.got = True
				init.SFX['checkpointget'].play()
				self.player.info['checkpoint'] = self.playerCheckDict[checkpointSprite]
				f = open("save", "w")
				for key in self.player.info.keys():
					f.write("{} {}\n".format(key, self.player.info[key]))
				f.close()

	def CheckPlayerXLevelCollisions(self):
		"""
		Check player to level collisions on the X-axis
		"""
		tile = pg.sprite.spritecollideany(self.player, self.levelGroup)

		if tile:
			self.ResolveXLevelCollisions(self.player, tile)

	def CheckPlayerYLevelCollisions(self):
		"""
		Check player to level collisions on the Y-axis
		"""
		tile = pg.sprite.spritecollideany(self.player, self.levelGroup)

		if tile:
			self.ResolveYLevelCollisions(self.player, tile)
			self.player.allowJump = True

	def CheckEnemyYLevelCollisions(self):
		"""
		Check enemy to level collisions on the Y-axis
		"""
		for enemies in self.enemyGroup.sprites():
			tile = pg.sprite.spritecollideany(enemies, self.levelGroup)

			if tile:
				self.ResolveYLevelCollisions(enemies, tile)

	def CheckEnemySwordCollisions(self):
		"""
		Check enemy to sword collisions. If there is a collision AND the player is in the attacking state
		then we need to decrement the enemy's health and check to see if they died. If they died, give the player
		experience.
		"""
		if self.player.attackState == c.ATTACKING:
			for enemies in self.enemyGroup.sprites():
				if enemies.rect.colliderect(self.player.weaponHbox) and enemies.isDead == False:
					enemies.TakeDamage(50 + self.player.STR * 10)
					enemies.CheckForDeath()
					if enemies.isDead:
						self.player.XP += 25

	def CheckEnemyFireballCollisions(self):
		"""
		Check enemy to fireball collisions. After that, the same process for checking damage and death as
		the enemy to sword collisions.
		"""
		for enemies in self.enemyGroup.sprites():
			fireball = pg.sprite.spritecollideany(enemies, self.fireballGroup)

			if fireball and enemies.isDead == False:
				enemies.TakeDamage(15 + self.player.INT * 2)
				enemies.CheckForDeath()
				if enemies.isDead:
					self.player.XP += 25
	
	def CheckEnemyPlayerCollision(self):
		"""
		Check to see if the enemy collided with the player, if they did, deal damage to the player.
		"""
		zombie = pg.sprite.spritecollideany(self.player, self.enemyGroup)
		if zombie and zombie.isDead == False:
			self.player.TakeDamage(25)

	def ResolveXLevelCollisions(self, entity, collider):
		"""
		@param entity: offending entity
		@param collider: the tile that the entity collided with.

		Resolve all collisions with the level between the tile and the entity provided on the x-axis.
		"""
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
		"""
		@param entity: offending entity
		@param collider: the tile that the entity collided with.

		Resolve all collisions with the level between the tile and the entity provided on the y-axis.
		"""
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
		"""
	    Move the player on the x-axis.
		"""
		self.player.relX += self.player.velX
		self.player.rect.x = self.player.relX - self.camera.x
		if self.player.facingRight:
			self.player.weaponHbox.x = self.player.rect.x + 50
		else:
			self.player.weaponHbox.x = self.player.rect.x - 71
	
	def MovePlayerY(self):
		"""
	    Move the player on the y-axis.
		"""
		self.player.relY += self.player.velY
		self.player.rect.y = self.player.relY - self.camera.y
		self.player.weaponHbox.y = self.player.rect.y + 22
	
	def UpdateCameraX(self):
		"""
		Move the camera on the x-axis
		"""

		third = self.camera.viewport.x + self.camera.viewport.w//3
		third2 = third * 2

		if self.player.velX < 0 and self.player.rect.centerx <= third:
			self.camera.Move(self.player.velX, 0)
		elif self.player.velX > 0 and self.player.rect.centerx >= third2:
			self.camera.Move(self.player.velX, 0)

	def UpdateCameraY(self):
		"""
		Move the camera on the y-axis.
		"""
		# Look at the player
		self.camera.LookAtY(self.player.relY + 75)

	def DrawLevel(self):
		"""
		Draw the level to a pygame surface once, and use that to draw the main surface of the game. If we draw again every frame
		then it will be very expensive and taxing on the computer.
		"""
		self.levelSurface.fill(c.BLACK)
		for layer in self.tiledMap.layers:
			if "Object" not in str(type(layer)):
				for x,y,image in layer.tiles():
					rect = image.get_rect()
					self.levelSurface.blit(pg.transform.scale(image, (int(rect.width*3), 
												(int(rect.width*3)))), 
												[c.TILE_SIZE * c.ZOOM * x, c.TILE_SIZE * c.ZOOM * y])

	def DrawEverything(self, surface):
		"""
		This method is called every frame and draws all things that need to be seen by the player.
		It also contains a debug drawing if the DEBUG_DRAW flag is true
		"""
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