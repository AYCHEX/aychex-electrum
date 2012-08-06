"""
py2app/py2exe build script for Electrum

Usage (Mac OS X):
     sudo python setup.py py2app
     sudo LITECOIN=true python setup.py py2app

"""

import sys, os, shutil, re
from setuptools import setup
from lib.version import ELECTRUM_VERSION as version
from lib.util import print_error
from lib import config

# Build Litecoin app if pass in LITECOIN=true
if os.environ.has_key('LITECOIN'):
    config.setup_litecoin()

name = config.title.replace(" ", "")
mainscript = 'electrum'

if sys.version_info[:3] < (2,6,0):
    print_error("Error: " + name + " requires Python version >= 2.6.0...")
    sys.exit(1)

if sys.platform == 'darwin':
    shutil.copy(mainscript, mainscript + '.py')
    mainscript += '.py'
    extra_options = dict(
        setup_requires=['py2app'],
        app=[mainscript],
        options=dict(py2app=dict(argv_emulation=True,
                                 argv_inject=config.argument,
                                 iconfile='electrum-%s.icns' % config.coin_lower,
                                 resources=["data/background.png", "data/style.css", "data/icons"])),
    )
elif sys.platform == 'win32':
    extra_options = dict(
        setup_requires=['py2exe'],
        app=[mainscript],
    )
else:
    extra_options = dict(
        # Normally unix-like platforms will use "setup.py install"
        # and install the main script as such
        scripts=[mainscript],
    )

setup(
    name = name,
    version = version,
    **extra_options
)

if sys.platform == 'darwin':
    # Remove the copied py file
    os.remove(mainscript)
    resource = "dist/" + name + ".app/Contents/Resources/"

    # Try to locate qt_menu
    # Let's try the port version first!
    if os.path.isdir("/opt/local/lib/Resources/qt_menu.nib"):
      qt_menu_location = "/opt/local/lib/Resources/qt_menu.nib"
    else:
      # No dice? Then let's try the brew version
      qt_menu_location = os.popen("mdfind -name qt_menu.nib | grep Cellar | head").read()
      qt_menu_location = re.sub('\n','', qt_menu_location)

    if(len(qt_menu_location) == 0):
      print "Sorry couldn't find your qt_menu.nib this probably won't work"

    # Need to include a copy of qt_menu.nib
    shutil.copytree(qt_menu_location, resource + "qt_menu.nib")
    # Need to touch qt.conf to avoid loading 2 sets of Qt libraries
    fname = resource + "qt.conf"
    with file(fname, 'a'):
        os.utime(fname, None)
