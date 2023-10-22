
import os
import multiprocessing
from . import run_shell_cmd, BR2_EXTERNAL_DIR, OUTPUT_DIR
from .config import Configure


CONFIGS_DIR = os.path.join(BR2_EXTERNAL_DIR, 'configs')
MAX_JOBS = str(multiprocessing.cpu_count())


class Build(object):
    def __init__(self, configure : Configure):
        self.configure = configure
    
    def build_all(self):
        if run_shell_cmd(f"make O={self.configure.builddir} -j{MAX_JOBS}", self.configure.env):
            return os.path.join(self.configure.builddir, 'images')
    