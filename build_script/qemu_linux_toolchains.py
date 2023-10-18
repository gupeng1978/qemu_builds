import py_build 
import json

br2_config = "intellif_qemu_aarch64_virt_toolchain_defconfig"
platform = "qemu_aarch64_linux_toolchains"


# 根据配置文件生成构建
py_build.br2_config_gen(br2_config, platform)
# output_img_dir = py_build.br2_build(platform)
# print(output_img_dir)
