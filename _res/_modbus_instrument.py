import os
import re
import datetime

import serial
from modbus_tk import defines
from modbus_tk import modbus_rtu
from modbus_tk import modbus_tcp

from mikopub.utils import log
from mikopub.utils import calc

# Modbus Apparatus Class
#
# Definition: specify connection type serial or ip address
#                 rtu serial connection requires port number, other connect parameters are pre-assigned in apparatus sub-class
#                 tcp connection requires ip address
#                 both requires slave ID, default is 1
#
# Function: connect device via serial rtu or ip tcp
#           convert register tuple data to float
#           read register
#           write register
#           log termination info


class _modbus_instrument(calc._Calc, object):
    def __init__(self, logFile=os.path.abspath(__file__).replace(r"\instrument", r"\log").replace(".py", ".log")):
        calc._Calc.__init__(self, logFile=logFile)
        # instrument name
        self.instrName = "_Modbus_Default"  # device info
        # alternative 1: modbus tcp IP direct connect
        self.tcpIP = "100.100.100.100"
        self.tcpPort = 502
        # alternative 2: modbus rtu serial com connect
        self.rtuPort = "COM0"
        self.portBaudRate = 9600
        self.bytesize = 8
        self.parity = "N"
        self.stopbits = 1
        # slave ID
        self.slaveID = 1
        # IO config
        self.timeout = 3200 / 1000
        # set logger
        self.logFile = logFile
        self.loglogger = log.setLogLogger(logFile=self.logFile, logName=self.instrName + " " + str(datetime.datetime.now()))
        pass

    def connectTCP(
            self,
            tcpIP: str,
            tcpPort: int = 502,
            slaveID: int = 1
            ) -> None:
        try:
            self.loglogger.info(f"[{self.instrName}]: Connect tcp IP:".ljust(48)+f"{tcpIP}")
            self.loglogger.info(f"[{self.instrName}]:         slave ID:".ljust(48)+f"{slaveID}")
            self.tcpIP = tcpIP
            self.tcpPort = tcpPort
            self.slaveID = slaveID
            self.master = modbus_tcp.TcpMaster(tcpIP, tcpPort)
            self.master.set_timeout(self.timeout)
            self.connectType = "TCP"
            self.loglogger.info(f"[{self.instrName}]: TCPIP connection OK")
        except BaseException as e:
            self.connectType = "Fail"
            raise RuntimeError(f"[{self.instrName}]: Modbus connect fail {e}")
        pass

    def connectRTU(
            self,
            rtuPort: str,
            rtuBaudrate: int = 9600,
            rtuBytesize: int = 8,
            rtuParity: str = "N",
            rtuStopbits: int = 1,
            slaveID: int = 1
            ) -> None:
        try:
            self.loglogger.info(f"[{self.instrName}]: Connect rtu port:".ljust(48)+f"{rtuPort}")
            self.loglogger.info(f"[{self.instrName}]:         slave ID:".ljust(48)+f"{slaveID}")
            self.rtuPort = rtuPort
            self.baudrate = rtuBaudrate
            self.bytesize = rtuBytesize
            self.parity = rtuParity
            self.stopbits = rtuStopbits
            self.slaveID = slaveID
            self.master = modbus_rtu.RtuMaster(serial.Serial(port=rtuPort, baudrate=int(rtuBaudrate), bytesize=int(rtuBytesize), parity=rtuParity, stopbits=int(rtuStopbits)))
            self.master.set_timeout(self.timeout)
            # self.master.set_verbose(True)
            self.connectType = "RTU"
            self.loglogger.info(f"[{self.instrName}]: RTU connection OK")
        except BaseException as e:
            self.connectType = "Fail"
            raise RuntimeError(f"[{self.instrName}]: Modbus connect fail {e}")
        pass

    def read(self, startID: int, readRegister: int) -> tuple:
        '''
        **Read specified quantity of register number starting from start ID
          startID: start ID of read register
          readRegister: number of registers to read
        **{"startID": {"Property": {"Type": "int"}},
           "readRegister": {"Property": {"Type": "int"}}}
        **tuple
        '''
        try:
            read = self.master.execute(slave=self.slaveID, function_code=defines.READ_HOLDING_REGISTERS, starting_address=startID, quantity_of_x=readRegister, output_value=0)
        except BaseException as e:
            raise RuntimeError(f"[{self.instrName}]: Read error \n{e}")
        if self.connectType == "RTU":
            self.loglogger.info(f"[{self.instrName}]: Read port:".ljust(48)+f"{self.rtuPort}")
        elif self.connectType == "TCP":
            self.loglogger.info(f"[{self.instrName}]: Read IP:".ljust(48)+f"{self.tcpIP}")
        else:
            raise RuntimeError(f"[{self.instrName}]: Modbus connect fail")
        self.loglogger.info(f"[{self.instrName}]:      slave ID:".ljust(48)+f"{self.slaveID}")
        self.loglogger.info(f"[{self.instrName}]:      start ID:".ljust(48)+f"{startID}")
        self.loglogger.info(f"[{self.instrName}]:      register number:".ljust(48)+f"{readRegister}")
        self.loglogger.info(f"[{self.instrName}]: Return:".ljust(48)+f"{read}")
        return read

    def write(self, startID: int, writeRegister: list) -> None:
        '''
        **Write specified quantity of register number starting from start ID
          startID: start ID of read register
          writeRegister: content of registers to write, format is list
        **{"startID": {"Property": {"Type": "int"}},
           "writeRegister": {"Property": {"Type": "list"}}}
        **None
        '''
        try:
            self.master.execute(slave=self.slaveID, function_code=defines.WRITE_MULTIPLE_REGISTERS, starting_address=startID, output_value=writeRegister)
        except BaseException as e:
            raise RuntimeError(f"[{self.instrName}]: Write error \n{e}")
        if self.connectType == "RTU":
            self.loglogger.info(f"[{self.instrName}]: Write port:".ljust(48)+f"{self.rtuPort}")
        elif self.connectType == "TCP":
            self.loglogger.info(f"[{self.instrName}]: Write IP:".ljust(48)+f"{self.tcpIP}")
        else:
            raise RuntimeError(f"[{self.instrName}]: Modbus connect fail")
        self.loglogger.info(f"[{self.instrName}]:       slave ID:".ljust(48)+f"{self.slaveID}")
        self.loglogger.info(f"[{self.instrName}]:       start ID:".ljust(48)+f"{startID}")
        self.loglogger.info(f"[{self.instrName}]:       register:".ljust(48)+f"{writeRegister}")
        pass

    def _termInfo(self) -> None:  # log device termination info
        '''
        **Log termination info in log, to be combined with device termination actions in the terminateDev() func
        **None
        **None
        '''
        self.loglogger.info(f"[{self.instrName}]: Terminated")
        pass

    pass


pass
