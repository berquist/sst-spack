#!/bin/sh

name=rocky
podman build --no-cache -t ${name} . \
    && podman run --rm -it ${name} /bin/bash
