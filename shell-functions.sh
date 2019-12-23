# vim: filetype=sh

if [ -n "$DEBUG" ]; then
    PS4=':${LINENO}+'
    set -x
fi

function clone() {
    if [[ "$@" == *"-h"* ]] || [[ "$@" == *"--help"* ]]; then
        eval ~/bin/clone "$@"
    else
        cd $(~/bin/clone $1)
    fi
}
