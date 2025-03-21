#!/bin/sh

podman build -t ubuntu . && podman run --rm -it ubuntu /bin/bash
