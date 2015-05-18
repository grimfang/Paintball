import sys
from direct.showbase.ShowBase import ShowBase
from direct.showbase import Audio3DManager
from direct.filter.CommonFilters import CommonFilters
from fsmGame import FSMGame
from panda3d.physics import (ForceNode,
    LinearVectorForce,
    PhysicsCollisionHandler)
from panda3d.core import (CollisionHandlerPusher,
    CollisionTraverser,
    Vec4)

from pandac.PandaModules import loadPrcFileData
# setup some starting vars in the config so the window is hiden at startup
loadPrcFileData("", "load-display pandagl")
loadPrcFileData("", "notify-timestamp 1")
loadPrcFileData("", "model-path ../data")

class Main(ShowBase):
    """Main function of the application
    initialise the engine (ShowBase)"""

    def __init__(self):
        """initialise the engine"""
        ShowBase.__init__(self)

        # disable pandas default mouse-camera controls so we can handle the cam
        # movements by ourself
        self.disableMouse()

        self.win.setClearColor(Vec4(0,0,0,1))

        # Event handling
        self.accept("escape", self.escape)
        self.accept("quit", sys.exit)
        self.accept("start", lambda: self.fsmGame.request("Singleplayer"))

        # Start physic simulation
        self.enableParticles()

        # enable gravity
        gravityFN=ForceNode('world-forces')
        gravityFNP=render.attachNewNode(gravityFN)
        gravityForce=LinearVectorForce(0,0,-9.81) #gravity acceleration
        gravityFN.addForce(gravityForce)
        self.physicsMgr.addLinearForce(gravityForce)

        # enable collision handling
        traverser = CollisionTraverser("base collision traverser")
        base.cTrav = traverser
        base.cTrav.setRespectPrevTransform(True)
        base.physicpusher = PhysicsCollisionHandler()
        base.physicpusher.addInPattern("%fn-hit")
        base.pusher = CollisionHandlerPusher()

        base.audio3d = Audio3DManager.Audio3DManager(base.sfxManagerList[0], camera)

        # enable shaders
        #self.render.setShaderAuto()

        # Simple postprocessing by the engine
        #self.filters = CommonFilters(base.win, base.cam)
        #self.filters.setCartoonInk(separation=2)
        #filters.delCartoonInk()

        # Initialize game states
        self.fsmGame = FSMGame()
        # Beginn with the menu
        self.fsmGame.request("Menu")

        if __debug__:
            from pandac.PandaModules import WindowProperties
            from panda3d.core import ConfigVariableInt
            self.fullscreen = False

            def toggleOobe():
                """Switch between free camera (steering with the mouse) and
                the camera controled by the game"""
                self.oobe()
            def explorer():
                """activates the Panda3D halp tool to explore the
                render Nodepath"""
                APP.render.explore()
            def toggleFullscreen():
                """Toggles the window between fullscreen and windowed mode"""
                self.fullscreen = not self.fullscreen
                props = WindowProperties()
                if self.fullscreen:
                    getW = base.pipe.getDisplayWidth
                    getH = base.pipe.getDisplayHeight
                    width = getW() if getW() != 0 else 800
                    height = getH() if getH() != 0 else 600
                    props.setSize(width, height)
                else:
                    sizeProp = ConfigVariableInt("win-size")
                    props.setSize(sizeProp.getWord(0), sizeProp.getWord(1))
                props.setFullscreen(self.fullscreen)
                props.setUndecorated(self.fullscreen)
                base.win.requestProperties(props)
            def toggleWireframe():
                """Switch between wired model view and normal view"""
                base.toggleWireframe()
            def showCollisions():
                """Render collision solids"""
                base.cTrav.showCollisions(render)
            from panda3d.core import PStatClient
            self.accept("f7", PStatClient.connect)
            self.accept("f8", showCollisions)
            self.accept("f9", toggleOobe)
            self.accept("f10", explorer)
            self.accept("f11", toggleFullscreen)
            self.accept("f12", toggleWireframe)

    def escape(self):
        if self.fsmGame.state == "Menu":
            sys.exit()
        else:
            self.fsmGame.request("Menu")

APP = Main()
APP.run()
