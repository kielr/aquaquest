////////////////////////////////////////
//////////////REQUIREMENTS//////////////

This project REQUIRES python3.5 along with pygame(which also requires SDL)

If pygame is not installed:

python -m pip install pygame
OR
python -m pip3 install pygame


Open python in terminal and type:

import pygame

If all is well, you should have no error

//////////////////////////////////////////
///////////////INSTALLATION///////////////

After making sure pygame is installed, all you need to do is run the following commands to install the system:

cd path/to/aquaquest-sdist-directory

After getting to the correct aquaquest directory with setup.py:

python setup.py build
python setup.py install - if you have root priviledges
sudo python setup.py install - if you don't have root priviledges

//////////////////////////////////////
///////////////USAGE//////////////////

After it is done installing, to run the game simple type the following command into console:

python -m aquaquest_play

If for some reason you are having trouble using the setup.py installer you can also just run it
from the sdist directory directly like so:

(while in sdist directory of project)
python aquaquest_play.py

//////////////////////////////////////
/////////////CONTROLS/////////////////

After starting the game, you'll be presented with the main menu.

W -> Moves the cursor UP
S -> Moves the cursor DOWN

Space, Enter, E -> Selects currently selected item from cursor

Each option does the following:
PLAY -> Starts a new game
CONTINUE -> If there is a save, continue from it
OPTIONS -> Go to options menu
QUIT -> Close the program

Once you're ingame the controls are like so:

ESC -> Go back to main menu (*unsaved progress will be lost!)
A -> Move Character LEFT
D -> Move Character RIGHT
Space -> JUMP and DOUBLEJUMP
E -> Melee attack
Q -> Magic attack

*Note: You save progress by reaching the tiny flags throughout each level

There are three stats in the game denoted by the text at the top of the screen:
STR - Affects melee attack damae
DEX - Affects ground and air speed
INT - Affects magic attack damage, speed, and lifetime

When you level up you can spend a skill point to on one of the stats by pressing the following numbers
on your number key row:

[1] -> increase STR by 1
[2] -> increase DEX by 1
[3] -> increase INT by 1

*NOTE: Max level for the player is 20 and highest the stat can be is 9

CHEATS FOR DEVELOPER AND GRADER CONVENIENCE:
F2 -> Deal 50 damage to player
F3 -> Heal 50 damage to player
F4 -> Rapidly give XP to player
F5 -> Turn window FPS counter ON/OFF


If you manage to get to the gameover(Congratulations) screen, ESC will bring you back to the main menu.

//////////////////////////////////////
////////////COMMENTARY////////////////

This is the readme/user guide for the CptS481 Project. For my project I proposed a game, and for the game I used PyGame and did 2D graphics.
The project was mostly a learning experience for me. I have never made a 2D game before and I have also never used python or pygame to do it.
I think the hardest part about this project was the collision and camera. PyGame does not come with it's own viewport/camera class for games
so I had to write in my own. It basically just involved having a camera x and y offset to everything in the world. Once I figured that out
it was pretty easy. Collision resolution was hard because it didn't play nice with how implemented the camera as I said before, and I am sure
that there are still plenty of bugs that are present because of the way I made them work with eachother.

Overall this was a very fun class project. I learned a lot and although I'm not sure I'd use python/pygame to do a 2D game, I had a lot of fun
doing it.

//////////////////////////////////////////////
//////////////////////////////////////////////
