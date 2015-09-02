from subprocess import call
from os import path
import os

class Builder:
    
    def __init__(self, recipe, tag, sofiles, workingDir):
        self.recipe = recipe
        self.tag = tag
        self.sofiles = sofiles
        self.workingDir = workingDir
        self.log = path.join(self.workingDir,"build.log")
        
    def build(self):
        command = ["abi-dumper", "-lver", self.tag]
        logfile = open(self.log, "w")
        if ( not path.exists(path.join(self.workingDir, "ABI.dump"))):
            call(self.recipe, shell=True, cwd=self.workingDir, stdout=logfile, stderr=logfile)
            for sofile in self.sofiles:
                command.append(os.path.realpath(path.join(self.workingDir,sofile)))
            call(command, cwd=self.workingDir, stdout=logfile, stderr=logfile)
            
        logfile.close()
        return path.exists(path.join(self.workingDir, "ABI.dump"))
    
    def getABI(self):
        return path.join(self.workingDir, "ABI.dump")
        