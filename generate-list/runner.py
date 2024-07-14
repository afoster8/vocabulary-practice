import tkinter as tk
from classes.add_csv import AddCSV
from classes.add_free_text import AddFreeText
from classes.delete_csv import DeleteCSV
from classes.delete_free_text import DeleteFreeText
from classes.combine import Combine

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Vocabulary List Generator')

        self.screens = {
            'home': tk.Frame(self),
            'add_csv': AddCSV(self),
            'add_free_text': AddFreeText(self),
            'delete_csv': DeleteCSV(self),
            'delete_free_text': DeleteFreeText(self),
            'combine': Combine(self)
        }

        self.current_screen = None

        self.setup_home_screen()
        self.center_window()

    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - self.winfo_reqwidth()) // 2 - 150
        y = (screen_height - self.winfo_reqheight()) // 2 - 150

        self.geometry('+{}+{}'.format(x, y))

    def setup_home_screen(self):
        for screen in self.screens.values():
            screen.grid_forget()
            
        self.intro_label = tk.Label(self, text='Vocabulary List Tool', font=('Helvetica', 16))
        self.intro_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        blurb_text = "Choose from one of the following options to manage your vocabulary lists."
        self.blurb_label = tk.Label(self, text=blurb_text, wraplength=400, justify='left')
        self.blurb_label.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 10))

        switch_to_add_csv_button = tk.Button(self, text='1: Add Entries using CSV', command=lambda: self.switch_screen('add_csv'))
        switch_to_add_csv_button.grid(row=2, column=0, padx=5, pady=5)

        switch_to_add_field_button = tk.Button(self, text='2: Add Entries', command=lambda: self.switch_screen('add_free_text'))
        switch_to_add_field_button.grid(row=2, column=1, padx=5, pady=5)

        switch_to_delete_csv_button = tk.Button(self, text='3: Delete Entries using CSV', command=lambda: self.switch_screen('delete_csv'))
        switch_to_delete_csv_button.grid(row=3, column=0, padx=5, pady=5)

        switch_to_delete_field_button = tk.Button(self, text='4: Delete Entries',command=lambda: self.switch_screen('delete_free_text'))
        switch_to_delete_field_button.grid(row=3, column=1, padx=5, pady=5)
        
        switch_to_combine_fields_button = tk.Button(self, text='5: Combine Entries',command=lambda: self.switch_screen('combine'))
        switch_to_combine_fields_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
        
        self.rebind()
        self.bind('<Escape>', lambda event: self.destroy())

    def switch_screen(self, screen_name, event=None):
        self.hide_home_buttons()
        if self.current_screen:
            self.current_screen.grid_forget()
            self.my_unbind()

        self.screens[screen_name].grid(row=1, column=0, columnspan=2, padx=0, pady=0)
        self.current_screen = self.screens[screen_name]
        
        if screen_name == 'home':
            self.rebind()
            self.setup_home_screen()
        else:
            self.screens[screen_name].rebind()
            
    def rebind(self):
        self.bind('1', lambda event: self.switch_screen('add_csv'))
        self.bind('2', lambda event: self.switch_screen('add_free_text'))
        self.bind('3', lambda event: self.switch_screen('delete_csv'))
        self.bind('4', lambda event: self.switch_screen('delete_free_text'))
        self.bind('5', lambda event: self.switch_screen('combine'))
            
    def my_unbind(self):
        self.unbind('1')
        self.unbind('2')
        self.unbind('3')
        self.unbind('4')
        self.unbind('5')

    def hide_home_buttons(self):
        for widget in self.winfo_children():
            if isinstance(widget, tk.Button):
                widget.grid_forget()
        self.blurb_label.grid_forget()
        self.intro_label.grid_forget()
        self.my_unbind()

if __name__ == '__main__':
    app = App()
    app.mainloop()
