import socket
import platform

def set_keepalive(s: socket.socket, 
                  after_idle_sec: int = 1,
                  interval_sec: int = 3,
                  max_fails: int = 5) -> None:
    if platform.system() == "Linux":
        s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, after_idle_sec)
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, interval_sec)
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, max_fails)
    elif platform.system() == "Windows":
        # Default value in the registry is 2 hours
        s.ioctl(socket.SIO_KEEPALIVE_VALS, (1, 60 * 60 * 2 * 1000, interval_sec * 1000))
    elif platform.system() == "Darwin":
        TCP_KEEPALIVE = 0x10

        s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        s.setsockopt(socket.IPPROTO_TCP, TCP_KEEPALIVE, interval_sec)
    else:
        raise NotImplementedError