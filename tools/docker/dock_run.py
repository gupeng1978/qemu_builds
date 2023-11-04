import os
import sys
import subprocess
import argparse
import tempfile
import tarfile

from datetime import datetime
from ftplib import FTP, error_perm
TOP_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOCKER_TOP_DIR = "/home/intellif/qemu_builds"
OUTPUT_DIR = os.path.join(TOP_DIR, 'output')
script_start_time = None
script_end_time = None

BT_FTP = { 'url': "192.168.14.107",
        'user': "intellif_build",
        'passwd': "123456",
        'top_dir': 'relay_build',
}    


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



def get_script_build_info(directory = OUTPUT_DIR, check_time = False):
    build_info = {'start': script_start_time.strftime("%Y-%m-%d %H:%M:%S"), 
                  'end': script_end_time.strftime("%Y-%m-%d %H:%M:%S"), 'build_dirs': []}
    
    for root, dirs, files in os.walk(directory):
        if 'docker' in dirs:
            docker_relpath = os.path.relpath(os.path.join(root, 'docker'), OUTPUT_DIR)
            # 获取docker_relpath目录下的.config文件
            config_file = os.path.join(root, 'docker', '.config')
            if os.path.exists(config_file):
                if check_time:
                    mtime = os.path.getmtime(config_file)
                    last_modified_date = datetime.fromtimestamp(mtime)
                    if script_start_time <= last_modified_date <= script_end_time:
                        build_info['build_dirs'].append(docker_relpath)
                else:
                    build_info['build_dirs'].append(docker_relpath)
    # print(f"build_dirs = {build_info['build_dirs']}")    
    return build_info
    

def upload_ftp(ftp_dir):
    build_info = get_script_build_info(check_time=False)
    if build_info.get('build_dirs') is None:
        return
    
    # for build_path in build_info['build_dirs']:
    #     print(build_path)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # 临时目录下创建build_info.txt
        build_info_file = os.path.join(temp_dir, 'build_info.txt')
        with open(build_info_file, 'w') as f:
            f.write(str(build_info))
        pass
    
        # 遍历build_info['build_dirs']，将目录下所有文件夹压缩为tar.gz文件，保存到临时目录            
        tar_cmd = f"tar -czvf {os.path.join(temp_dir, 'output.tar.gz')} "
        for build_path in build_info['build_dirs']:
            tar_cmd += f"{build_path}"
            pass
        
        if run_shell_cmd(tar_cmd, os.environ, OUTPUT_DIR).returncode != 0:
            raise ValueError(f"tar {build_info['build_dirs']} failed")
        
        
        # 上传到ftp服务器
        uploader = FTPUploader(BT_FTP)
        try:
            uploader.connect()
            uploader.create_or_clear_directory(ftp_dir)
             # 遍历临时目录下所有文件，上传到ftp服务器
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    local_path = os.path.join(root, file)
                    remote_name = os.path.relpath(local_path, temp_dir)
                    uploader.upload_file(local_path, remote_name)
                    
        except (error_perm, Exception) as e:
            print(f"An error occurred in upload_ftp: {e}")
        finally:
            uploader.quit()
            
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run a Python script in a Docker container')
    parser.add_argument('--image', required=True, help='Docker image name')
    parser.add_argument('--script', required=True, help='Python script name')
    parser.add_argument('--sudo_passwd', required=True, help='sudo password')
    parser.add_argument('--ftp_upload', required=False, help='build ftp upload dir')
    parser.add_argument('--with_relay', required=False, help='build with relay from ftp')
    parser.add_argument('--pre_dl', required=False, help='build with bt2 dl cache')
    args = parser.parse_args()
    
    try:
        script_start_time = datetime.now()
        run_script(args)
        script_end_time = datetime.now()
        upload_ftp(args.ftp_upload)
    except Exception as e:
        # 在异常发生时执行额外的操作
        print(f"An error occurred: {e}")
        if run_shell_cmd(f"echo {args.sudo_passwd} | sudo -S chown -R {os.environ['USER']}:{os.environ['USER']} {TOP_DIR}", os.environ, TOP_DIR).returncode != 0:
            raise ValueError(f"chown {TOP_DIR} failed")
        sys.exit(1)  
    pass

