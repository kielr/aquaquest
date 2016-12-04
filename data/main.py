__author__ = "kiel.regusters"
from . import init
from . import gamemanager
from . states import main_menu, load_screen, world
from . import constants as c

def main():
	""" Sets up screen states. """
	game = gamemanager.GameManager()
	stateDict = {c.MAIN_MENU: main_menu.Menu(),
				 c.LOAD_SCREEN: load_screen.LoadScreen(),
				 c.MAP: world.World()}

	game.SetupStates(stateDict, c.MAIN_MENU)
	game.main()

	