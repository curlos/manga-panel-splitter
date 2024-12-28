import tkinter as tk
from tkinter import filedialog
import subprocess
import sys


def select_folder():
    # Create a root window
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    root.attributes(
        "-topmost", True
    )  # Ensure the dialog is on top of all other windows

    # Force focus to the root window to ensure the dialog appears in front
    root.deiconify()
    root.lift()
    root.focus_force()

    # Open the folder selection dialog
    folder_path = filedialog.askdirectory(title="Select a Folder", parent=root)

    # Check if a folder was selected
    if folder_path:
        print(f"Selected folder: {folder_path}")
    else:
        print("No folder selected.")

    # Clean up the root window
    root.destroy()

    return folder_path


def pip_install_or_uninstall_tool(module_name: str, action: str):
    """
    Install or uninstall a Python module using pip.

    Args:
        module_name (str): The name of the module to manage.
        action (str): The action to perform ('install' or 'uninstall').

    Raises:
        ValueError: If an invalid action is provided.
    """
    if action not in {"install", "uninstall"}:
        raise ValueError("Invalid action. Use 'install' or 'uninstall'.")

    try:
        # Construct the pip command in a single list
        pip_command = [
            sys.executable,  # The python executable (like the venv/bin/python folder)
            "-m",
            "pip",
            action,
            (
                "-y" if action == "uninstall" else ""
            ),  # Automatically say "Yes" to any uninstall prompts instead of having to wait for manual user input.
            module_name.replace("_", "-"),
        ]

        # Remove any empty strings from the command list
        pip_command = [cmd for cmd in pip_command if cmd]

        print(f"Attempting to {action} '{module_name}'...")

        result = subprocess.run(
            pip_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if result.returncode == 0:
            print(f"'{module_name}' {action}ed successfully!")
        else:
            print(f"Failed to {action} '{module_name}'. Please try manually.")
            print(result.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"An error occurred while trying to {action} '{module_name}': {e}")
        sys.exit(1)


def is_tool_installed(module_name: str) -> bool:
    """
    Check if a Python module is executable using `python3 -m`.

    Args:
        module_name (str): The name of the module to check.

    Returns:
        bool: True if the module can be executed, False otherwise.
    """
    try:
        # Test invoking the module with `python3 -m module_name --help`
        result = subprocess.run(
            [sys.executable, "-m", module_name, "--help"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Check if the error message indicates the module is not installed
        if "No module named" in result.stderr:
            return False

        # Return True if no errors related to missing modules are found
        return result.returncode == 0
    except FileNotFoundError:
        return False  # Python executable or module not found
    except Exception as e:
        print(f"An unexpected error occurred while checking {module_name}: {e}")
        return False
