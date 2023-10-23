import sys
sys.path.append("../tools/")

from br2_build.config import Configure
from br2_build.build import Build

config = Configure("qemu_intellif_defconfig", "qemu_aarch64").\
        app_opencv_resize(enable = True, clean = True, log_level = 'ERROR').\
        app_hello_world(enable = True, clean = True).\
        update_config()

        
build = Build(config)
build.build_all()

