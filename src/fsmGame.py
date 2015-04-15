
from direct.fsm.FSM import FSM

import helper

from menu import Menu
from player import Player
from hud import HUD
from world import World

class FSMGame(FSM):
    def __init__(self):
        FSM.__init__(self, "FSM-Game")
        self.menu = Menu()
        self.player = Player()
        self.world = World()

    def enterMenu(self):
        helper.show_cursor()
        self.menu.show()

    def exitMenu(self):
        self.menu.hide()

    def enterSingleplayer(self):
        helper.hide_cursor()
        self.world.run()
        self.player.run()
        self.player.setPos(self.world.getStartPos())

    def exitSingleplayer(self):
        self.player.stop()
        self.world.stop()
