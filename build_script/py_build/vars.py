import os

TOP_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTPUT_DIR = os.path.join(TOP_DIR, 'output')
BR2_EXTERNAL_DIR = os.path.join(TOP_DIR, 'intellif', 'buildroot')
BUILDROOT_DIR = os.path.join(TOP_DIR, 'buildroot')
BUILDROOT_DL_DIR = os.path.join(BUILDROOT_DIR, 'dl')
LINUX_SOURCE_DIR = os.path.join(TOP_DIR, 'intellif', 'source', 'linux')
BUILDROOT_TARBALL_DIR = os.path.join(BR2_EXTERNAL_DIR, 'tarball')
