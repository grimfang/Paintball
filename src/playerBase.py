from direct.showbase.DirectObject import DirectObject
from panda3d.core import LPoint3f
from panda3d.core import CollisionSphere
from panda3d.core import CollisionRay
from panda3d.core import CollisionNode
from panda3d.core import CollisionHandlerFloor
from direct.actor.Actor import Actor
from gun import Gun

class PlayerBase(DirectObject):
    def __init__(self):
        # Player Model setup
        self.player = Actor("Player",
                            {"Run":"Player-Run",
                            "Idle":"Player-Idle"})
        self.player.setBlend(frameBlend = True)
        self.player.setPos(0, 0, 0)
        self.player.reparentTo(render)
        self.player.hide()

        # team
        self.playerTeam = ""

        # basic player values
        self.maxHits = 1
        self.currentHits = 0
        self.isOut = False

        self.TorsorControl = self.player.controlJoint(None,"modelRoot","Torsor")

        # setup the collision detection
        # wall and object collision
        self.playerSphere = CollisionSphere(0, 0, 1, 1)
        self.playerCollision = self.player.attachNewNode(CollisionNode("playerCollision%d"%id(self)))
        self.playerCollision.node().addSolid(self.playerSphere)
        base.pusher.addCollider(self.playerCollision, self.player)
        base.cTrav.addCollider(self.playerCollision, base.pusher)
        # foot (walk) collision
        self.playerFootRay = self.player.attachNewNode(CollisionNode("playerFootCollision%d"%id(self)))
        self.playerFootRay.node().addSolid(CollisionRay(0, 0, 2, 0, 0, -1))
        self.playerFootRay.node().setIntoCollideMask(0)
        self.lifter = CollisionHandlerFloor()
        self.lifter.addCollider(self.playerFootRay, self.player)
        base.cTrav.addCollider(self.playerFootRay, self.lifter)

        # Player weapon setup
        self.gunAttach = self.player.exposeJoint(None, "modelRoot", "WeaponSlot_R")
        self.color = LPoint3f(0, 0, 1)
        self.gun = Gun(id(self))
        self.gun.reparentTo(self.gunAttach)
        self.gun.hide()
        self.gun.setColor(self.color)

        self.hud = None

        # Player controls setup
        self.keyMap = {"left":0, "right":0, "forward":0, "backward":0}
        # screen sizes
        self.winXhalf = base.win.getXSize() / 2
        self.winYhalf = base.win.getYSize() / 2
        self.mouseSpeedX = 0.1
        self.mouseSpeedY = 0.1
        # AI controllable variables
        self.AIP = 0.0
        self.AIH = 0.0

        self.movespeed = 5.0

        self.userControlled = False

        self.accept("Bulet-hit-playerCollision%d" % id(self), self.hit)
        self.accept("window-event", self.recalcAspectRatio)

    def runBase(self):
        self.player.show()
        self.gun.show()
        taskMgr.add(self.move, "moveTask%d"%id(self), priority=-4)

    def stopBase(self):
        self.gun.remove()
        self.player.delete()
        taskMgr.remove("moveTask%d"%id(self))

    def setKey(self, key, value):
        self.keyMap[key] = value

    def setPos(self, pos):
        self.player.setPos(pos)

    def shoot(self, shotVec=None):
        self.gun.shoot(shotVec)
        if self.hud != None:
            self.hud.updateAmmo(self.gun.maxAmmunition, self.gun.ammunition)

    def reload(self):
        self.gun.reload()
        if self.hud != None:
            self.hud.updateAmmo(self.gun.maxAmmunition, self.gun.ammunition)

    def recalcAspectRatio(self, window):
        self.winXhalf = window.getXSize() / 2
        self.winYhalf = window.getYSize() / 2

    def hit(self):
        self.currentHits
        if self.maxHits >= self.currentHits:
            base.messenger.send("GameOver-player%d" % id(self))
            self.isOut = True

    def move(self, task):

        if self.userControlled:
            if not base.mouseWatcherNode.hasMouse(): return task.cont
            self.pointer = base.win.getPointer(0)
            mouseX = self.pointer.getX()
            mouseY = self.pointer.getY()

            if base.win.movePointer(0, self.winXhalf, self.winYhalf):
                p = self.TorsorControl.getP() + (mouseY - self.winYhalf) * self.mouseSpeedY
                if p <-80:
                    p = -80
                elif p > 90:
                    p = 90
                self.TorsorControl.setP(p)

                h = self.player.getH() - (mouseX - self.winXhalf) * self.mouseSpeedX
                if h <-360:
                    h = 360
                elif h > 360:
                    h = -360
                self.player.setH(h)
        else:
            self.TorsorControl.setP(self.AIP)
            self.player.setH(self.AIH)

        if self.keyMap["left"] != 0:
            self.player.setX(self.player, self.movespeed * globalClock.getDt())
        if self.keyMap["right"] != 0:
            self.player.setX(self.player, -self.movespeed * globalClock.getDt())
        if self.keyMap["forward"] != 0:
            if self.player.getCurrentAnim() != "Run":
                self.player.loop("Run")
                self.player.setPlayRate(5, "Run")
            self.player.setY(self.player, -self.movespeed * globalClock.getDt())
        else:
            self.player.stop("Run")
        if self.keyMap["backward"] != 0:
            self.player.setY(self.player, self.movespeed * globalClock.getDt())

        if not (self.keyMap["left"] or self.keyMap["right"] or
                self.keyMap["forward"] or self.keyMap["backward"] or
                self.player.getCurrentAnim() == "Idle"):
            self.player.loop("Idle")

        return task.cont
