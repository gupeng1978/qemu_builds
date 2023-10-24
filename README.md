# 仓库设计说明
## buildroot原理
[Buildroot原理介绍](docs/从树莓派4构建理解buildroot原理.docx)

## 设计目的
本仓库是借助buildroot的qemu平台构建来验证intellif芯片的SDK构建设计思路，要求:
1. 满足外部客户在公网下方便使用，基于sdk开发包环境灵活修改，快速构建；
2. 满足内部版本快速集成，针对jenkis的集成特点，减少重复构建以及磁盘占用量，支持不同主机分布式构建；
3. 满足内部子模块快速构建需求，各个子模块能独立构建；
4. 满足研发的三方库扩展需求，比如在芯片上能执行基于cmake的 opencv三方库应用开发；

## 设计思路
1. 剥离buildroot相关的配置到intellif/buildroot中，采用BR2_EXTERNAL方式加载芯片packages以及配置，buildroot子仓库灵活升级；
2. 允许local package的源码发布以及编译，支持sdk中packages 源码发布和构建;
3. 提供python3 脚本封装，便于用户使用；
4. SoC构建需求复杂且组合很多，设计上采用基础defconfig配置 + 脚本API方式来解决编译的问题；
5. 支持docker编译，解决不同主机host库的差异以及依赖库安装问题，比如不同host的gcc版本；


## 仓库目录说明
| 一级目录       | 二级目录            | 用途  |
|-------------|-----------------|------------|
| buildroot |  | buildroot子仓库链接，用于构建soc 镜像，支持灵活升级到最新版本 |
| intellif | buildroot | intellif soc芯片的buildroot配置，包括board, configs, package等 |
| intellif | source | intellif soc芯片开源的package, 包括linux， sdk apps, libs |
| tools |  | intellif soc芯片发布的工具 |
| tools | br2_build | intellif soc芯片发布的buildroot编译构建python包 |
| sample | | intellif soc芯片发布的sample代码，包括构建，sdk api sample等 |
| doc | | intellif soc芯片发布的文档等 |


# 如何使用
## 依赖库工具安装
```
udo apt update
sudo apt-get install python-is-python3
sudo apt install qemu qemu-kvm libvirt-daemon libvirt-daemon-system bridge-utils virt-manager
```

## 快速上手

1. 仓库下载，编译sample，启动qemu
```
git clone --recurse-submodules https://github.com/gupeng1978/qemu_builds.git
cd qemu_builds 
python sample/qemu_linux_build.py # 脚本编译
sh output/qemu_aarch64/images/start-qemu.sh
```

2. 进入qemu（以root账号）linux，cd /usr/bin/，执行app开头的sample示例：

## 如何增加package包
### app_hello_world package
该例子演示简单的cmake的源码包构建，不依赖任何三方库。
1. 源码扩展：在intellif/source目录里增加app_hello_world目录以及对应的源码以及CMakeLists.txt；
2. BT2 External package扩展：在intellif/buildroot/package增加app_hello_world配置，其中配置文件见下，使用标准cmake package接入，选择local本地文件；
```
APP_HELLO_WORLD_VERSION = 0.1
APP_HELLO_WORLD_LICENSE = MIT
APP_HELLO_WORLD_SITE = $(TOPDIR)/../intellif/source/app_hello_world
APP_HELLO_WORLD_SITE_METHOD = local
APP_HELLO_WORLD_INSTALL_STAGING = NO
$(eval $(cmake-package))
```
3. Tools脚本编译扩展：在tools/br2_build的config.py增加接口扩展：
```
def app_hello_world(self, enable : bool):
    self.br2_updated_configs.append("BR2_PACKAGE_APP_HELLO_WORLD=y" if enable else "BR2_PACKAGE_APP_HELLO_WORLD=n")
    return self
```
4. 在脚本sample/qemu_linux_build.py中增加app_hello_world配置
5. 执行：qemu下进入/user/bin目录，执行app_hello_world

### app_opencv_resize package
该例子演示依赖opencv库开发，app如何存放图片数据文件，如何传递构建参数。
1. 使用下面的配置修改方法，增加qemu_intellif_defconfig opencv相关的依赖库(目前已经更新支持opencv库)；
2. 源码扩展：在intellif/source目录里增加app_opencv_resize目录以及对应的源码以及CMakeLists.txt, 一般package中的图片等数据install到/usr/share目录中，cmake支持参数CMAKE_BUILD_TYPE,LOG_LEVEL;
3. BT2 External package扩展：
- 在intellif/buildroot/package增加app_opencv_resize配置, 其中需要增加构建控制参数:BR2_PACKAGE_APP_OPENCV_RESIZE_LOG_LEVEL和BR2_PACKAGE_APP_OPENCV_RESIZE_BUILD_TYPE
- 在app_opencv_resize.mk文件中增加build参数传递APP_OPENCV_RESIZE_CONF_OPTS变量控制；
4. Tools脚本编译扩展：在tools/br2_build的config.py增加接口扩展：
```
def app_opencv_resize(self, enable : bool, clean : bool = True, log_level : str = "DEBUG", build_type : str = "Release"):
    self.br2_updated_configs.append("BR2_PACKAGE_APP_OPENCV_RESIZE=y" if enable else "BR2_PACKAGE_APP_OPENCV_RESIZE=n")
    
    # check valid
    if log_level not in ["DEBUG", "INFO", "ERROR"]:
        raise ValueError(f"log_level must be one of DEBUG, INFO, WARN, ERROR")
    if build_type not in ["Debug", "Release"]:
        raise ValueError(f"build_type must be one of Debug, Release")
    
    if enable:
            self.br2_updated_configs.append(f'BR2_PACKAGE_APP_OPENCV_RESIZE_LOG_LEVEL="LOG_LEVEL_{log_level}"')
            self.br2_updated_configs.append(f'BR2_PACKAGE_APP_OPENCV_RESIZE_BUILD_TYPE="{build_type}"')
        
    if clean:
        self.br2_packages_clean.append("app_opencv_resize")
    return self
```
5. 执行：qemu下进入/user/bin目录，执行app_opencv_resize


## 配置以及接口扩展注意事项
1. 用户可以直接修改defconfig配置，但如果需要安装/删除三方库，那么必须通过buildroot的menuconfig配置（自动解决依赖关系），以修改/home/gupeng/github/qemu_builds/intellif/buildroot/configs/qemu_intellif_defconfig 为例来说明：

```
# 1. 配置写入到 buildroot/.config
make BR2_DEFCONFIG=/home/gupeng/github/qemu_builds/intellif/buildroot/configs/qemu_intellif_defconfig  defconfig

# 2. GUI修改配置，自动解决依赖关系，保存到.config
make menuconfig

# 3. .config精简后写回到qemu_intellif_defconfig, 此处可以看到三方库的BR2配置修改；
make BR2_DEFCONFIG=/home/gupeng/github/qemu_builds/intellif/buildroot/configs/qemu_intellif_defconfig savedefconfig

```

2. 通过configure.py增加BR2参数写法务必规范，更新配置后需要检测.config文件配置是否生效，下面几种情况需要注意：
- BR2的参数在buildroot中无法识别的，所有参数必须在config.in中定义；
- BR2的参数依赖关系必须满足，比如app依赖opencv库（多个库），但defconfig中必须打开依赖的package；
- 添加cmake的配置参数,比如-DCMAKE_BUILD_TYPE="Release", 注意添加""（原因是解决make olddefconfig自动增加""，mk配置中会删除“”);


3. 通过BR2_EXTERNAL扩展的packages的依赖关系必须显示指明，对于buildroot而言，任意package没有指明依赖关系,package的构建顺序是不确定的，比如HCP库依赖HAL，MAL库，HAL依赖库依赖linux等；


4. linux内核本地源码构建很特殊，修改脚本务必注意。buildroot的linux.mk文件很复杂，而且内部也有不少package 依赖linux ，移植到外部定制custom_linux.mk文件不可行。linux.mk文件不支持源码build，只能通过TAR包，GIT等方式下载。设计上先打包linux source包(TAR包)，然后buildroot会缓存到dl下载目录，再加压到到build目录下编译，内核代码修改后，如果需要编译，需要显示调用Configure的linux_local(clean = true)接口，删除linux的中间结果。

```
BR2_LINUX_KERNEL=y
BR2_LINUX_KERNEL_CUSTOM_TARBALL=y
BR2_LINUX_KERNEL_CUSTOM_TARBALL_LOCATION="file://$(BR2_EXTERNAL_INTELLIF_PATH)/tarball/linux.tar"
BR2_LINUX_KERNEL_USE_CUSTOM_CONFIG=y
BR2_LINUX_KERNEL_CUSTOM_CONFIG_FILE="$(BR2_EXTERNAL_INTELLIF_PATH)/board/qemu/aarch64-virt/linux.config"
BR2_LINUX_KERNEL_NEEDS_HOST_OPENSSL=y
```


# python接口
1. [python api脚本: config](tools/br2_build/config.py)
2. [python api脚本: build](tools/br2_build/build.py)


