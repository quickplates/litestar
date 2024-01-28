#!/usr/bin/env bash

# Create shell history cache files if they don't exist for some reason
touch /persist/shellhistory/.bash_history
touch /persist/shellhistory/.zsh_history

# Use GitHub token secret if it exists
if [[ -s /secrets/.ghtoken && -r /secrets/.ghtoken ]]; then
	token="$(cat /secrets/.ghtoken)"
	confighome="${XDG_CONFIG_HOME:-${HOME}/.config/}"

	# Add GitHub token to Nix config
	configfile="${confighome}/nix/nix.conf"
	tmpfile="$(mktemp)"

	mkdir -p "$(dirname "${configfile}")"
	touch "${configfile}"

	if grep -q extra-access-tokens "${configfile}"; then
		sed "s|extra-access-tokens.*|extra-access-tokens = github.com=${token}|" "${configfile}" >"${tmpfile}"
		cat "${tmpfile}" >"${configfile}"
		rm "${tmpfile}"
	else
		echo "extra-access-tokens = github.com=${token}" >>"${configfile}"
	fi
fi
