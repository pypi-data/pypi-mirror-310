
"""
Abstract base classes for handling ZeroMQ socket operations.
"""

import abc
import threading
import zmq
from zmq.eventloop import ioloop, zmqstream

from brainmaze_zmq.utils import (
    setup_request_socket, setup_reply_socket, setup_publisher_socket,
    setup_subscriber_socket, setup_pull_socket, is_socket_alive
)

class ABExitHandler(abc.ABC):
    """
    Abstract base class for handling an exit signal via a ZeroMQ PULL socket.
    """
    def __init__(self):
        """
        Initialize the ABExitHandler with context and socket attributes.
        """
        self.exit_socket: zmq.Socket = None
        self.context: zmq.Context = None

    def setup_exit_handler(self, port: int):
        """
        Set up a PULL socket to listen for an exit signal.

        Args:
            port (int): The port to bind the PULL socket to.
        """
        if self.context is None:
            self.context = zmq.Context()

        self.exit_socket = setup_pull_socket(port, self.context)
        stream_pull = zmqstream.ZMQStream(self.exit_socket)
        stream_pull.on_recv(self.on_recv_exit)

    def on_recv_exit(self, msg):
        """
        Handle receiving an exit signal.

        Args:
            msg (list): The message received via the PULL socket.
        """
        if msg[0] == b'Exit':
            ioloop.IOLoop.instance().add_callback(self.stop)

    def kill_exit_handler(self):
        """
        Close the exit socket and clean up resources.
        """
        if self.exit_socket is not None:
            self.exit_socket.close()
            self.exit_socket = None

    @abc.abstractmethod
    def stop(self):
        """
        Abstract method to be implemented by subclasses to handle stopping operations.
        """


class ABReplyHandler(abc.ABC):
    """
    Abstract base class for handling a REPLY mechanism via a ZeroMQ REP socket.
    """
    def __init__(self):
        """
        Initialize the ABReplyHandler with context and socket attributes
        """
        self.reply_socket: zmq.Socket = None
        self.context: zmq.Context = None

    def setup_reply_handler(self, port: int):
        """
        Set up a REP socket to handle incoming requests.

        Args:
            port (int): The port to bind the REP socket to.
        """
        if self.context is None:
            self.context = zmq.Context()

        self.reply_socket = setup_reply_socket(port, self.context)
        stream_rep = zmqstream.ZMQStream(self.reply_socket)
        stream_rep.on_recv(self.reply)

    def kill_reply_handler(self):
        """
        Close the reply socket and clean up resources.
        """
        if self.reply_socket is not None:
            self.reply_socket.close()
            self.reply_socket = None

    @abc.abstractmethod
    def reply(self, msg):
        """
        Abstract method to handle incoming messages and provide a reply.

        Args:
            msg (list): The message received via the REP socket.
        """


class ABRequestHandler(abc.ABC):

    """
    Abstract base class for handling requests via a ZeroMQ REQ socket.
    """
    def __init__(self):
        """
        Initialize the ABRequestHandler with context and socket attributes.
        """
        self.request_socket: zmq.Socket = None
        self.request_port: int = None
        self.context: zmq.Context = None
        self.pending_requests: list = None
        self.lock: threading.Lock = None

    def setup_request_handler(self, port: int):
        """
        Set up a REQ socket to send requests.

        Args:
            port (int): The port to connect the REQ socket to.
        """
        self.request_port = port
        if self.context is None:
            self.context = zmq.Context()

        self.request_socket = setup_request_socket(self.request_port, self.context)

    def kill_request_handler(self):
        """
        Close the request socket and clean up resources.
        """
        if self.request_socket is not None:
            if is_socket_alive(self.request_socket):
                self.request_socket.close()
                self.request_socket = None

    def request_reply(self, msg):
        """
        Send a request and wait for a reply.

        Args:
            msg (str): The request message to send.

        Returns:
            Any: The reply received from the server.
        """
        self.request_socket.send_string(msg)
        return self.request_socket.recv_pyobj()  # zmq.NOBLOCK


class ABPublisherHandler(abc.ABC):  # done as send_multipart
    """
    Abstract base class for publishing messages via a ZeroMQ PUB socket.
    """
    def __init__(self):
        """
        Initialize the ABPublisherHandler with context and socket attributes.
        """
        self.publisher_socket: zmq.Socket = None
        self.context: zmq.Context = None

    def setup_publisher_handler(self, port: int):
        """
        Set up a PUB socket to publish messages.

        Args:
            port (int): The port to bind the PUB socket to.
        """
        if self.context is None:
            self.context = zmq.Context()

        self.publisher_socket = setup_publisher_socket(port, self.context)

    def kill_publisher_handler(self):
        """
        Close the publisher socket and clean up resources.
        """
        if self.publisher_socket is not None:
            self.publisher_socket.close()
            self.publisher_socket = None

    def publish(self, topic: str, msg: tuple):
        """
        Publish a message with a topic.

        Args:
            topic (str): The topic for the message.
            msg (tuple): The message to publish.
        """
        self.publisher_socket.send_multipart((topic.encode(),) + msg)


class ABSubscriberHandler(abc.ABC):
    """
    Abstract base class for subscribing to messages via a ZeroMQ SUB socket.
    """
    def __init__(self):
        """
        Initialize the ABSubscriberHandler with context and socket attributes.
        """
        self.subscriber_socket: zmq.Socket = None
        self.context: zmq.Context = None

    def setup_subscriber_handler(self, port: int, topic: str):
        """
        Set up a SUB socket to subscribe to messages on a topic.

        Args:
            port (int): The port to connect the SUB socket to.
            topic (str): The topic to subscribe to.
        """
        if self.context is None:
            self.context = zmq.Context()

        self.subscriber_socket = setup_subscriber_socket(port, topic, self.context)
        stream_sub = zmqstream.ZMQStream(self.subscriber_socket)
        stream_sub.on_recv(self.on_recv_data)

    def kill_subscriber_handler(self):
        """
        Close the subscriber socket and clean up resources.
        """
        if self.subscriber_socket is not None:
            self.subscriber_socket.close()
            self.subscriber_socket = None

    @abc.abstractmethod
    def on_recv_data(self, msg):
        """
        Abstract method to handle incoming data.

        Args:
            msg (list): The message received via the SUB socket.
        """
