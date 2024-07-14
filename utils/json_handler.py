import json
import os
import csv

kanji_file = 'files/kanji.json'
words_file_template = 'files/{}_words.json'

history = {'kanji': [], 'word': {}}

def save_to_json(data, mode, message_label, language=None):
    if mode == 'kanji':
        save_kanji_to_json(data, message_label)
    elif mode == 'word':
        save_word_to_json(data, language, message_label)

def save_kanji_to_json(data, message_label):
    kanji = data[0]
    onyomi = data[1]
    kunyomi = data[2]

    if os.path.exists(kanji_file):
        with open(kanji_file, 'r', encoding='utf-8') as file:
            try:
                json_data = json.load(file)
            except json.JSONDecodeError:
                json_data = []
    else:
        json_data = []
        
    if len(kanji) == 0:
        message_label.config(text='Must fill out kanji field', fg='red')
        return

    history['kanji'].append(json_data.copy())
    entry = {'kanji': kanji, 'onyomi': onyomi, 'kunyomi': kunyomi}
    json_data.append(entry)

    with open(kanji_file, 'w', encoding='utf-8') as file:
        json.dump(json_data, file, ensure_ascii=False, indent=4)
    
    message_label.config(text='Data saved successfully!', fg='green')
      
def save_word_to_json(data, language, message_label):
    word = data[0]
    meaning = data[1]

    words_file = words_file_template.format(language)

    if os.path.exists(words_file):
        with open(words_file, 'r', encoding='utf-8') as file:
            try:
                json_data = json.load(file)
            except json.JSONDecodeError:
                json_data = []
    else:
        json_data = []
        
    if len(word) == 0:
        message_label.config(text='Must fill out word field', fg='red')
        return
    
    if len(language) == 0:
        message_label.config(text='Must fill out language field', fg='red')
        return

    if language not in history['word']:
        history['word'][language] = []

    history['word'][language].append(json_data.copy())
    entry = {'word': word, 'meaning': meaning}
    json_data.append(entry)

    with open(words_file, 'w', encoding='utf-8') as file:
        json.dump(json_data, file, ensure_ascii=False, indent=4)
        
    message_label.config(text='Data saved successfully!', fg='green')

def delete_from_json(key, mode, message_label, language=None):
    if mode == 'word':
        file_name = words_file_template.format(language)
    elif mode == 'kanji':
        file_name = kanji_file

    if os.path.exists(file_name):
        with open(file_name, 'r', encoding='utf-8') as file:
            try:
                json_data = json.load(file)
            except json.JSONDecodeError:
                json_data = []
    else:
        json_data = []

    filtered_data = [entry for entry in json_data if entry[mode].strip() != key.strip()]
    deleted_data = len(json_data) - len(filtered_data)

    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(filtered_data, file, ensure_ascii=False, indent=4)
    
    message_label.config(text=f'{deleted_data} records of {key} deleted', fg='green')
        
def delete_multiple_from_json(data_file, mode, message_label, language=None):
    if mode == 'word':
        file_name = words_file_template.format(language)
    elif mode == 'kanji':
        file_name = kanji_file

    if os.path.exists(file_name):
        with open(file_name, 'r', encoding='utf-8') as file:
            try:
                json_data = json.load(file)
            except json.JSONDecodeError:
                json_data = []
    else:
        json_data = []
        
    if os.path.exists(data_file):
        with open(data_file, 'r', encoding='utf-8') as file:
            try:
                csv_reader = csv.reader(file)
                csv_data = list(csv_reader)
            except Exception as e:
                message_label.config(text=f'CSV file {data_file} is unreadable', fg='red')
                return
    else:
        message_label.config(text=f'CSV file {data_file} does not exist', fg='red')
        return

    filtered_data = [entry for entry in json_data if not any(entry[mode].strip() == item[0].strip() for item in csv_data)]
    deleted_count = len(json_data) - len(filtered_data)
  
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(filtered_data, file, ensure_ascii=False, indent=4)

    message_label.config(text=f'{deleted_count} records deleted', fg='green')