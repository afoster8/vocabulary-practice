import json
import os
import csv

def save_to_json(data, file_path, message_label):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            try:
                json_data = json.load(file)
            except json.JSONDecodeError:
                json_data = []
    else:
        json_data = []

    json_data.append(data)
    
    for row in json_data:
        row['level'] = 0 if not 'level' in row.keys() else row['level']

    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(json_data, file, ensure_ascii=False, indent=4)
    except Exception as e:
        message_label.config(text=f'File {file_path} is not valid.')
        return
      
    message_label.config(text='Data saved successfully!', fg='green')

def delete_from_json(key, file_name, message_label):
    if os.path.exists(file_name):
        with open(file_name, 'r', encoding='utf-8') as file:
            try:
                json_data = json.load(file) 
            except json.JSONDecodeError:
                json_data = []
    else:
        json_data = []      
        
    first_field = next(iter(json_data[0].keys()))

    filtered_data = [entry for entry in json_data if entry[first_field].strip() != key.strip()]
    deleted_data = len(json_data) - len(filtered_data)

    try:
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(filtered_data, file, ensure_ascii=False, indent=4)
    except Exception as e:
        message_label.config(text=f'File {file_name} is not valid.')
        return
    
    message_label.config(text=f'{deleted_data} records of {key} deleted', fg='green')
        
def delete_multiple_from_json(csv_file, json_file, message_label):
    if os.path.exists(json_file):
        with open(json_file, 'r', encoding='utf-8') as file:
            try:
                json_data = json.load(file)
            except json.JSONDecodeError:
                json_data = []
    else:
        json_data = []
        
    if os.path.exists(csv_file):
        with open(csv_file, 'r', encoding='utf-8') as file:
            try:
                csv_reader = csv.reader(file)
                csv_data = list(csv_reader)
            except Exception as e:
                message_label.config(text=f'CSV file {csv_file} is unreadable', fg='red')
                return
    else:
        message_label.config(text=f'CSV file {csv_file} does not exist', fg='red')
        return
      
    csv_data = [row[0] for row in csv_data]
    first_field = next(iter(json_data[0].keys()))

    filtered_data = [entry for entry in json_data if not any(entry[first_field].strip() == item.strip() for item in csv_data)]
    deleted_count = len(json_data) - len(filtered_data)
  
    try:
        with open(json_file, 'w', encoding='utf-8') as file:
            json.dump(filtered_data, file, ensure_ascii=False, indent=4)
    except Exception as e:
            message_label.config(text=f'File {json_file} is not valid.')
            return

    message_label.config(text=f'{deleted_count} records deleted', fg='green')
    
def get_headers_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)
        if isinstance(json_data, list) and json_data:
            return list(json_data[0].keys())
        elif isinstance(json_data, dict):
            return list(json_data.keys())
        else:
            raise ValueError("Unsupported JSON format or empty file")
          
def combine_terms(file_path, message_label):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            try:
                json_data = json.load(file)
            except json.JSONDecodeError:
                message_label.config(text=f'JSON file {file_path} is unreadable', fg='red')
                return
    else:
        message_label.config(text=f'JSON file {file_path} does not exist', fg='red')
        return
      
    combined_data = {}
    combined_count = 0
    
    for entry in json_data:
        first_field = list(entry.keys())[0]
        key = entry[first_field]
        if key in combined_data:
            for k, v in entry.items():
                if k != first_field:
                    if k in combined_data[key]:
                        if k == 'level':
                            combined_data[key][k] = min(combined_data[key][k], v)
                        else:
                            existing_values = set(combined_data[key][k].split(', '))
                            if v not in existing_values:
                                combined_data[key][k] += f', {v}'
                    else:
                        combined_data[key][k] = v
            combined_count += 1
        else:
            combined_data[key] = entry

    filtered_data = [entry for entry in combined_data.values()]
  
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(filtered_data, file, ensure_ascii=False, indent=4)
    except Exception as e:
            message_label.config(text=f'File {file_path} is not valid.')
            return

    message_label.config(text=f'{combined_count} records combined', fg='green')