__author__ = "kielregusters"

"""
Initializes display and will eventually create dictionaries of all content that will be used
"""
import os
import pygame as pg
from . import load
from . import debug

# Control where the window for the game is created
os.environ["SDL_VIDEO_CENTERED"] = "1"

# Initialize the pygame environment
pg.init()
pg.mixer.init(48000, -16, 1, 1024)

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