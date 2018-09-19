import sys
import pandas as pd
import re
from collections import OrderedDict
from test import Test
from log import Log


class IndentData:

    # constructor with excel data
    def __init__(self, excel):
        self.testdict = OrderedDict()
        self.readExcel(excel)
        self.sheets = None

    # read Excel Data by G200
    # need exception for other types of excel file.
    def readExcel(self, filepath):

        try:
            self.sheets = pd.read_excel(filepath,
                                        usecols=[1, 2, 4, 5, 6],
                                        sheet_name=None,
                                        skiprows=[0, 1])

        except FileNotFoundError:
            Log.addLog("Read Excel Error: " + filepath + " is not found.")
            return

        except:
            Log.addLog("Read Excel Error: " + str(sys.exc_info()[0]) + str(sys.exc_info()[1]))
            return

        od = OrderedDict()
        for key, val in self.sheets.items():
            m = re.match(r"Test\s.(\d+)$", key)
            if m:
                val.columns = ["depth", "load", "harmonic", "hardness", "modulus"]
                val = val.dropna()
                val = val[val.hardness < 1e10]
                val = val[val.modulus < 1e10]
                val["1/h"] = 1000 / val["depth"]
                val["H^2"] = val["hardness"] * val["hardness"]
                val = val.reset_index()
                test = Test(m.group(1), val)
                od[m.group(1)] = test

        self.testdict = OrderedDict(sorted(od.items(), key=lambda x: x[0]))
        Log.addLog("Excel File (" + filepath + ") is successfully read.")

    # get index list of tests
    def getIndexList(self):
        return self.testdict.keys()

    # get DataFrame of index
    def getTest(self, index):
        return self.testdict[index]
