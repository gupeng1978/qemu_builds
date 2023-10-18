import py_build 
import json

br2_config = "intellif_qemu_aarch64_virt_defconfig"
platform = "qemu_aarch64_virt"


# 查找buildroot支持的包
ret = py_build.br2_find_packets("opencv")
print(ret)

# 查看已安装的包信息
installed_pkts = py_build.br2_installed_pkts_info(platform)
print(json.dumps(installed_pkts, indent=4))


# 根据配置文件生成构建
# py_build.br2_config_gen(br2_config, platform)
# output_img_dir = py_build.br2_build(platform)
# print(output_img_dir)



