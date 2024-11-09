# TalkMate-Windows

Interface allowing you to have a conversation with a LLM assistant and on your personnal data.
Also, the app is very customizable, you can give specific instructions to your LLM and change rag system parameters.


## Installation

=> Click on **TalkMate-Installer.exe** to download the app (be careful to install the necessary applications in Tech Stack).

=> Afterwards you click on **setup.exe** to build environment for the app.


## Tech Stack

**[Application you have to install on your computer]**

- **Python 3.11.7** (https://www.python.org/downloads/release/python-3117/)

- **Ollama** (https://ollama.com/download)

- **CUDA 11.8** (https://developer.nvidia.com/cuda-11-8-0-download-archive)


## Configuration Synthetic Voices

If you want to have more synthetic voices available, on Windows you have to go to the narrator settings and you can download the voices you want.

If this doesn't work and doesn't recognize the voices you have installed on the narrator settings, follow this steps :
1. Open the **Registry Editor** by pressing the **“Windows” and “R”** keys simultaneously, then type **“regedit”** and press Enter.

2. Navigate to the registry key : **HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech_OneCore\Voices\Tokens**.

3. Export this key to a **REG file** (with a right click on the file).

4. Open this file with a text editor and replace all occurrences of **HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech_OneCore\Voices\Tokens** 
with **HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\SPEECH\Voices\Tokens**.

5. Save the modified file and double-click it to import the changes to the registry.


## Author

- [@nixiz0](https://github.com/nixiz0)