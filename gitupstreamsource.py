from os import path, makedirs
from subprocess import call
from shutil import rmtree, copytree, ignore_patterns
from dulwich.repo import Repo
from dulwich.porcelain import tag_list
from distutils.version import LooseVersion
import re
import os

class GitUpstremSource():

    def __init__(self, name, url, target = "", branches = []):
        self.url = url
        self.name = name
        if (target == ""):
            self.target = path.join("repo", name)
        else:
            self.target = target
        self.branches = branches

    def update(self):
        self.versions = []
        if (path.exists(self.target)):
            print("Pulling updates from: " + self.url)
            call(["git", "-C", self.target, "pull"])
        else:
            print("Cloning fresh repository from: " + self.url)
            makedirs(self.target)
            call(["git", "clone", self.url, self.target])
        return True
    
    def listVersion(self, regexs):
        repo = Repo(self.target)
        tags = tag_list(repo)
        result = []
    
        for tag in tags:
            tag = tag.decode('utf-8')
            for rex in regexs:
                if (re.match(rex, tag)):
                    result.append(tag)
    
        result=list(set(result))
        result.sort(key=LooseVersion)
        result.extend(self.branches)
        return result

    def extractVersion(self, version, targetPath):
        print("Checking out tag: " + version)
        _path = path.join(targetPath, version)
        if (path.exists(_path) and version in self.branches):
            rmtree(_path)      
            
        if (not path.exists(_path)):      
            devnull = open(os.devnull, 'w')
            call(["git", "-C", self.target, "checkout", version], stdout=devnull, stderr=devnull)
            copytree(self.target, _path, ignore=ignore_patterns('*.git', '.gitignore'))
            call(["git", "-C", self.target, "checkout", "master"], stdout=devnull, stderr=devnull)
            
        return _path
