import os
import subprocess
import sys
import re


TOP_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTPUT_DIR = os.path.join(TOP_DIR, 'output')
BR2_EXTERNAL_DIR = os.path.join(TOP_DIR, 'intellif', 'buildroot')
BUILDROOT_DIR = os.path.join(TOP_DIR, 'buildroot')
BUILDROOT_DL_DIR = os.path.join(BUILDROOT_DIR, 'dl')
LINUX_SOURCE_DIR = os.path.join(TOP_DIR, 'intellif', 'source', 'linux')
BUILDROOT_TARBALL_DIR = os.path.join(BR2_EXTERNAL_DIR, 'tarball')


if os.path.basename(TOP_DIR).split('.')[0] != "qemu_builds":
    raise ValueError(f"TOP_DIR {TOP_DIR} is Set incorrectly")

def run_shell_cmd(cmd : str, env : dict = {"PATH": os.environ["PATH"]}, dir : str = BUILDROOT_DIR):
    """
    Runs a shell command with the specified environment variables and working directory.

    Args:
        cmd (str): The shell command to run.
        env (dict, optional): The environment variables to use when running the command. Defaults to {"PATH": os.environ["PATH"]}.
        dir (str, optional): The working directory to use when running the command. Defaults to BUILDROOT_DIR.

    Raises:
        ValueError: If the command fails to run.

    Returns:
        subprocess.CompletedProcess: The result of running the command.
    """
    try:
        out = subprocess.run(cmd, shell=True, check=True, text=True, cwd=dir, env=env, stdout=sys.stdout, stderr=sys.stderr)
    except subprocess.CalledProcessError as e:
        raise ValueError(f'error: run_shell_cmd run {cmd} failed, ret_code = {e.returncode}, dir = {dir}')
    return out



def read_buildroot_config(config_path, key):
    """
    Reads the Buildroot .config file and returns the value of the specified key.

    Parameters:
    config_path (str): Path to the .config file.
    key (str): The key to look for, e.g., "BR2_TOOLCHAIN".

    Returns:
    str or None: The value of the specified key, or None if the key is not set.
    """
    try:
        with open(config_path, 'r') as file:
            for line in file:
                # Split each line on the equals sign to separate the key from the value
                parts = line.strip().split('=')
                # Check if the first part matches the specified key
                if parts[0] == key:
                    # If the key is found, return the value
                    return parts[1].strip('\"')
    except FileNotFoundError:
        print(f"Error: {config_path} not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    # If the function reaches this point, the key was not found in the file
    return None


def create_git_repo_tar(repo_path, output_path):
    """
    Creates a tar archive of the git repository at the specified path.

    Args:
        repo_path (str): The path to the git repository.
        output_path (str): The path to the directory where the archive will be saved.

    Returns:
        str: The path to the compressed tar archive.
    """
    repo_name = os.path.basename(repo_path).split('.')[0]
    tar_file = os.path.join(output_path, f'{repo_name}.tar')
    run_shell_cmd(cmd = f"tar -cvf {tar_file} --exclude=./.git  {repo_name}", dir = os.path.join(repo_path,".."));
    return tar_file



def get_env_in_docker():
    """
    Returns True if the current environment is running inside a Docker container, False otherwise.
    """
    try:
        with open('/proc/1/cgroup', 'rt') as ifh:
            return 'docker' in ifh.read()
    except Exception:
        return False

def get_buildroot_packages(package_pattern):
    """
    Get the buildroot packages and version information that match the given package pattern.

    Args:
        package_pattern (str): The package pattern to match.

    Returns:
        dict: A dictionary containing the buildroot packages and their version information that match the given package pattern.
    """
    package_dir = os.path.join(BUILDROOT_DIR, "package")
    # 以package_pattern，后接0个或者多个数字，以.mk结尾
    reg_pattern = package_pattern + r'\d*\.mk$'
    # package名
    # _VERSION
    # 0个或多个空格、tab
    # =
    # package版本
    version_pattern = '(.+)_VERSION[ \t]*=(.+)'
    pack_dict = {}

    for root, dirs, files in os.walk(package_dir):
        for file in files:
            if re.match(reg_pattern, file):
                file = os.path.join(root, file)
                with open(file, 'r') as f:
                    for i, line in enumerate(f):
                        match = re.search(version_pattern, line)
                        if(match):
                            pack_dict[match.group(1).lower()] = match.group(2).strip()
                            break
    return pack_dict
