#!/bin/sh

podman build -t arch . && podman run --rm -it arch /bin/bash
