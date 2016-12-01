from . import init
from . import gamemanager
from . states import main_menu
__author__ = "kiel.regusters"
from . import constants as c
def main():
	""" Sets up screen states. """
	game = gamemanager.GameManager()
	stateDict = {c.MAIN_MENU: main_menu.Menu()}

	game.SetupStates(stateDict, c.MAIN_MENU)
	game.main()

	