import socket


class OtherResourceManager(object):
    def __init__(self) -> None:
        pass

    def open_resource(self, resource_name: str) -> "Resource":
        ren = resource_name.split("::")
        if ren[0] == "UDPIP":
            res = UDPResource(ren[1], int(ren[2]))
        else:
            res = Resource()

        return res


class Resource(object):
    def __init__(self) -> None:
        pass

    pass


class UDPResource(Resource):
    def __init__(self, udpIP, udpPort) -> None:
        self.skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udpIP = udpIP
        self.udpPort = udpPort
        self.write_termination = None
        self.read_termination = "\n"
        self.encoding = "utf-8"
        self._timeout = 1000
        pass

    @property
    def timeout(self) -> float | int:
        return self._timeout

    @timeout.setter
    def timeout(self, new_timeout) -> None:
        self._timeout = new_timeout
        self.skt.settimeout(new_timeout/1000)
        pass

    def close(self) -> None:
        self.skt.close()
        pass

    def read(self, **kwargs) -> str:
        data = self.read_raw()
        if "encoding" in kwargs:
            data = data.decode(encoding=kwargs["encoding"])
        else:
            data = data.decode(encoding=self.encoding)

        return data

    def read_raw(self, **kwargs) -> bytes:
        data = b""
        while True:
            try:
                chunk, address = self.skt.recvfrom(2048)
                if address != (self.udpIP, self.udpPort):
                    continue
                data = data + chunk
                if data.endswith(bytes(self.read_termination, self.encoding)):  # need to add encoding
                    break
            except socket.timeout as e:
                raise e
            except BaseException as e:
                raise e

        return data

    def read_bytes(self, bytes, **kwargs) -> bytes:
        data = b""
        try:
            data, address = self.skt.recvfrom(bytes)
            if address != (self.udpIP, self.udpPort):
                raise UnexpectedSenderError("Unexpected message sender:", address, (self.udpIP, self.udpPort))
        except socket.timeout as e:
            raise e
        except BaseException as e:
            raise e

        return data

    def write(self, cmd: str, **kwargs):
        if self.write_termination is not None:
            cmd = cmd + self.write_termination
        if "encoding" in kwargs:
            cmd = cmd.encode(encoding=kwargs["encoding"])
        else:
            cmd = cmd.encode(encoding=self.encoding)
        try:
            self.skt.sendto(cmd, (self.udpIP, self.udpPort))
        except BaseException as e:
            raise e
        pass

    def write_raw(self, cmd: bytes, **kwargs):
        if self.write_termination is not None:
            cmd = cmd + bytes(self.write_termination, self.encoding)
        try:
            self.skt.sendto(cmd, (self.udpIP, self.udpPort))
        except BaseException as e:
            raise e
        pass

    pass


class UnexpectedSenderError(Exception):
    """Exception raised when the sender of a UDP message is unexpected."""
    def __init__(self, message, sender, expected_sender):
        super().__init__(message)
        self.sender = sender
        self.expected_sender = expected_sender

    pass


pass
