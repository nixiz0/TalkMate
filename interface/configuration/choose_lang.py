def get_lang(lang_choice):
    with open('interface/CONFIG.py', 'r') as file:
        lines = file.readlines()
    
    with open('interface/CONFIG.py', 'w') as file:
        for line in lines:
            if line.startswith('LANG ='):
                file.write(f"LANG = '{lang_choice}'\n")
            else:
                file.write(line)
