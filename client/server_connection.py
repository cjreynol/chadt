from socket import socket, SO_REUSEADDR, SOL_SOCKET, timeout

from chadt.chadt_component import ChadtComponent
from chadt.message import Message
from chadt.message_type import MessageType


class ServerConnection(ChadtComponent):

    TRANSCEIVER_TIMEOUT = 0.5

    def __init__(self, username, server_host, server_port, client_in_queue, client_out_queue):
        self.username = username

        self.client_in_queue = client_in_queue
        self.client_out_queue = client_out_queue

        self.transceiver = None
        self.pre_startup(username, server_host, server_port)

        super().__init__()

    def start(self):
        super().start(self.transceive)

    def shutdown(self):
        super().shutdown(self.transceiver)

    def transceive(self):
        self.receive_messages()
        self.transmit_messages()

    def transmit_messages(self):
        if len(self.client_out_queue) > 0:
            message_text = self.client_out_queue.pop(0)
            bytes_message = self.add_header(message_text)
            self.transceiver.sendall(bytes_message)

    def add_header(self, message_text):
        message = Message(message_text, self.username)
        return message.make_bytes()

    def receive_messages(self):
        try:
            header = self.transceiver.recv(Message.HEADER_LENGTH)
            if len(header) > 0:
                message_length =  Message.get_header(header)[3]
                message_text = self.transceiver.recv(message_length)
                self.add_message_to_in_queue(header + message_text)
        except timeout:
            pass

    def add_message_to_in_queue(self, byte_array):
        message = Message.bytes_to_message(byte_array)
        self.client_in_queue.append(message)

    def pre_startup(self, username, server_host, server_port):
        self.transceiver = self.create_socket()
        self.connect_socket(username, server_host, server_port)
        self.transceiver.settimeout(ServerConnection.TRANSCEIVER_TIMEOUT)

    def create_socket(self):
        s = socket()
        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        return s

    def connect_socket(self, username, server_host, server_port):
        self.transceiver.connect((server_host, server_port))
        username_request = Message("", username, MessageType.USERNAME_REQUEST)
        self.transceiver.sendall(username_request.make_bytes())

        response = self.transceiver.recv(Message.HEADER_LENGTH)
        message = Message.bytes_to_message(response)

        if message.message_type == MessageType.USERNAME_REJECTED:
            raise RuntimeError("Username rejected, try again.")
        elif message.message_type == MessageType.USERNAME_ACCEPTED:
            pass
        else:
            raise RuntimeError("Unexpected message type.")
