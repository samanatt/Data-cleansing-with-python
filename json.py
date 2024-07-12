import json
import os

def replace_forbidden_chars(text):
    try:
        forbidden_chars = r'["\'\[\]{}(),;:!@#$%^&*+=<>?/\\|`~]'
        return ''.join('_' if char in forbidden_chars else char for char in text)
    except Exception as e:
        print(f"Error in replace_forbidden_chars: {e}")
        return text

def clean_json_object(data):
    try:
        if isinstance(data, dict):
            return {replace_forbidden_chars(k): clean_json_object(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [clean_json_object(item) for item in data]
        elif isinstance(data, str):
            return replace_forbidden_chars(data)
        else:
            return data
    except Exception as e:
        print(f"Error in clean_json_object: {e}")
        return data

def process_json_file(input_file, output_file, root):
    try:
        input_path = os.path.join(root, input_file)
        output_path = os.path.join(root, f"out_{input_file}")

        with open(input_path, 'r', encoding='utf-8') as infile, open(output_path, 'w', encoding='utf-8') as outfile:
            for line in infile:
                try:
                    # Try to parse each line as a JSON object
                    data = json.loads(line.strip())
                    cleaned_data = clean_json_object(data)
                    json.dump(cleaned_data, outfile)
                    outfile.write('\n')  # Add newline after each JSON object
                except json.JSONDecodeError:
                    # If the line is not a valid JSON, write it as is
                    outfile.write(line)

        # Remove the original file
        os.remove(input_path)
        print(f"Processed {input_file} -> out_{input_file}")
    except Exception as e:
        print(f"Error processing {input_file}: {e}")

# Main execution
if __name__ == "__main__":
    try:
        root_directory = input("Enter the root directory path: ")
        for root, dirs, files in os.walk(root_directory):
            for file in files:
                if file.lower().endswith('.json'):
                    process_json_file(file, f"out_{file}", root)
    except Exception as e:
        print(f"An error occurred: {e}")
