import os

def delete_log_files(directory):
    # Walk through the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if the file is a log file
            if file.endswith('.log'):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")

if __name__ == "__main__":
    # Replace 'your_directory' with the path to the directory you want to clean
    userInput=''
    while not userInput:
        userInput=input("tap to delete logs:\n")
        delete_log_files(os.path.dirname(__file__))