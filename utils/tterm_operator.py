import os
import time
import datetime

import pywinauto.keyboard
from pywinauto.application import Application

from mikopub.utils import log


class teraterm_operator(object):
    _teratermPath = r'"C:\Program Files (x86)\teraterm5\ttermpro.exe"'
    pass

    def __init__(self) -> None:
        self.instrName = "TeraTerm"
        # teraterm start command
        self.startCmd = ""
        # tcp/ip config
        self.tcpIP = "192.168.0.255"
        self.tcpPort = "8900"
        # serial configs
        self.comPort = 0
        self.baudrate = 9600
        self.bytesize = 8
        self.parity = "none"
        self.stopbits = 1
        # set logger
        self.loglogger = log.setLogLogger()
        pass

    @classmethod
    def _processPath(cls, path: str) -> str:
        '''Process ttl path to normalize special chars'''
        propth = ""
        for c in str(path):
            if c in list(pywinauto.keyboard.MODIFIERS) + ['(', ')']:
                propth += ('{' + c + '}')
            elif c in ['{', '}']:
                propth += ('(' + c + ')')
            else:
                propth += c
        return propth

    @classmethod
    def setTeratermPath(cls, path: str) -> None:
        teraterm_operator._teratermPath = path
        pass

    def connectLocal(self) -> None:
        self.startCmd = teraterm_operator._teratermPath
        pass

    def connectIP(self, tcpIP, tcpPort) -> None:
        pass

    def connectSerial(
            self,
            comPort: str | int,
            baudrate: int = 9600,
            bytesize: int = 8,
            parity: str = "none",
            stopbits: int = 1
            ) -> None:
        self.comPort = comPort
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        cfgport = f" /C={self.comPort}"
        cfgbaudrate = f" /BAUD={self.baudrate}"
        cfgbytesize = f" /CDATABIT={self.bytesize}"
        cfgparity = f" /CPARITY={self.parity.lower()}"
        cfgstopbit = f" /CSTOPBIT={self.stopbits}"
        configParse = cfgport + cfgbaudrate + cfgbytesize + cfgparity + cfgstopbit
        self.startCmd = teraterm_operator._teratermPath + configParse
        pass

    def execTTL(self, ttlPath: str, close=True) -> None:
        '''
        Execute TTL macro
          ttlPath: TTL file path
          close: whether close window after execution
        '''
        self.loglogger.info(f"[{self.instrName}]: Start Teraterm:".ljust(40)+f"{self.startCmd}")
        # ttlPathPcd = teraterm_operator._processPath(ttlPath)

        app = Application(backend="uia").start(self.startCmd, timeout=6)
        time.sleep(1.6)
        appwin = app.window(title_re=".*Tera Term - .*")
        # appwin.print_control_identifiers()

        self.loglogger.info(f"[{self.instrName}]: Check connection")
        errwin = appwin.window(title_re=".*Tera Term: エラ.*")
        if errwin.exists(timeout=0.4):
            raise RuntimeError(f"[{self.instrName}]: Connection error \n")
        newinn = appwin.window(title_re=".*Tera Term: 新しい.*")
        if newinn.exists(timeout=0.4):
            # pywinauto.keyboard.send_keys("{ESC}")
            newinn.close()
        self.loglogger.info(f"[{self.instrName}]: Connection OK")

        self.loglogger.info(f"[{self.instrName}]: Load macro:".ljust(40)+f"{ttlPath}")
        ttmwin = app.window(title_re=".*Tera Term - .*")
        pywinauto.keyboard.send_keys("{VK_MENU down}om{VK_MENU up}")
        time.sleep(1.2)

        opn = Application(backend="uia").connect(title_re=".*MACRO: Open macro.*", timeout=10)
        opnwin = opn.window(title_re=".*MACRO:.*")
        opnwin.child_window(title_re=".*ファイル名|File name.*", control_type="Edit").set_text(ttlPath)
        # pywinauto.keyboard.send_keys(ttlPathPcd, with_spaces=True)
        pywinauto.keyboard.send_keys("{VK_MENU down}o{VK_MENU up}")
        macerrwin = opn.window(title_re=".*MACRO:.*")
        if macerrwin.exists(timeout=0.6):
            raise RuntimeError(f"[{self.instrName}]: Macro find error \n")

        self.loglogger.info(f"[{self.instrName}]: Exec macro:".ljust(40)+f"{ttlPath}")
        self.loglogger.info(f"[{self.instrName}]: Wait for completion")
        try:
            popup = Application(backend="uia").connect(title_re=".*MACRO - .*", timeout=1.6)
            popwin = popup.window(title_re=".*MACRO - .*")
            while popwin.exists(timeout=0.4):
                pass
            time.sleep(0.2)
        except BaseException:
            pass
        finally:
            # pywinauto.keyboard.send_keys("{VK_MENU down}fx{VK_MENU up}")
            if close:
                ttmwin.close()
            pass

        self.loglogger.info(f"[{self.instrName}]: Exec complete")
        pass

    def execCommand(self, command: str | list, close=True) -> None:
        self.loglogger.info(f"[{self.instrName}]: Start Teraterm:".ljust(40)+f"{self.startCmd}")
        # ttlPathPcd = teraterm_operator._processPath(ttlPath)

        app = Application(backend="uia").start(self.startCmd, timeout=6)
        time.sleep(1.6)
        appwin = app.window(title_re=".*Tera Term - .*")
        # appwin.print_control_identifiers()

        self.loglogger.info(f"[{self.instrName}]: Check connection")
        errwin = appwin.window(title_re=".*Tera Term: エラ.*")
        if errwin.exists(timeout=0.4):
            raise RuntimeError(f"[{self.instrName}]: Connection error \n")
        newinn = appwin.window(title_re=".*Tera Term: 新しい.*")
        if newinn.exists(timeout=0.4):
            # pywinauto.keyboard.send_keys("{ESC}")
            newinn.close()
        self.loglogger.info(f"[{self.instrName}]: Connection OK")

        if type(command) is str:
            command = [command]

        ttmwin = app.window(title_re=".*Tera Term VT.*")
        for cmd in command:
            self.loglogger.info(f"[{self.instrName}]: Run command:".ljust(40)+f"{cmd}")
            pywinauto.keyboard.send_keys(cmd, with_spaces=True)
            pywinauto.keyboard.send_keys("{ENTER}")
            time.sleep(0.6)

        if close:
            ttmwin.close()

        pass


if __name__ == '__main__':
    teraterm_operator.setTeratermPath(r'"C:\Program Files (x86)\teraterm5\ttermpro.exe"')
    to = teraterm_operator()
    to.connectSerial(comPort=9, baudrate=115200)
    macro_list = []
    for m in macro_list:
        to.execTTL(m, close=True)
    to.execCommand(["", "", "", "00112233", "", ""], close=True)
    pass


pass
