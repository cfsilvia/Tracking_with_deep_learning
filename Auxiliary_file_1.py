# -*- coding: utf-8 -*-
"""
Script to add 'left_' or 'right_' prefix to filenames in a selected folder.
"""

import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog


def select_folder():
    """Prompt user to select a folder."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    folder_path = filedialog.askdirectory(title="Select folder containing files to rename")
    return folder_path


def get_prefix_choice():
    """Prompt user to choose between 'left_' or 'right_' prefix."""
    root = tk.Tk()
    root.withdraw()

    # Create a dialog to choose prefix
    choice = simpledialog.askstring(
        "Prefix Choice",
        "Enter 'left' or 'right' to add as prefix to filenames:",
        initialvalue="left"
    )

    if choice and choice.lower() in ['left', 'right']:
        return choice.lower() + "_"
    else:
        messagebox.showerror("Error", "Invalid choice. Please enter 'left' or 'right'.")
        return None


def rename_files_in_folder(folder_path, prefix):
    """Rename all files in the folder by adding the prefix."""
    if not os.path.exists(folder_path):
        messagebox.showerror("Error", f"Folder does not exist: {folder_path}")
        return

    files_renamed = 0
    errors = []

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Only rename files, not directories
        if os.path.isfile(file_path):
            new_filename = prefix + filename
            new_file_path = os.path.join(folder_path, new_filename)

            try:
                os.rename(file_path, new_file_path)
                files_renamed += 1
                print(f"Renamed: {filename} -> {new_filename}")
            except Exception as e:
                errors.append(f"Failed to rename {filename}: {str(e)}")

    # Show summary
    if files_renamed > 0:
        messagebox.showinfo("Success", f"Successfully renamed {files_renamed} files.")
    else:
        messagebox.showwarning("Warning", "No files were renamed.")

    if errors:
        error_message = "\n".join(errors)
        messagebox.showerror("Errors", f"Some files could not be renamed:\n{error_message}")


def main():
    """Main function to run the renaming process."""
    folder_path = select_folder()
    if not folder_path:
        return  # User cancelled

    prefix = get_prefix_choice()
    if not prefix:
        return  # Invalid choice

    # Confirm action
    confirm = messagebox.askyesno(
        "Confirm",
        f"Are you sure you want to add '{prefix[:-1]}' prefix to all files in:\n{folder_path}?"
    )

    if confirm:
        rename_files_in_folder(folder_path, prefix)


if __name__ == "__main__":
    main()