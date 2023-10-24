
import os
from . import run_shell_cmd, BR2_EXTERNAL_DIR, OUTPUT_DIR



CONFIGS_DIR = os.path.join(BR2_EXTERNAL_DIR, 'configs')


class Configure(object):
    def __init__(self, defconfig, platform):
        self.defconfig = os.path.join(CONFIGS_DIR, defconfig)
        self.builddir = os.path.join(OUTPUT_DIR, platform)
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
    
    def linux(self, enable):
        return self
    
    def update_config(self):
        if self.br2_updated_configs:
            print(f"update config: {self.br2_updated_configs}")
            with open(os.path.join(self.builddir, '.config'), 'a') as f:
                for config in self.br2_updated_configs:
                    f.write(config + '\n')
        run_shell_cmd(f"make O={self.builddir} olddefconfig", self.env)        
        self.check_config_valid()
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