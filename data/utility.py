__author__ = "kiel.regusters"
""" This module contains the Overhead class."""
import pygame as pg
from . import init

class Overhead(object):
	""" The Overhead class keeps track of certain information that needs to be seen by other objects. """
	def __init__(self, state):
		self.state = state