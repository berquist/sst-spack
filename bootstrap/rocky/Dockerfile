FROM rockylinux:9.3.20231119@sha256:d7be1c094cc5845ee815d4632fe377514ee6ebcf8efaed6892889657e5ddaaa6

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
