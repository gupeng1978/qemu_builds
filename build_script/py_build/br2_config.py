import os
import sys
import subprocess
import fnmatch
import re
import json

from .vars import TOP_DIR, OUTPUT_DIR,BR2_EXTERNAL_DIR, BUILDROOT_DIR

CONFIGS_DIR = os.path.join(BR2_EXTERNAL_DIR, 'configs')


def br2_config_gen(config_file, output_platform):
    config_full_file = os.path.join(CONFIGS_DIR, config_file)    
    output_full_dir = os.path.join(OUTPUT_DIR, output_platform)
    if not os.path.exists(config_full_file):
        raise ValueError(f"config file {config_full_file} does not exist")

    # Use subprocess to execute the command
    cmd = f"make BR2_EXTERNAL={BR2_EXTERNAL_DIR} O={output_full_dir} {config_file}"
    ret = subprocess.run(cmd, shell=True, check=True, text=True, cwd=BUILDROOT_DIR, stdout=sys.stdout, stderr=sys.stderr)
    print(ret)



def br2_find_packets(pkg_pattern):
    pkgs_dir = os.path.join(BUILDROOT_DIR, "package")    
    result = []
    pkg_pattern = pkg_pattern + "*.mk"
    print(pkgs_dir,pkg_pattern)
    for root, dirs, files in os.walk(pkgs_dir):
        for file in files:
            if fnmatch.fnmatch(file,pkg_pattern):
                pkg_name = os.path.basename(file).split('.')[0]
                pkg_name_upper = str.upper(pkg_name)
                with open(os.path.join(root, file), 'r') as f:
                    for line in f.readlines():
                        match = re.search(f'{pkg_name_upper}_VERSION\s*=\s*([\d.]+)', line)
                        if match:                            
                            result.append({'pkg':pkg_name, 'version':match.group(1)})
                            break
    return result

def br2_installed_pkts_info(output_platform):
    output_full_dir = os.path.join(OUTPUT_DIR, output_platform)

    cmd = f"make O={output_full_dir} show-info"
    try:
        ret = subprocess.check_output(cmd, shell=True, cwd=BUILDROOT_DIR)
        pks_info = json.loads(ret)
        filterd_pkts_info = {} # 过滤host-pkgs
        for key, value in pks_info.items():
            if not key.startswith("host-"):
                filterd_pkts_info[key] = value
        return filterd_pkts_info
        
    except subprocess.CalledProcessError as e:
        print(f'buildroot get installed packets info failed，ret_code: {e.returncode}, output = {e.output}')
    
    return None

