from panda3d.core import CollisionInvSphere
from panda3d.core import CollisionNode

class World():
    def __init__(self):
        # simple level
        self.environ = loader.loadModel("world")
        self.environ.reparentTo(render)
        self.environ.hide()

        #spaceSphere = CollisionInvSphere(0, 0, 0, 200)
        #space = render.attachNewNode(CollisionNode('outerSpaceCollision'))
        #space.node().addSolid(spaceSphere)
        #space.show()

    def run(self):
        self.environ.show()

    def stop(self):
        self.environ.hide()

    def getStartPos(self):
        pos = self.environ.find("**/start_point").getPos()
        pos.setZ(pos.getZ() + 15.0)
        return pos
