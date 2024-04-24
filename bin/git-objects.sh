#!/usr/bin/env bash

if [ -n "$DEBUG" ]; then
    PS4=':${LINENO}+'
    set -x
fi

SCRIPT_FILE="$0"
SCRIPT_NAME="$(basename "$SCRIPT_FILE")"
SCRIPT_PATH="$(dirname "$SCRIPT_FILE")"
[ -n "$VERBOSE" ] && echo "SCRIPT_FILE=$SCRIPT_FILE"
[ -n "$VERBOSE" ] && echo "SCRIPT_NAME=$SCRIPT_NAME"
[ -n "$VERBOSE" ] && echo "SCRIPT_PATH=$SCRIPT_PATH"
if [ -L "$0" ]; then
    REAL_FILE="$(readlink "$0")"
    REAL_NAME="$(basename "$REAL_FILE")"
    REAL_PATH="$(dirname "$REAL_FILE")"
    [ -n "$VERBOSE" ] && echo "REAL_FILE=$REAL_FILE"
    [ -n "$VERBOSE" ] && echo "REAL_NAME=$REAL_NAME"
    [ -n "$VERBOSE" ] && echo "REAL_PATH=$REAL_PATH"
fi

OBJDIR=".git/objects"
if [[ -n "$@" ]]; then
    args=( "$@" )
else
    args=( "$OBJDIR" )
fi
for arg in $args; do
    if [[ "$arg" != "$OBJDIR"* ]]; then
        arg="$OBJDIR/$arg"
    fi
    for object in $(find "$arg" -type f); do
        echo
        echo "$object"
        python -c "import zlib,sys;sys.stdout.write(zlib.decompress(sys.stdin.read()))" <$object | hd
    done
done
