# 24.04, noble-20250127, noble, latest
FROM ubuntu:noble-20250415.1@sha256:6015f66923d7afbc53558d7ccffd325d43b4e249f41a6e93eef074c9505d2233

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
