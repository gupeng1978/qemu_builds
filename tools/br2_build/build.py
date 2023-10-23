
import os
import multiprocessing
from . import run_shell_cmd, BR2_EXTERNAL_DIR, OUTPUT_DIR
from .config import Configure


CONFIGS_DIR = os.path.join(BR2_EXTERNAL_DIR, 'configs')
MAX_JOBS = str(multiprocessing.cpu_count())


class Build(object):
    def __init__(self, configure : Configure):
        self.configure = configure
        self.br2_packages_clean = configure.br2_packages_clean
        for pkt in self.br2_packages_clean:
            print(f"clean {pkt}")
            run_shell_cmd(f"make O={self.configure.builddir} {pkt}-dirclean", self.configure.env)
        pass
    
    def build_all(self):
        if run_shell_cmd(f"make O={self.configure.builddir} -j{MAX_JOBS}", self.configure.env):
            return os.path.join(self.configure.builddir, 'images')
    
    
    def _clean(self):
        pass    
    