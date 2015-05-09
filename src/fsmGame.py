
from direct.fsm.FSM import FSM

import helper

from menu import Menu
from player import Player
from playerNPC import NPC
from hud import HUD
from result import Result
from world import World

from panda3d.core import LPoint3f

class FSMGame(FSM):
    def __init__(self):
        FSM.__init__(self, "FSM-Game")
        self.menu = Menu()
        self.gameResult = Result()
        self.numNPCs = 7

    def enterMenu(self):
        helper.show_cursor()
        self.menu.show()

    def exitMenu(self):
        self.menu.hide()

    def enterSingleplayer(self):
        helper.hide_cursor()

        self.world = World()
        self.world.run()

        self.player = Player()
        self.player.run()
        self.player.setPos(self.world.getStartPos(1))
        self.player.setTeam("Yellow")
        self.player.setColor(LPoint3f(1, 1, 0))

        #self.player.setSpectator(self.world.getSpectatorNode())

        # create non player characters
        self.npcs = []
        for i in range(self.numNPCs):
            self.npcs.append(NPC())
            self.npcs[i].setPos(self.world.getStartPos(i+2))
            self.npcs[i].setBunker(self.world.getBunker())
            if i < self.numNPCs/2:
                self.npcs[i].setTeam("Yellow")
                self.npcs[i].setColor(LPoint3f(1, 1, 0))
            else:
                self.npcs[i].setTeam("Blue")
                self.npcs[i].setColor(LPoint3f(0, 0, 1))
            self.npcs[i].run()

        for i in range(self.numNPCs):
            el = []
            if self.npcs[i].playerTeam != self.player.playerTeam:
                el.append(self.player)
            for j in range(self.numNPCs):
                if self.npcs[i].playerTeam != self.npcs[j].playerTeam:
                    el.append(self.npcs[j])
            self.npcs[i].setEnemies(el)
        taskMgr.add(self.checkGameOver, "checkGameOver")

    def exitSingleplayer(self):
        self.player.stop()
        for i in range(len(self.npcs)):
            self.npcs[i].stop()
        self.npcs = []
        self.world.stop()
        del self.world
        self.gameResult.hide()
        taskMgr.remove("checkGameOver")

    def checkGameOver(self, task):
        if self is None: return task.done
        if self.player.isOut:
            self.player.setSpectator(self.world.getSpectatorNode())
        allEnemyNpcsOut = True
        for npc in self.npcs:
            if npc.playerTeam != self.player.playerTeam:
                if not npc.isOut:
                    allEnemyNpcsOut = False
                    break

        teams = []
        if not self.player.isOut:
            teams.append(self.player.playerTeam)
        for npc in self.npcs:
            if not npc.isOut and not npc.playerTeam in teams:
                teams.append(npc.playerTeam)
        if len(teams) == 1:
            self.gameResult.setTeam(teams[0])
            self.gameResult.show()
            return task.done
        elif len(teams) == 0:
            self.gameResult.setTeam("Draw")
            self.gameResult.show()
            return task.done

        return task.cont
