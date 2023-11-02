
import os
from . import run_shell_cmd, read_buildroot_config, create_git_repo_tar
from . import BR2_EXTERNAL_DIR, OUTPUT_DIR, LINUX_SOURCE_DIR, BUILDROOT_TARBALL_DIR



CONFIGS_DIR = os.path.join(BR2_EXTERNAL_DIR, 'configs')


class Configure(object):
    def __init__(self, defconfig, platform):
        self.defconfig = os.path.join(CONFIGS_DIR, defconfig)
        self.builddir = os.path.join(OUTPUT_DIR, platform)
        self.configfile = os.path.join(self.builddir, '.config')
        self.br2_updated_configs = []
        self.br2_packages_clean = []
        self.env = {"PATH": os.environ["PATH"]}
        run_shell_cmd(f"make O={self.builddir} BR2_EXTERNAL={BR2_EXTERNAL_DIR} {defconfig}", self.env)
    
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
    
    def app_hello_world(self, enable : bool,  clean : bool = True):
        self.br2_updated_configs.append("BR2_PACKAGE_APP_HELLO_WORLD=y" if enable else "BR2_PACKAGE_APP_HELLO_WORLD=n")
        if clean:
            self.br2_packages_clean.append("app_hello_world")
        return self
    
    def ko_hello_world(self, enable : bool,  clean : bool = True):
        self.br2_updated_configs.append("BR2_PACKAGE_KO_HELLO_WORLD=y" if enable else "BR2_PACKAGE_KO_HELLO_WORLD=n")
        if clean:
            self.br2_packages_clean.append("ko_hello_world")
        return self
    
    def sdk_drv(self, enable : bool,  clean : bool = True):
        self.br2_updated_configs.append("BR2_PACKAGE_SDK_DRV=y" if enable else "BR2_PACKAGE_SDK_DRV=n")
        self.br2_updated_configs.append("BR2_PACKAGE_SDK_DRV_KO=y" if enable else "BR2_PACKAGE_SDK_DRV_KO=n")
        if clean:
            self.br2_packages_clean.append("sdk_drv")
            self.br2_packages_clean.append("sdk_drv_ko")
        return self
    
    def update_config(self):
        if self.br2_updated_configs:
            print(f"update config: {self.br2_updated_configs}")
            with open(self.configfile , 'a') as f:
                for config in self.br2_updated_configs:
                    f.write(config + '\n')
            run_shell_cmd(f"make O={self.builddir} olddefconfig", self.env)        
            self.check_config_valid()
            
        # 如果linux.tar包不存在，则创建
        linux_tarball = os.path.join(BUILDROOT_TARBALL_DIR, 'linux.tar')
        if read_buildroot_config(self.configfile, 'BR2_LINUX_KERNEL_CUSTOM_TARBALL_LOCATION') == "file://$(BR2_EXTERNAL_INTELLIF_PATH)/tarball/linux.tar" and not os.path.exists(linux_tarball):
            create_git_repo_tar(LINUX_SOURCE_DIR, BUILDROOT_TARBALL_DIR)            
        return self
    
    def check_config_valid(self):
        """Check if the .config is contains all lines present in the defconfig."""
        configfile = os.path.join(self.builddir, '.config')
        with open(configfile) as configf:
            configlines = configf.readlines()
        configlines = [line.strip() for line in configlines if line.strip().startswith('BR2')]

        with open(self.defconfig) as defconfigf:
            defconfiglines = defconfigf.readlines()
        defconfiglines = [line.strip() for line in defconfiglines if line.strip().startswith('BR2')]
        defconfiglines += self.br2_updated_configs

        # Check that all the defconfig lines are still present
        for defconfigline in defconfiglines:
            if defconfigline not in configlines:                
                raise ValueError(f"defconfig {self.defconfig} is not valid, Missing: {defconfigline.strip()}\n" )


