from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import DirectFrame
from direct.gui.DirectGui import DirectButton
from panda3d.core import TextNode

class Menu(DirectObject):
    def __init__(self):
        #self.accept("RatioChanged", self.recalcAspectRatio)
        self.accept("window-event", self.recalcAspectRatio)

        self.frameMain = DirectFrame(
            # size of the frame
            frameSize = (base.a2dLeft, base.a2dRight,
                         base.a2dTop, base.a2dBottom),
            # position of the frame
            pos = (0, 0, 0),
            # tramsparent bg color
            frameColor = (0, 0, 0, 0),
            sortOrder = 0)

        self.btnStart = self.createButton("Start", 0.25, self.btnStart_Click)
        self.btnStart.reparentTo(self.frameMain)

        self.btnQuit = self.createButton("Quit", -0.25, self.btnQuit_Click)
        self.btnQuit.reparentTo(self.frameMain)

        self.recalcAspectRatio(base.win)

        # hide all buttons at startup
        self.hide()

    def show(self):
        self.frameMain.show()
        self.recalcAspectRatio(base.win)

    def hide(self):
        self.frameMain.hide()

    def recalcAspectRatio(self, window):
        """get the new aspect ratio to resize the mainframe"""
        screenResMultiplier = window.getXSize() / window.getYSize()
        self.frameMain["frameSize"] = (
            base.a2dLeft, base.a2dRight,
            base.a2dTop, base.a2dBottom)
        self.btnQuit["text_scale"] = (0.5*screenResMultiplier, 0.5, 0.5)
        self.btnStart["text_scale"] = (0.5*screenResMultiplier, 0.5, 0.5)


    def createButton(self, text, yPos, command):
        btn = DirectButton(
            scale = (0.25, 0.25, 0.25),
            # some temp text
            text = text,
            text_scale = (0.5, 0.5, 0.5),
            # set the alignment to right
            text_align = TextNode.ACenter,
            # put the text on the right side of the button
            #text_pos = (4.1, -0.15),
            # set the text color to black
            text_fg = (0,0,0,1),
            # set the buttons images
            #geom = (self.defaultBtnMaps.find("**/button_ready"),
            #        self.defaultBtnMaps.find("**/button_click"),
            #        self.defaultBtnMaps.find("**/button_rollover"),
            #        self.defaultBtnMaps.find("**/button_disabled")),
            #relief = 1,
            #frameColor = (0,0,0,0),
            #pressEffect = False,
            pos = (0, 0, yPos),
            command = command,
            rolloverSound = None,
            clickSound = None)
        btn.setTransparency(1)
        return btn

    def btnStart_Click(self):
        base.messenger.send("start")

    def btnQuit_Click(self):
        base.messenger.send("quit")
