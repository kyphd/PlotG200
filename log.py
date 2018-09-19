class Log:

    statusbarStr = None
    log = []

    @staticmethod
    def addLog(log):
        Log.log.append(log)
        if Log.statusbarStr is not None:
            Log.statusbarStr.set(log)
        print(log)

    @staticmethod
    def getLog():
        return Log.log

    @staticmethod
    def getRecentLog():
        return Log.log[-1]

    @staticmethod
    def setStatusbarStr(stringvar):
        Log.statusbarStr = stringvar
