"""
The module of the main game manager of the project. Contains the GameManager class that keeps track of the current state of the game.
"""

__author__ = "kiel.regusters"
from . import debug
from . import init
from . states import world
from . import debug
from . import constants as c
import pygame as pg

class GameManager(object):
	""" This class is the main control class for the entire project. It handles the main game loop,
		the event loop, and logic for switching states (main menu, levels, etc) """
	def __init__(self):
		self.screen = pg.display.get_surface()
		self.done = False
		self.showFPS = True
		self.clock = pg.time.Clock()
		self.caption = "Aquaquest! "
		self.fps = 60
		self.keys = pg.key.get_pressed()
		self.stateDict = {}
		self.currentTime = 0.0
		self.stateName = None
		self.state = None

	def HandleEvents(self, events):
		""" Listens for certain events like quit """
		for event in events:
			if event.type == pg.QUIT:
				self.done = True
			elif event.type == pg.KEYDOWN:
				self.keys = pg.key.get_pressed()
				self.HandleWindowOptions()
			elif event.type == pg.KEYUP:
				self.keys = pg.key.get_pressed()

	def HandleWindowOptions(self):
		""" Handles turning window options on or off """
		if self.keys[pg.K_F5] == 1:
			self.showFPS = not self.showFPS
			if not self.showFPS:
				pg.display.set_caption("Aquaquest! ")

	
	def SetupStates(self, stateDict, startState):
		"""
		Sets up the state dictionary for the game.
		"""
		self.stateDict = stateDict
		self.stateName = startState
		self.state = self.stateDict[self.stateName]

	def Update(self, events):
		""" Runs the update loops of the various states of the game. """
		self.currentTime = pg.time.get_ticks()
		if self.state.quit:
			self.done = True
			return
		elif self.state.done:
			self.FlipState()
		self.state.Update(self.screen, self.keys, self.currentTime, events)

	def FlipState(self):
		""" When a state finishes, this method is called to transition the game to the next state, whatever it may be."""
		# Keep the current state and the next state in memory 
		previous, self.stateName = self.stateName, self.state.next
		# Clean up the state
		self.state.Clean()
		if self.stateName == "loadmap":
			# If we get here then we need to load the character save.
			#try:
			f = open("save", "r")
			content = f.readlines()
			game_info = {}
			for data in content:
				e = data.split()
				try:
					game_info[e[0]] = int(e[1])
				except:
					game_info[e[0]] = e[1]
			f.close()
			loadedWorld = world.World()
			self.state = loadedWorld
			self.state.Continue(self.currentTime, game_info)

			#except:
			#	debug.debug("Error loading save, perhaps there isn't one?")
			#	self.state = self.stateDict[c.MAIN_MENU]
		else:
			self.state = self.stateDict[self.stateName]
			self.state.StartUp(self.currentTime)
		self.previous = previous
		

	# Blit the title
	def main(self):
		""" Main loop for the entire program """
		while not self.done:
			self.screen.fill((0,0,0))
			events = pg.event.get()
			self.HandleEvents(events)
			self.Update(events)


			pg.display.update()
			self.clock.tick(self.fps) # Limit the fps to 60 for now
			if self.showFPS:
				fps = self.clock.get_fps()
				pg.display.set_caption(self.caption + "- {:.2f} FPS".format(fps))