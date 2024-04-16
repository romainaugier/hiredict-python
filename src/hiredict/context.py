from __future__ import annotations

import socket
import atexit
import io
import traceback

import hiredict.log as log
import hiredict.net as net


REPLY_BUF_SIZE = 256


class HiRedictReply():

    __slots__ = (
        "_buffer"
    )
    
    def __init__(self) -> None:
        self._buffer = io.BytesIO()

    def _parse_reply(self) -> bytes:
        r_bufs = [v for v in self._buffer.getvalue().split(b"\r\n") if v.strip() != b""]
        
        if len(r_bufs) != 2:
            return r_bufs[0]

        length, value = r_bufs

        length = int(length.replace(b"$", b""))

        value = value[0:length]

        return value

    @staticmethod
    def Error() -> HiRedictReply:
        return HiRedictReply()

    def append(self, content: bytes) -> None:
        self._buffer.write(content)

    def asBytes(self) -> bytes:
        return self._parse_reply()

    def asString(self) -> str:
        return str(self._parse_reply())

    def asInteger(self) -> int:
        return int(self._parse_reply())

    def Ok(self) -> bool:
        return self._buffer.getvalue()[:3] == b"+OK"

    def Error(self) -> bool:
        return self._buffer.getbuffer().nbytes == 0 or self._buffer.getvalue()[:4] == b"-ERR"

    def ErrorMessage(self) -> str:
        if self._buffer.getbuffer().nbytes == 0:
            return "No error message was returned"

        return self._buffer.getvalue()[3:].decode(error="replace")

    def Pong(self) -> bool:
        return self._buffer.getvalue()[:5] == b"+PONG"

    def Denied(self) -> bool:
        return self._buffer.getvalue()[:7] == b"-DENIED"

class HiRedictContext():
    
    def __init__(self, host: str, port: int, connection_timeout: float = 5.0, recv_timeout: float = 0.1) -> None:
        self._host = host
        self._port = port
        self._running = False

        log.debug("Initializing HiRedictContext")

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.settimeout(connection_timeout)

        # No delay
        self._socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        # Keep alive
        net.set_keepalive(self._socket)
        
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

        self._socket.settimeout(recv_timeout)

        pingReply = self.sendCommand("PING")

        if pingReply.Denied():
            log.critical("Access to redict is denied")
            log.critical(pingReply.str())
            return
        elif pingReply.Error():
            log.critical("Error during initial ping command to redict")
            return

        self._running = True

        atexit.register(self.close)

        log.debug("HiRedict context running")

    def isRunning(self) -> bool:
        return self._running

    def sendCommand(self, command: str) -> HiRedictReply:
        commandFmt = "{0}\r\n".format(command).encode()

        try:
            self._socket.send(commandFmt)

            reply = HiRedictReply()

            while True:
                buf = self._socket.recv(REPLY_BUF_SIZE)

                reply.append(buf)

                nread = len(buf)

                if nread < REPLY_BUF_SIZE:
                    break
            
            return reply
        except socket.timeout:
            return reply
        except OSError:
            log.critical(f"Cannot send command \"{commandFmt}\" to redict-db, socket error (host: {self._host}, port: {self._port})")
            log.critical(traceback.format_exc())
            return HiRedictReply.Error()

    def close(self) -> None:
        if self._running:
            log.debug("Closing HiRedict context")

            self._socket.close()
            self._running = False