#!/usr/bin/python3

__author__ = "Peter Spiess-Knafl"
__copyright__ = "Copyright 2015"
__license__ = "GPLv3"
__version__ = "0.1"
__email__ = "dev@spiessknafl.at"
__status__ = "Development"

import sys
import os
import yaml
import re
from subprocess import call
from dulwich.repo import Repo
from dulwich.porcelain import tag_list
from shutil import copytree, ignore_patterns, rmtree
from distutils.version import LooseVersion


def checkoutTag(tag):
    print("Checking out tag: " + tag)
    if (os.path.exists("builds/"+tag)):
        rmtree("builds/"+tag)
    devnull = open(os.devnull, 'w')
    call(["git", "-C", "repo", "checkout", tag], stdout=devnull, stderr=devnull)

    copytree("repo/", "builds/"+tag, ignore=ignore_patterns('*.git', '.gitignore'))
    
    call(["git", "-C", "repo", "checkout", "master"], stdout=devnull, stderr=devnull)

def buildTag(recipe, tag):
    print("Building tag: " + tag)
    call(recipe, shell=True, cwd="builds/"+tag)

def abiDump(sofiles, tag):
    print("Creating abi-dump for: " + str(sofiles))
    command = ["abi-dumper", "-lver", tag]
    for sofile in sofiles:
        command.append(os.path.realpath("builds/"+tag+"/"+sofile))

    print(str(command))
    call(command, cwd="builds/"+tag)

def getMatchingTags(spec):
    repo = Repo("repo")
    tags = tag_list(repo)
    result = []

    for tag in tags:
        tag = tag.decode('utf-8')
        for recipe in spec["recipes"]:
            if (re.match(recipe["tag"], tag)):
                result.append(tag)

    result=list(set(result))
    result.sort(key=LooseVersion)

    return result

def getRecipeForTag(spec, tag):
    for recipe in spec["recipes"]:
        if (re.match(recipe["tag"], tag)):
            return recipe["script"]
    return ""

def getSOfileForTag(spec, tag):
    for recipe in spec["recipes"]:
        if (re.match(recipe["tag"], tag)):
            return recipe["libraries"]
    return []


def createOrUpdateRepo(spec):
    if (os.path.exists("repo")):
        print("Pulling updates from: " + spec["url"])
        call(["git", "-C", "repo", "pull"])
    else:
        print("Cloning fresh repo from: " + spec["url"])
        os.makedirs("repo")
        call(["git", "clone", spec["url"], "repo"])

def createABIReport(spec, tags):
    
    refs = list(tags)
    refs.extend(spec["branches"])

    for index in range(0,len(refs)-1):
        tag1 = refs[index]
        tag2 = refs[index+1]
        print (refs[index] + " -> " + refs[index+1])

        call(["abi-compliance-checker", "-l", spec["name"], "-old", "builds/"+tag1+"/ABI.dump", "-new", "builds/"+tag2+"/ABI.dump", "-xml"])
        call(["abi-compliance-checker", "-l", spec["name"], "-old", "builds/"+tag1+"/ABI.dump", "-new", "builds/"+tag2+"/ABI.dump"])

def main():
    if (len(sys.argv) < 2):
        print("Error: please provide a specification file as argument")
        sys.exit(1)

    with open(sys.argv[1], 'r') as stream:
        spec = yaml.load(stream)
        createOrUpdateRepo(spec)
        tags = getMatchingTags(spec)

        for tag in tags:
            if (not os.path.exists("builds/"+tag)):
                checkoutTag(tag)
                buildTag(getRecipeForTag(spec, tag), tag)
                abiDump(getSOfileForTag(spec, tag), tag)

        for branch in spec["branches"]:
            checkoutTag(branch)
            buildTag(spec["recipes"][len(spec["recipes"])-1]["script"], branch)
            abiDump(spec["recipes"][len(spec["recipes"])-1]["libraries"], branch)

        createABIReport(spec, tags)

if __name__ == "__main__":
    main()
