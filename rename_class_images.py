import os  
  
def remove_invalid_chars(filename):  
    invalid_chars = '<>:"/\|?*'  
    for char in invalid_chars:  
        filename = filename.replace(char, '')  
    return filename  
  
def rename_files_in_directory(root_directory):  
    for foldername, subfolders, filenames in os.walk(root_directory):  
        for filename in filenames:  
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):  
                original_file_path = os.path.join(foldername, filename)  
                new_file_path = os.path.join(foldername, remove_invalid_chars(filename))  
                if original_file_path != new_file_path:  
                    os.rename(original_file_path, new_file_path)  
                    print(f"Renamed {original_file_path} to {new_file_path}")  

root_directory = "./class-images"  
rename_files_in_directory(root_directory)  
