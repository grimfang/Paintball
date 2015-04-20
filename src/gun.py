from bullet import Bullet

class Gun:
    def __init__(self, playerID):
        self.model = loader.loadModel("Marker")
        self.model.setR(-90)
        self.model.setScale(0.5)

        self.maxAmmunition = 40
        self.ammunition = 40

        self.playerID = playerID

    def reparentTo(self, parent):
        self.model.reparentTo(parent)

    def setColor(self, color):
        self.color = color

    def shoot(self, shotVec=None):
        if self.ammunition > 0:
            b = Bullet(self.playerID, self.color)
            pos = self.model.find("**/BulletStart").getPos(render)
            hpr = self.model.getHpr(render)
            hpr.setX(hpr.getX() + 90.0)
            b.shoot(pos, shotVec)
            self.ammunition -= 1

    def reload(self):
        self.ammunition = self.maxAmmunition

    def show(self):
        self.model.show()

    def hide(self):
        self.model.hide()

    def remove(self):
        self.model.removeNode()

