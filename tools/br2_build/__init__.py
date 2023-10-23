import os
import subprocess
import sys

TOP_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTPUT_DIR = os.path.join(TOP_DIR, 'output')
BR2_EXTERNAL_DIR = os.path.join(TOP_DIR, 'intellif', 'buildroot')
BUILDROOT_DIR = os.path.join(TOP_DIR, 'buildroot')
BUILDROOT_DL_DIR = os.path.join(BUILDROOT_DIR, 'dl')
LINUX_SOURCE_DIR = os.path.join(TOP_DIR, 'intellif', 'source', 'linux')
BUILDROOT_TARBALL_DIR = os.path.join(BR2_EXTERNAL_DIR, 'tarball')


if os.path.basename(TOP_DIR).split('.')[0] != "qemu_builds":
    raise ValueError(f"TOP_DIR {TOP_DIR} is Set incorrectly")



def run_shell_cmd(cmd : str, env : dict, dir : str = BUILDROOT_DIR):    
    try:
        out = subprocess.run(cmd, shell=True, check=True, text=True, cwd=BUILDROOT_DIR, env=env, stdout=sys.stdout, stderr=sys.stderr)
    except subprocess.CalledProcessError as e:        
        raise ValueError(f'error: run_shell_cmd run {cmd} failed, ret_code = {e.returncode}')
        
