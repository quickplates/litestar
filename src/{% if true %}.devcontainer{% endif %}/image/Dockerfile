# Using one of the offical dev container images as base
# Going with Ubuntu, because it has glibc, which some tools might need
# It also has git, zsh and a bunch of other stuff preinstalled
# Also, it includes a non-root 'vscode' user with sudo access
# The version is pinned to ensure reproducibility
FROM mcr.microsoft.com/devcontainers/base:1.2.3-ubuntu-24.04

ENV REMOTE_USER=vscode

# Setup script
COPY setup.sh /tmp/setup.sh

RUN /tmp/setup.sh && \
    rm /tmp/setup.sh

# Lifecycle hooks
COPY hooks/ /hooks/
