import tkinter as tk
from tkinter import filedialog
from utils.csv_handler import convert_csv_to_json

class AddCSV(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.app = parent
        self.create_widgets()

    def create_widgets(self):
        self.intro_label = tk.Label(self, text='Add terms using a CSV', font=('Helvetica', 16))
        self.intro_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        
        blurb_text = "This tool allows you to use a CSV file to generate a new JSON vocabulary list, or add vocabulary terms to an existing JSON vocabulary list."
        blurb_label = tk.Label(self, text=blurb_text, wraplength=400, justify='left')
        blurb_label.grid(row=1, column=0, columnspan=3, padx=10, pady=(0, 10))     
           
        csv_label = tk.Label(self, text='Select CSV File:')
        csv_label.grid(row=2, column=0, padx=10, pady=10) 
        self.csv_entry = tk.Entry(self, width=20)
        self.csv_entry.grid(row=2, column=1, padx=10, pady=10)
        browse_button = tk.Button(self, text='Browse', command=self.browse_csv_file)
        browse_button.grid(row=2, column=2, padx=10, pady=10)
        
        headers_label = tk.Label(self, text='Enter Headers:')
        headers_label.grid(row=3, column=0, padx=10, pady=10)
        self.headers_entry = tk.Entry(self, width=20)
        self.headers_entry.grid(row=3, column=1, padx=10, pady=10)
        self.headers_entry.bind('<Return>', self.convert_csv)
        
        convert_button = tk.Button(self, text='Convert CSV to JSON', command=self.convert_csv)
        convert_button.grid(row=4, column=0, columnspan=3, pady=10)
        
        return_home_button = tk.Button(self, text='Home', command=self.return_home)
        return_home_button.grid(row=5, column=0, columnspan=3, pady=10)
        
        self.message_label = tk.Label(self, text='', fg='red')
        
    def rebind(self):
        self.app.bind('<Control-b>', lambda event: self.browse_csv_file())
        self.app.bind('<Home>', lambda event: self.return_home())
        
    def my_unbind(self):
        self.app.unbind('<Control-b>')
        self.app.unbind('<Home>')    
        
    def browse_csv_file(self):
        file_path = filedialog.askopenfilename(filetypes=[('CSV files', '*.csv')])
        if file_path:
            self.csv_entry.delete(0, tk.END)
            self.csv_entry.insert(0, file_path)
    
    def convert_csv(self, event=None):
        file_path = self.csv_entry.get()
        headers = self.headers_entry.get().strip().split(',')
        
        convert_csv_to_json(file_path, headers, self.message_label)
        self.message_label.grid(row=6, column=0, columnspan=3, pady=10)
          
        self.csv_entry.delete(0, tk.END)
        self.headers_entry.delete(0, tk.END)
        
    def return_home(self):
        self.message_label.grid_remove()
        self.csv_entry.delete(0, tk.END)
        self.headers_entry.delete(0, tk.END)
        self.app.switch_screen('home')


