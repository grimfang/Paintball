from direct.showbase.DirectObject import DirectObject
from panda3d.core import (
    LPoint3f,
    CollisionSphere,
    CollisionRay,
    CollisionNode,
    CollisionHandlerFloor,
    TextNode,
    TextureStage,
    Texture,
    PNMImage,
    PNMBrush,
    PNMPainter,
    BitMask32,
    Camera,
    NodePath,
    TransparencyAttrib,
    LColorf)
from direct.gui.DirectGui import DirectLabel
from direct.actor.Actor import Actor
from gun import Gun

class PlayerBase(DirectObject):
    def __init__(self):
        # Player Model setup
        self.player = Actor("Player",
                            {"Run":"Player-Run",
                            "Sidestep":"Player-Sidestep",
                            "Idle":"Player-Idle"})
        self.player.setBlend(frameBlend = True)
        self.player.setPos(0, 0, 0)
        self.player.pose("Idle", 0)
        self.player.reparentTo(render)
        self.player.hide()

        self.footstep = base.audio3d.loadSfx('footstep.ogg')
        self.footstep.setLoop(True)
        base.audio3d.attachSoundToObject(self.footstep, self.player)

        # Create a brush to paint on the texture
        splat = PNMImage("../data/Splat.png")
        self.colorBrush = PNMBrush.makeImage(splat, 6, 6, 1)

        CamMask = BitMask32.bit(0)
        AvBufMask = BitMask32.bit(1)
        self.avbuf = None
        if base.win:
            self.avbufTex = Texture('avbuf')
            self.avbuf = base.win.makeTextureBuffer('avbuf', 256, 256, self.avbufTex, True)
            cam = Camera('avbuf')
            cam.setLens(base.camNode.getLens())
            self.avbufCam = base.cam.attachNewNode(cam)
            dr = self.avbuf.makeDisplayRegion()
            dr.setCamera(self.avbufCam)
            self.avbuf.setActive(False)
            self.avbuf.setClearColor((1, 0, 0, 1))
            cam.setCameraMask(AvBufMask)
            base.camNode.setCameraMask(CamMask)

            # avbuf renders everything it sees with the gradient texture.
            tex = loader.loadTexture('gradient.png')
            np = NodePath('np')
            np.setTexture(tex, 100)
            np.setColor((1, 1, 1, 1), 100)
            np.setColorScaleOff(100)
            np.setTransparency(TransparencyAttrib.MNone, 100)
            np.setLightOff(100)
            cam.setInitialState(np.getState())
            #render.hide(AvBufMask)

        # Setup a texture stage to paint on the player
        self.paintTs = TextureStage('paintTs')
        self.paintTs.setMode(TextureStage.MDecal)
        self.paintTs.setSort(10)
        self.paintTs.setPriority(10)

        self.tex = Texture('paint_av_%s'%id(self))

        # Setup a PNMImage that will hold the paintable texture of the player
        self.imageSizeX = 64
        self.imageSizeY = 64
        self.p = PNMImage(self.imageSizeX, self.imageSizeY, 4)
        self.p.fill(1)
        self.p.alphaFill(0)
        self.tex.load(self.p)
        self.tex.setWrapU(self.tex.WMClamp)
        self.tex.setWrapV(self.tex.WMClamp)

        # Apply the paintable texture to the avatar
        self.player.setTexture(self.paintTs, self.tex)

        # team
        self.playerTeam = ""
        # A lable that will display the players team
        self.lblTeam = DirectLabel(
            scale = 1,
            pos = (0, 0, 3),
            frameColor = (0, 0, 0, 0),
            text = "TEAM",
            text_align = TextNode.ACenter,
            text_fg = (0,0,0,1))
        self.lblTeam.reparentTo(self.player)
        self.lblTeam.setBillboardPointEye()

        # basic player values
        self.maxHits = 3
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
        self.color = LPoint3f(1, 1, 1)
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
        taskMgr.remove("moveTask%d"%id(self))
        self.ignoreAll()
        self.gun.remove()
        self.footstep.stop()
        base.audio3d.detachSound(self.footstep)
        self.player.delete()

    def setKey(self, key, value):
        self.keyMap[key] = value

    def setPos(self, pos):
        self.player.setPos(pos)

    def setColor(self, color=LPoint3f(0,0,0)):
        self.color = color
        self.gun.setColor(color)
        c = (color[0], color[1], color[2], 1.0)
        self.lblTeam["text_fg"] = c

    def setTeam(self, team):
        self.playerTeam = team
        self.lblTeam["text"] = team


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

    def hit(self, entry, color):
        self.currentHits += 1

        # Create a brush to paint on the texture
        splat = PNMImage("../data/Splat.png")
        splat = splat * LColorf(color[0], color[1], color[2], 1.0)
        self.colorBrush = PNMBrush.makeImage(splat, 6, 6, 1)

        self.paintAvatar(entry)

        if self.currentHits >= self.maxHits:
            base.messenger.send("GameOver-player%d" % id(self))
            self.isOut = True

    def __paint(self, s, t):
        """ Paints a point on the avatar at texture coordinates (s, t). """
        x = (s * self.p.getXSize())
        y = ((1.0 - t) * self.p.getYSize())

        # Draw in color directly on the avatar
        p1 = PNMPainter(self.p)
        p1.setPen(self.colorBrush)
        p1.drawPoint(x, y)

        self.tex.load(self.p)
        self.tex.setWrapU(self.tex.WMClamp)
        self.tex.setWrapV(self.tex.WMClamp)

        self.paintDirty = True

    def paintAvatar(self, entry):
        """ Paints onto an avatar.  Returns true on success, false on
        failure (because there are no avatar pixels under the mouse,
        for instance). """

        # First, we have to render the avatar in its false-color
        # image, to determine which part of its texture is under the
        # mouse.
        if not self.avbuf:
            return False

        #mpos = base.mouseWatcherNode.getMouse()
        mpos = entry.getSurfacePoint(self.player)
        ppos = entry.getSurfacePoint(render)

        self.player.showThrough(BitMask32.bit(1))
        self.avbuf.setActive(True)
        base.graphicsEngine.renderFrame()
        self.player.show(BitMask32.bit(1))
        self.avbuf.setActive(False)

        # Now we have the rendered image in self.avbufTex.
        if not self.avbufTex.hasRamImage():
            print "Weird, no image in avbufTex."
            return False
        p = PNMImage()
        self.avbufTex.store(p)
        ix = int((1 + mpos.getX()) * p.getXSize() * 0.5)
        iy = int((1 - mpos.getY()) * p.getYSize() * 0.5)
        x = 1
        if ix >= 0 and ix < p.getXSize() and iy >= 0 and iy < p.getYSize():
            s = p.getBlue(ix, iy)
            t = p.getGreen(ix, iy)
            x = p.getRed(ix, iy)
        if x > 0.5:
            # Off the avatar.
            return False

        # At point (s, t) on the avatar's map.

        self.__paint(s, t)
        return True

    def move(self, task):
        if self is None: return task.done
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

        forward =  self.keyMap["forward"] != 0
        backward = self.keyMap["backward"] != 0

        if self.keyMap["left"] != 0:
            if self.player.getCurrentAnim() != "Sidestep" and not (forward or backward):
                self.player.loop("Sidestep")
                self.player.setPlayRate(5, "Sidestep")
            self.player.setX(self.player, self.movespeed * globalClock.getDt())
        elif self.keyMap["right"] != 0:
            if self.player.getCurrentAnim() != "Sidestep" and not (forward or backward):
                self.player.loop("Sidestep")
                self.player.setPlayRate(5, "Sidestep")
            self.player.setX(self.player, -self.movespeed * globalClock.getDt())
        else:
            self.player.stop("Sidestep")
        if forward:
            if self.player.getCurrentAnim() != "Run":
                self.player.loop("Run")
                self.player.setPlayRate(5, "Run")
            self.player.setY(self.player, -self.movespeed * globalClock.getDt())
        elif backward:
            if self.player.getCurrentAnim() != "Run":
                self.player.loop("Run")
                self.player.setPlayRate(-5, "Run")
            self.player.setY(self.player, self.movespeed * globalClock.getDt())
        else:
            self.player.stop("Run")

        if not (self.keyMap["left"] or self.keyMap["right"] or
                self.keyMap["forward"] or self.keyMap["backward"] or
                self.player.getCurrentAnim() == "Idle"):
            self.player.loop("Idle")
            self.footstep.stop()
        else:
            self.footstep.play()

        return task.cont
