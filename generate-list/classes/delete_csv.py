import tkinter as tk
from tkinter import filedialog
from utils.json_handler import delete_multiple_from_json

class DeleteCSV(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.app = parent
        self.create_widgets()

    def create_widgets(self):
        self.intro_label = tk.Label(self, text='Delete multiple terms using CSV', font=('Helvetica', 16))
        self.intro_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        
        blurb_text = "This tool allows you to delete multiple terms from a JSON vocabulary list file using a CSV list."
        blurb_label = tk.Label(self, text=blurb_text, wraplength=400, justify='left')
        blurb_label.grid(row=1, column=0, columnspan=3, padx=10, pady=(0, 10))
        
        csv_label = tk.Label(self, text='Select CSV File:')
        csv_label.grid(row=2, column=0, padx=10, pady=10)
        self.csv_entry = tk.Entry(self, width=20)
        self.csv_entry.grid(row=2, column=1, padx=10, pady=10)
        browse_button = tk.Button(self, text='Browse', command=self.browse_csv_file)
        browse_button.grid(row=2, column=2, padx=10, pady=10)
        
        json_label = tk.Label(self, text='Select JSON File:')
        json_label.grid(row=3, column=0, padx=10, pady=10) 
        self.json_entry = tk.Entry(self, width=20)
        self.json_entry.grid(row=3, column=1, padx=10, pady=10)
        browse_button = tk.Button(self, text='Browse', command=self.browse_json_file)
        browse_button.grid(row=3, column=2, padx=10, pady=10)
        
        convert_button = tk.Button(self, text='Delete', command=self.convert_csv)
        convert_button.grid(row=5, column=0, columnspan=3, pady=10)
        
        return_home_button = tk.Button(self, text='Home', command=self.return_home)
        return_home_button.grid(row=6, column=0, columnspan=3, pady=10)
        
        self.message_label = tk.Label(self, text='', fg='red')
        
    def rebind(self):
        self.app.bind('<Control-b>', lambda event: self.browse_csv_file())
        self.app.bind('<Control-c>', lambda event: self.browse_json_file())
        self.app.bind('<Home>', lambda event: self.return_home())
        
    def my_unbind(self):
        self.app.unbind('<Control-b>')
        self.app.unbind('<Control-c>')
        self.app.unbind('<Home>')        
    
    def browse_csv_file(self):
        csv_file_path = filedialog.askopenfilename(filetypes=[('CSV files', '*.csv')])
        if csv_file_path:
            self.csv_entry.delete(0, tk.END)
            self.csv_entry.insert(0, csv_file_path)
            
    def browse_json_file(self):
        json_file_path = filedialog.askopenfilename(filetypes=[('JSON files', '*.json')])
        if json_file_path:
            self.json_entry.delete(0, tk.END)
            self.json_entry.insert(0, json_file_path)
    
    def convert_csv(self):
        self.message_label.grid(row=7, column=0, columnspan=3, pady=10)
        json_file = self.json_entry.get()
        csv_file = self.csv_entry.get()
        
        if len(json_file) > 0:
            if len(csv_file) > 0:
                delete_multiple_from_json(csv_file, json_file, self.message_label)
            else: 
                self.message_label.config(text=f'Please choose a source CSV file', fg='red')
        else:
            self.message_label.config(text=f'Please choose a source JSON file', fg='red')
          
        self.csv_entry.delete(0, tk.END)
        self.json_entry.delete(0, tk.END)
        
    def return_home(self):
        self.message_label.grid_remove()
        self.csv_entry.delete(0, tk.END)
        self.json_entry.delete(0, tk.END)
        self.app.switch_screen('home')

