import socket
from .event_handler import SocketEventHandler
from echo_harvest.helpers.logger import logging as logger

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
port = 8000
serversocket.bind((host, port))


def start_socket_connection():
    serversocket.listen(5)
    logger.info("SOCKET::SERVER:STARTED: Server started and listening")
    while 1:
        (clientsocket, address) = serversocket.accept()
        logger.info("SOCKET::SERVER:CLIENT_REQUEST: Connect to {}".format(address))
        data = clientsocket.recv(1024).decode()
        handler = SocketEventHandler(data)
        clientsocket.send(handler.generate_response().encode())
        logger.info("SOCKET::SERVER:CLIENT_RESPONSE: Sent status response")
