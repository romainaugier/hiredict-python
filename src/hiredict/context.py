from __future__ import annotations

import socket
import atexit
import io
import traceback

import hiredict.log as log
import hiredict.net as net


REPLY_BUF_SIZE = 256

class HiRedictContext():
    
    def __init__(self,
                 host: str,
                 port: int,
                 db: int = 0,
                 protocol: int = 2,
                 connection_timeout: float = 5.0,
                 recv_timeout: float = 0.1) -> None:
        self._host = host
        self._port = port
        self._db = db
        self._protocol = 0
        self._running = False

        self._socket = None

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