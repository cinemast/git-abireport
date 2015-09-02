from subprocess import call
import os
import shutil
from os import path
from abireport import AbiReport
from os.path import dirname

class CompatReport():
    
    def __init__(self, name, build1, build2, basepath = "."):
        self.name = name
        self.build1 = build1
        self.build2 = build2
        self.basepath = basepath
        self.valid = False
        self.reportname = path.join(basepath, "compat_reports", name, build1.tag + "_to_" + build2.tag, "compat_report.xml")
    def isGenerated(self):
        return path.exists(self.reportname)
        
    def generateReport(self):
        
        if (not self.isGenerated()):
            fnull = open(os.devnull, 'w')
            call(["abi-compliance-checker", "-l", self.name, "-old", self.build1.getABI(), "-new", self.build2.getABI(), "-xml"], stdout=fnull, stderr=fnull, cwd=self.basepath)
            call(["abi-compliance-checker", "-l", self.name, "-old", self.build1.getABI(), "-new", self.build2.getABI()], stdout=fnull, stderr=fnull, cwd=self.basepath)

            if (not path.exists(dirname(self.reportname))):
                os.makedirs(dirname(self.reportname))
    
            shutil.copyfile(self.build1.log, path.join(dirname(self.reportname),"build1.log"))
            shutil.copyfile(self.build2.log, path.join(dirname(self.reportname),"build2.log"))

            
        if (self.isGenerated()):
            self.valid = True
            self.report = AbiReport(self.reportname)
        return self.valid