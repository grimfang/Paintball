from panda3d.core import CollisionInvSphere
from panda3d.core import CollisionNode
from panda3d.core import VBase4
from panda3d.core import PointLight
from panda3d.core import AmbientLight

class World():
    def __init__(self):
        # simple level

        #self.environ = loader.loadModel("world")
        #self.environ.reparentTo(render)
        #self.environ.hide()

        self.environ = loader.loadModel("IndoorLevel01")
        self.environ.reparentTo(render)
        self.environ.hide()

        #for i in range(9):
        #    print "load lamp: Lamp.%03d" % i
        #    lampPos = self.environ.find("**/Lamp.%03d" % i).getPos()
        #    plight = PointLight('plight')
        #    plight.setColor(VBase4(0.2, 0.2, 0.2, 1))
        #    plnp = render.attachNewNode(plight)
        #    plnp.setPos(lampPos)
        #    render.setLight(plnp)

        #self.ambientlight = AmbientLight('ambient light')
        #self.ambientlight.setColor(VBase4(0.2, 0.2, 0.2, 1))
        #self.ambientlightnp = render.attachNewNode(self.ambientlight)
        #render.setLight(self.ambientlightnp)

        #spaceSphere = CollisionInvSphere(0, 0, 0, 200)
        #space = render.attachNewNode(CollisionNode('outerSpaceCollision'))
        #space.node().addSolid(spaceSphere)
        #space.show()

    def run(self):
        self.environ.show()

    def stop(self):
        self.environ.hide()

    def getStartPos(self, posNr):
        pos = self.environ.find("**/StartPos%d" % posNr).getPos()
        return pos

    def getSpectatorNode(self):
        node = self.environ.find("**/Spectator")
        return node

    def getBunker(self):
        bunker = self.environ.findAllMatches("**/BunkerPos.*")
        return bunker
