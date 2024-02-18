import subprocess
import readline
import os
import signal
import sys

# ANSI escape codes for colors and formatting
YELLOW = '\033[93m'
BOLD = '\033[1m'
RESET_COLOR = '\033[0m'

def clear_screen():
    """Clear the screen"""
    if os.name == 'posix':
        _ = subprocess.call('clear', shell=True)
    else:
        _ = subprocess.call('cls', shell=True)

def signal_handler(sig, frame):
    """Handle Ctrl+C (SIGINT) signal"""
    print("\nmacsh: End.")
    sys.exit(0)

# Register signal handler for Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

def format_path(path):
    """Format path to replace forward slashes with backslashes"""
    return path.replace("/", "\\")

# Dictionary of commands and their descriptions
COMMANDS = {
    "echo": "Prints the given message.",
    "cd": "Changes the current directory.",
    "ls": "Lists files and directories in the current directory.",
    "help": "Displays help information about available commands.",
    "end": "Exits the MicroActive shell.",
    "gitc": "Clones a Git repository. Usage: gitc [REPOSITORY_URL]",
    "version": "Shows the version of the MicroActive shell.",
    "mkdir": "Creates a new directory.",
    "make": "Creates an empty file.",
    "let": "Moves or renames files or directories."
}

printMe="""
MicroActive Shell v1.0.0
Copyright, Shane Ladd, 2024

Enter 'help' to show commands

"""

print(printMe)

while True:
    try:
        current_directory = format_path(os.getcwd())
        cmd = input(YELLOW + BOLD + f"C:{current_directory} " + RESET_COLOR)
        if not cmd.strip():  # If input is empty
            print("\n\n")  # Print two new lines
            continue  # Skip to the next iteration
        elif cmd.startswith("echo "):
            print(cmd[5:])
        elif cmd.startswith("cd "):
            try:
                os.chdir(cmd[3:])
            except FileNotFoundError:
                print("ERROR: Directory not found")
        elif cmd.startswith("gitc "):
            try:
                repository_url = cmd[5:]
                subprocess.call(["git", "clone", repository_url])
            except Exception as e:
                print(f"ERROR: Failed to clone repository: {e}")
        elif cmd.startswith("mkdir "):
            try:
                directory_name = cmd[6:]
                os.makedirs(directory_name)
                print(f"Directory '{directory_name}' created successfully.")
            except FileExistsError:
                print(f"ERROR: Directory '{directory_name}' already exists.")
            except Exception as e:
                print(f"ERROR: Failed to create directory '{directory_name}': {e}")
        elif cmd.startswith("make "):
            try:
                file_name = cmd[5:]
                with open(file_name, 'w'):
                    pass
                print(f"File '{file_name}' created successfully.")
            except Exception as e:
                print(f"ERROR: Failed to create file '{file_name}': {e}")
        elif cmd.startswith("let "):
            try:
                source, destination = cmd[4:].split()
                os.rename(source, destination)
                print(f"'{source}' moved to '{destination}' successfully.")
            except Exception as e:
                print(f"ERROR: Failed to move '{source}' to '{destination}': {e}")
        elif cmd == "ls":
            print("FILE                    EXTENSION                    TYPE")
            print("-" * 60)
            for item in os.listdir():
                if os.path.isfile(item):
                    filename, extension = os.path.splitext(item)
                    print(f"{filename.ljust(24)}{extension.ljust(28)}{'File'}")
                elif os.path.isdir(item):
                    print(f"{item.ljust(24)}{'<DIR>'.ljust(28)}{'Directory'}")
        elif cmd == "help":
            print("Available commands:")
            for command, description in COMMANDS.items():
                print(f"{command}: {description}")
        elif cmd == "end":
            print("macsh: End.")
            break
        elif cmd == "macsh":
            print("MicroActive shell: version 1.0.0")
        elif cmd == "version":
            print("MicroActive shell: version 1.0.0")
        else:
            print(f"ERROR: unrecognized command '{cmd}'")
    except KeyboardInterrupt:
        print("\nEnding MicroActive. Exiting...")
        break
    except Exception as e:
        print(f"An error occurred: {e}")

# Register Ctrl+L to clear screen
readline.parse_and_bind("^L: clear_screen")

