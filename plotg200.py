# PlotG200 main


class PlotG200:
    APPNAME = "PlotG200"
    AUTHOR = "K.Yabuuchi"
    VERSION = "0.1"
    GITHUB = "https://github.com/kyphd/PlotG200.git"


if __name__ == '__main__':
    from mytk import MyTk

    gui = MyTk()
    gui.show()
