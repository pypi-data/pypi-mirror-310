
"""
Socket utility functions for ZeroMQ and general networking operations.
"""

import socket
import time
import zmq
from pythonping import ping

def send_exit_signal(port, context=None):
    """
    Sends an exit signal to a specific ZeroMQ port.

    Args:
        port (int): Port to send the exit signal.
        context (zmq.Context, optional): ZeroMQ context to use.
                                        If not provided, a new one is created.

    Returns:
        bool: Always returns False (placeholder for success indication).
    """
    context_provided = context is not None
    if context_provided is False:
        context = zmq.Context()

    success = False
    zmq_exit_socket = context.socket(zmq.PUSH)
    zmq_exit_socket.setsockopt(zmq.LINGER, 0)
    zmq_exit_socket.setsockopt(zmq.SNDTIMEO, 20)
    zmq_exit_socket.connect(
        f"tcp://localhost:{port}")  # Connect to the process / thread
    zmq_exit_socket.send(b'Exit')

    time.sleep(.1)
    zmq_exit_socket.close()
    time.sleep(.1)

    if context_provided is False:
        context.term()

    time.sleep(.1)
    return success

def setup_pull_socket(port, context):
    """
    Sets up a ZeroMQ PULL socket.

    Args:
        port (int): Port to bind the socket to.
        context (zmq.Context): ZeroMQ context to use.

    Returns:
        zmq.Socket: Configured PULL socket.
    """
    zmq_exit_socket = context.socket(zmq.PULL)
    zmq_exit_socket.setsockopt(zmq.LINGER, 0)
    zmq_exit_socket.bind(f"tcp://*:{port}")
    time.sleep(.1)
    return zmq_exit_socket

def setup_push_socket(port, context):
    """
    Sets up a ZeroMQ PUSH socket.

    Args:
        port (int): Port to connect the socket to.
        context (zmq.Context): ZeroMQ context to use.

    Returns:
        zmq.Socket: Configured PUSH socket.
    """
    zmq_exit_socket = context.socket(zmq.PUSH)
    zmq_exit_socket.setsockopt(zmq.LINGER, 0)
    zmq_exit_socket.setsockopt(zmq.SNDTIMEO, 100)
    zmq_exit_socket.connect(f"tcp://localhost:{port}")
    time.sleep(.1)
    return zmq_exit_socket

def setup_request_socket(port, context):
    """
    Sets up a ZeroMQ REQ socket.

    Args:
        port (int): Port to connect the socket to.
        context (zmq.Context): ZeroMQ context to use.

    Returns:
        zmq.Socket: Configured REQ socket.
    """
    zmq_request_socket = context.socket(zmq.REQ)
    zmq_request_socket.setsockopt(zmq.LINGER, 0)
    zmq_request_socket.setsockopt(zmq.REQ_RELAXED, 1)
    zmq_request_socket.setsockopt(zmq.REQ_CORRELATE, 1)
    zmq_request_socket.setsockopt(zmq.RCVTIMEO, 200)
    zmq_request_socket.setsockopt(zmq.SNDTIMEO, 200)
    zmq_request_socket.connect(f"tcp://localhost:{port}")
    time.sleep(.1)
    return zmq_request_socket

def setup_reply_socket(port, context):
    """
    Sets up a ZeroMQ REP socket.

    Args:
        port (int): Port to bind the socket to.
        context (zmq.Context): ZeroMQ context to use.

    Returns:
        zmq.Socket: Configured REP socket.
    """
    zmq_reply_socket = context.socket(zmq.REP)
    zmq_reply_socket.setsockopt(zmq.LINGER, 0)
    zmq_reply_socket.setsockopt(zmq.RCVTIMEO, 200)
    zmq_reply_socket.setsockopt(zmq.SNDTIMEO, 200)
    zmq_reply_socket.bind(f"tcp://*:{port}")
    time.sleep(.1)
    return zmq_reply_socket

def setup_publisher_socket(port, context):
    """
    Sets up a ZeroMQ PUB socket.

    Args:
        port (int): Port to bind the socket to.
        context (zmq.Context): ZeroMQ context to use.

    Returns:
        zmq.Socket: Configured PUB socket.
    """
    zmq_publisher_socket = context.socket(zmq.PUB)
    zmq_publisher_socket.setsockopt(zmq.LINGER, 0)
    zmq_publisher_socket.bind(f"tcp://*:{port}")
    time.sleep(.1)
    return zmq_publisher_socket

def setup_subscriber_socket(port, sub_topic, context):
    """
    Sets up a ZeroMQ SUB socket.

    Args:
        port (int): Port to connect the socket to.
        sub_topic (str): Subscription topic filter.
        context (zmq.Context): ZeroMQ context to use.

    Returns:
        zmq.Socket: Configured SUB socket.
    """
    zmq_subscriber_socket = context.socket(zmq.SUB)
    zmq_subscriber_socket.setsockopt(zmq.LINGER, 0)
    zmq_subscriber_socket.setsockopt_string(zmq.SUBSCRIBE, sub_topic)
    zmq_subscriber_socket.connect(f"tcp://localhost:{port}")
    time.sleep(.1)
    return zmq_subscriber_socket

def is_socket_alive(socket_instance: zmq.Socket):
    """
    Checks if a ZeroMQ socket is alive and operational.

    Args:
        zmq_socket (zmq.Socket): ZeroMQ socket to check.

    Returns:
        bool: True if the socket is alive, False otherwise.
    """
    if socket_instance is None:
        return False
    try:
        # Get the value of the ZMQ_EVENTS socket option
        events = socket_instance.getsockopt(zmq.EVENTS)
        # Check if the socket is readable or writable
        return (events & zmq.POLLIN) or (events & zmq.POLLOUT)
    except zmq.ZMQError:
        return False

def ping_ip(ip_address: str):
    """
    Pings an IP address to check connectivity.

    Args:
        ip_address (str): IP address to ping.

    Returns:
        bool: True if the ping is successful, False otherwise.
    """
    response = ping(ip_address, count=1, verbose=True, timeout=0.5)

    if response.success():
        return True

    return False

def check_port(ip_address: str, port: int):
    """
    Checks if a port on a given IP address is open.

    Args:
        ip_address (str): IP address to check.
        port (int): Port number to check.

    Returns:
        bool: True if the port is open, False otherwise.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)  # Timeout in seconds
    success = False
    try:
        result = sock.connect_ex((ip_address, port))
        if result == 0:
            success = True
    finally:
        sock.close()

    return success
