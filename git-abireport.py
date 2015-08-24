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
    
    print(tags)
    
    builds = []
    logfile = open("compat.log", "w")
    for index in range(0,len(tags)):
        tag = tags[index]
        versionPath = repo.extractVersion(tag, buildPath)
        build = Builder(spec.getRecipe(tag), tag, spec.getSOfiles(tag), versionPath)
        builds.append(build)
        if (not build.build()):
            print("Error building: " + tag, ", see: " + path.join(versionPath, "build.log"), file=sys.stderr)
        elif (index > 0):
            tag1 = tags[index-1]
            tag2 = tag
            reportname = path.join("compat_reports",spec.getName(), tag1 + "_to_" + tag2, "compart_report.xml")
            if (not path.exists(reportname)):
                    print("Comparing: " + tag1 + " -> " + tag2)
                    call(["abi-compliance-checker", "-l", spec.getName(), "-old", builds[index-1].getABI(), "-new", builds[index].getABI(), "-xml"], stdout=logfile, stderr=logfile)
                    call(["abi-compliance-checker", "-l", spec.getName(), "-old", builds[index-1].getABI(), "-new", builds[index].getABI()], stdout=logfile, stderr=logfile)
                    if (not path.exists(reportname)):
                        print("Error comparing: " + tag1 + " -> " + tag2, file=sys.stderr)                
    logfile.close()
if __name__ == "__main__":
    main()
