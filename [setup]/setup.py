# [BUILD] Install pyinstaller and run the command (to build .exe file) :
# <= pyinstaller --onefile --icon=interface/ressources/icon.ico [setup]/setup.py => 

import os
import platform
import subprocess


# ---[ANSI COLOR]---
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"

# ---[SCRIPT INSTALLATION LOGIC]---
def start_ollama():
    if platform.system() == 'Windows':
        subprocess.Popen(['start', 'cmd', '/c', 'ollama serve'], shell=True)
    else:
        subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', 'ollama serve; exit'], shell=True)

def build_env():
    if not os.path.exists('.env'):
        subprocess.run(['python', '-m', 'venv', '.env'])
        print(f"{CYAN}Virtual environment created.{RESET}")
    else:
        print(f"{CYAN}Virtual environment already exists.{RESET}")

def start_and_install_lib():
    if platform.system() == 'Windows':
        activate_script = '.env\\Scripts\\activate.bat'
        pip_executable = '.env\\Scripts\\pip'
        python_executable = '.env\\Scripts\\python'
    else:
        activate_script = '.env/bin/activate'
        pip_executable = '.env/bin/pip'
        python_executable = '.env/bin/python'

    # Activate the virtual environment
    subprocess.run(activate_script, shell=True)
    print(f"{CYAN}Virtual environment activated.{RESET}")

    # Check if required libraries are installed
    try:
        subprocess.run([pip_executable, 'show', 'langchain'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run([pip_executable, 'show', 'streamlit'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"{CYAN}Required libraries are already installed.{RESET}")
    except subprocess.CalledProcessError:
        print(f"{CYAN}Installing required libraries...{RESET}")
        subprocess.run([pip_executable, 'install', '-r', 'requirements.txt'])

        # Ask user for installation mode after installing requirements
        while True:
            mode = input(f"{GREEN}Choose LLMs installation mode (1 for default, 2 for custom (download yourself LLMs you want)): {RESET}").strip()
            if mode in ['1', '2']:
                break
            print(f"{RED}Invalid input. Please enter 1 for default or 2 for custom.{RESET}")

        if mode == '1':
            subprocess.run(['ollama', 'pull', 'llama3.1:latest'], check=True)
            subprocess.run(['ollama', 'pull', 'nomic-embed-text:latest'], check=True)

    # Start the app interface
    subprocess.run([python_executable, '-m', 'streamlit', 'run', 'interface/menu.py'], check=True)

def auto_run():
    start_ollama()
    build_env()
    start_and_install_lib()

if __name__ == "__main__":
    auto_run()