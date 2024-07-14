import csv
import json
import os
from tkinter import filedialog

def convert_csv_to_json(file_path, headers, message_label):
    default_file = '../files/output.json'
    if not os.path.isfile(file_path):
        message_label.config(text=f'File {file_path} not found', fg='red')
        return
    
    if not headers:
        message_label.config(text='You must specify headers', fg='red')
        return
      
    headers = [header.strip() for header in headers]
    
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as csvfile:
            csv_reader = csv.DictReader(csvfile, fieldnames=headers)
            csv_data = [row for row in csv_reader if row[headers[0]].strip()]
            num_empty_first_field = sum(1 for row in csv_reader if not row[headers[0]].strip())
        
        target_file = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json"), ("All files", "*.*")])

        if os.path.exists(target_file):
            with open(target_file, 'r', encoding='utf-8') as json_file:
                try:
                    json_data = json.load(json_file)
                except json.JSONDecodeError:
                    json_data = []
        else:
            json_data = []
        
        json_data.extend(csv_data)
        
        for row in json_data:
            row['level'] = 0 if not 'level' in row.keys() else row['level']
        
        if target_file:
            with open(target_file, 'w', encoding='utf-8') as json_file:
                json.dump(json_data, json_file, ensure_ascii=False, indent=4)
        else:
            message_label.config(text=f'No file chosen', fg='red')
            return

        if num_empty_first_field > 0:
            message_label.config(text=f'{num_empty_first_field} rows with empty first field were skipped', fg='orange')
        else:
            message_label.config(text=f'CSV data converted and added to {target_file if target_file else default_file}', fg='green')
    
    except Exception as e:
        message_label.config(text=f'An error occurred! {e}', fg='red')
