import subprocess
import os
import sys

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
    try:
        tar_file = os.path.join(output_path, f'{repo_name}.tar')
        cmd = f"tar -cvf {tar_file} --exclude=./.git  {repo_name}"
        ret = subprocess.run(cmd, shell=True, check=True, text=True, cwd=os.path.join(repo_path,".."), stdout=sys.stdout, stderr=sys.stderr)              
        return tar_file
    except Exception as e:
        raise Exception(f'Error creating archive: {e}')

