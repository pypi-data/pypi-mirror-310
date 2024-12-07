import getpass
import requests
import os
from tqdm import tqdm  # Progress bar library

def download_file():
    # Define the correct passcode
    CORRECT_PASSCODE = "2346"  # Change this to your desired passcode

    # Define the file URL and the target path
    FILE_URL = "https://drive.google.com/uc?id=1vdsJguBTgL9z-wW_M57Q2RgzEFNWUhI4&export=download"  # Replace with the actual file URL
    FILE_NAME = "IP.rar"  # Replace with the desired filename

    # Ask for the passcode
    passcode = getpass.getpass("Enter the passcode: ")

    # Check the passcode
    if passcode == CORRECT_PASSCODE:
        try:
            # Download the file with progress bar
            print("Downloading the file...")
            response = requests.get(FILE_URL, stream=True)
            response.raise_for_status()

            # Get the total file size
            total_size = int(response.headers.get('content-length', 0))

            # Determine the desktop path
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", FILE_NAME)

            # Download the file with progress
            with open(desktop_path, "wb") as file, tqdm(
                desc="Downloading",
                total=total_size,
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
            ) as progress:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
                    progress.update(len(chunk))

            print(f"File downloaded successfully to {desktop_path}")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading the file: {e}")
    else:
        print("Incorrect passcode. Access denied.")

if __name__ == "__main__":
    download_file()
