import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../tools'))

from br2_build import get_buildroot_packages

print(get_buildroot_packages('opencv'))
print(get_buildroot_packages('opencv3'))
print(get_buildroot_packages('opencv4'))

print(get_buildroot_packages('sqlite'))
print(get_buildroot_packages('pkg-kconfig'))
print(get_buildroot_packages('live555'))
print(get_buildroot_packages('uclibc'))
print(get_buildroot_packages('glibc'))
print(get_buildroot_packages('cmake'))
print(get_buildroot_packages('make'))
print(get_buildroot_packages('meson'))
print(get_buildroot_packages('bison'))

print(get_buildroot_packages('lvm2'))
print(get_buildroot_packages('libpfm4'))
print(get_buildroot_packages('libgit2'))
print(get_buildroot_packages('lv'))

print(get_buildroot_packages('snort'))
print(get_buildroot_packages('snort3'))

print(get_buildroot_packages('libgtk'))
print(get_buildroot_packages('libgtk3'))

print(get_buildroot_packages('s6'))
print(get_buildroot_packages('s'))

print(get_buildroot_packages('iperf'))
print(get_buildroot_packages('x'))
print(get_buildroot_packages('python-urllib'))

print(get_buildroot_packages('pcre'))
print(get_buildroot_packages('pcre2'))

print(get_buildroot_packages('libss'))
print(get_buildroot_packages('libss7'))
print(get_buildroot_packages('libssh'))
print(get_buildroot_packages('libssh2'))

print(get_buildroot_packages('modsecurity'))


print(get_buildroot_packages('libsigc'))
print(get_buildroot_packages('libsigc2'))

print(get_buildroot_packages('python-requests'))

print(get_buildroot_packages('zlib'))
print(get_buildroot_packages('libzlib'))

print(get_buildroot_packages('libfuse'))
print(get_buildroot_packages('libfuse3'))

print(get_buildroot_packages('gnupg'))
print(get_buildroot_packages('gnupg2'))

print(get_buildroot_packages('tinyxml'))
print(get_buildroot_packages('tinyxml2'))

print(get_buildroot_packages('qt'))

print(get_buildroot_packages('jack'))
