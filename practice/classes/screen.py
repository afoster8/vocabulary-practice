import json
import os
import random
import tkinter as tk
import classes.convert as cv

class Screen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.app = parent
        self.data = None
        self.current_word = None
        self.current_index = 0
        self.level_threshold = 10
        self.correct_count = 0
        self.total_count = 0
        self.answered_incorrectly = False
        self.end_of_list = False
        self.identifier_field = None
        self.field_names_to_check = []
        self.create_widgets()
        
    def create_widgets(self):
        self.question_label = tk.Label(self, text='', font=('Helvetica', 16))
        self.question_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        
        self.answer_entry = tk.Entry(self, width=20)
        self.answer_entry.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
        self.answer_entry.bind('<Return>', self.check_answer)
        self.answer_entry.focus_set()
        
        self.next_button = tk.Button(self, text='Next', command=self.next_word)
        self.next_button.grid(row=2, column=0, columnspan=3, pady=10)
        
        self.message_label = tk.Label(self, text='')
        self.message_label.grid(row=3, column=0, columnspan=3, padx=10, pady=10)
        
        self.return_home_button = tk.Button(self, text='Home', command=self.return_home)
        self.return_home_button.grid(row=4, column=0, columnspan=3, pady=10)
        
    def rebind(self):
        self.app.bind('<Home>', lambda event: self.return_home())
        
    def my_unbind(self):
        self.app.unbind('<Home>')   
        
    def load_data(self):
        file_path = self.app.file_path
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                try:
                    json_data = json.load(file)
                    self.data = [word for word in json_data if word.get('level', 0) <= self.level_threshold]
                    random.shuffle(self.data) 
                    self.correct_count = 0
                    self.total_count = 0
                except json.JSONDecodeError:
                    self.data = []
        else:
            self.data = []
            
        self.identifier_field = list(self.data[0].keys())[0] 
        excluded_fields = [self.identifier_field, 'level']
        self.field_names_to_check = [field for field in self.data[0].keys() if field not in excluded_fields]
        
    def next_word(self):
        if self.data:
            if self.total_count > 0 and self.total_count % len(self.data) == 0:
                self.display_score()
                return
            self.current_index = self.total_count % len(self.data)
            self.current_word = self.data[self.current_index]
            self.question_label.config(text=f"{self.current_word[self.identifier_field]}")
            self.answer_entry.delete(0, tk.END)
            self.message_label.config(text='')
            self.total_count += 1
            self.answered_incorrectly = False
        else:
            self.question_label.config(text="No data available.")
            self.answer_entry.grid_remove()
            self.next_button.grid_remove()
        
    def check_answer(self, event=None):
        if self.end_of_list:
            self.end_of_list = False
            self.next_word()
        elif self.search_fields():
            self.next_word()
        else:
            self.message_label.config(text='Incorrect. Try again!', fg='red')
            self.answered_incorrectly = True
            self.level_down()
                
    def search_fields(self):
        answer = self.answer_entry.get().strip()
        answer_kana = cv.romajiToJapanese(self.answer_entry.get().strip())
        
        for field_name in self.field_names_to_check:
            if answer == self.current_word.get(field_name) or answer_kana == self.current_word.get(field_name):
                if not self.answered_incorrectly:
                    self.correct_count += 1
                    self.level_up()
                return True
        
        return False
    
    def level_up(self):
        self.current_word['level'] = min(self.current_word.get('level', 0) + 1, 10)  
        self.save_data()
        
    def level_down(self):
        self.current_word['level'] = max(self.current_word.get('level', 0) - 1, 0)  
    
    def save_data(self):
        file_path = self.app.file_path
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)
            
    def return_home(self):
        self.data = None
        self.current_word = None
        self.current_index = 0
        self.level_threshold = 10
        self.correct_count = 0
        self.total_count = 0
        self.answered_incorrectly = False
        self.end_of_list = False
        self.identifier_field = None
        self.field_names_to_check = []
        self.app.switch_screen('home')

    def display_score(self):
        self.end_of_list = True
        percentage_correct = (self.correct_count / self.total_count) * 100
        self.message_label.config(text=f'Score: {self.correct_count}/{self.total_count} ({percentage_correct:.2f}% correct)', fg='blue')
        self.correct_count = 0
        self.total_count = 0
        self.answered_incorrectly = False