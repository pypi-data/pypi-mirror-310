import os
import requests

# Database of files (file number: download URL)
file_db = {
    1: "https://drive.google.com/uc?export=download&id=1BLuHc9i5Mtks0S7ChrZEwfUQjgUzH87-",
    2: "https://drive.google.com/uc?export=download&id=1VOa6yGWCpsyPJTWwOI3NEBd6G73GwaNU",
    3: "https://drive.google.com/uc?export=download&id=1g4Rbfd0JpPhhFtO9YNK2r3DiOqRq_jQy",
    4: "https://drive.google.com/uc?export=download&id=1v4P39GUTbpsfh9AA200P0tF0FTXmeKL8",
    9: "https://drive.google.com/uc?export=download&id=1L5bFX_RHeRLjDE82sNXf-jMDvTBf0A86",
    8:"https://drive.google.com/uc?export=download&id=13jWYPj8q5cBY6q-2MZpIz1ARN-K0EpvC",
    10: "https://drive.google.com/uc?export=download&id=1-MQAxZ4WC4v0c01N0TZEQm7T17b6Ilk3",
}

def get_file_name(file_number):
    """Generate file name based on the file number."""
    return f"ex-{file_number}.txt"

def get_desktop_path():
    """Get the Desktop path of the current user."""
    return os.path.join(os.path.expanduser("~"), "Desktop")

def main():
    print("Welcome!")
    print("Enter the file number you want to download:")

    try:
        # Get user input
        file_number = int(input("File Number: "))

        # Check if the file number exists in the database
        if file_number in file_db:
            file_url = file_db[file_number]
            file_name = get_file_name(file_number)  # Generate the file name

            desktop_path = get_desktop_path()  # Get the user's Desktop directory
            file_path = os.path.join(desktop_path, file_name)  # Full path to save the file

            print(f"Downloading {file_name} to Desktop...")

            # Download the file
            response = requests.get(file_url, stream=True)
            response.raise_for_status()  # Raise error for bad HTTP responses

            # Save the file locally on the Desktop
            with open(file_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print(f"{file_name} has been downloaded to {desktop_path}")
        else:
            print("Invalid file number. Please try again.")
    except ValueError:
        print("Invalid input! Please enter a valid number.")
    except requests.RequestException as e:
        print(f"Failed to download the file: {e}")
    except OSError as e:
        print(f"Error saving the file: {e}")

if __name__ == "__main__":
    main()

