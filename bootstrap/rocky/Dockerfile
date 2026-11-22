FROM rockylinux:9.9.20261112@sha256:03303863808e9cd79f0c58c833db3e5f9cde9f2abe16804a267b05dc54af86e4

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
