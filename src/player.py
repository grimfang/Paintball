from direct.showbase.DirectObject import DirectObject
from playerBase import PlayerBase
from hud import HUD

class Player(PlayerBase, DirectObject):
    def __init__(self):
        PlayerBase.__init__(self)

        self.userControlled = True

        # Player HUD setup
        self.hud = HUD()

    def run(self):
        self.hud.show()

        # realod the gun
        self.reload()
        # setup the players camera
        self.Eyes = self.player.exposeJoint(None, "modelRoot", "Eyes")
        camera.setPos(0,0,0)
        camera.setHpr(0,0,0)
        camera.reparentTo(self.Eyes)
        base.camLens.setFov(90)
        base.camLens.setNear(0.001)

        # accept the players input
        self.accept("w", self.setKey, ["forward",1])
        self.accept("w-up", self.setKey, ["forward",0])
        self.accept("a", self.setKey, ["left",1])
        self.accept("a-up", self.setKey, ["left",0])
        self.accept("s", self.setKey, ["backward",1])
        self.accept("s-up", self.setKey, ["backward",0])
        self.accept("d", self.setKey, ["right",1])
        self.accept("d-up", self.setKey, ["right",0])
        self.accept("r", self.reload)
        self.accept("mouse1", self.shoot)

        self.accept("GameOver-player%d" % id(self), self.gameOver)
        self.runBase()

    def stop(self):
        self.hud.hide()
        self.ignore("w")
        self.ignore("w-up")
        self.ignore("a")
        self.ignore("a-up")
        self.ignore("s")
        self.ignore("s-up")
        self.ignore("d")
        self.ignore("d-up")
        self.ignore("mouse1")

        self.ignore("GameOver-player%d" % id(self))
        self.stopBase()

    def setSpectator(self, cameraPositionNode):
        camera.setPos(cameraPositionNode.getPos())
        camera.lookAt(0,0,0)
        base.camLens.setFov(60)
        camera.reparentTo(render)

    def gameOver(self):
        self.stop()
