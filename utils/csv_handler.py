import csv
import json
import os

def convert_csv_to_json(file_path, mode, message_label, language=None):
    if not os.path.isfile(file_path):
        message_label.config(text=f'File {file_path} not found', fg='red')
        return
    
    if mode == 'kanji':
        target_file = 'files/kanji.json'
        expected_fields = ['kanji', 'onyomi', 'kunyomi']
    elif mode == 'word':
        if len(language) == 0:
            message_label.config(text='Must fill out language field', fg='red')
            return
        target_file = f'files/{language}_words.json'
        expected_fields = ['word', 'meaning']
    else:
        message_label.config(text='Invalid mode specified', fg='red')
        return
    
    try:
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            data = list(csv_reader)
        
        filtered_data = []
        
        for row in data:
            if mode == 'kanji' and len(row) == 3 and len(row[0]) > 0:
                filtered_data.append({expected_fields[i]: row[i].strip() for i in range(3)})
            elif mode == 'word' and len(row) == 2 and len(row[0]) > 0:
                filtered_data.append({expected_fields[i]: row[i].strip() for i in range(2)})
        
        num_empty_first_field = sum(1 for row in data if len(row[0]) == 0)

        if os.path.exists(target_file):
            with open(target_file, 'r', encoding='utf-8') as json_file:
                try:
                    json_data = json.load(json_file)
                except json.JSONDecodeError:
                    json_data = []
        else:
            json_data = []
        
        json_data.extend(filtered_data)
        
        with open(target_file, 'w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, ensure_ascii=False, indent=4)
            
        if num_empty_first_field > 0:
            message_label.config(text=f'{num_empty_first_field} rows with empty first field were skipped', fg='orange')
        else:
            message_label.config(text=f'CSV data converted and added to {target_file}', fg='green')
    
    except Exception as e:
        message_label.config(text=f'An error occurred! {str(e)}', fg='red')
