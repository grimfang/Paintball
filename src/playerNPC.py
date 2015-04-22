from playerBase import PlayerBase
from panda3d.ai import AICharacter
from panda3d.core import Point3
from direct.fsm.FSM import FSM
import random, math


#Basic ideas for AI
# after starting the game:
#    run into closest bunker
#    randomly step left or right outside of the bunker and shoot in the
#      player or opposite teams direction
#    if it's calm around the player randomly move out of the bunker and
#      run into a new one or if only one player is left run toward him
#    if he is close to the player shoot flee backward if not in attack
#      mode or similar where he is intended to move towards the player

class NPC(PlayerBase, FSM):
    def __init__(self):
        FSM.__init__(self, 'Player-AI')
        PlayerBase.__init__(self)

        random.seed()

        #self.AIchar = AICharacter("wanderer",self.player, 100, 0.5, 20)
        #base.AIworld.addAiChar(self.AIchar)
        #self.AIbehaviors = self.AIchar.getAiBehaviors()

        #self.AIbehaviors.wander(50, 0, 100, 1.0)
        #self.player.loop("Run")
        self.accept("GameOver-player%d" % id(self), self.gameOver)

        # firerate in bullets per second
        self.fireRate = 1/5 # five shots per second
        self.lastShot = 0

        self.stepOutTime = 0
        self.stepBackTime = 1
        self.isOutOfBunker = False

        self.trackedEnemy = None

        self.allBunker = []

    def enterDoHide(self):
        # move the character in the closest bunker

        bunkerDistances = {}
        # search closest bunker
        curPos = self.player.getPos()
        for bunker in self.allBunker:
            playerBunkerVec = curPos - bunker.getPos(render)
            playerBunkerVec.setZ(0)
            bunkerDist = playerBunkerVec.length()
            if bunkerDist not in bunkerDistances:
                bunkerDistances[bunkerDist] = [bunker]
            else:
                bunkerDistances[bunkerDist].append(bunker)

        selectedBunker = random.choice(
            bunkerDistances[min(bunkerDistances.keys())])
        self.AIH = self.getDeg(curPos, selectedBunker.getPos(render))
        self.setKey("forward", 1)
        self.destPos = selectedBunker.getPos(render)

    def exitDoHide(self):
        self.setKey("forward", 0)

    def enterHidden(self):
        pass

    def exitHidden(self):
        pass

    def enterStepOutOfBunker(self):
        # do a step outside the current Bunker and shoot
        pass

    def exitStepOutOfBnker(self):
        # return to the safe bunker position
        pass

    def enterFlee(self):
        # run away from the current closest enemy
        pass

    def exitFlee(self):
        # hide in a new bunker
        pass

    def run(self):
        self.runBase()
        taskMgr.add(self.aiTask, "AI-Task%d" % id(self))
        self.request("DoHide")

    def setBunker(self, bunker):
        self.allBunker = bunker

    def setEnemies(self, enemies):
        self.allEnemies = enemies

    def stop(self):
        taskMgr.remove("setKey1%d"%id(self))
        taskMgr.remove("setOOB1%d"%id(self))
        taskMgr.remove("setKey2%d"%id(self))
        taskMgr.remove("setKey3%d"%id(self))
        taskMgr.remove("setOOB2%d"%id(self))
        taskMgr.remove("AI-Task%d" % id(self))
        self.stopBase()

    def gameOver(self):
        self.stop()

    def getEnemyPos(self):
        isEnemyAlive = False
        for enemy in self.allEnemies:
            if not enemy.isOut:
                isEnemyAlive = True
                break
        if not isEnemyAlive: return Point3(0,0,0)
        while (self.trackedEnemy == None or self.trackedEnemy.player.isEmpty()):
            self.trackedEnemy = random.choice(self.allEnemies)
        return self.trackedEnemy.player.getPos()

    def checkEnemyList(self):
        for enemy in self.allEnemies[:]:
            if enemy.isOut:
                self.allEnemies.remove(enemy)

    def aiTask(self, task):
        # check the current AI states and switch between them

        self.checkEnemyList()

        # get the elapsed time and store it in "elapsed"
        elapsed = globalClock.getDt()

        # track a random enemy
        if len(self.allEnemies) > 0:
            self.trackedEnemy = random.choice(self.allEnemies)
        # TODO: check if we have a closer enemy which we can directly see

        if self.state == "DoHide":
            # ceck if the player has reached the hide possition
            if self.player.getX() <= self.destPos.getX() + 0.5 and \
               self.player.getX() >= self.destPos.getX() - 0.5 and \
               self.player.getY() >= self.destPos.getY() - 0.5 and \
               self.player.getY() <= self.destPos.getY() + 0.5:
                # Player reached destination
                self.request("Hidden")
        elif self.state == "Hidden":
            enemyPos = self.getEnemyPos()
            curPos = self.player.getPos()
            # TODO: Slowly move to that heading value
            self.AIH = self.getDeg(curPos, enemyPos)
            self.request("StepOutOfBnker")
        elif self.state == "StepOutOfBnker":
            if not self.isOutOfBunker and self.stepOutTime <= 0:
                self.stepOutTime = random.uniform(3.0, 4.5)

            self.stepOutTime -= elapsed
            if not self.isOutOfBunker and self.stepOutTime <= 0:
                self.stepOutDirection = random.choice(["l", "r"])
                def setOutOfBunker(oob):
                    self.isOutOfBunker = oob
                if self.stepOutDirection == "l":
                    self.setKey("left", 1)
                    taskMgr.doMethodLater(0.2, self.setKey, "setKey1%d"%id(self), extraArgs=["left", 0])
                    taskMgr.doMethodLater(0.2, setOutOfBunker, "setOOB1%d"%id(self), extraArgs=[True])
                    taskMgr.doMethodLater(1.2, self.setKey, "setKey2%d"%id(self), extraArgs=["right", 1])
                    taskMgr.doMethodLater(1.4, self.setKey, "setKey3%d"%id(self), extraArgs=["right", 0])
                    taskMgr.doMethodLater(1.4, setOutOfBunker, "setOOB2%d"%id(self), extraArgs=[False])
                else:
                    self.setKey("right", 1)
                    taskMgr.doMethodLater(0.2, self.setKey, "setKey1%d"%id(self), extraArgs=["right", 0])
                    taskMgr.doMethodLater(0.2, setOutOfBunker, "setOOB1%d"%id(self), extraArgs=[True])
                    taskMgr.doMethodLater(1.2, self.setKey, "setKey2%d"%id(self), extraArgs=["left", 1])
                    taskMgr.doMethodLater(1.4, self.setKey, "setKey3%d"%id(self), extraArgs=["left", 0])
                    taskMgr.doMethodLater(1.4, setOutOfBunker, "setOOB2%d"%id(self), extraArgs=[False])

            if self.isOutOfBunker:
                self.lastShot += elapsed
                if self.lastShot >= self.fireRate:
                    # we can shoot
                    v = self.getEnemyPos() - self.player.getPos()
                    v.normalize()
                    self.shoot(v)
                    if self.gun.ammunition == 0:
                        self.reload()
                    self.lastShot = 0

        return task.cont


    def getDeg(self, pointA, pointB):
        vector = pointA - pointB
        x = vector.getX()
        y = vector.getY()
        return -(math.atan2(x, y) * 180 / math.pi)
