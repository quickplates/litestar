#!/usr/bin/env bash

_shell="$1"
_build="$2"
_cache="$3"

if [[ -z ${_shell} ]]; then
	echo "You need to specify the name of the shell to build"
	exit 1
fi

if [[ -z ${_build} ]]; then
	echo "You need to specify the name of the build directory"
	exit 2
fi

if [[ -z ${_cache} ]]; then
	echo "You need to specify the name of the cache directory"
	exit 3
fi

# Import cached store if available
if [[ -f "${_cache}/archive.nar" ]]; then
	nix-store --import <"${_cache}/archive.nar"
fi

# We need to create necessary directories first
mkdir --parents "${_build}/closure/"

# Save system to variable so we can reuse it easily
_system=$(nix eval --impure --raw --expr 'builtins.currentSystem')

# This will build the shell and all its dependencies
nix build --no-link "path:./#devShells.${_system}.${_shell}"

# Save all paths needed for shell to a file
nix path-info --quiet --quiet --quiet --quiet --quiet --recursive "path:./#devShells.${_system}.${_shell}" >"${_build}/paths"

# Copy all paths to a separate directory
# shellcheck disable=SC2046
cp --recursive $(cat "${_build}/paths" || true) "${_build}/closure/"

# Generate activation script for shell and copy it
nix print-dev-env "path:./#devShells.${_system}.${_shell}" >"${_build}/activate"

# Save all paths needed for shell to cache
# shellcheck disable=SC2046
nix-store --export $(cat "${_build}/paths" || true) >"${_cache}/archive.nar"
