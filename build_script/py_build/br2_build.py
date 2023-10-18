import os
import subprocess
import multiprocessing
from .vars import TOP_DIR, OUTPUT_DIR,BR2_EXTERNAL_DIR, BUILDROOT_DIR


MAX_JOBS = str(multiprocessing.cpu_count())


def br2_build(output_platform):
    output_full_dir = os.path.join(OUTPUT_DIR, output_platform)
    output_config_file = os.path.join(output_full_dir, ".config")
    if not os.path.exists(output_config_file):
        raise ValueError(f"config file {output_config_file} does not exist")

    # Use subprocess to execute the command
    cmd = f"make O={output_full_dir} -j{MAX_JOBS}"
    try:
        ret = subprocess.check_output(cmd, shell=True, cwd=BUILDROOT_DIR)
        return os.path.join(output_full_dir, 'images')
    except subprocess.CalledProcessError as e:
        print(f'buildroot make failed，ret_code: {e.returncode}, output = {e.output}')
    
    return None

