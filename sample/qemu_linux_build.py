import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../tools'))

from br2_build.config import Configure
from br2_build.build import Build

config = (
    Configure("qemu_intellif_defconfig", "qemu_aarch64")
    .app_opencv_resize(enable=True,clean=True,log_level='DEBUG',build_type='Debug') # 编译opencv_resize，clean package, 设置编译参数
    .app_hello_world(enable=True,clean=True)
    .update_config()
)

build = (
        Build(config).
        # linux_clean(). # 重新编译linux源码
        build_all()
)

