#!/usr/bin/env bash

REMOTE_USER="${REMOTE_USER:?}"
REMOTE_USER_PASSWD="$(getent passwd "${REMOTE_USER}")"
REMOTE_USER_HOME="$(echo "${REMOTE_USER_PASSWD}" | cut -d: -f6)"

# Setup default shell
chsh -s /usr/bin/zsh "${REMOTE_USER}"

# Setup direnv
cat <<EOF >>"${REMOTE_USER_HOME}/.bashrc"
eval "\$(direnv hook bash)"
EOF

cat <<EOF >>"${REMOTE_USER_HOME}/.zshrc"
eval "\$(direnv hook zsh)"
EOF

# Setup starship
cat <<EOF >>"${REMOTE_USER_HOME}/.bashrc"
eval "\$(starship init bash)"
EOF

cat <<EOF >>"${REMOTE_USER_HOME}/.zshrc"
eval "\$(starship init zsh)"
EOF

# Setup secrets directory
mkdir -p /secrets/

chown -R "${REMOTE_USER}:" /secrets/

# Setup shell history cache
mkdir -p /persist/shellhistory/

touch /persist/shellhistory/.bash_history
touch /persist/shellhistory/.zsh_history

chown -R "${REMOTE_USER}:" /persist/shellhistory/

cat <<EOF >>"${REMOTE_USER_HOME}/.bashrc"
export HISTFILE=/persist/shellhistory/.bash_history
EOF

cat <<EOF >>"${REMOTE_USER_HOME}/.zshrc"
export HISTFILE=/persist/shellhistory/.zsh_history
EOF

# Setup trunk cache
mkdir -p /cache/trunk/

chown -R "${REMOTE_USER}:" /cache/trunk/

cat <<EOF >>"${REMOTE_USER_HOME}/.bashrc"
export TRUNK_CACHE=/cache/trunk/
EOF

cat <<EOF >>"${REMOTE_USER_HOME}/.zshrc"
export TRUNK_CACHE=/cache/trunk/
EOF
