import os
import sys
import subprocess
import multiprocessing
from .vars import TOP_DIR, OUTPUT_DIR,BR2_EXTERNAL_DIR, BUILDROOT_DIR, BUILDROOT_TARBALL_DIR, BUILDROOT_DL_DIR,LINUX_SOURCE_DIR
from .tools import create_git_repo_tar

MAX_JOBS = str(multiprocessing.cpu_count())


def br2_build(output_platform):
    output_full_dir = os.path.join(OUTPUT_DIR, output_platform)
    output_config_file = os.path.join(output_full_dir, ".config")
    if not os.path.exists(output_config_file):
        raise ValueError(f"config file {output_config_file} does not exist")

    # Use subprocess to execute the command
    cmd = f"make O={output_full_dir} -j{MAX_JOBS}"
    try:
        ret = subprocess.run(cmd, shell=True, check=True, text=True, cwd=BUILDROOT_DIR, stdout=sys.stdout, stderr=sys.stderr)
        return os.path.join(output_full_dir, 'images')
    except subprocess.CalledProcessError as e:
        print(f'buildroot make failed, ret_code: {e.returncode}')
    return None


def br2_linux_kernel_prebuild(output_platform):
    # 清除buildroot的linux目录缓存tarball
    linux_tarball_cached = os.path.join(BUILDROOT_DL_DIR, 'linux', 'linux.tar')    
    if os.path.exists(linux_tarball_cached):
        os.remove(linux_tarball_cached)
        
    # 清除output目录下的linux目录
    output_full_dir = os.path.join(OUTPUT_DIR, output_platform, 'build','linux-custom')
    if os.path.exists(output_full_dir):
        os.system(f"rm -rf {output_full_dir}")
    
    # 创建linux源码tarball
    tar = create_git_repo_tar(LINUX_SOURCE_DIR, BUILDROOT_TARBALL_DIR)
    print(tar)
    pass


def br2_package_clean(output_platform, pkt):
    output_full_dir = os.path.join(OUTPUT_DIR, output_platform)    
    # Use subprocess to execute the command
    cmd = f"make O={output_full_dir} {pkt}-dirclean"
    try:
        ret = subprocess.run(cmd, shell=True, check=True, text=True, cwd=BUILDROOT_DIR, stdout=sys.stdout, stderr=sys.stderr)
    except subprocess.CalledProcessError as e:
        print(f'buildroot clean pkt {pkt} failed, ret_code: {e.returncode}')

    
    
