# 24.04, noble-20250127, noble, latest
FROM ubuntu:26.04@sha256:19fcd1bf268f02b60aca3bd30bd8a6d9a11759a430e32921833e65f16d87348a

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get -y update \
    && apt-get -y upgrade \
    git
WORKDIR /root
RUN git clone https://github.com/spack/spack.git
ENV PATH="/root/spack/bin:${PATH}"
RUN apt-get -y install \
    bzip2 \
    python3 \
    unzip \
    xz-utils
RUN spack bootstrap now
