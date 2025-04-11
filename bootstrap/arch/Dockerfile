FROM archlinux:base-devel-20250302.0.316047@sha256:61b9b05cf6a7a42aa1a32f0b00c92dcfc0b6acf3af2db1b86ab29f6605b21401

RUN pacman -Syu --noconfirm \
    && pacman -S --noconfirm \
    git
WORKDIR /root
RUN git clone https://github.com/spack/spack.git
ENV PATH="/root/spack/bin:${PATH}"
RUN pacman -S --noconfirm \
    python
RUN spack bootstrap now
RUN spack env create -d . \
    && eval `spack env activate --sh -d .` \
    && spack add python@3.9 \
    && spack add python-venv \
    && spack concretize --fresh --deprecated --force
#RUN spack install --deprecated -y --fail-fast
