import tkinter as tk
from tkinter import filedialog, ttk
from utils.json_handler import save_to_json, get_headers_from_json

class AddFreeText(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.app = parent
        self.max_idx = 3
        self.file_name = None
        self.create_widgets()

    def create_widgets(self):
        self.intro_label = tk.Label(self, text='Add vocab terms', font=('Helvetica', 16))
        self.intro_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        
        blurb_text = "This tool allows you to add terms to a JSON vocab list. Begin with an existing vocabulary list with the Enter from JSON option, or start a new list with the Enter from scratch option."
        blurb_label = tk.Label(self, text=blurb_text, wraplength=400, justify='left')
        blurb_label.grid(row=1, column=0, columnspan=3, padx=10, pady=(0, 10))
        
        mode_label = tk.Label(self, text='Select Input Mode:')
        mode_label.grid(row=2, column=0, padx=10, pady=10)
        self.input_mode_var = tk.StringVar()
        input_mode_option = ttk.OptionMenu(self, self.input_mode_var, 'Enter from JSON', 'Enter from JSON', 'Enter from scratch')
        input_mode_option.grid(row=2, column=1, padx=10, pady=10)
        
        self.input_mode_var.trace_add('write', self.input_mode_changed)
        
        self.populate_initial_ui()
        
    def rebind(self):
        self.app.bind('<Control-b>', lambda event: self.browse_json_file())
        self.app.bind('<Home>', lambda event: self.return_home())
        
    def my_unbind(self):
        self.app.unbind('<Control-b>')
        self.app.unbind('<Home>')
        
    def populate_initial_ui(self):
        self.browse_json_label = tk.Label(self, text='Select JSON file')
        self.browse_json_label.grid(row=3, column=0, padx=10, pady=10)
        self.json_entry = tk.Entry(self, width=20)
        self.json_entry.grid(row=3, column=1, padx=10, pady=10)
        self.browse_json_button = tk.Button(self, text='Browse', command=self.browse_json_file)
        self.browse_json_button.grid(row=3, column=2, padx=10, pady=10)
        
        self.headers_label = tk.Label(self, text='Enter Headers:')
        self.headers_entry = tk.Entry(self, width=20)
        self.headers_button = tk.Button(self, text='Enter', command=self.create_fields_from_headers)
        
        self.message_label = tk.Label(self, text='', fg='red')
        
        self.populate_buttons(self.max_idx)

    def input_mode_changed(self, *args):
        if self.input_mode_var.get() == 'Enter from JSON':
            self.file_name = None
            self.clear_dynamic_fields()
            self.headers_label.grid_remove()
            self.headers_entry.grid_remove()
            self.headers_entry.grid_remove()
            self.message_label.grid_remove()
            self.browse_json_label.grid(row=3, column=0, padx=10, pady=10)
            self.json_entry.grid(row=3, column=1, padx=10, pady=10)
            self.browse_json_button.grid(row=3, column=2, padx=10, pady=10)
            self.json_entry.delete(0, tk.END)
            
        else:
            self.file_name = None
            self.clear_dynamic_fields()
            self.browse_json_label.grid_remove()
            self.json_entry.grid_remove()
            self.browse_json_button.grid_remove()
            self.message_label.grid_remove()
            self.headers_label.grid(row=3, column=0, padx=10, pady=10)
            self.headers_entry.grid(row=3, column=1, padx=10, pady=10)
            self.headers_button.grid(row=3, column=2, padx=10, pady=10)
            self.headers_entry.bind('<Return>', self.create_fields_from_headers)
    
    def browse_json_file(self):
        self.file_name = filedialog.askopenfilename(filetypes=[('JSON files', '*.json')])
        if self.file_name:
            headers = get_headers_from_json(self.file_name)
            self.populate_dynamic_fields(headers)
            self.json_entry.delete(0, tk.END)
            self.json_entry.insert(0, self.file_name)
        
    def create_fields_from_headers(self, event=None):
        if len(self.headers_entry.get()) > 0:
            headers = [header.strip() for header in self.headers_entry.get().split(',')]
            self.populate_dynamic_fields(headers)
    
    def populate_dynamic_fields(self, headers):
        self.clear_dynamic_fields()
        self.entries = []
        for idx, header in enumerate(headers):
            if header.lower() == 'level': 
                continue
            label = tk.Label(self, text=f'{header.capitalize()}:')
            label.grid(row=4 + idx, column=0, padx=10, pady=10)
            entry = tk.Entry(self, width=20)
            entry.grid(row=4 + idx, column=1, padx=10, pady=10)
            self.entries.append((label, entry, header))
            
        self.entries[-1][1].bind('<Return>', self.save_to_json)
            
        self.max_idx = idx + 4
        self.populate_buttons(self.max_idx)
        self.message_label.grid_remove()

    def clear_dynamic_fields(self):
        if hasattr(self, 'entries'):
            for label, entry, _ in self.entries:
                label.destroy()
                entry.destroy()
        self.entries = []

    def populate_buttons(self, idx):
        if hasattr(self, 'save_button'):
            self.save_button.destroy()
        if hasattr(self, 'return_home_button'):
            self.return_home_button.destroy()
            
        self.save_button = tk.Button(self, text='Save to JSON', command=self.save_to_json)
        self.save_button.grid(row=idx+1, column=0, columnspan=3, pady=10)
        
        self.return_home_button = tk.Button(self, text='Home', command=self.return_home)
        self.return_home_button.grid(row=idx+2, column=0, columnspan=3, pady=10)
        
        self.max_idx = idx + 3
    
    def save_to_json(self, event=None):
        data = {}
        if not hasattr(self, 'entries') or not self.entries:
            self.message_label.config(text='Please enter headers', fg='red')
            self.message_label.grid(row=self.max_idx, column=0, columnspan=3, pady=10)
            return
            
        for _, entry, header in self.entries:
            data[header] = entry.get()
            
        if data[self.entries[0][2]] == '':
            self.message_label.config(text='First field cannot be empty', fg='red')
            self.message_label.grid(row=self.max_idx, column=0, columnspan=3, pady=10)
            return
        
        if not self.file_name:
            self.file_name = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        
        save_to_json(data, self.file_name, self.message_label)
        
        self.clear_entries()
        self.message_label.grid(row=self.max_idx, column=0, columnspan=3, pady=10)
        self.entries[0][1].focus_set()

    def clear_entries(self):
        for _, entry, _ in self.entries:
            entry.delete(0, tk.END)
    
    def return_home(self):
        self.clear_dynamic_fields()
        self.json_entry.delete(0, tk.END)
        self.message_label.grid_remove()
        self.file_name = None
        self.app.switch_screen('home')


