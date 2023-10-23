# 设计目的
本仓库是借助buildroot的qemu平台构建来验证intellif芯片的SDK构建设计思路，核心要求:
1. 满足外部客户在公网下方便使用，基于sdk开发包环境灵活修改，快速构建；
2. 满足内部版本快速集成，针对jenkis的集成特点，减少重复构建以及磁盘占用量，支持不同主机分布式构建；
3. 满足内部子模块快速构建需求，各个子模块能独立构建；
4. 满足研发的三方库扩展需求，比如在芯片上能执行基于cmake的 opencv三方库应用开发；


# 设计思路
1. 剥离buildroot相关的配置到intellif/buildroot中，采用BR2_EXTERNAL方式加载芯片packages以及配置，buildroot子仓库灵活升级；
2. 采用local子模块package方式，解决buildroot多次构建重复下载package源码问题, 支持package单独编译；
3. 采用python3 脚本封装，便于用户使用；
4. 支持docker编译，解决不同主机host库的差异以及依赖库安装问题，比如不同host的gcc版本；



# python接口设计
1. 支持分级别编译； 基础镜像 + docker打包；

import intellif_soc

build_envs.toolchain_download()
build_envs.source_checkout()
base_img.builds(...)


python包：
aiohttp


linux配置文件放在用户intellif自己的目录下，通过BR2_LINUX_KERNEL_CUSTOM_CONFIG_FILE配置，比linux内核自带BR2_LINUX_KERNEL_DEFCONFIG的配置文件更加灵活。
同理，对于设备树也是如此。

buildroot的linux.mk文件很复杂，而且内部也有不少package 依赖linux ，移植到外部定制custom_linux.mk文件不可行。

linux.mk文件不支持源码build，只能通过TAR包，GIT等方式下载。
对于自定义的package，是支持local源码编译的，参考app_opencv_demo_o.mk写法；
app_opencv_demo_0的编译，需要删除build再编译。
步骤：
1. Syncing from source dir：拷贝到build目录
2. Configuring: 调用cmake生成makefile
3. Building
4. Installing to target

make O=/home/gupeng/github/qemu_builds/output/qemu_aarch64_linux_toolchains app_opencv_demo_0-rebuild, 重新编译单个pkg；
make O=/home/gupeng/github/qemu_builds/output/qemu_aarch64_linux_toolchains app_opencv_demo_0-dirclean


在 config.in 文件中添加 depends on BR2_PACKAGE_OPENCV4 是为了确保配置阶段的依赖关系，而在 *.mk 文件中添加 APP_OPENCV_DEMO_0_DEPENDENCIES = opencv4 是为了确保构建阶段的依赖关系。这两个步骤通常都是必需的，以确保 APP_OPENCV_DEMO_0 仅在 opencv4 可用时才被构建

必须使用menuconfig解决配置依赖关系。


增加Configure异常检测机制；
1. 如果写错配置名称，那么会检测到错误；
2. 如果配置中库依赖关系不满足，那么会检测到错误, 比如BR2_PACKAGE_APP_OPENCV_DEMO_0依赖BR2_PACKAGE_OPENCV4_LIB_IMGPROC库，如果未打开依赖库，那么也会报错；