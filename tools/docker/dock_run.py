import os
import sys
import subprocess
import argparse
from datetime import datetime
from ftplib import FTP, error_perm
TOP_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOCKER_TOP_DIR = "/home/intellif/qemu_builds"
OUTPUT_DIR = os.path.join(TOP_DIR, 'output')



    

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

script_start_time = None
script_end_time = None

def get_script_build_platform(directory = OUTPUT_DIR):
    modified_config_files = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == '.config':
                file_path = os.path.join(root, file)
                mtime = os.path.getmtime(file_path)
                last_modified_date = datetime.fromtimestamp(mtime)
                if script_start_time <= last_modified_date <= script_end_time:
                    modified_config_files.append(file_path)
        pass
    
    print(f"modified_config_files = {modified_config_files}")    
    
    #check file 包括目录docker
    for file in modified_config_files:
        if file.find('docker') == -1:
            raise ValueError(f"docker build failed, no need upload ftp")
    pass



class FTPUploader:
    def __init__(self, config):
        self.config = config
        self.ftp = FTP()

    def connect(self):
        self.ftp.connect(self.config['url'], 21)
        self.ftp.login(self.config['user'], self.config['passwd'])
        self.ftp.set_pasv(False)
        self.ftp.cwd(self.config['top_dir'])

    def create_or_clear_directory(self, directory):
        if directory not in self.ftp.nlst():
            self.ftp.mkd(directory)
        self.ftp.cwd(directory)
        for file in self.ftp.nlst():
            self.ftp.delete(file)

    def upload_file(self, local_path, remote_name):
        with open(local_path, 'rb') as file:
            self.ftp.storbinary(f'STOR {remote_name}', file)

    def quit(self):
        self.ftp.quit()

BT_FTP = { 'url': "192.168.14.107",
        'user': "intellif_build",
        'passwd': "123456",
        'top_dir': 'relay_build',
}    

def upload_ftp(ftp_dir):
    uploader = FTPUploader(BT_FTP)
    try:
        uploader.connect()
        uploader.create_or_clear_directory(ftp_dir)
        uploader.upload_file('/home/gupeng/github/qemu_builds/tools/docker/Dockerfile', 'Dockerfile')
    except (error_perm, Exception) as e:
        print(f"An error occurred: {e}")
    finally:
        uploader.quit()


# def upload_ftp(ftp_dir):
#     # get_script_build_platform()
    
    
#     # 连接到ftp服务器
#     ftp = FTP()
#     ftp.connect(BT_FTP['url'], 21)
#     ftp.login(BT_FTP['user'], BT_FTP['passwd'])
#     ftp.set_pasv(False)
#     ftp.cwd(BT_FTP['top_dir'])
    
    
#     #创建目录，如果目录存在则清空目录内容
#     # check ftp_dir是否存在
#     if ftp_dir not in ftp.nlst():
#         ftp.mkd(ftp_dir)
#     ftp.cwd(ftp_dir)
#     for file in ftp.nlst():
#         ftp.delete(file)
    
    
#     # 上传文件/home/gupeng/github/qemu_builds/tools/docker/Dockerfile到ftp服务器
#     ftp.storbinary('STOR Dockerfile', open('/home/gupeng/github/qemu_builds/tools/docker/Dockerfile', 'rb'))
    
#     ftp.quit()    
#     pass


if __name__ == '__main__':
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='Run a Python script in a Docker container')
    parser.add_argument('--image', required=True, help='Docker image name')
    parser.add_argument('--script', required=True, help='Python script name')
    parser.add_argument('--sudo_passwd', required=True, help='sudo password')
    parser.add_argument('--ftp', required=False, help='build ftp upload dir')
    args = parser.parse_args()
    
    try:
        script_start_time = datetime.now()
        # run_script(args)
        script_end_time = datetime.now()
        upload_ftp(args.ftp)
    except Exception as e:
        # 在异常发生时执行额外的操作
        print(f"An error occurred: {e}")
        if run_shell_cmd(f"echo {args.sudo_passwd} | sudo -S chown -R {os.environ['USER']}:{os.environ['USER']} {TOP_DIR}", os.environ, TOP_DIR).returncode != 0:
            raise ValueError(f"chown {TOP_DIR} failed")
        sys.exit(1)  
    pass

