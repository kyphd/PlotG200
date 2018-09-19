import os
import matplotlib
matplotlib.use('TkAgg')
from tkinter import *
from tkinter.scrolledtext import ScrolledText
import tkinter.filedialog as tkfd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from collections import OrderedDict
import csv
from plotg200 import PlotG200
from indentdata import IndentData
from log import Log


class MyTk:

    plotTypeDict = OrderedDict()
    plotTypeDict["load - depth"]       = ["depth", "load",     "$Depth (nm)$",   "$Load (mN)$"]
    plotTypeDict["harmonic - depth"]   = ["depth", "harmonic", "$Depth (nm)$",   "$Harmonic Contact Stiffness (N/m)$"]
    plotTypeDict["hardness - depth"]   = ["depth", "hardness", "$Depth (nm)$",   "$Hardness (GPa)$"]
    plotTypeDict["modulus - depth"]    = ["depth", "modulus",  "$Depth (nm)$",   "$Modulus (GPa)$"]
    plotTypeDict["H^2 - 1/h (NixGao)"] = ["1/h",   "H^2",      "$1/h (\mu m^{-1})$", "$H^{2} (GPa^{2})$"]

    colorlist = ['Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
                 'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
                 'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']

    openFTyp = [('Excel file', '*.xls'), ('Excel file', '*.xlsx')]
    saveFTyp = [('Image', '*.png')]

    welcomemessage = "Hello, " + PlotG200.APPNAME + " ver." + PlotG200.VERSION + " by " + PlotG200.AUTHOR + \
                     " See " + PlotG200.GITHUB + "."

    def __init__(self):

        # open excel file and read data
        self.root = Tk()
        self.testlistText = None
        self.fig = None
        self.sp = None
        self.canvas = None
        self.fittingText = None
        self.statusbar = None

        self.plotType = StringVar()
        self.minxVar = StringVar()
        self.maxxVar = StringVar()
        self.minyVar = StringVar()
        self.maxyVar = StringVar()
        self.plotColor = StringVar()
        self.alphaVar = DoubleVar()
        self.lineplot = BooleanVar()
        self.legend = BooleanVar()
        self.statusbarStr = StringVar()
        self.fittingcurve = BooleanVar()
        self.h0Var = DoubleVar()

        Log.setStatusbarStr(self.statusbarStr)

        self.data = None
        self.checkedDict = dict()
        self.minxdict = dict()
        self.maxxdict = dict()

        self.dirpath = os.path.abspath(os.path.dirname(__file__))
        self.makewindow()

    def show(self):

        self.root.mainloop()

    def makewindow(self):

        # root window
        self.root.title("PlotG200")
        self.root.geometry("1200x640")

        # main frame
        mainframe = Frame(self.root)
        mainframe.pack(side=TOP)

        # left frame
        frame1 = Frame(mainframe)
        frame1.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)

        # center frame
        frame2 = Frame(mainframe)
        frame2.grid(row=0, column=1, padx=10, pady=10, sticky=NSEW)

        # right frame
        frame3 = Frame(mainframe)
        frame3.grid(row=0, column=2, padx=10, pady=10, sticky=NSEW)

        # left frame - 0
        frame10 = LabelFrame(frame1, relief="groove", text=u"Open File")
        frame10.pack(side=TOP, ipadx=2, ipady=2, fill=X)
        openButton = Button(frame10, text="open file", command=self._openfile)
        openButton.pack(side=TOP)

        # left frame - 1st
        frame11 = LabelFrame(frame1, relief="groove", text=u"Plot Type")
        frame11.pack(side=TOP, ipadx=2, ipady=2, fill=X)

        self.plotType.set(list(MyTk.plotTypeDict.keys())[0])
        plottypeOM = OptionMenu(frame11, self.plotType, *MyTk.plotTypeDict.keys(), command=self._plot)
        plottypeOM.pack(side=TOP, fill=X)

        # left frame - 2nd
        frame12 = LabelFrame(frame1, relief="groove", text="Select Test")
        frame12.pack(side=TOP, pady=10, ipadx=2, ipady=2)

        # Bug for Mac "two-finger scroll": https://bugs.python.org/issue10731
        self.testlistText = ScrolledText(frame12, borderwidth=0, width=20, height=25, state=DISABLED)
        self.testlistText.grid(row=0, column=0, pady=10)

        # center frame - 1st for plot
        self.fig = Figure()
        self.sp = self.fig.add_subplot(1, 1, 1)
        self.sp.tick_params(direction='in')
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame2)
        self.canvas.get_tk_widget().pack(side=TOP, expand=0)
        self.canvas.get_tk_widget().pack(side=TOP, expand=0)
        self.canvas.draw()

        # center frame - 2nd
        frame22 = Frame(frame2)
        frame22.pack(side=TOP)

        # xrange
        label221 = Label(frame22, text="x range:")
        label221.pack(side=LEFT)
        self.minxVar.trace_add("write", lambda name, index, mode, sv=self.minxVar: self._plot())
        minxEntry = Entry(frame22, width=7, textvariable=self.minxVar)
        minxEntry.pack(side=LEFT)
        label222 = Label(frame22, text="-")
        label222.pack(side=LEFT)
        self.maxxVar.trace_add("write", lambda name, index, mode, sv=self.maxxVar: self._plot())
        maxxEntry = Entry(frame22, width=7, textvariable=self.maxxVar)
        maxxEntry.pack(side=LEFT)

        # yrange
        label223 = Label(frame22, text="    y range:")
        label223.pack(side=LEFT)
        self.minyVar.trace_add("write", lambda name, index, mode, sv=self.minyVar: self._plot())
        minyEntry = Entry(frame22, width=7, textvariable=self.minyVar)
        minyEntry.pack(side=LEFT)
        label224 = Label(frame22, text="-")
        label224.pack(side=LEFT)
        self.maxyVar.trace_add("write", lambda name, index, mode, sv=self.maxyVar: self._plot())
        maxyEntry = Entry(frame22, width=7, textvariable=self.maxyVar)
        maxyEntry.pack(side=LEFT)

        # center frame - 3rd
        frame23 = Frame(frame2)
        frame23.pack(side=TOP)

        # plot color
        label231 = Label(frame23, text="Plot Color: ")
        label231.pack(side=LEFT)
        self.plotColor.set(MyTk.colorlist[0])
        plotColorOM = OptionMenu(frame23, self.plotColor, *MyTk.colorlist, command=self._plot)
        plotColorOM.pack(side=LEFT)

        # alpha
        label232 = Label(frame23, text=" Alpha: ")
        label232.pack(side=LEFT)
        self.alphaVar.set(1.0)
        alphaScale = Scale(frame23, orient='h', from_=0.0, to=1.0, resolution=0.01, variable=self.alphaVar, command=self._plot)
        alphaScale.pack(side=LEFT)

        # line plot
        self.lineplot.set(False)
        lineCB = Checkbutton(frame23, text="line plot", variable=self.lineplot, command=self._plot)
        lineCB.pack(side=LEFT)

        # legend
        self.legend.set(True)
        legendCB = Checkbutton(frame23, text="legend", variable=self.legend, command=self._plot)
        legendCB.pack(side=LEFT)

        # center frame - 4th
        frame24 = Frame(frame2)
        frame24.pack(side=TOP)

        # fitting for Nix-Gao button
        self.fittingcurve.set(False)
        fittingCB = Checkbutton(frame24, text="show fitting curve (Nix-Gao)", variable=self.fittingcurve, command=self._plot)
        fittingCB.pack(side=LEFT)

        # center frame - last for some buttons
        frame2x = Frame(frame2)
        frame2x.pack(side=TOP)
        saveImgButton = Button(frame2x, text="Save Figure", command=self._saveImg)
        saveImgButton.pack(side=LEFT)

        # right frame 1st for nix-gao
        frame31 = LabelFrame(frame3, relief="groove", text=u"Fitting Parameter for Nix-Gao Plot.")
        frame31.pack(side=TOP)

        # fitting params for nix-gao
        # Bug for Mac "two-finger scroll": https://bugs.python.org/issue10731
        self.fittingText = Text(frame31, borderwidth=0, width=42, height=33, state=DISABLED)
        self.fittingText.grid(row=0, column=0, sticky=NSEW)
        xScrollbar = Scrollbar(frame31, orient=HORIZONTAL)
        xScrollbar.config(command=self.fittingText.xview)
        xScrollbar.grid(row=1, column=0, sticky=EW)
        yScrollbar = Scrollbar(frame31, orient=VERTICAL)
        yScrollbar.config(command=self.fittingText.yview)
        yScrollbar.grid(row=0, column=1, sticky=NS)
        self.fittingText.config(xscrollcommand=xScrollbar.set, yscrollcommand=yScrollbar.set, wrap=NONE)

        # H0 = average(sqrt(b))
        frame33 = Frame(frame3)
        frame33.pack(side=TOP)
        h0label = Label(frame33, text="H0 = ")
        h0label.pack(side=LEFT)
        h0entry = Entry(frame33, textvariable=self.h0Var, state="readonly", relief=FLAT)
        h0entry.pack(side=LEFT)

        # saveCsv button
        frame32 = Frame(frame3)
        frame32.pack(side=TOP)
        saveCsvButton = Button(frame32, text="Save CSV", command=self._saveCsv)
        saveCsvButton.pack(side=TOP)

        # status bar
        self.statusbarStr.set(MyTk.welcomemessage)
        self.statusbar = Label(self.root, textvariable=self.statusbarStr, bd=1, relief=SUNKEN, anchor=W, padx=5)
        self.statusbar.pack(side=BOTTOM, fill=X)

    # open excel file and read data as IndentData
    def _openfile(self):

        filepath = tkfd.askopenfilename(filetypes=MyTk.openFTyp, initialdir=self.dirpath)
        self.dirpath = os.path.dirname(filepath)
        self.data = IndentData(filepath)
        self._updateCheckbox()
        self._updateFittingTable()
        self.sp.cla()
        self.canvas.draw()

    # update Checkbutton in frame12
    def _updateCheckbox(self):

        # make checkbutton for select test
        self.testlistText.config(state=NORMAL)
        self.testlistText.delete(1.0, END)
        self.checkedDict = dict()
        for i in self.data.getIndexList():
            self.checkedDict[i] = BooleanVar()
            cb = Checkbutton(text="Test %s   " % i,
                             variable=self.checkedDict[i],
                             command=self._tickcb)
            self.testlistText.window_create(END, window=cb)
            self.testlistText.insert(END, "\n")
        self.testlistText.config(state=DISABLED)

    def _updateFittingTable(self):

        # make table for fitting text
        self.fittingText.config(state=NORMAL)
        self.fittingText.delete(1.0, END)

        # label
        s1 = StringVar()
        s1.set("Test")
        l1 = Entry(self.fittingText, textvariable=s1, width=3, borderwidth=1, relief=FLAT, state="readonly", justify=CENTER)
        self.fittingText.window_create(END, window=l1)
        s2 = StringVar()
        s2.set("min x")
        l2 = Entry(self.fittingText, textvariable=s2, width=4, borderwidth=1, relief=FLAT, state="readonly", justify=CENTER)
        self.fittingText.window_create(END, window=l2)
        s3 = StringVar()
        s3.set("max x")
        l3 = Entry(self.fittingText, textvariable=s3, width=4, borderwidth=1, relief=FLAT, state="readonly", justify=CENTER)
        self.fittingText.window_create(END, window=l3)
        s4 = StringVar()
        s4.set("a")
        l4 = Entry(self.fittingText, textvariable=s4, width=5, borderwidth=1, relief=FLAT, state="readonly", justify=CENTER)
        self.fittingText.window_create(END, window=l4)
        s5 = StringVar()
        s5.set("b")
        l5 = Entry(self.fittingText, textvariable=s5, width=5, borderwidth=1, relief=FLAT, state="readonly", justify=CENTER)
        self.fittingText.window_create(END, window=l5)
        s6 = StringVar()
        s6.set("r")
        l6 = Entry(self.fittingText, textvariable=s6, width=5, borderwidth=1, relief=FLAT, state="readonly", justify=CENTER)
        self.fittingText.window_create(END, window=l6)
        self.fittingText.insert(END, "\n")

        j = 0
        sum_sqrt_b = 0.0
        self.minxdict = dict()
        self.maxxdict = dict()
        for key, val in self.checkedDict.items():
            if val.get():
                param = self.data.getTest(key).getParams()
                s1 = StringVar()
                s1.set(param[0])
                l1 = Entry(self.fittingText, textvariable=s1, width=3, borderwidth=1, relief=FLAT, state="readonly", justify=CENTER)
                self.fittingText.window_create(END, window=l1)
                self.minxdict[key] = StringVar()
                self.minxdict[key].set(param[1])
                self.maxxdict[key] = StringVar()
                self.maxxdict[key].set(param[2])
                l2 = Entry(self.fittingText, textvariable=self.minxdict[key], width=4, borderwidth=1, relief=RIDGE)
                l2.bind("<Return>", self._updateFitParam)
                self.fittingText.window_create(END, window=l2)
                l3 = Entry(self.fittingText, textvariable=self.maxxdict[key], width=4, borderwidth=1, relief=RIDGE)
                l3.bind("<Return>", self._updateFitParam)
                self.fittingText.window_create(END, window=l3)
                s4 = StringVar()
                s4.set(param[3])
                l4 = Entry(self.fittingText, textvariable=s4, width=5, borderwidth=1, relief=FLAT, state="readonly")
                self.fittingText.window_create(END, window=l4)
                s5 = StringVar()
                s5.set(param[4])
                l5 = Entry(self.fittingText, textvariable=s5, width=5, borderwidth=1, relief=FLAT, state="readonly")
                self.fittingText.window_create(END, window=l5)
                s6 = StringVar()
                s6.set(param[5])
                l6 = Entry(self.fittingText, textvariable=s6, width=5, borderwidth=1, relief=FLAT, state="readonly")
                self.fittingText.window_create(END, window=l6)
                self.fittingText.insert(END, "\n")

                sum_sqrt_b = sum_sqrt_b + np.sqrt(param[4])
                j += 1

        self.fittingText.config(state=DISABLED)
        if j == 0:
            self.h0Var.set(0.0)
        else:
            self.h0Var.set(sum_sqrt_b / j)

        Log.addLog("Fitting Parameters are successfully updated.")

    def _tickcb(self):
        self._updateFittingTable()
        self._plot()

    def _updateFitParam(self, event):

        for key, val in self.checkedDict.items():
            if val.get():
                try:
                    self.data.getTest(key).updateminx(float(self.minxdict[key].get()))
                except ValueError:
                    print(key, "minx: ", sys.exc_info())
                    return

                try:
                    self.data.getTest(key).updatemaxx(float(self.maxxdict[key].get()))
                except ValueError:
                    print(key, "maxx: ", sys.exc_info())
                    return

        self._updateFittingTable()
        self._plot()

    def _plot(self, *kwargs):

        if self.data is None:
            return

        self.sp.cla()

        # color
        cmap = plt.get_cmap(self.plotColor.get())
        plotnum = [val.get() for val in list(self.checkedDict.values())].count(True)
        if plotnum < 10:
            plotnum = 10

        # plot type: line or scatter
        kwd = {}
        if self.lineplot.get():
            kwd = {'kind': 'line', 'lw': 1}
        else:
            kwd = {'kind': 'scatter', 's': 1}

        i = 0
        for key, val in self.checkedDict.items():
            if val.get():
                if self.legend.get():
                    kwd["label"] = key
                else:
                    kwd["legend"] = False

                self.data.getTest(key).df.plot(ax=self.sp,
                                               x=self.plotTypeDict[self.plotType.get()][0],
                                               y=self.plotTypeDict[self.plotType.get()][1],
                                               c=cmap(1 - ((float(i) / plotnum) * 0.7)),
                                               alpha=self.alphaVar.get(),
                                               **kwd)

                if self.fittingcurve.get() and self.plotType.get() == "H^2 - 1/h (NixGao)":
                    x = np.array([0.0, 1000.0])
                    y = self.data.getTest(key).fit_a * x + self.data.getTest(key).fit_b
                    self.sp.plot(x, y, alpha=self.alphaVar.get())

                i += 1
        self.sp.set_xlabel(self.plotTypeDict[self.plotType.get()][2])
        self.sp.set_ylabel(self.plotTypeDict[self.plotType.get()][3])

        try:
            self.sp.set_xlim(xmin=float(self.minxVar.get()))
        except ValueError:
            print("xmin: ", sys.exc_info())

        try:
            self.sp.set_xlim(xmax=float(self.maxxVar.get()))
        except ValueError:
            print("xmax: ", sys.exc_info())

        try:
            self.sp.set_ylim(ymin=float(self.minyVar.get()))
        except ValueError:
            print("ymin: ", sys.exc_info())

        try:
            self.sp.set_ylim(ymax=float(self.maxyVar.get()))
        except ValueError:
            print("ymax: ", sys.exc_info())

        self.canvas.draw()

        Log.addLog("Plot is updated.")

    def _saveImg(self):
        filepath = tkfd.asksaveasfilename(filetypes=MyTk.saveFTyp, initialdir=self.dirpath,
                                          initialfile="plot", defaultextension=".png")
        try:
            self.fig.savefig(filepath)
        except:
            Log.addLog("Save error: " + str(sys.exc_info()[0]) + str(sys.exc_info()[1]))

        Log.addLog(filepath + " is successfully saved.")

    def _saveCsv(self):
        filepath = tkfd.asksaveasfilename(filetypes=MyTk.saveFTyp, initialdir=self.dirpath,
                                          initialfile="fittingParam", defaultextension=".csv")
        try:
            with open(filepath, "w") as f:
                writer = csv.writer(f, lineterminator='\n')
                writer.writerow(["# Fitting parameter by PlotG200 using numpy polyfit. y = a * x + b: r = residual"])
                writer.writerow(["# https://docs.scipy.org/doc/numpy/reference/generated/numpy.polyfit.html"])
                writer.writerow(["Test", "min x", "max x", "a", "b", "r", "rank", "singular_value1", "singular_values2", "rcond"])
                for key, val in self.checkedDict.items():
                    if val.get():
                        writer.writerow(self.data.getTest(key).getParams())

        except:
            Log.addLog("Save CSV Error: " + str(sys.exc_info()[0]) + str(sys.exc_info()[1]))

        Log.addLog("CSV (" + filepath + ") is successfully saved.")
