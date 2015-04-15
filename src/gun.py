from bullet import Bullet

class Gun:
    def __init__(self):
        self.model = loader.loadModel("Marker")
        self.model.setPos(0.8, 1, -0.5)

        self.maxAmmunition = 40
        self.ammunition = 40

    def reparentTo(self, parent):
        self.model.reparentTo(parent)

    def setColor(self, color):
        self.color = color

    def shoot(self):
        if self.ammunition > 0:
            b = Bullet(1, self.color)
            pos = self.model.find("**/BulletStart").getPos(render)
            hpr = self.model.getHpr(render)
            hpr.setX(hpr.getX() + 90.0)
            b.shoot(pos)
            self.ammunition -= 1

    def reload(self):
        self.ammunition = self.maxAmmunition

    def show(self):
        self.model.show()

    def hide(self):
        self.model.hide()

