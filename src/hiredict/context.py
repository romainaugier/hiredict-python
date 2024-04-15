import socket
import atexit
import io
import traceback

import hiredict.log as log


REPLY_BUF_SIZE = 256


class HiRedictReply():

    __slots__ = (
        "_buffer"
    )
    
    def __init__(self, content: bytes) -> None:
        self._buffer = io.BytesIO()
        self._buffer.write(content)

    def append(self, content: bytes) -> None:
        self._buffer.write(content)

    def str(self) -> str:
        return str(self._buffer.getvalue().decode(errors="replace"))

class HiRedictContext():

    _socket: socket.socket
    _running: bool
    
    def __init__(self, host: str, port: int, timeout: float) -> None:
        self._host = host
        self._port = port
        self._running = False

        log.debug("Initializing HiRedictContext")

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.settimeout(timeout)
        
        try:
            self._socket.connect((self._host, self._port))
        except TimeoutError:
            log.critical(f"Cannot connect to redict-db, timeout reached (host: {self._host}, port: {self._port})")
            log.critical(traceback.format_exc())
            return
        except OSError:
            log.critical(f"Cannot connect to redict-db, socket error (host: {self._host}, port: {self._port})")
            log.critical(traceback.format_exc())
            return

        if self.sendCommand("PING") is None:
            log.critical("Error during ping command sent, check the log for more informations")
            return

        self._running = True

        atexit.register(self.close)

    def isRunning(self) -> bool:
        return self._running

    def sendCommand(self, command: str) -> HiRedictReply:
        commandFmt = f"{command}\r\n\0"

        try:
            nwrite = self._socket.send(commandFmt.encode())

            if nwrite < len(commandFmt):
                log.critical(f"Cannot send command \"{command}\" to redict-db, error during socket.send (host: {self._host}, port: {self._port})")
                return None

            reply = HiRedictReply(b"")

            while True:
                buf = self._socket.recv(REPLY_BUF_SIZE)

                nread = len(buf)

                if nread == 0:
                    break

                reply.append(buf)
            
            return reply
        except TimeoutError:
            log.critical(f"Cannot send command \"{command}\" to redict-db, timeout reached (host: {self._host}, port: {self._port})")
            return None
        except OSError:
            log.critical(f"Cannot send command \"{command}\" to redict-db, socket error (host: {self._host}, port: {self._port})")
            return None

    def close(self) -> None:
        if self._running:
            self._socket.close()
            self._running = False