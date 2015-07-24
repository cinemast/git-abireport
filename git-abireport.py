#!/usr/bin/python3

import sys
import os
import yaml
import re
from subprocess import call
from dulwich.repo import Repo
from dulwich.porcelain import tag_list


def checkoutTag(tag):
    print("Checking out tag: " + tag)

def buildTag(tag):
    print("Building tag: " + tag)

def abiDump(sofile):
    print("Creating abi-dump for: " + sofile)

def getMatchingTags(spec):
    repo = Repo("repo")
    tags = tag_list(repo)
    result = []

    for tag in tags:
        tag = tag.decode('utf-8')
        for recipe in spec["recipes"]:
            print(recipe["tag"])
        print(tag)


    return result

def createOrUpdateRepo(spec):
    if (os.path.exists("repo")):
        print("Pulling updates from: " + spec["url"])
        call(["git", "-C", "repo", "pull"])
    else:
        print("Cloning fresh repo from: " + spec["url"])
        os.makedirs("repo")
        call(["git", "clone", spec["url"], "repo"])


def main():
    if (len(sys.argv) < 2):
        print("Error: please provide a specification file as argument")
        sys.exit(1)

    with open(sys.argv[1], 'r') as stream:
        spec = yaml.load(stream)
        createOrUpdateRepo(spec)
        print(getMatchingTags(spec))





if __name__ == "__main__":
    main()
