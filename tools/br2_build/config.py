
import os
from . import run_shell_cmd, BR2_EXTERNAL_DIR, OUTPUT_DIR



CONFIGS_DIR = os.path.join(BR2_EXTERNAL_DIR, 'configs')


class Configure(object):
    def __init__(self, defconfig, platform):
        self.defconfig = os.path.join(CONFIGS_DIR, defconfig)
        self.builddir = os.path.join(OUTPUT_DIR, platform)
        self.br2_updated_configs = []
        self.env = {"PATH": os.environ["PATH"]}
        run_shell_cmd(f"make O={self.builddir} BR2_EXTERNAL={BR2_EXTERNAL_DIR} {defconfig}", self.env)
    
    def app_opencv_demo_0(self, enable : bool):
        self.br2_updated_configs.append("BR2_PACKAGE_APP_OPENCV_DEMO_0=y" if enable else "BR2_PACKAGE_APP_OPENCV_DEMO_0=n")
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
        return self
