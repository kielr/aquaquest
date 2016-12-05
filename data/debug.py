__author__ = "kiel.regusters"
"""
Simple module to print debug information.
"""

DEBUG = True
DEBUG_DRAW = False


def debug(string):
	if DEBUG:
		print("DEBUG = ", end="")
		print(string)