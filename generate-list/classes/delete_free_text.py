import tkinter as tk
from tkinter import filedialog
from utils.json_handler import delete_from_json

class DeleteFreeText(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.app = parent
        self.file_path = None
        self.create_widgets()

    def create_widgets(self):
        self.intro_label = tk.Label(self, text='Delete terms', font=('Helvetica', 16))
        self.intro_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        
        blurb_text = "This tool allows you to delete terms from a JSON vocabulary list. The tool will delete all terms with initial fields that match the search term."
        blurb_label = tk.Label(self, text=blurb_text, wraplength=400, justify='left')
        blurb_label.grid(row=1, column=0, columnspan=3, padx=10, pady=(0, 10))
        
        json_label = tk.Label(self, text='Select JSON File:')
        json_label.grid(row=2, column=0, padx=10, pady=10) 
        self.json_entry = tk.Entry(self, width=20)
        self.json_entry.grid(row=2, column=1, padx=10, pady=10)
        browse_button = tk.Button(self, text='Browse', command=self.browse_json_file)
        browse_button.grid(row=2, column=2, padx=10, pady=10)
      
        self.search_label = tk.Label(self, text='Search:')
        self.search_label.grid(row=4, column=0, padx=10, pady=10)
        
        self.search_entry = tk.Entry(self, width=20)
        self.search_entry.grid(row=4, column=1, padx=10, pady=10)
        self.search_entry.bind('<Return>', self.delete) 
        
        delete_button = tk.Button(self, text='Delete', command=self.delete)
        delete_button.grid(row=4, column=2, padx=10, pady=10)
            
        return_home_button = tk.Button(self, text='Home', command=self.return_home)
        return_home_button.grid(row=5, column=0, columnspan=3, pady=10)
        
        self.message_label = tk.Label(self, text='', fg='red')
        
    def rebind(self):
        self.app.bind('<Control-b>', lambda event: self.browse_json_file())
        self.app.bind('<Home>', lambda event: self.return_home())
        
    def my_unbind(self):
        self.app.unbind('<Control-b>')
        self.app.unbind('<Home>')
        
    def browse_json_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[('JSON files', '*.json')])
        if self.file_path:
            self.json_entry.delete(0, tk.END)
            self.json_entry.insert(0, self.file_path)
            self.search_entry.focus_set()
    
    def delete(self, event=None):
        if len(self.json_entry.get()) > 0:
            if len(self.search_entry.get()) > 0:
                delete_from_json(self.search_entry.get(), self.file_path, self.message_label)
            else: 
                self.message_label.config(text=f'Search entry must not be empty', fg='red')
        else:
            self.message_label.config(text=f'Please choose a source JSON file', fg='red')
            
        self.message_label.grid(row=6, column=0, columnspan=3, pady=10)
            
        self.search_entry.delete(0, tk.END)
        self.search_entry.focus_set()
        
    def return_home(self):
        self.file_path = None
        self.json_entry.delete(0, tk.END)
        self.search_entry.delete(0, tk.END)
        self.message_label.grid_remove()
        self.app.switch_screen('home')
