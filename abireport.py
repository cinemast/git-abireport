__author__ = "Peter Spiess-Knafl"
__copyright__ = "Copyright 2015"
__license__ = "GPLv3"
__email__ = "dev@spiessknafl.at"

from lxml import etree

class Problems:
    def __init__(self, root, kind, problemType):
        self.high = int(root.xpath('/reports/report[@kind="'+kind+'"]/problem_summary/problems_with_'+problemType+'/high/text()')[0])
        self.medium = int(root.xpath('/reports/report[@kind="'+kind+'"]/problem_summary/problems_with_'+problemType+'/medium/text()')[0])
        self.low = int(root.xpath('/reports/report[@kind="'+kind+'"]/problem_summary/problems_with_'+problemType+'/low/text()')[0])
        self.safe = int(root.xpath('/reports/report[@kind="'+kind+'"]/problem_summary/problems_with_'+problemType+'/safe/text()')[0])

class Report:
    def __init__(self, root, kind):
        self.verdict = root.xpath('/reports/report[@kind="'+kind+'"]/test_results/verdict/text()')[0]
        self.affected = root.xpath('/reports/report[@kind="'+kind+'"]/test_results/affected/text()')[0]

        self.addedSymbols = int(root.xpath('/reports/report[@kind="'+kind+'"]/problem_summary/added_symbols/text()')[0])
        self.removedSymbols = int(root.xpath('/reports/report[@kind="'+kind+'"]/problem_summary/removed_symbols/text()')[0])
        self.typeProblems = Problems(root,kind,"types")
        self.symbolProblems = Problems(root,kind,"symbols")
        self.constantProblems = int(root.xpath('/reports/report[@kind="'+kind+'"]/problem_summary/problems_with_constants/low/text()')[0])

class AbiReport:
    def __init__(self, xmlfile):
        self._root = etree.parse(xmlfile).getroot()
        self.source = Report(self._root, "source")
        self.binary = Report(self._root, "binary")

