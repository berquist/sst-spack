#!/bin/sh

podman build -t rocky . && podman run --rm -it rocky /bin/bash
