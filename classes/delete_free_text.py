import tkinter as tk
from tkinter import ttk
from utils.json_handler import delete_from_json

class DeleteFreeText(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.app = parent
        self.create_widgets()

    def create_widgets(self):
        mode_label = tk.Label(self, text='Select Mode:')
        mode_label.grid(row=0, column=0, padx=10, pady=10)        
        self.mode_var = tk.StringVar()
        self.mode_var.set('kanji')  
        mode_option = ttk.OptionMenu(self, self.mode_var, 'kanji', 'kanji', 'word')
        mode_option.grid(row=0, column=1, padx=10, pady=10)
        
        language_label = tk.Label(self, text='Enter Language:')
        language_label.grid(row=1, column=0, padx=10, pady=10)
        self.language_entry = tk.Entry(self, width=30)
        self.language_entry.grid(row=1, column=1, padx=10, pady=10)
        self.language_entry.grid_remove()  
        language_label.grid_remove()
        
        def mode_changed(*args):
            if self.mode_var.get() == 'word':
                self.language_entry.grid()
                language_label.grid()
                if hasattr(self, 'message_label'):
                    self.message_label.destroy()
            else:
                self.language_entry.grid_remove()
                language_label.grid_remove()
                if hasattr(self, 'message_label'):
                    self.message_label.destroy()
        
        self.mode_var.trace_add('write', mode_changed)
      
        self.search_label = tk.Label(self, text='Search:')
        self.search_label.grid(row=2, column=0, padx=10, pady=10)
        
        self.search_entry = tk.Entry(self, width=30)
        self.search_entry.grid(row=2, column=1, padx=10, pady=10)
        self.search_entry.bind('<Return>', self.delete)
        
        delete_button = tk.Button(self, text='Delete', command=self.delete)
        delete_button.grid(row=2, column=2, padx=10, pady=10)
            
        return_home_button = tk.Button(self, text='Home', command=self.return_home)
        return_home_button.grid(row=3, column=0, columnspan=3, pady=10)
    
    def delete(self, event=None):
        self.message_label = tk.Label(self, text='', fg='red')
        self.message_label.grid(row=4, column=0, columnspan=3, pady=10)
        
        if len(self.search_entry.get()) > 0:
            delete_from_json(self.search_entry.get(), self.mode_var.get(), self.message_label, self.language_entry.get())
        else: 
            self.message_label.config(text=f'Search entry must not be empty', fg='red')
            
        self.search_entry.delete(0, tk.END)
        self.search_entry.focus_set()
        
    def return_home(self):
        self.app.switch_screen('home')
