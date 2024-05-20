def filename_cleaning(file_name:str):
    special_characters = ['!', '*', "'", '(', ')', ';', ':', '&', '=', '+', '$', ',', '/', '?', '#', '[', ']', ' ', '<', '>', '%', '{', '}', '|', '^', '`', '~', "\\", '-', '.','\"']
    for char in special_characters:
        file_name = file_name.replace(char, '')
    return file_name