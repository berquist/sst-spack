# 24.04, noble-20250127, noble, latest
FROM ubuntu:26.04@sha256:9559ceb7c21e528e233e8dff26a0fb2682f4094cce06176eeb075d87a22b31de

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
