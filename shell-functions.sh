#!/usr/bin/zsh

if [ -n "$DEBUG" ]; then
    PS4=':${LINENO}+'
    set -x
fi

function clone-lite() {
    if [[ "$@" == *"-h"* ]] || [[ "$@" == *"--help"* ]]; then
        ~/bin/clone-lite "$@"
    else
        local result
        result=$(~/bin/clone-lite "$@") || return $?
        cd "$result"
    fi
}

function rm-tag() {
    TAG="$1"
    git tag -d $TAG; git push origin :$TAG
}

function github-url() {
    FILENAME=$1
    REPOPATH=$(git rev-parse --show-toplevel)
    RELPATH=$(realpath --relative-to="$REPOPATH" "$PWD")
    FILEPATH="$RELPATH/$FILENAME"
    FILEPATH="${FILEPATH#*./}"
    BRANCH=$(git symbolic-ref --short HEAD)
    REMOTE=$(git config --get remote.origin.url)
    REPONAME=$(python3 <<-EOF
from urllib.parse import urlparse
pr = urlparse("$REMOTE")
print(pr.path)
EOF
)
    TYPE=tree
    [ -n "$FILENAME" ] && [ -f "$FILENAME" ] && TYPE=blob
    echo "https://github.com$REPONAME/$TYPE/$BRANCH/$FILEPATH"
}

