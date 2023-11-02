FROM ubuntu:20.04

LABEL version="0.1"
LABEL author="intellif"
LABEL description="Buildroot container for intellif edge10 soc"

# Setup environment
ENV DEBIAN_FRONTEND noninteractive

# The container has no package lists, so need to update first
RUN dpkg --add-architecture i386 && \
    apt-get -o APT::Retries=3 update -y
RUN apt-get -o APT::Retries=3 install -y --no-install-recommends \
        bc \
        build-essential \
        bzr \
        ca-certificates \
        cmake \
        cpio \
        cvs \
        file \
        g++-multilib \
        git \
        libc6:i386 \
        libncurses5-dev \
        locales \
        mercurial \
        openssh-server \
        python3 \
        python3-flake8 \
        python3-magic \
        python3-nose2 \
        python3-pexpect \
        python3-pytest \
        qemu-system-arm \
        qemu-system-misc \
        qemu-system-x86 \
        rsync \
        shellcheck \
        subversion \
        unzip \
        wget \
        && \
    apt-get -y autoremove && \
    apt-get -y clean

# To be able to generate a toolchain with locales, enable one UTF-8 locale
RUN sed -i 's/# \(en_US.UTF-8\)/\1/' /etc/locale.gen && \
    /usr/sbin/locale-gen

RUN useradd -ms /bin/bash intellif && \
    chown -R intellif:intellif /home/intellif

USER intellif
WORKDIR /home/intellif
ENV HOME /home/intellif
ENV LC_ALL en_US.UTF-8
