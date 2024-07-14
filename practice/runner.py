import os
import tkinter as tk
from tkinter import filedialog
from classes.screen import Screen

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Vocabulary Practice Game')

        self.screens = {
            'home': tk.Frame(self),
            'other': Screen(self)
        }

        self.current_screen = None
        self.file_path = None
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
            
        self.intro_label = tk.Label(self, text='Vocabulary Practice Game', font=('Helvetica', 16))
        self.intro_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        
        blurb_text = "Practice vocabulary using JSON vocabulary list."
        self.blurb_label = tk.Label(self, text=blurb_text, wraplength=400, justify='left')
        self.blurb_label.grid(row=1, column=0, columnspan=3, padx=10, pady=(0, 10))
        
        self.browse_json_label = tk.Label(self, text='Select JSON file')
        self.browse_json_label.grid(row=3, column=0, padx=10, pady=10)
        self.json_entry = tk.Entry(self, width=20)
        self.json_entry.grid(row=3, column=1, padx=10, pady=10)
        self.json_entry.bind('<Return>', self.on_json_entry_return)
        self.browse_json_button = tk.Button(self, text='Browse', command=self.browse_json_file)
        self.browse_json_button.grid(row=3, column=2, padx=10, pady=10)
        
        self.rebind()
        self.bind('<Escape>', lambda event: self.destroy())
        
    def browse_json_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[('JSON files', '*.json')])
        if self.file_path:
            self.json_entry.delete(0, tk.END)
            self.json_entry.insert(0, self.file_path)
            self.switch_screen('other')  
        
    def hide_home_buttons(self):
        self.browse_json_label.grid_forget()
        self.browse_json_button.grid_forget()
        self.json_entry.grid_forget()
        self.intro_label.grid_forget()
        self.blurb_label.grid_forget()
                
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
            self.screens[screen_name].load_data()
            self.screens[screen_name].next_word()
            self.screens[screen_name].rebind()
            
    def on_json_entry_return(self, event):
        self.switch_screen('other')

    def rebind(self):
        self.bind('<Control-b>', lambda event: self.browse_json_file())
            
    def my_unbind(self):
        self.unbind('<Control-b>')

if __name__ == '__main__':
    app = App()
    app.mainloop()
