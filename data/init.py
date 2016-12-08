__author__ = "kiel.regusters"

"""
Initializes display and will create dictionaries of all content that will be used
"""
import os
import pygame as pg
import load
import debug

# Control where the window for the game is created
os.environ["SDL_VIDEO_CENTERED"] = "1"

# Initialize the pygame environment
pg.mixer.pre_init(44100, -16, 1, 4096)
pg.init()

# Control which kind of events we see in the event queue
#pg.event.set_allowed([pg.KEYDOWN, pg.KEYUP, pg.QUIT])

# Set the caption of the window
pg.display.set_caption("Aquaquest!")

# Set the dimensions of the window
SCREEN = pg.display.set_mode((800, 600))
SCREEN_RECTANGLE = SCREEN.get_rect()

# Load content

# Music
BGM = load.load_all_music(os.path.join("resources","music"))

# SFX
SFX = load.load_all_sfx(os.path.join("resources", "sfx"))

# Map Tilesets
TILESETS = load.load_all_gfx(os.path.join("resources", "tilesets"))
GRAPHICS = load.load_all_gfx(os.path.join("resources", "graphics"))

debug.debug("DONE: Loaded all content.")