# 24.04, noble-20250127, noble, latest
FROM ubuntu:26.04@sha256:6a06111c3b0a8600feadb270aec771dc239bf407b25625f93f44ab00e11f4d3c

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
