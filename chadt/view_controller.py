from chadt.system_message_handler import SystemMessageHandler


class ViewController(SystemMessageHandler):

    MIN_PORT = 0
    MAX_PORT = 65535
    
    def __init__(self):
        super().__init__()
        self.view = None

    def assign_view(self, view):
        self.view = view

    def is_valid_port_num(self, num):
        return_value = True
        try:
            num = int(num)
            if num < self.MIN_PORT or num > self.MAX_PORT:
                return_value = False
        except ValueError:
            return_value = False

        return return_value

    def quit(self):
        raise NotImplementedError("Needs to be implemented.")
