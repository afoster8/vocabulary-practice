import tkinter as tk
from tkinter import ttk
from utils.json_handler import save_to_json

class AddFreeText(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.app = parent
        self.create_widgets()

    def create_widgets(self):
        mode_label = tk.Label(self, text='Select Mode:')
        mode_label.grid(row=0, column=0, padx=10, pady=10)        
        self.mode_var = tk.StringVar()
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
                self.kill_kanji_fields()
                self.language_entry.grid()
                language_label.grid()
                self.populate_word_fields()
                self.language_entry.focus_set()
                self.populate_buttons()
                if hasattr(self, 'message_label'):
                  self.message_label.grid_remove()
            else:
                self.kill_word_fields()
                self.language_entry.grid_remove()
                language_label.grid_remove()
                self.populate_kanji_fields()
                self.kanji_entry.focus_set()
                self.populate_buttons()
                if hasattr(self, 'message_label'):
                  self.message_label.grid_remove()
        
        self.populate_kanji_fields()
        self.kanji_entry.focus_set()
        self.populate_buttons()
        
        self.mode_var.trace_add('write', mode_changed)
        
    def kill_kanji_fields(self):
        self.kanji_label.destroy()
        self.onyomi_label.destroy()
        self.kunyomi_label.destroy()
        self.kanji_entry.destroy()
        self.onyomi_entry.destroy()
        self.kunyomi_entry.destroy()
      
    def kill_word_fields(self):
        self.word_label.destroy()
        self.meaning_label.destroy()
        self.word_entry.destroy()
        self.meaning_entry.destroy()
        
    def clear_entries(self):
      if self.mode_var.get() == 'kanji':
          self.kanji_entry.delete(0, tk.END)
          self.onyomi_entry.delete(0, tk.END)
          self.kunyomi_entry.delete(0, tk.END)
          self.kanji_entry.focus_set()
      elif self.mode_var.get() == 'word':
          self.word_entry.delete(0, tk.END)
          self.meaning_entry.delete(0, tk.END)
          self.word_entry.focus_set()
        
    def populate_word_fields(self):
        self.word_label = tk.Label(self, text='Word:')
        self.word_label.grid(row=2, column=0, padx=10, pady=10)
        
        self.word_entry = tk.Entry(self, width=30)
        self.word_entry.grid(row=2, column=1, padx=10, pady=10)
        
        self.meaning_label = tk.Label(self, text='Meaning:')
        self.meaning_label.grid(row=3, column=0, padx=10, pady=0)
        
        self.meaning_entry = tk.Entry(self, width=30)
        self.meaning_entry.grid(row=3, column=1, padx=10, pady=10)
        self.meaning_entry.bind('<Return>', self.save_to_json)
    
    def populate_kanji_fields(self):
        self.kanji_label = tk.Label(self, text='Kanji:')
        self.kanji_label.grid(row=2, column=0, padx=10, pady=10)
        
        self.kanji_entry = tk.Entry(self, width=30)
        self.kanji_entry.grid(row=2, column=1, padx=10, pady=10)
        
        self.onyomi_label = tk.Label(self, text='Onyomi:')
        self.onyomi_label.grid(row=3, column=0, padx=10, pady=10)
        
        self.onyomi_entry = tk.Entry(self, width=30)
        self.onyomi_entry.grid(row=3, column=1, padx=10, pady=10)
        self.onyomi_entry.bind('<Return>', self.save_to_json)
        
        self.kunyomi_label = tk.Label(self, text='Kunyomi:')
        self.kunyomi_label.grid(row=4, column=0, padx=10, pady=10) 
        
        self.kunyomi_entry = tk.Entry(self, width=30)
        self.kunyomi_entry.grid(row=4, column=1, padx=10, pady=10)
        self.kunyomi_entry.bind('<Return>', self.save_to_json)
        
    def populate_buttons(self):
        save_button = tk.Button(self, text='Save to JSON', command=self.save_to_json)
        save_button.grid(row=5, column=0, columnspan=2, pady=10)
        
        return_home_button = tk.Button(self, text='Home', command=self.return_home)
        return_home_button.grid(row=6, column=0, columnspan=3, pady=10)
    
    def save_to_json(self, event=None):
        self.message_label = tk.Label(self, text='', fg='red')
        self.message_label.grid(row=7, column=0, columnspan=2, pady=10)
          
        if self.mode_var.get() == 'kanji':
            kanji = self.kanji_entry.get()
            onyomi = self.onyomi_entry.get()
            kunyomi = self.kunyomi_entry.get()
            save_to_json([kanji, onyomi, kunyomi], 'kanji', self.message_label)
            self.message_label.grid()
            self.clear_entries()
            
        elif self.mode_var.get() == 'word':
            word = self.word_entry.get()
            meaning = self.meaning_entry.get()
            language = self.language_entry.get()
            save_to_json([word, meaning], 'word', self.message_label, language)
            self.message_label.grid()
            self.clear_entries()
    
    def return_home(self):
        self.app.switch_screen('home')


