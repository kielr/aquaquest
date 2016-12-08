"""
Simple module to print debug information.
"""

__author__ = "kiel.regusters"

DEBUG = True
DEBUG_DRAW = False


def debug(string):
	if DEBUG:
		print("DEBUG = ", end="")
		print(string)