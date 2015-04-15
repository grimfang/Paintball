import os
from direct.showbase.DirectObject import DirectObject
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.DirectLabel import DirectLabel
from panda3d.core import TextNode

class HUD(DirectObject):
    def __init__(self):

        self.winXhalf = base.win.getXSize() / 2
        self.winYhalf = base.win.getYSize() / 2

        croshairsize = 0.05#17.0

        self.crosshair = OnscreenImage(
            image = os.path.join("..", "data", "crosshair.png"),
            scale = (croshairsize, 1, croshairsize),
            #pos = (self.winXhalf - croshairsize/2.0, 0, -self.winYhalf - croshairsize/2.0)
            pos = (0, 0, 0)
            )
        self.crosshair.setTransparency(1)

        self.ammo = DirectLabel(
            scale = 0.15,
            text = "100/100",
            pos = (base.a2dLeft + 0.025, 0.0, base.a2dBottom + 0.05),
            text_align = TextNode.ALeft,
            frameColor = (0, 0, 0, 0),
            text_fg = (1,1,1,1),
            text_shadow = (0, 0, 0, 1),
            text_shadowOffset = (0.05, 0.05)
            )
        self.ammo.setTransparency(1)

        self.accept("window-event", self.recalcAspectRatio)
        self.hide()

    def show(self):
        self.crosshair.show()
        self.ammo.show()

    def hide(self):
        self.crosshair.hide()
        self.ammo.hide()

    def updateAmmo(self, maxAmmo, ammo):
        self.ammo["text"] = "%02d/%02d" % (maxAmmo, ammo)

    def recalcAspectRatio(self, window):
        self.ammo.setPos(base.a2dLeft + 0.025, 0.0, base.a2dBottom + 0.05),
