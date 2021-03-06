from direct.showbase.DirectObject import DirectObject
from panda3d.physics import ForceNode
from panda3d.physics import LinearVectorForce
from panda3d.physics import ActorNode
from panda3d.core import CollisionSphere
from panda3d.core import CollisionNode
from panda3d.core import NodePath
from panda3d.core import LPoint3f
from panda3d.core import Point3

class Bullet(DirectObject):
    def __init__(self, playerID, color=LPoint3f(0,0,0)):
        self.color = color
        self.playerID = playerID

        self.bulletNP = NodePath("Bullet-%d" % id(self))
        self.bulletAN = ActorNode("bullet-physics-%d" % id(self))
        # set the mass of the ball to 3.3g = average weight of a paintball
        self.bulletAN.getPhysicsObject().setMass(0.033)
        self.bulletANP = self.bulletNP.attachNewNode(self.bulletAN)
        base.physicsMgr.attachPhysicalNode(self.bulletAN)
        self.bullet = loader.loadModel("Bullet")
        self.bullet.setScale(2)
        self.bullet.setColorScale(
            self.color.getX(),
            self.color.getY(),
            self.color.getZ(),
            1.0)
        self.bullet.reparentTo(self.bulletANP)

        # setup the collision detection
        # 17.3 mm (0.0173) = size of a .68cal paintball
        self.bulletColName = "bulletCollision-%02d" % id(self)
        self.bulletSphere = CollisionSphere(0, 0, 0, 0.0173*2)
        self.bulletCollision = self.bulletANP.attachNewNode(CollisionNode(self.bulletColName))
        self.bulletCollision.node().addSolid(self.bulletSphere)
        #self.bulletCollision.show()
        base.physicpusher.addCollider(self.bulletCollision, self.bulletANP)
        base.cTrav.addCollider(self.bulletCollision, base.physicpusher)

    def shoot(self, pos, shootVec=None):
        if shootVec != None:
            v = shootVec
            v *= 214.0
        else:
            # Get from/to points from mouse click
            pMouse = base.mouseWatcherNode.getMouse()
            pFrom = Point3()
            pTo = Point3()
            base.camLens.extrude(pMouse, pFrom, pTo)

            pFrom = render.getRelativePoint(base.cam, pFrom)
            pTo = render.getRelativePoint(base.cam, pTo)

            # Calculate initial velocity
            v = pTo - pFrom
            v.normalize()
            v *= 214.0

        self.bulletNP.setPos(pos)
        self.bulletNP.reparentTo(render)
        self.bulletFN = ForceNode("Bullet-force-%d" % id(self))
        self.bulletFNP = self.bulletNP.attachNewNode(self.bulletFN)
        # speed of a paintball when he leafes the muzzle: 214 fps
        self.lvf = LinearVectorForce(v)
        self.lvf.setMassDependent(1)
        self.bulletFN.addForce(self.lvf)
        self.bulletAN.getPhysical(0).addLinearForce(self.lvf)

        self.accept("bulletCollision-%d-hit" % id(self), self.bulletHit)
        taskMgr.doMethodLater(
            2,
            self.doRemove,
            'doRemove-%d' % id(self),
            appendTask=True)

    def doRemove(self, task):
        if self is None: return task.done
        self.ignoreAll()
        self.bulletNP.removeNode()
        self.bulletAN.getPhysical(0).removeLinearForce(self.lvf)
        return task.done

    def bulletHit(self, entry):
        hitName = entry.getIntoNode().getName()
        if str(self.playerID) not in hitName and \
            self.bulletColName not in hitName:
            base.messenger.send("Bulet-hit-%s" % hitName, [entry, self.color])
            self.bulletNP.removeNode()
            self.bulletAN.getPhysical(0).removeLinearForce(self.lvf)
