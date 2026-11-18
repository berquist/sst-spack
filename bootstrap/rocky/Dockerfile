FROM rockylinux:10.3.20261112@sha256:48fbd5632d0593a347f3a36b30ae857b3a4a66862a013be9d2ce47d1eb94d61c

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
