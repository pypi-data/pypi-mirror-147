import errno
import socket
import select

from websocket import WebSocket

from pwnlib.log import getLogger
from pwnlib.tubes.tube import tube

log = getLogger(__name__)


class websocket(tube):
    def __init__(self, url, headers=None, *args, **kwargs):
        if headers is None:
            headers = {}
        super(websocket, self).__init__(*args, **kwargs)
        self.closed = {"recv": False, "send": False}
        self.sock = WebSocket()
        self.url = url
        self.sock.connect(url, header=headers)

    def recv_raw(self, numb):
        if self.closed["recv"]:
            raise EOFError

        while True:
            try:
                data = self.sock.recv()
                if isinstance(data, str):
                    data = data.encode()
                break
            except socket.timeout:
                return None
            except IOError as e:
                if e.errno in (errno.EAGAIN, errno.ETIMEDOUT) or 'timed out' in e.strerror:
                    return None
                elif e.errno in (errno.ECONNREFUSED, errno.ECONNRESET):
                    self.shutdown("recv")
                    raise EOFError
                elif e.errno == errno.EINTR:
                    continue
                else:
                    raise

        if not data:
            self.shutdown("recv")
            raise EOFError

        return data

    def send_raw(self, data):
        if self.closed["send"]:
            raise EOFError

        try:
            self.sock.send_binary(data)
        except IOError as e:
            eof_numbers = (errno.EPIPE, errno.ECONNRESET, errno.ECONNREFUSED)
            if e.errno in eof_numbers or 'Socket is closed' in e.args:
                self.shutdown("send")
                raise EOFError
            else:
                raise

    def settimeout_raw(self, timeout):
        if getattr(self, 'sock', None):
            self.sock.settimeout(timeout)

    def can_recv_raw(self, timeout):
        if not self.sock or self.closed["recv"] or not self.sock.sock:
            return False

        can_recv = select.select(
            [self.sock.sock], [], [], timeout) == ([self.sock.sock], [], [])

        if not can_recv:
            return False

        try:
            self.sock.sock.recv(1, socket.MSG_PEEK)
        except EOFError:
            return False

        return True

    def connected_raw(self, direction):
        """
        Tests:

            >>> l = listen()
            >>> r = remote('localhost', l.lport)
            >>> r.connected()
            True
            >>> l.close()
            >>> time.sleep(0.1) # Avoid race condition
            >>> r.connected()
            False
        """
        # If there's no socket, it's definitely closed
        if not self.sock:
            return False

        # If we have noticed a connection close in a given direction before,
        # return fast.
        if self.closed.get(direction, False):
            return False

        # If a connection is closed in all manners, return fast
        if all(self.closed.values()):
            return False

        # Use poll() to determine the connection state
        want = {
            'recv': select.POLLIN,
            'send': select.POLLOUT,
            'any': select.POLLIN | select.POLLOUT,
        }[direction]

        poll = select.poll()
        poll.register(self, want | select.POLLHUP | select.POLLERR)

        for fd, event in poll.poll(0):
            if event & select.POLLHUP:
                self.close()
                return False
            if event & select.POLLIN:
                return True
            if event & select.POLLOUT:
                return True

        return True

    def close(self):
        if not getattr(self, 'sock', None):
            return

        self.closed['send'] = True
        self.closed['recv'] = True

        self.sock.close()
        self.sock = None
        self._close_msg()

    def _close_msg(self):
        self.info('Closed connection to %s', self.url)

    def fileno(self):
        if not self.sock:
            self.error("A closed socket does not have a file number")

        return self.sock.fileno()

    def shutdown_raw(self, direction):
        if self.closed[direction]:
            return

        self.closed[direction] = True

        if direction == "send":
            try:
                self.sock.shutdown(socket.SHUT_WR)
            except IOError as e:
                if e.errno == errno.ENOTCONN:
                    pass
                else:
                    raise

        if direction == "recv":
            try:
                self.sock.shutdown(socket.SHUT_RD)
            except IOError as e:
                if e.errno == errno.ENOTCONN:
                    pass
                else:
                    raise

        if False not in self.closed.values():
            self.close()
