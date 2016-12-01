from . import debug as info
from . import init
from . import spritesheet
from . import state
import pygame as pg
import pytmx
from util_pygame import load_pygame

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
		pass

	## How to blit the map:
	#for layer in test.layers:
	#	for x,y,image in layer.tiles():
	#		self.screen.blit(image, [16 * x, 16 * y])

	# Blit the title
	def main(self):
		""" Main loop for the entire program """
		while not self.done:
			self.screen.fill((0,0,0))
			events = pg.event.get()
			self.HandleEvents(events)
			self.Update(events)
			test = load_pygame("resources/maps/test.tmx")


			pg.display.update()
			self.clock.tick(self.fps) # Limit the fps to 60 for now
			if self.showFPS:
				fps = self.clock.get_fps()
				pg.display.set_caption(self.caption + "- {:.2f} FPS".format(fps))