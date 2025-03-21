FROM rockylinux:9.3.20231119

RUN dnf -y upgrade \
    && dnf -y install \
    git
WORKDIR /root
RUN git clone https://github.com/spack/spack.git
ENV PATH="/root/spack/bin:${PATH}"
RUN dnf -y install \
    bzip2 \
    patch \
    unzip \
    xz
RUN spack bootstrap now
