
import os
import multiprocessing
from . import run_shell_cmd, read_buildroot_config, create_git_repo_tar
from . import BR2_EXTERNAL_DIR, OUTPUT_DIR, LINUX_SOURCE_DIR, BUILDROOT_TARBALL_DIR, BUILDROOT_DL_DIR
from .config import Configure


CONFIGS_DIR = os.path.join(BR2_EXTERNAL_DIR, 'configs')
MAX_JOBS = str(multiprocessing.cpu_count())


class Build(object):
    def __init__(self, configure : Configure):
        self.configure = configure
        self.br2_packages_clean = configure.br2_packages_clean
        for pkt in self.br2_packages_clean:
            print(f"clean {pkt}")
            run_shell_cmd(f"make O={self.configure.builddir} {pkt}-dirclean", self.configure.env)
        pass

    def linux_clean(self):
        if read_buildroot_config(self.configure.configfile, 'BR2_LINUX_KERNEL_CUSTOM_TARBALL_LOCATION') == "file://$(BR2_EXTERNAL_INTELLIF_PATH)/tarball/linux.tar" :

            # 清除buildroot的linux目录缓存tarball
            linux_tarball_cached = os.path.join(BUILDROOT_DL_DIR, 'linux', 'linux.tar')
            if os.path.exists(linux_tarball_cached):
                os.remove(linux_tarball_cached)

            # 清除output目录下的linux目录
            output_full_dir = os.path.join(self.configure.builddir, 'build','linux-custom')
            if os.path.exists(output_full_dir):
                os.system(f"rm -rf {output_full_dir}")

            # 创建linux源码tarball
            create_git_repo_tar(LINUX_SOURCE_DIR, BUILDROOT_TARBALL_DIR)
        return self


    def build_all(self):
        if run_shell_cmd(f"make O={self.configure.builddir} -j{MAX_JOBS}", self.configure.env):
            return os.path.join(self.configure.builddir, 'images')
        return self

    """
    @brief 生成buildroot的build graph
    @param self 类对象
    @return 包含build graph pdf输出文件的目录路径，该路径下有多个输出文件，如：build.hist-build.pdf、build.pie-steps.pdf
            build.hist-name.pdf、build.timeline.pdf、build.pie-packages.pdf、build.hist-duration.pdf
    @note buildroot无法只生成一个整的pdf文件，需要再使用pdftk、pdfunite命令合并为一个整的pdf文件
    """
    def graph_build(self):
        if run_shell_cmd(f"make O={self.configure.builddir} graph-build -j{MAX_JOBS}", self.configure.env):
            return os.path.join(self.configure.builddir, 'graphs/')
        return self

    """
    @brief 生成buildroot的build depends
    @param self 类对象
    @return 生成的graph-depends.pdf文件路径
    """
    def graph_depends(self):
        if run_shell_cmd(f"make O={self.configure.builddir} graph-depends -j{MAX_JOBS}", self.configure.env):
            return os.path.join(self.configure.builddir, 'graphs/graph-depends.pdf')
        return self
