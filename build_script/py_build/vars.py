import os

TOP_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTPUT_DIR = os.path.join(TOP_DIR, 'output')
BR2_EXTERNAL_DIR = os.path.join(TOP_DIR, 'intellif', 'buildroot')
BUILDROOT_DIR = os.path.join(TOP_DIR, 'buildroot')