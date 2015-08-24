#!/usr/bin/python3
__author__ = "Peter Spiess-Knafl"
__copyright__ = "Copyright 2015"
__license__ = "GPLv3"
__version__ = "0.1"
__email__ = "dev@spiessknafl.at"
__status__ = "Development"

import sys
from os import path
from subprocess import call
from builder import Builder
from upstreamspecification import UpstreamSpecification
from gitupstreamsource import GitUpstremSource

def createSummary(spec, tags):
    return False
    

def main():
    if (len(sys.argv) < 2):
        print("Error: please provide a specification file as argument")
        sys.exit(1)

    spec = UpstreamSpecification(sys.argv[1])
    
    sourcePath = path.join("sources", spec.getName())
    buildPath = path.join("builds",spec.getName())
    
    repo = GitUpstremSource(spec.getName(), spec.getUrl(), sourcePath, spec.getBranches())
    repo.update()
    tags = repo.listVersion(spec.getTags())
    oldBuild = None
    for index in range(0,len(tags)-1):
        tag = tags[index]
        versionPath = repo.extractVersion(tag, buildPath)
        build = Builder(spec.getRecipe(tag), tag, spec.getSOfiles(tag), versionPath)
        if (not build.build()):
            print("Error building: " + tag, ", see: " + path.join(versionPath, "build.log"), file=sys.stderr)
        else:
            if (oldBuild is not None):
                tag1 = tags[index-1]
                tag2 = tag
                print(tag1 + " -> " + tag2)
                call(["abi-compliance-checker", "-l", spec.getName(), "-old", oldBuild.getABI(), "-new", build.getABI(), "-xml"])
                call(["abi-compliance-checker", "-l", spec.getName(), "-old", oldBuild.getABI(), "-new", build.getABI()]) 
            oldBuild = build
                

if __name__ == "__main__":
    main()
