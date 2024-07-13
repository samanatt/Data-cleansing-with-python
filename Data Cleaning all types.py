import os
import pandas as pd
import xlrd
import openpyxl
import json
#import docx2txt

# Function to replace forbidden characters
def replace_forbidden_chars(text):
    forbidden_chars = [
        "'", '"', '`', '~', '!', '@', '#', '$', '%', '^', '&', '*', ')', '-', '+', '=', '|', '}', ']', '[', '{', '?', '.', ':', ';', '//', '\\', '/'
    ]
    
    for char in forbidden_chars:
        text = str(text).replace(char, "_")
    
    return text

def process_excel_file(input_file, output_file):
    try:
        file_extension = os.path.splitext(input_file)[1].lower()
        
        if file_extension == ".xls":
            # Process .xls files using xlrd
            print(f"Processing .xls file: {input_file}")
            df = pd.read_excel(input_file, engine='xlrd')
            df.columns = [replace_forbidden_chars(col) for col in df.columns]
            df.to_csv(output_file, index=False, encoding='utf-16')
            print(f"Output file '{output_file}' created.")
        
        elif file_extension == ".xlsx":
            # Process .xlsx files using openpyxl
            print(f"Processing .xlsx file: {input_file}")
            df = pd.read_excel(input_file, engine='openpyxl')
            df.columns = [replace_forbidden_chars(col) for col in df.columns]
            df.to_csv(output_file, index=False, encoding='utf-16')
            print(f"Output file '{output_file}' created.")
    
    except Exception as e:
        print(f"Error processing file '{input_file}': {e}")

def process_files(folder_path):
    output_files = []
    for root, dirs, filenames in os.walk(folder_path):
        for filename in filenames:
            input_file = os.path.join(root, filename)
            output_file = os.path.join(root, f"out_{os.path.splitext(filename)[0]}.csv")
            process_excel_file(input_file, output_file)
            output_files.append(output_file)
            os.remove(input_file)  # Delete the input file
    
    return output_files

def clean_json_data(data):
    if isinstance(data, dict):
        cleaned_dict = {}
        for key, value in data.items():
            cleaned_key = replace_forbidden_chars(key)
            cleaned_value = clean_json_data(value)
            cleaned_dict[cleaned_key] = cleaned_value
        return cleaned_dict
    elif isinstance(data, list):
        cleaned_list = []
        for item in data:
            cleaned_item = clean_json_data(item)
            cleaned_list.append(cleaned_item)
        return cleaned_list
    elif isinstance(data, str):
        return replace_forbidden_chars(data)
    else:
        return data

def process_csv_file(input_file, output_file):
    try:
        print(f"Processing CSV file: {input_file}")
        df = pd.read_csv(input_file, encoding='utf-16')
        df.columns = [replace_forbidden_chars(col) for col in df.columns]
        df.to_csv(output_file, index=False, encoding='utf-16')
        print(f"Output file '{output_file}' created.")
    except Exception as e:
        print(f"Error processing file '{input_file}': {e}")

def process_text_file(input_file, output_file):
    try:
        print(f"Processing text file: {input_file}")
        with open(input_file, 'r', encoding='utf-16', errors='ignore') as input_f, open(output_file, 'w', encoding='utf-16') as output_f:
            for line in input_f:
                cleaned_line = replace_forbidden_chars(line)
                output_f.write(cleaned_line)
        print(f"Output file '{output_file}' created.")
    except Exception as e:
        print(f"Error processing file '{input_file}': {e}")

def process_json_file(input_file, output_file):
    try:
        print(f"Processing JSON file: {input_file}")
        with open(input_file, 'r', encoding='utf-16', errors='ignore') as input_f:
            json_string = input_f.readlines()
        data = json.loads(json_string)
        cleaned_data = clean_json_data(data)
        with open(output_file, 'w', encoding='utf-16') as output_f:
            json.dump(cleaned_data, output_f, indent=4, ensure_ascii=False)
        print(f"Output file '{output_file}' created.")
    except Exception as e:
        print(f"Error processing file '{input_file}': {e}")

#def process_doc_file(input_file, output_file):
    #try:
        #print(f"Processing .doc file: {input_file}")
        #text = docx2txt.process(input_file)
        #cleaned_text = replace_forbidden_chars(text)
        #with open(output_file, 'w', encoding='utf-16') as output_f:
            #output_f.write(cleaned_text)
        #print(f"Output file '{output_file}' created.")
    #except Exception as e:
        #print(f"Error processing file '{input_file}': {e}")

def process_folder(folder_path):
    output_files = []
    for root, dirs, filenames in os.walk(folder_path):
        for filename in filenames:
            input_file = os.path.join(root, filename)
            file_extension = os.path.splitext(filename)[1].lower()
            output_file = os.path.join(root, f"out_{os.path.splitext(filename)[0]}.csv")
            failed_file = os.path.join(root, f"failed_{filename}")

            try:
                if file_extension == ".csv":
                    process_csv_file(input_file, output_file)
                elif file_extension == ".txt":
                    process_text_file(input_file, output_file)
                elif file_extension == ".json":
                    process_json_file(input_file, output_file)
                elif file_extension in [".xls", ".xlsx"]:
                    process_excel_file(input_file, output_file)
                else:
                    print(f"Unsupported file type: {input_file}")
                    os.rename(input_file, failed_file)
                    continue  # Skip unsupported file types

                output_files.append(output_file)
                os.remove(input_file)  # Delete the input file
            except Exception as e:
                print(f"Error processing file '{input_file}': {e}")
                os.rename(input_file, failed_file)  # Move failed files to failed_
                continue  # Skip failed files

    return output_files

folder_path = r"D:\data"  # Replace with the actual path to your folder

output_files = process_folder(folder_path)
#print(f"Output files: {output_files}")
#print(f"Failed files: {failed_files}")