import subprocess

def install_extensions(extension_file):
    try:
        print("start")
        # Open the file containing the list of extensions
        with open(extension_file, "r") as file:
            extensions = file.readlines()
        
        for extension in extensions:
            print(extension)
            # Strip whitespace and skip empty lines
            extension = extension.strip()
            if not extension:
                continue

            # Install the extension using subprocess
            print(f"Installing extension: {extension}")
            result = subprocess.run(
                ["code", "--install-extension", extension],
                capture_output=True,
                text=True
            )
            
            # Check for success or failure
            if result.returncode == 0:
                print(f"Successfully installed: {extension}")
            else:
                print(f"Failed to install: {extension}")
                print(f"Error: {result.stderr}")

    except FileNotFoundError:
        print(f"Error: File '{extension_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Provide the path to your extensions.txt file
install_extensions("extensions.txt")
