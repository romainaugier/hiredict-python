import socket
import log
import sys

RECV_BUF_SIZE = 256

class Console():
    
    def __init__(self, host: str, port: int) -> None:
        self._host = host
        self._port = port

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self._socket.connect((self._host, self._port))
        except:
            log.error(f"Cannot connect to Redict ({self._host}, {self._port})")
            sys.exit(1)
        
    def run(self) -> None:
        
        while True:
            input_cmd = input(f"Redict > ")

            if not input_cmd.endswith("\\r\\n"):
                input_cmd += "\\r\\n"

            try:
                self._socket.send(input_cmd.encode())
                
                resp = self._socket.recv(RECV_BUF_SIZE)
            except:
                log.error("")