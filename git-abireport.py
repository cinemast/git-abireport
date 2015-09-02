#!/usr/bin/python3
from compatreport import CompatReport
__author__ = "Peter Spiess-Knafl"
__copyright__ = "Copyright 2015"
__license__ = "GPLv3"
__version__ = "0.1"
__email__ = "dev@spiessknafl.at"
__status__ = "Development"

import sys
import datetime
from os import path
from subprocess import call
from builder import Builder
from upstreamspecification import UpstreamSpecification
from gitupstreamsource import GitUpstremSource
from jinja2 import Environment, PackageLoader
from jinja2 import Template

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

    builds = []
    reports = []
    for index in range(0,len(tags)):
        tag = tags[index]
        versionPath = repo.extractVersion(tag, buildPath)
        build = Builder(spec.getRecipe(tag), tag, spec.getSOfiles(tag), versionPath)
        builds.append(build)
        
        if (not build.build()):
            print("Error building: " + tag, ", see: " + path.join(versionPath, "build.log"), file=sys.stderr)
        if (index > 0):
            report = CompatReport(spec.getName(), builds[index-1], builds[index])
            if (not report.generateReport()):
                print ("Error comparing: " + builds[index-1].tag + " -> " + builds[index].tag, file=sys.stderr)
            else:
                print ("Compared " + builds[index-1].tag + " -> " + builds[index].tag)
            reports.append(report)
            
    reports = reversed(reports)
    env = Environment(loader=PackageLoader("git-abireport", "template"))
    template = env.get_template('report.html')
    with open(path.join("compat_reports",spec.getName() +'_compat_report.html'), 'w') as reportfile:
        now = datetime.datetime.now()
        print(template.render(name=spec.getName(), url=spec.getUrl(), reports=reports, update=now.strftime("%Y-%m-%d %H:%M:%S")), file=reportfile)
                        
if __name__ == "__main__":
    main()
