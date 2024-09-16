import logging

# General loggers for simultaneously outputing to log file and console
# Usage:
#       import generalLogger module
#       create logger as loglogger1 = generalLogger.setLogLogger(logFile=logFile1.log, logIndex="log1")
#                        loglogger2 = generalLogger.setLogLogger(logFile=logFIle2.log, logIndex="log2")
#                        csvlogger = generalLogger.setCsvLogger(logFile=logFile3.csv)
#       substitute print("info") with loglogger1.info("info")
#                                     loglogger2.info("info")
#                                     csvlogger.info("info, info")


def setLogLogger(logFile: str | None = None, logName="defaultlog1bobo", setLevel="DEBUG", toConsole=True):
    '''e.g. {"GeneralFunc/log.log", "log1"}'''
    # logFile: file name including path from "Automatic_Test_Set"
    # logIndex: logger index used to create different log files
    loglogger = logging.getLogger(logName)
    loglogger.setLevel(setLevel)  # default proceed all info
    # basicFormat = "%(asctime)s,%(msecs)03d %(filename)s -%(levelname)s- %(message)s"
    basicFormat = "%(asctime)s,%(msecs)03d -%(levelname)s- %(message)s"
    dateFormat = "%Y/%m/%d %H:%M:%S"
    formatter = logging.Formatter(fmt=basicFormat, datefmt=dateFormat)
    loglogger.handlers.clear()
    if toConsole:
        consoleHandler = logging.StreamHandler()  # print to console
        consoleHandler.setFormatter(formatter)
        loglogger.addHandler(consoleHandler)
    if logFile is not None:
        if not logFile.endswith(".log"):
            logFile = logFile + ".log"
        txtHandler = logging.FileHandler(logFile, encoding="utf-8")  # print to log
        txtHandler.setFormatter(formatter)
        loglogger.addHandler(txtHandler)

    return loglogger


class CsvLogger(logging.Logger, object):
    """Overload Logger for new csv logging methods"""
    def __init__(self, name: str):
        logging.Logger.__init__(self, name=name)
        # super().__init__(name)
        # csv var
        self.var = {}
        self._varlen = 0
        pass

    def _logTitle(self):
        title = ", ".join(list(self.var.keys()))
        self.info(title)
        pass

    def logVar(self):
        if self._varlen != len(self.var):  # if variable space change, update and relog title row
            self._varlen = len(self.var)
            self._logTitle()
            pass
        datalist = [str(item) for item in self.var.values()]
        data = ",".join(datalist)
        self.info(data)
        pass


def setCsvLogger(logFile: str, logName="defaultlog1biubiu", setLevel="DEBUG", toConsole=False):
    '''e.g. {"GeneralFunc/log.csv", "log1"}'''
    # logFile: file name including path from "Automatic_Test_Set"
    # logIndex: logger index used to create different log files
    # add variable record and auto log attributes and functions to logging.Logger class
    csvlogger = CsvLogger(logName)  # csvlogger = logging.getLogger(logName): sub class
    csvlogger.setLevel(setLevel)  # default proceed all level info
    basicFormat = "%(asctime)s;%(msecs)03d, %(message)s"
    dateFormat = "%Y/%m/%d %H:%M:%S"
    formatter = logging.Formatter(fmt=basicFormat, datefmt=dateFormat)
    csvlogger.handlers.clear()
    if toConsole:
        consoleHandler = logging.StreamHandler()  # print to console
        consoleHandler.setFormatter(formatter)
        csvlogger.addHandler(consoleHandler)
    if not logFile.endswith(".csv"):
        logFile = logFile + ".csv"
    csvHandler = logging.FileHandler(logFile, encoding="utf-8")  # print to csv
    csvHandler.setFormatter(formatter)
    csvlogger.addHandler(csvHandler)

    return csvlogger


if __name__ == "__main__":
    # loglogger1 = setLogLogger(logFile="log1.log", logName="log1")
    # loglogger2 = setLogLogger(logFile="log2.log", logName="log2")
    csvlogger3 = setCsvLogger(logFile="log3.csv", logName="log3")
    # loglogger1.info("test1")
    # loglogger1.warning("tft")
    # loglogger2.info("test2")
    # loglogger2.debug('fjd')
    csvlogger3.info("test3")
    csvlogger3.info("dkdkd, gtht")
    # pass
    import time
    import datetime
    csvlogger3.var["number"] = 355
    csvlogger3.var["ppl"] = 2 * 4 + 6
    csvlogger3.var["location"] = "jane's home"
    csvlogger3.logVar()
    for i in [1, 2, 5, 34, 45, 4, 3452, 4345, 54, 867]:
        csvlogger3.var["time"] = datetime.datetime.now()
        csvlogger3.var["number"] = 355
        csvlogger3.var["ppl"] = 2 * i + 6
        csvlogger3.var["location"] = "jane's home"
        csvlogger3.logVar()
        time.sleep(2.2)
    csvlogger3.var["new var"] = "Joe 11"
    csvlogger3.logVar()
    pass


pass
