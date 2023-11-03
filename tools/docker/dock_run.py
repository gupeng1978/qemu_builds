import os
import sys
import subprocess
import argparse

TOP_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOCKER_TOP_DIR = "/home/intellif/qemu_builds"

def run_shell_cmd(cmd : str, env : dict , dir : str ):
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
        print(f"run_shell_cmd: {cmd}")
        out = subprocess.run(cmd, shell=True, check=True, text=True, cwd=dir, env=env, stdout=sys.stdout, stderr=sys.stderr)
    except subprocess.CalledProcessError as e:
        raise ValueError(f'error: run_shell_cmd run {cmd} failed, ret_code = {e.returncode}, dir = {dir}')
    return out


TOP_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOCKER_TOP_DIR = "/home/intellif/qemu_builds"



def get_docker_script_path(script_file):
    """
    Get the path of the script file in the Docker container.

    Args:
        script_file (str): The path of the script file in the host machine.

    Raises:
        ValueError: If the script_file does not exist.

    Returns:
        str: The path of the script file in the Docker container.
    """
    # check script_file valid
    if not os.path.exists(script_file):
        raise ValueError(f"script_file {script_file} not exist")
    
    # 获取script_file相对于TOP_DIR的相对路径
    script_file_path = os.path.abspath(script_file)
    script_file_path = os.path.relpath(script_file_path, TOP_DIR)
    
    # 计算script_file相对于DOCKER_TOP_DIR的相对路径
    docker_script_file_path = os.path.join(DOCKER_TOP_DIR, script_file_path)
    
    print(f"docker_script_file_path = {docker_script_file_path}")
    
    return docker_script_file_path


def run_script(args):
    print(f"run in docker... {args.image}, {args.script}")
    script_in_docker = get_docker_script_path(args.script)
    
    # check docker是否安装
    if run_shell_cmd("docker -v", os.environ, TOP_DIR).returncode != 0:
        raise ValueError(f"docker not install")
    
    # check docker image是否存在
    if run_shell_cmd(f"echo {args.sudo_passwd} | sudo -S docker images | grep {args.image}", os.environ, TOP_DIR).returncode != 0:
        raise ValueError(f"docker image {args.image} not exist")
    
    # chown TOP_DIR to intellif
    if run_shell_cmd(f"echo {args.sudo_passwd} | sudo -S chown -R intellif:intellif {TOP_DIR}", os.environ, TOP_DIR).returncode != 0:
        raise ValueError(f"chown {TOP_DIR} failed")
    
    # 启动镜像，mount TOP_DIR到DOCKER_TOP_DIR，并执行脚本    
    if run_shell_cmd(f"sudo docker run -it --rm -v /etc/localtime:/etc/localtime:ro -v /etc/timezone:/etc/timezone:ro -v {TOP_DIR}:{DOCKER_TOP_DIR} {args.image} python3 {script_in_docker}", os.environ, TOP_DIR).returncode != 0:
        raise ValueError(f"docker run failed")
    
    # chown TOP_DIR to current user
    if run_shell_cmd(f"echo {args.sudo_passwd} | sudo -S chown -R {os.environ['USER']}:{os.environ['USER']} {TOP_DIR}", os.environ, TOP_DIR).returncode != 0:
        raise ValueError(f"chown {TOP_DIR} failed")
    
    pass
    
def upload_ftp():
    pass


if __name__ == '__main__':
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='Run a Python script in a Docker container')
    parser.add_argument('--image', required=True, help='Docker image name')
    parser.add_argument('--script', required=True, help='Python script name')
    parser.add_argument('--sudo_passwd', required=True, help='sudo password')
    args = parser.parse_args()
    
    try:
        run_script(args)
        upload_ftp()
    except Exception as e:
        # 在异常发生时执行额外的操作
        if run_shell_cmd(f"echo {args.sudo_passwd} | sudo -S chown -R {os.environ['USER']}:{os.environ['USER']} {TOP_DIR}", os.environ, TOP_DIR).returncode != 0:
            raise ValueError(f"chown {TOP_DIR} failed")
        sys.exit(1)  
    pass

