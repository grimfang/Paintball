from direct.gui.DirectGui import DirectLabel
from panda3d.core import TextNode

class Result():
    def __init__(self):
        self.txtresult = DirectLabel(
            scale = 0.25,
            frameColor = (0, 0, 0, 0),
            text = "",
            #text_align = TextNode.ACenter,
            text_fg = (0,0,0,1))
        self.txtresult.setTransparency(1)

    def setTeam(self, team):
        self.txtresult["text"] = "Team %s win" % team
        if team == "Yellow":
            self.txtresult["text_fg"] = (1,1,0,1)
        else:
            self.txtresult["text_fg"] = (0,0,1,1)

    def show(self):
        self.txtresult.show()

    def hide(self):
        self.txtresult.hide()
