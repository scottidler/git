#!/usr/bin/env python3

import sys
import subprocess
import ruamel.yaml
import argparse

def get_stale_branches(days, ref="refs/remotes/origin"):
    cmd = [
        "git", "for-each-ref", "--sort=-committerdate", ref,
        "--format=%(committerdate:short) %(refname:short) %(committername)"
    ]

    result = subprocess.check_output(cmd).decode('utf-8').splitlines()

    branches = []
    for line in result:
        date, branch, *author_parts = line.split()
        author = ' '.join(author_parts)
        days_since_commit = (int(subprocess.check_output(["date", "+%s"])) - int(subprocess.check_output(["date", "-d", date, "+%s"]))) // (24*60*60)
        if days_since_commit >= days:
            branches.append({
                "days": days_since_commit,
                "branch": branch,
                "author": author
            })

    return branches

def generate_yaml(branches):
    authors_dict = {}
    for branch in branches:
        author = branch["author"]
        if author not in authors_dict:
            authors_dict[author] = []
        authors_dict[author].append({
            branch["branch"]: branch["days"]
        })

    # Sort authors by number of branches
    sorted_authors = sorted(authors_dict.items(), key=lambda x: len(x[1]), reverse=True)

    yaml_data = {"authors": []}
    for author, branches in sorted_authors:
        # Sort branches in descending order based on days
        sorted_branches = sorted(branches, key=lambda x: list(x.values())[0], reverse=True)
        yaml_data["authors"].append({
            author: {
                "branches": sorted_branches,
                "count": len(branches)
            }
        })

    yaml = ruamel.yaml.YAML()
    yaml.dump(yaml_data, sys.stdout)

def main():
    parser = argparse.ArgumentParser(description='Generate a YAML report of stale branches.')
    parser.add_argument('days', type=int, help='Number of days to consider a branch stale.')
    parser.add_argument('--ref', default="refs/remotes/origin", help='Git reference to check. Default is refs/remotes/origin.')

    args = parser.parse_args()

    branches = get_stale_branches(args.days, args.ref)
    generate_yaml(branches)

if __name__ == "__main__":
    main()

