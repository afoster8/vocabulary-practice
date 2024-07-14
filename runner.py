import tkinter as tk
from classes.add_csv import AddCSV
from classes.add_free_text import AddFreeText
from classes.delete_csv import DeleteCSV
from classes.delete_free_text import DeleteFreeText

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('CSV Converter and JSON Manipulator')

        self.screens = {
            'home': tk.Frame(self),
            'add_csv': AddCSV(self),
            'add_free_text': AddFreeText(self),
            'delete_csv': DeleteCSV(self),
            'delete_free_text': DeleteFreeText(self)
        }

        self.current_screen = None

        self.setup_home_screen()

    def setup_home_screen(self):
        for screen in self.screens.values():
            screen.grid_forget()
            
        self.intro_label = tk.Label(self, text='Welcome to CSV Converter and JSON Manipulator', font=('Helvetica', 16))
        self.intro_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        switch_to_add_csv_button = tk.Button(self, text='Add from CSV', command=self.switch_to_add_csv)
        switch_to_add_csv_button.grid(row=1, column=0, padx=5, pady=5)

        switch_to_add_field_button = tk.Button(self, text='Add by Field Entry', command=self.switch_to_add_free_text)
        switch_to_add_field_button.grid(row=1, column=1, padx=5, pady=5)

        switch_to_delete_csv_button = tk.Button(self, text='Delete Entries using CSV', command=self.switch_to_delete_csv)
        switch_to_delete_csv_button.grid(row=2, column=0, padx=5, pady=5)

        switch_to_delete_field_button = tk.Button(self, text='Delete by Search', command=self.switch_to_delete_free_text)
        switch_to_delete_field_button.grid(row=2, column=1, padx=5, pady=5)

    def switch_to_add_csv(self):
        self.hide_home_buttons()
        self.switch_screen('add_csv')

    def switch_to_add_free_text(self):
        self.hide_home_buttons()
        self.switch_screen('add_free_text')

    def switch_to_delete_csv(self):
        self.hide_home_buttons()
        self.switch_screen('delete_csv')

    def switch_to_delete_free_text(self):
        self.hide_home_buttons()
        self.switch_screen('delete_free_text')

    def switch_screen(self, screen_name):
        if self.current_screen:
            self.current_screen.grid_forget()
            if hasattr(self.current_screen, 'message_label'):
                self.current_screen.message_label.destroy()

        self.intro_label.grid_forget()
        self.screens[screen_name].grid(row=1, column=0, columnspan=2, padx=0, pady=0)
        self.current_screen = self.screens[screen_name]
        
        if screen_name == 'home':
            self.setup_home_screen()

    def hide_home_buttons(self):
        for widget in self.winfo_children():
            if isinstance(widget, tk.Button):
                widget.grid_forget()

if __name__ == '__main__':
    app = App()
    app.mainloop()
