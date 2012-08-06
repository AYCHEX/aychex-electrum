import os
import platform
import sys
import config

def print_error(*args):
    for item in args:
      sys.stderr.write(str(item))

    sys.stderr.write("\n")
    sys.stderr.flush()

def appdata_dir():
    if platform.system() == "Windows":
        return os.path.join(os.environ["APPDATA"], config.wallet_dir)
    elif platform.system() == "Linux":
        return os.path.join(sys.prefix, "share", config.wallet_dir.lower())
    elif (platform.system() == "Darwin" or
          platform.system() == "DragonFly"):
        return "/Library/Application Support/%s" % config.wallet_dir
    else:
        raise Exception("Unknown system")

def get_resource_path(*args):
    return os.path.join(".", *args)

