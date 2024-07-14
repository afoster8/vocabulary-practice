import tkinter as tk
from tkinter import filedialog, ttk
from utils.json_handler import delete_multiple_from_json

class DeleteCSV(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.app = parent
        self.create_widgets()

    def create_widgets(self):
        csv_label = tk.Label(self, text='Select CSV File:')
        csv_label.grid(row=0, column=0, padx=10, pady=10)
        self.csv_entry = tk.Entry(self, width=20)
        self.csv_entry.grid(row=0, column=1, padx=10, pady=10)
        browse_button = tk.Button(self, text='Browse', command=self.browse_csv_file)
        browse_button.grid(row=0, column=2, padx=10, pady=10)
        
        mode_label = tk.Label(self, text='Select Mode:')
        mode_label.grid(row=1, column=0, padx=10, pady=10)        
        self.mode_var = tk.StringVar()
        self.mode_var.set('kanji')  
        mode_option = ttk.OptionMenu(self, self.mode_var, 'kanji', 'kanji', 'word')
        mode_option.grid(row=1, column=1, padx=10, pady=10)
        
        language_label = tk.Label(self, text='Enter Language:')
        language_label.grid(row=2, column=0, padx=10, pady=10)
        self.language_entry = tk.Entry(self, width=20)
        self.language_entry.grid(row=2, column=1, padx=10, pady=10)
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
        
        convert_button = tk.Button(self, text='Convert CSV to JSON', command=self.convert_csv)
        convert_button.grid(row=3, column=0, columnspan=3, pady=10)
        
        return_home_button = tk.Button(self, text='Home', command=self.return_home)
        return_home_button.grid(row=4, column=0, columnspan=3, pady=10)
    
    def browse_csv_file(self):
        file_path = filedialog.askopenfilename(filetypes=[('CSV files', '*.csv')])
        if file_path:
            self.csv_entry.delete(0, tk.END)
            self.csv_entry.insert(0, file_path)
    
    def convert_csv(self):
        self.message_label = tk.Label(self, text='', fg='red')
        self.message_label.grid(row=7, column=0, columnspan=3, pady=10)
            
        file_path = self.csv_entry.get()
        delete_multiple_from_json(file_path, self.mode_var.get(), self.message_label, self.language_entry.get().strip())
          
        self.csv_entry.delete(0, tk.END)
        
    def return_home(self):
        self.app.switch_screen('home')

