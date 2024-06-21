import os
import pandas as pd
import xlrd
import json
import openpyxl
import csv
import shutil

# Function to replace forbidden characters
def replace_forbidden_chars(text):
    forbidden_chars = [
        "'", '"', '~', "!", "@", "#", "$", "%", "^", "&", "*", ")", "-", "=", "|", "}", "]", "{", "?", ".", ":"
    ]
    for char in forbidden_chars:
        text = str(text).replace(char, "_")
    return text

def process_file(input_file):
    try:
        file_extension = os.path.splitext(input_file)[1].lower()
        file_name = os.path.basename(input_file)
        dir_name = os.path.dirname(input_file)
        temp_output_file = os.path.join(dir_name, f"temp_out_{file_name}")
        final_output_file = os.path.join(dir_name, f"out_{file_name}")
        
        if file_extension in ['.xls', '.xlsx']:
            process_excel_file(input_file, temp_output_file)
        elif file_extension == '.json':
            process_json_file(input_file, temp_output_file)
        elif file_extension == '.txt':
            process_text_file(input_file, temp_output_file)
        elif file_extension == '.csv':
            process_csv_file(input_file, temp_output_file)
        else:
            print(f"Skipping unsupported file type: {input_file}")
            return

        # Delete input file
        os.remove(input_file)
        
        # Rename temp output file to final output file
        os.rename(temp_output_file, final_output_file)
        
        print(f"Processed: {input_file}")
        print(f"Output file: {final_output_file}")
    
    except Exception as e:
        print(f"Error processing file '{input_file}': {e}")
        failed_file = os.path.join(os.path.dirname(input_file), f"failed_{os.path.basename(input_file)}")
        shutil.move(input_file, failed_file)
        print(f"Moved failed file to: {failed_file}")

def process_excel_file(input_file, output_file):
    file_extension = os.path.splitext(input_file)[1].lower()
    
    if file_extension == '.xls':
        print(f"Processing .xls file: {input_file}")
        df = pd.read_excel(input_file, engine="xlrd")
    elif file_extension == '.xlsx':
        print(f"Processing .xlsx file: {input_file}")
        df = pd.read_excel(input_file, engine="openpyxl")
    
    df.columns = [replace_forbidden_chars(col) for col in df.columns]
    df.to_excel(output_file, index=False, engine="openpyxl")

def process_json_file(input_file, output_file):
    print(f"Processing JSON file: {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Convert JSON to DataFrame
    df = pd.json_normalize(data)
    df.columns = [replace_forbidden_chars(col) for col in df.columns]
    
    df.to_json(output_file, orient='records', indent=2)

def process_text_file(input_file, output_file):
    print(f"Processing text file: {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Remove leading/trailing whitespace and replace forbidden characters
    cleaned_lines = [replace_forbidden_chars(line.strip()) for line in lines]
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(cleaned_lines))

def process_csv_file(input_file, output_file):
    print(f"Processing CSV file: {input_file}")
    df = pd.read_csv(input_file, encoding='utf-8')
    df.columns = [replace_forbidden_chars(col) for col in df.columns]
    
    # Clean data in all columns
    for col in df.columns:
        df[col] = df[col].apply(lambda x: replace_forbidden_chars(str(x)))
    
    df.to_csv(output_file, index=False, encoding='utf-8')

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            process_file(file_path)

# Replace 'your_directory_path' with the path to the directory containing your files
process_directory('your_directory_path')
