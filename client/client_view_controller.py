from chadt.chadt_view_controller import ChadtViewController
from chadt.chadt_exceptions import UsernameCurrentlyUnstableException, UsernameTooLongException

from client.client import Client
from client.client_chat_view import ClientChatView
from client.client_config_view import ClientConfigView


class ClientViewController(ChadtViewController):
    
    def __init__(self):
        super().__init__()
        self.client = None

    def start_controller(self):
        self.setup_config_view()

    def confirm_button(self, server_host_entry, server_port_entry):
        def f():
            server_port = server_port_entry.get()
            server_host = server_host_entry.get()
            if not self.is_valid_port_num(server_port):
                self.view.invalid_port_warning()
            else:
                self.swap_to_chat_view()
                self.create_client(server_host, int(server_port))
        return f

    def setup_config_view(self):
        self.view = ClientConfigView()
        self.view.set_confirm_button_command(self.confirm_button)
        self.view.add_quit_function(self.quit)

    def swap_to_chat_view(self):
        self.view.quit()
        self.setup_chat_view()

    def setup_chat_view(self):
        self.view = ClientChatView()
        self.view.set_message_entry_button_commands(self.send_message_button)
        self.view.set_username_entry_button_commands(self.send_username_button)
        self.view.add_quit_function(self.quit)

    def create_client(self, server_host, server_port):
        self.client = Client(server_host, server_port)
        self.client.add_message_in_queue_observer(self.display_new_text_message)
        self.client.add_connected_users_observer(self.update_list_of_users)
        self.client.set_username_rejected_observer(self.respond_to_rejected_username)
        self.client.set_shutdown_observer(self.respond_to_shutdown)
        self.client.start_client()

    def display_new_text_message(self, message_queue):
        message = message_queue.pop(0)
        self.view.display_new_text_message(message.get_display_string())

    def send_message_button(self, message_entry):
        def f(event = None):
            recipient = self.view.get_users_box_selection()
            self.client.add_message_to_out_queue(message_entry.get(), recipient)
            self.view.clear_message_entry_box()
        return f

    def quit(self):
        if self.client is not None:
            self.client.shutdown_client()
        self.view.quit()

    def send_username_button(self, username_entry):
        def f(event = None):
            try:
                requested_username = username_entry.get()
                self.client.send_username_request(requested_username)
                self.view.clear_username_entry_box()
            except UsernameCurrentlyUnstableException:
                self.view.warning_message("Username Unstable", "Username is currently being updated, please wait until it is set to try again.")
            except UsernameTooLongException:
                # should make a constants file for numbers like sender max length
                self.view.warning_message("Username Too Long", "Username requested is too long, please limit it to 16 chars")
                
        return f

    def update_list_of_users(self, user_list):
        self.view.update_list_of_users(user_list)

    def respond_to_rejected_username(self):
        self.view.warning_message("Username Rejected", "Username requested was rejected by the server.")

    def respond_to_shutdown(self):
        self.view.warning_message("Server Shutdown", "Server was shutdown, client shutting down now.")
        self.quit()
