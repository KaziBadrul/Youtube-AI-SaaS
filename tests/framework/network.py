"""Universal network denial trap for offline test suites."""
import http.client
import socket
import urllib.request
from typing import Any


class NetworkAccessDeniedError(RuntimeError):
    """Raised when an outbound network call is attempted in an offline test suite."""
    pass


_DENIED_MESSAGE = "Network access prohibited in offline test suites (T003 boundary)"


def _deny_call(*args: Any, **kwargs: Any) -> Any:
    raise NetworkAccessDeniedError(_DENIED_MESSAGE)


class NetworkTrap:
    """
    Context manager and controller that intercepts socket and HTTP operations,
    preventing any external network access.
    """

    def __init__(self) -> None:
        self._orig_socket_connect = None
        self._orig_socket_connect_ex = None
        self._orig_socket_sendto = None
        self._orig_socket_sendall = None
        self._orig_create_connection = None
        self._orig_getaddrinfo = None
        self._orig_gethostbyname = None
        self._orig_gethostbyname_ex = None
        self._orig_gethostbyaddr = None
        self._orig_http_connect = None
        self._orig_https_connect = None
        self._orig_urlopen = None
        self._installed = False

    def install(self) -> "NetworkTrap":
        if self._installed:
            return self

        # Save originals
        self._orig_socket_connect = socket.socket.connect
        self._orig_socket_connect_ex = socket.socket.connect_ex
        self._orig_socket_sendto = socket.socket.sendto
        self._orig_socket_sendall = socket.socket.sendall
        self._orig_create_connection = socket.create_connection
        self._orig_getaddrinfo = socket.getaddrinfo
        self._orig_gethostbyname = socket.gethostbyname
        self._orig_gethostbyname_ex = socket.gethostbyname_ex
        self._orig_gethostbyaddr = socket.gethostbyaddr
        self._orig_http_connect = http.client.HTTPConnection.connect
        self._orig_https_connect = http.client.HTTPSConnection.connect
        self._orig_urlopen = urllib.request.urlopen

        # Patch with denials
        socket.socket.connect = _deny_call
        socket.socket.connect_ex = _deny_call
        socket.socket.sendto = _deny_call
        socket.socket.sendall = _deny_call
        socket.create_connection = _deny_call
        socket.getaddrinfo = _deny_call
        socket.gethostbyname = _deny_call
        socket.gethostbyname_ex = _deny_call
        socket.gethostbyaddr = _deny_call
        http.client.HTTPConnection.connect = _deny_call
        http.client.HTTPSConnection.connect = _deny_call
        urllib.request.urlopen = _deny_call

        self._installed = True
        return self

    def uninstall(self) -> None:
        if not self._installed:
            return

        socket.socket.connect = self._orig_socket_connect
        socket.socket.connect_ex = self._orig_socket_connect_ex
        socket.socket.sendto = self._orig_socket_sendto
        socket.socket.sendall = self._orig_socket_sendall
        socket.create_connection = self._orig_create_connection
        socket.getaddrinfo = self._orig_getaddrinfo
        socket.gethostbyname = self._orig_gethostbyname
        socket.gethostbyname_ex = self._orig_gethostbyname_ex
        socket.gethostbyaddr = self._orig_gethostbyaddr
        http.client.HTTPConnection.connect = self._orig_http_connect
        http.client.HTTPSConnection.connect = self._orig_https_connect
        urllib.request.urlopen = self._orig_urlopen

        self._installed = False

    def __enter__(self) -> "NetworkTrap":
        return self.install()

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.uninstall()


_GLOBAL_TRAP = NetworkTrap()


def install_global_network_trap() -> None:
    """Globally enforce network prohibition in current process."""
    _GLOBAL_TRAP.install()


def uninstall_global_network_trap() -> None:
    """Uninstall the global network trap."""
    _GLOBAL_TRAP.uninstall()
