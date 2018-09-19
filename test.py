import sys
import numpy as np
from log import Log


class Test:

    def __init__(self, index, df):
        self.index = index
        self.df = df
        self.minx = 3.0
        self.minx_tmp = 3.0
        self.maxx = 5.0
        self.maxx_tmp = 5.0
        self.fit_a = 0.0
        self.fit_b = 0.1
        self.fit_r = 0.0
        self.fit_rank = 0.0
        self.fit_singular_values1 = 0.0
        self.fit_singular_values2 = 0.0
        self.fit_rcond = 0.0

        self.fitting()

    # fitting for Nix-Gao
    def fitting(self):
        df = self.df[self.minx_tmp <= self.df["1/h"]][self.df["1/h"] <= self.maxx_tmp]
        x = df["1/h"].values
        y = df["H^2"].values

        try:
            # https://docs.scipy.org/doc/numpy/reference/generated/numpy.polyfit.html
            fittingval = np.polyfit(x, y, 1, full=True)
        except:
            Log.addLog("fitting error: " + str(sys.exc_info()[0]) + str(sys.exc_info()[1]))
            return

        self.minx = self.minx_tmp
        self.maxx = self.maxx_tmp
        self.fit_a = fittingval[0][0]
        self.fit_b = fittingval[0][1]
        self.fit_r = fittingval[1][0]
        self.fit_rank = fittingval[2]
        self.fit_singular_values1 = fittingval[3][0]
        self.fit_singular_values2 = fittingval[3][1]
        self.fit_rcond = fittingval[4]

    def getParams(self):
        return [self.index, self.minx, self.maxx, self.fit_a, self.fit_b, self.fit_r, self.fit_rank,
                self.fit_singular_values1, self.fit_singular_values2, self.fit_rcond]

    def updateminx(self, val):
        self.minx_tmp = val
        self.fitting()

    def updatemaxx(self, val):
        self.maxx_tmp = val
        self.fitting()

    def _checkpolyfit(self, minx, maxx):
        df = self.df[minx <= self.df["1/h"]][self.df["1/h"] <= maxx]
        x = df["1/h"].values
        y = df["H^2"].values
        try:
            np.polyfit(x, y, 1)
        except:
            Log.addLog("fitting error: " + str(sys.exc_info()[0]) + str(sys.exc_info()[1]))
            return False

        return True
