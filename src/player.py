from direct.showbase.DirectObject import DirectObject
from panda3d.core import LPoint3f
from panda3d.core import CollisionSphere
from panda3d.core import CollisionRay
from panda3d.core import CollisionNode
from panda3d.core import CollisionHandlerFloor
from hud import HUD
from gun import Gun

class Player(DirectObject):
    def __init__(self):
        # Player Model setup
        self.player = loader.loadModel("smiley")
        self.player.setPos(0, 0, 0)
        self.player.reparentTo(render)
        self.player.hide()

        # setup the collision detection
        # wall and object collision
        self.playerSphere = CollisionSphere(0, 0, 0, 1)
        self.playerCollision = self.player.attachNewNode(CollisionNode("playerCollision"))
        self.playerCollision.node().addSolid(self.playerSphere)
        self.playerCollision.show()
        base.pusher.addCollider(self.playerCollision, self.player)
        base.cTrav.addCollider(self.playerCollision, base.pusher)
        # foot (walk) collision
        self.playerFootRay = self.player.attachNewNode(CollisionNode('playerFootCollision'))
        self.playerFootRay.node().addSolid(CollisionRay(0, 0, -1.5, 0, 0, -1))
        self.playerFootRay.node().setIntoCollideMask(0)
        self.lifter = CollisionHandlerFloor()
        self.lifter.addCollider(self.playerFootRay, self.player)
        base.cTrav.addCollider(self.playerFootRay, self.lifter)

        # Player weapon setup
        self.color = LPoint3f(0, 0, 1)
        self.gun = Gun()
        self.gun.reparentTo(camera)
        self.gun.hide()
        self.gun.setColor(self.color)

        # Player HUD setup
        self.hud = HUD()
        self.hud.updateAmmo(self.gun.maxAmmunition, self.gun.ammunition)

        # Player controls setup
        self.keyMap = {"left":0, "right":0, "forward":0, "backward":0}
        # screen sizes
        self.winXhalf = base.win.getXSize() / 2
        self.winYhalf = base.win.getYSize() / 2
        self.mouseSpeedX = 0.1
        self.mouseSpeedY = 0.1

        self.movespeed = 5.0

        # Player camera setup
        camera.setH(180)
        camera.reparentTo(self.player)
        camera.setZ(self.player, 2)
        base.camLens.setFov(90)
        base.camLens.setNear(0.001)

        self.accept("window-event", self.recalcAspectRatio)

    def run(self):
        self.player.show()
        self.hud.show()
        self.gun.show()
        self.accept("w", self.setKey, ["forward",1])
        self.accept("w-up", self.setKey, ["forward",0])
        self.accept("a", self.setKey, ["left",1])
        self.accept("a-up", self.setKey, ["left",0])
        self.accept("s", self.setKey, ["backward",1])
        self.accept("s-up", self.setKey, ["backward",0])
        self.accept("d", self.setKey, ["right",1])
        self.accept("d-up", self.setKey, ["right",0])
        self.accept("r", self.gun.reload)
        self.accept("mouse1", self.shoot)
        taskMgr.add(self.move, "moveTask", priority=-4)

    def stop(self):
        self.player.hide()
        self.hud.hide()
        self.gun.hide()
        self.ignore("w")
        self.ignore("w-up")
        self.ignore("a")
        self.ignore("a-up")
        self.ignore("s")
        self.ignore("s-up")
        self.ignore("d")
        self.ignore("d-up")
        self.ignore("mouse1")
        taskMgr.remove("moveTask")

    def setKey(self, key, value):
        self.keyMap[key] = value

    def setPos(self, pos):
        self.player.setPos(pos)

    def shoot(self):
        self.gun.shoot()
        self.hud.updateAmmo(self.gun.maxAmmunition, self.gun.ammunition)

    def recalcAspectRatio(self, window):
        self.winXhalf = window.getXSize() / 2
        self.winYhalf = window.getYSize() / 2

    def move(self, task):
        if not base.mouseWatcherNode.hasMouse(): return task.cont

        pointer = base.win.getPointer(0)
        mouseX = pointer.getX()
        mouseY = pointer.getY()

        if base.win.movePointer(0, self.winXhalf, self.winYhalf):
            p = camera.getP() - (mouseY - self.winYhalf) * self.mouseSpeedY
            if p <-80:
                p = -80
            elif p > 90:
                p = 90
            camera.setP(p)

            h = self.player.getH() - (mouseX - self.winXhalf) * self.mouseSpeedX
            if h <-360:
                h = 360
            elif h > 360:
                h = -360
            self.player.setH(h)

        if self.keyMap["left"] != 0:
            self.player.setX(self.player, self.movespeed * globalClock.getDt())
        if self.keyMap["right"] != 0:
            self.player.setX(self.player, -self.movespeed * globalClock.getDt())
        if self.keyMap["forward"] != 0:
            self.player.setY(self.player, -self.movespeed * globalClock.getDt())
        if self.keyMap["backward"] != 0:
            self.player.setY(self.player, self.movespeed * globalClock.getDt())

        return task.cont
