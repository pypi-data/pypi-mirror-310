import requests
import re
import os
import zipfile
from win32com.client import Dispatch
from bs4 import BeautifulSoup
import py7zr
import subprocess
import argparse

URL = "https://drive.google.com/uc?export=download" 
USERCONTENT_URL = "https://drive.usercontent.google.com/download"

def extract_file_id(drive_url):
    # Regex pattern to extract the file ID from a Google Drive link
    pattern = r"[-\w]{25,}"
    match = re.search(pattern, drive_url)
    
    if match:
        return match.group(0)  # return the file ID
    else:
        raise ValueError("No valid file ID found in the provided Google Drive URL.")

def parse_command_line_args():
    # Create the parser
    parser = argparse.ArgumentParser(description="Process URL, Destination, and Startup arguments.")
    
    # Add required positional argument (URL)
    parser.add_argument('URL', type=str, help="URL to be processed (mandatory argument)")
    
    # Add optional argument (Destination)
    parser.add_argument('-d', '--destination', type=str, help="Specify the destination (optional)")
    
    # Add optional string argument (Startup)
    parser.add_argument('-s', '--startup', type=str, help="Specify the startup value (optional); DO NOT PUT illegal symbols or it will lead to undefined behaviour")

    #What file to launch after the installation is complete
    parser.add_argument('-l', '--launch', type=str, help="Specify the file name for the file that you want to launch after your program is downloaded (optional)")
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Accessing the arguments
    print(f"URL: {args.URL}")
    
    if args.destination:
        print(f"Destination: {args.destination}")
    
    if args.startup:
        print(f"Startup: {args.startup}")   

    if args.launch:
        print(f"Launch: {args.launch}")

    download_file_from_google_drive(args.URL, args.destination, args.startup, args.launch)

def if_virus_scan_warning(session, destination, file_size): 
    """If google drive virus scan warning appears"""
    
    if os.path.isfile(destination) and os.path.basename(destination).split('/')[-1] == "downloaded_file":
        with open(destination) as f: 
            s = f.read()
            f.close()
            if os.path.exists(destination):
                os.remove(destination)
                print(f"{"downloaded_file"} has been removed.")
            else:
                print(f"{"downloaded_file"} does not exist.")


            soup = BeautifulSoup(s, 'html.parser')

            id = soup.find('input', {"name" : "id"})['value']
            export = soup.find('input', {"name" : "export"})['value']
            confirm = soup.find('input', {"name" : "confirm"})['value']
            uuid = soup.find('input', {"name" : "uuid"})['value']

            if id:
                second_response_for_download_confirmation =  session.get(USERCONTENT_URL + "?id=" + id + "&export=" + export + "&confirm=" + confirm + "&uuid=" + uuid, stream=True)
                second_file_name = get_file_name_from_response(second_response_for_download_confirmation)
                
                real_destination = get_directory_from_file(destination) + "\\" + second_file_name

                save_response_content(second_response_for_download_confirmation, real_destination, file_size)
                verify_download(second_response_for_download_confirmation, real_destination)
                
            else: print("Id is none")
        


        if os.path.exists(real_destination):
            return real_destination
        else: return False

def download_file_from_google_drive(
    drive_url, destination=None, add_shortcut_to_startup_folder=None, launch_file_after_download=None
):

    # Extract the file ID from the provided URL
    file_id = extract_file_id(drive_url)

    session = requests.Session()

    # Initialize headers and file size for resuming downloads
    headers = {}
    file_size = 0

    if destination is None:
        # Default to the current working directory
        destination = os.getcwd()
    else:
        # Ensure the destination is treated as a directory
        if not destination.endswith(os.path.sep):  # Add separator if missing
            if not os.path.splitext(destination)[1]:  # No file extension implies folder
                destination += os.path.sep
        
        os.makedirs(destination, exist_ok=True)

    # If the destination is a directory, append the file name
    if os.path.isdir(destination):
        response = session.get(URL, params={'id': file_id}, stream=True)
        file_name = get_file_name_from_response(response)
        destination = os.path.join(destination, file_name)


    if destination is None or os.path.isdir(destination):
        # Get file name from headers
        response = session.get(URL, params={'id': file_id}, stream=True)
        file_name = get_file_name_from_response(response)
        
        # If destination is a directory, save the file there
        if destination is None:
            destination = os.getcwd()
        else:
            # Create the directory if it doesn't exist
            os.makedirs(destination, exist_ok=True)
        destination = os.path.join(destination, file_name)
    else:
        # If destination is a full file path, ensure its directory exists
        directory = os.path.dirname(destination)
        os.makedirs(directory, exist_ok=True)


    # If the file already exists, get its size for resuming the download
    if os.path.exists(destination) and os.path.isfile(destination):
        file_size = os.path.getsize(destination)
        headers['Range'] = f"bytes={file_size}-"

    # Perform the download (with resume support if applicable)
    response = session.get(URL, params={"id": file_id}, headers=headers, stream=True)

    # Check for a download confirmation token for large files
    token = get_confirm_token(response)
    if token:
        params = {"id": file_id, "confirm": token}
        response = session.get(URL, params=params, stream=True)

    # Save the file
    save_response_content(response, destination, file_size)

    # Verify the file download by comparing Content-Length with the actual file size
    if not verify_download(response, destination):
        os.remove(destination)  # Remove the incomplete file
        raise Exception(f"Download of file '{destination}' failed or was incomplete.")

    # Check for Google Drive virus scan warnings
    extracted_file = if_virus_scan_warning(session, destination, file_size)

    if extracted_file is None:
        pass
        # No downloaded_file was detected.
    elif extracted_file is False:
        pass
        # Download of second file failed.
    else:
        # Extract the archive if an additional file was downloaded
        extract_archive(extracted_file, destination)

    # Handle extraction of the main zip file
    if os.path.exists(destination) and extracted_file is None:
        if os.path.isfile(destination):
            if extract_archive(destination, os.path.dirname(destination)) != -1:
                os.remove(destination)

    # Add a shortcut to the startup folder if requested
    if add_shortcut_to_startup_folder:
        if not os.path.isdir(destination):
            destination_dir = get_directory_from_file(destination)
        else:
            destination_dir = destination

        if destination_dir:
            shortcut_path = os.path.join(
                get_startup_folder(), f"{add_shortcut_to_startup_folder}.lnk"
            )
            create_shortcut(shortcut_path, os.path.join(destination_dir, add_shortcut_to_startup_folder))
        else:
            shortcut_path = os.path.join(
                get_startup_folder(), f"{add_shortcut_to_startup_folder}.lnk"
            )
            create_shortcut(shortcut_path, os.path.join(os.getcwd(), add_shortcut_to_startup_folder))

    # Launch the program after download if requested
    if launch_file_after_download:
        launch_program_after_install(destination, launch_file_after_download)
        

    # Return the final file path
    return os.path.join(destination)

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None

def save_response_content(response, destination, file_size):
    CHUNK_SIZE = 32768  # Chunk size to download large files
    #destination = get_directory_from_file(destination)
    # Open file in append mode to resume download if necessary
    with open(destination, "ab" if file_size > 0 else "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive chunks
                f.write(chunk)

def get_file_name_from_response(response):
    # Extract the filename from the Content-Disposition header
    if 'Content-Disposition' in response.headers:
        content_disposition = response.headers['Content-Disposition']
        file_name = re.findall('filename="(.+)"', content_disposition)
        if file_name:
            return file_name[0]
    
    # Fallback to a default name if filename not found
    return "downloaded_file"

def get_directory_from_file(file_path):
    """
    Converts a file path to its parent directory.

    Args:
        file_path (str): The full path to the file.

    Returns:
        str: The directory containing the file.
    """
    return os.path.dirname(file_path)

def verify_download(response, destination):
    """
    Verifies if the downloaded file is complete by comparing the content-length header
    with the actual file size.
    """
    # Get the content-length from the response headers (if available)
    content_length = response.headers.get('Content-Length')
    if content_length is None:
        # If content-length is not provided, skip the check
        return True
    
    # Convert content-length to an integer
    expected_size = int(content_length)

    # Get the actual file size
    actual_size = os.path.getsize(destination)

    # Check if the sizes match
    return actual_size == expected_size

def extract_archive(file_path, extract_to = None):

    if not os.path.isdir(extract_to):
        extract_to = get_directory_from_file(extract_to)
    
    
    # Determine file extension
    file_ext = os.path.splitext(file_path)[-1].lower()
    
    if file_ext == '.zip':
        # Extract ZIP files
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
            
        #print(f"Extracted ZIP archive: {file_path}")

    elif file_ext == '.7z':
        # Extract 7z files
        with py7zr.SevenZipFile(file_path, mode='r') as seven_z_ref:
            seven_z_ref.extractall(path=extract_to)
        
        #print(f"Extracted 7z archive: {file_path}")

    else:
        #print(f"Unsupported file type: {file_ext}")
        return -1



def launch_program_after_install(destination, exe_path):
    if not os.path.isdir(destination):
        destination = get_directory_from_file(destination)
        

    if os.path.isfile(destination + "\\" + exe_path):
        # Start the new process as a separate parent process
        process = subprocess.Popen(destination + "\\" + exe_path)

        # You can interact with `process` here or just let it run independently
        #print(f"Started new process with PID: {process.pid}")
    


def get_startup_folder():
    """
    Returns the path to the shell:startup folder.
    """
    home = os.path.expanduser("~")
    startup_folder = os.path.join(home, "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
    return startup_folder

def create_shortcut(path, target):
    """
    path = where the shortcut will be created
    target = file/directory to which the shortcut is pointing
    """
    #print("Target: ", target)
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(path)
    shortcut.Targetpath = target
    shortcut.save()
