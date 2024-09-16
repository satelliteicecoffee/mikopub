'''
mikopub.utils.task
Task and task template for test taskflows
'''
import sys

from mikopub.utils import log
from mikopub._res._visa_instrument import _visa_instrument
if sys.platform.startswith("win"):
    from mikopub._res._modbus_instrument import _modbus_instrument
if sys.platform.startswith("linux"):
    from mikopub._res._spi_instrument import _spi_instrument


class Task(object):
    '''
    mikopub taskflow structure
        _taskConfig()
        _logConifg()
        _initInstr()
    '''
    def __init__(self) -> None:
        # self.filepath = os.path.abspath(__file__)
        # self.filedict = os.path.dirname(os.path.abspath(__file__))

        self.log = log.setLogLogger()
        self.csv = None

        self.var = {}
        self.instrs = []

        self._taskConfig()
        pass

    def __enter__(self):
        self._initConfig()
        self._logConfig()
        self._initInstr()

        # scan all instance variables, loaded instrument to task if not loaded
        for attr_name in dir(self):
            attr_value = getattr(self, attr_name)
            if sys.platform.startswith("win"):
                incld_instr = (_visa_instrument, _modbus_instrument)
            elif sys.platform.startswith("linux"):
                incld_instr = (_visa_instrument, _spi_instrument)
            else:
                pass
            if isinstance(attr_value, incld_instr):
                self.log.info(f"[{attr_value.instrName}]: Loaded to instr list")
                self.instrs.append(attr_value)
                pass

        # add logger to instruments and switch remote on
        for instr in self.instrs:
            instr.loglogger = self.log
            if hasattr(instr, "switchRemote") and callable(getattr(instr, "switchRemote")):
                instr.switchRemote(toStatus="on")
                pass
            self.log.info(f"[{instr.instrName}]: Loaded to task workflow")

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Cleanup, terminate instruments and close session
        for instr in self.instrs:
            self.log.info(f"[{instr.instrName}]: Terminate")
            instr.terminateInstr()
            instr.instr.close()
            pass

        # Print error
        if exc_type:
            print("Error occurs during flow execution")
            print(f"{exc_type}: {exc_val}")
        else:
            pass

        # Return False to propagate the exception, if any
        return False

    def _taskConfig(self):
        '''task configuration placeholder, constants only, no function'''
        pass

    def _initConfig(self):
        '''task configuration initiation placeholder, function only, no constant'''
        pass

    def _logConfig(self):
        '''task configuration placeholder, including default csv config'''
        pass

    def _initInstr(self):
        '''instrument initialization placeholder'''
        pass

    def addInstr(self, *instr):
        # add instrument to workflow
        for i in instr:
            if i not in self.instrs:
                self.log.info(f"[{i.instrName}]: Loaded to instr list")
                self.instrs.append(i)
        pass

    def setloglogger(self, filename, path, toConsole=True):
        '''
        e.g. filename="log.log", path="task/data"
        '''
        filepath = path + "/" + filename
        self.log = log.setLogLogger(logFile=filepath, logName="Task_Global_LOG", toConsole=toConsole)
        return self.log

    def setcsvlogger(self, filename, path, toConsole=False):
        '''
        e.g. filename="log.csv", path="task/data"
        '''
        filepath = path + "/" + filename
        self.csv = log.setCsvLogger(logFile=filepath, logName="Task_Global_CSV", toConsole=toConsole)
        return self.csv

    def logTitle(self):
        if self.csv is None:
            raise NameError("csv logger not defined, use setcsvlogger to set log")
        self.csv._logTitle()
        pass

    def logVar(self):
        if self.csv is None:
            raise NameError("csv logger not defined, use setcsvlogger to set log")
        self.csv.var = self.var.copy()
        self.csv.logVar()
        pass

    def test(self):
        '''add test flow like this'''
        pass

    pass


if __name__ == "__main__":
    with Task() as t:
        t.test()
        pass
    pass

pass
