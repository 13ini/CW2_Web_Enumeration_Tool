import subprocess
import sys
import os

def run_cli():
    """Launch the CLI version of the Web Enumeration Tool."""
    subprocess.run([sys.executable, "enumeration.py"])

def run_gui():
    """Launch the GUI version of the Web Enumeration Tool."""
    subprocess.run([sys.executable, "enumeration_gui.py"])

def menu():
    """Display a menu to choose between CLI and GUI mode."""
    while True:
        print("\nWeb Enumeration Tool Launcher")
        print("1. Launch CLI Interface")
        print("2. Launch GUI Interface")
        print("3. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            run_cli()
        elif choice == "2":
            run_gui()
        elif choice == "3":
            print("Exiting the launcher.")
            sys.exit()
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    menu()
