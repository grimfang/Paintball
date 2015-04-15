from pandac.PandaModules import WindowProperties

def hide_cursor():
    """set the Cursor invisible"""
    props = WindowProperties()
    props.setCursorHidden(True)
    # somehow the window gets undecorated after hiding the cursor
    # so we reset it here to the value we need
    #props.setUndecorated(settings.fullscreen)
    base.win.requestProperties(props)

def show_cursor():
    """set the Cursor visible again"""
    props = WindowProperties()
    props.setCursorHidden(False)
    # set the filename to the mouse cursor
    #x11 = os.path.join("data", "Cursor.x11")
    #win = os.path.join("data", "Cursor.ico")
    #if sys.platform.startswith("linux"):
    #    props.setCursorFilename(x11)
    #else:
    #    props.setCursorFilename(win)
    #props.setUndecorated(settings.fullscreen)
    base.win.requestProperties(props)
