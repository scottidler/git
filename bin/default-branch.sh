#!/usr/bin/env bash

if [ -n "$DEBUG" ]; then
	PS4=':${LINENO}+'
	set -x
fi

REPONAME=$1
USERNAME=$2
PASSWORD=$3
URL=https://github.com/$REPONAME

if [ -z "$REPONAME" ]; then
	echo "error: REPONAME is required"
	exit 1
fi

if [ -n "$USERNAME" ]; then
	if [ -n "$PASSWORD" ]; then
		URL=https://$USERNAME:$PASSWORD@github.com/$REPONAME
	else
		echo "error: USERNAME=$USERNAME provided, but PASSWORD not given"
		exit 1
	fi

fi

git ls-remote --symref $URL HEAD | awk '/^ref:/ {sub(/refs\/heads\//, "", $2); print $2}'
