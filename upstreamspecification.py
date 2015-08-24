import yaml
import re


class UpstreamSpecification:
    
    def __init__(self, filePath):
        with open(filePath, 'r') as stream:
            self.spec = yaml.load(stream)
            
    def getName(self):
        return self.spec["name"]
    
    def getUrl(self):
        return self.spec["url"]
            
    def getBranches(self):
        return self.spec["branches"]
    
    def getTags(self):
        result = []
        for recipe in self.spec["recipes"]:
            result.append(recipe["tag"])
        return result
    
    def getSOfiles(self, tag):
        for recipe in self.spec["recipes"]:
            if (re.match(recipe["tag"], tag)):
                return recipe["libraries"]
        return []
    
    def getRecipe(self, tag):
        for recipe in self.spec["recipes"]:
            if (re.match(recipe["tag"], tag)):
                return recipe["script"]
        return ""