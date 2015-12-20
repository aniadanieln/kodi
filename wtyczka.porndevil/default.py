import xbmcaddon
import xbmcplugin

__plugin__ = 'PornDevil'
__author__ = 'noVak'
__svn_url__ = 'xxx'
__credits__ = 'noVak'
__version__ = '1.0.1'

addon = xbmcaddon.Addon(id='wtyczka.porndevil')
rootDir = addon.getAddonInfo('path')

xbmcplugin.setContent(int(sys.argv[1]), 'movies')
xbmc.executebuiltin('Container.SetViewMode(500)') # "Thumbnail" view


if rootDir[-1] == ';':
    rootDir = rootDir[0:-1]

class Main:
    def __init__(self):
        self.pDialog = None
        self.curr_file = ''
        self.run()

    def run(self):
        import videodevil
        videodevil.Main()

win = Main()
