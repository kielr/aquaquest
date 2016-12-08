__author__ = "kiel.regusters"
import sys
import os
sys.path.insert(0, os.path.join("data", "libs"))
sys.path.insert(0, os.path.join("data"))
sys.path.insert(0, os.path.join("data", "states"))
import pygame as pg
from data.main import main

if __name__ == "__main__":
	main()
	pg.quit()
	sys.exit()