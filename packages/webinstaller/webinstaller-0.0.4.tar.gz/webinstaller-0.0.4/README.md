# Webinstaller
A Python library designed for seamless file downloads from Google Drive, offering robust features to simplify the process. It allows you to specify a custom destination folder for downloads and supports popular archive formats like .zip and .rar. The library also provides convenient options to launch downloaded files and add them to the Windows startup folder, if desired. With built-in CLI support, it ensures ease of use from the command line. Additionally, the library is resilient against connection interruptions, automatically resuming downloads once the connection is restored.

# Contents
- ## [Installation](https://github.com/Sal0ID/webinstaller#installation-1)
- ## [Simplest use](https://github.com/Sal0ID/webinstaller#simplest-use-1)
- ## [Advanced usage](https://github.com/Sal0ID/webinstaller/blob/main/README.md#advanced-usage-1)
  - [Specify destination](https://github.com/Sal0ID/webinstaller/blob/main/README.md#specify-destination)
  - [CLI use](https://github.com/Sal0ID/webinstaller/blob/main/README.md#cli-usage)
  - [Launch file after download](https://github.com/Sal0ID/webinstaller/blob/main/README.md#launch-file-after-download)
  - [Add shortcut to startup folder](https://github.com/Sal0ID/webinstaller/blob/main/README.md#add-shortcut-to-startup-folder)
 
# Installation
1. Upload some random file to google drive right click it Share->Share->Set general access to anyone with the link
2. Install library with this commands or with pip
 ```
git clone https://github.com/Sal0ID/webinstaller
cd webinstaller
pip install build
py -m build
pip install dist/webinstaller-0.0.4-py3-none-any.whl
 ```
# Simplest use
Create venv or just create python file
```
from webinstaller import webinstaller

drive_url = "insert_link_from_google_drive_here"

webinstaller.download_file_from_google_drive(drive_url)
```
3. Congratulations, you can launch your program!
# Advanced usage
## Specify destination
You can specify the destination folder for downloaded files. If the file is in .zip or .rar format, it will be automatically exported to the destination folder that you provided. You can use relative or absolute path. If destination folder doesn`t exist it will create it.

```
from webinstaller import webinstaller

drive_url = "insert_link_from_google_drive_here"
destination = "amogus" 

webinstaller.download_file_from_google_drive(drive_url, destination = destination) #Will create amogus folder and download file there
```
## CLI usage
1. Create .py file with following content:
```
from webinstaller import webinstaller

webinstaller.parse_command_line_args()
```
2. Create executable file via pyinstaller
```
pyinstaller --noconfirm --onefile --windowed  "path_to_your_py_file"
```
3. You are ready to go, now you can pass following arguments to .exe file:
   - URL to the google drive file (mandatory positional argument)
   - --destination (-d) Destination where to save downloaded file/archive (optional)
   - --launch (-l) Specify the file name for the file that you want to launch after your program is downloaded (optional) ; relative path from destination folder
   - --startup (-s) Specify file name to which shortcut will be created in windows startup directory (optional).  
## **Example:**
```
main.exe https://google.com -d folder -l main.exe -s onstartup.exe
```
## Launch file after download
```
from webinstaller import webinstaller

drive_url = "insert_link_from_google_drive_here"

webinstaller.download_file_from_google_drive(drive_url, launch_file_after_download = "deleteme.exe") # File deleteme.exe will be lauched after download if it exists. Also you can pass other arguments
```
## Add shortcut to startup folder
Program will create shortcut in C:\Users\User_Name\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup pointing to file that you specify. You can pass other arguments
```
from webinstaller import webinstaller

drive_url = "insert_link_from_google_drive_here"

webinstaller.download_file_from_google_drive(drive_url, add_shortcut_to_startup_folder = "deleteme.exe") # 
```
