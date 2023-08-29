#!/usr/bin/zsh

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

function clone-lite() {
    if [[ "$@" == *"-h"* ]] || [[ "$@" == *"--help"* ]]; then
        eval ~/bin/clone-lite "$@"
    else
        cd $(~/bin/clone-lite $1)
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

#function stale-branches() {
#  DAYS=$1;
#  REF=${2-refs/remotes/origin}
#  git for-each-ref --sort=-committerdate $REF --format='%(committerdate:short) %(refname:short) %(committername)' | while read date branch author; do
#    days_since_commit=$(( ( $(date +%s) - $(date -d "$date" +%s) ) / (24*60*60) ));
#    if [ $days_since_commit -ge $DAYS ] && ! git merge-base --is-ancestor $branch main; then
#      echo "$days_since_commit | $branch | $author";
#    fi;
#  done | sort -n
#}

stale-branches() {
    DAYS=$1 
    REF=${2-refs/remotes/origin} 

    git for-each-ref --sort=-committerdate $REF --format='%(committerdate:short) %(refname:short) %(committername)' | while read date branch author
    do
        days_since_commit=$(( ( $(date +%s) - $(date -d "$date" +%s) ) / (24*60*60) )) 
        if [ $days_since_commit -ge $DAYS ] && ! git merge-base --is-ancestor $branch main
        then
            echo "$days_since_commit | $branch | $author"
        fi
    done |
    awk -F ' \\| ' '{print $3 " | " $1 " | " $2}' | 
    sort -k1,1 -k2,2n | 
    awk '
        { lines[$1] = lines[$1] "\n" $0; count[$1]++ }
        END { for (a in lines) print count[a] " | " a lines[a] }
    ' | 
    sort -rn | 
    awk -F ' \\| ' '{
        for (i=3; i<=NF; i++) {
            print $2 " | " $i
        }
    }'
}

