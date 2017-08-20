import tkinter as tk

from chadt.chadt_view import ChadtView


class ClientView(ChadtView):

    def __init__(self, controller):
        super().__init__("Chadt Client", controller)
        self.text = None
        self.message_entry = None

    def add_config_widgets(self):

        l2 = tk.Label(self.root, text="Choose Server host/port:")
        server_host_entry = tk.Entry(self.root)
        server_host_entry.insert(0, "localhost")
        server_port_entry = tk.Entry(self.root)
        server_port_entry.insert(0, "50000")

        b = tk.Button(self.root, text="Confirm", command=self.controller.confirm_button(server_host_entry, server_port_entry))
        
        l2.grid(row=0, column=0)
        server_host_entry.grid(row=0, column=1)
        server_port_entry.grid(row=0, column=2)

        b.grid(row=3, column=0)

    def add_main_widgets(self):
        self.text = tk.Text(self.root, height=10, width=80)
        self.text.bind("<Key>", lambda x: "break") 
        # this^ bind effectively makes the text widget read-only
        scroll = tk.Scrollbar(self.root, command=self.text.yview)
        self.text["yscrollcommand"] = scroll.set

        self.message_entry = tk.Entry(self.root)
        self.message_entry.insert(0, "Enter messages here")
        self.root.bind("<Return>", self.controller.send_message_button(self.message_entry))
        send_message_button = tk.Button(self.root, text="Send Message", command=self.controller.send_message_button(self.message_entry))

        username_entry = tk.Entry(self.root)
        username_entry.insert(0, "Enter username here")
        update_username_button = tk.Button(self.root, text="Update Username", command=self.controller.update_username_button(username_entry))
        
        self.text.grid(row=0, column=0)
        scroll.grid(row=0, column=1)

        username_entry.grid(row=0, column=1)
        update_username_button.grid(row=1, column=1)

        self.message_entry.grid(row=2, column=0)
        send_message_button.grid(row=2, column=1)

    def display_new_text_message(self, message):
        self.text.insert(tk.END, message+"\n")
        self.text.see(tk.END)

    def clear_entry_box(self):
        self.message_entry.delete(0, tk.END)
