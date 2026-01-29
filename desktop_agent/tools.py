import platform
import subprocess
import os
import tkinter as tk
from tkinter import filedialog
from langchain_core.tools import tool
from storage import load_apps, save_apps

@tool
def list_apps():
    """Returns a list of all registered applications in the collection."""
    apps = load_apps()
    if not apps: return "Your collection is currently empty."
    return "Current registered apps:\n" + "\n".join([f"- {n}: {p}" for n, p in apps.items()])

@tool
def remove_app(app_name: str):
    """Removes an application from the collection by name."""
    apps = load_apps()
    app_key = app_name.lower().strip()
    if app_key in apps:
        del apps[app_key]
        save_apps(apps)
        return f"Successfully removed '{app_name}'."
    return f"Error: '{app_name}' not found."

@tool
def rename_app(old_name: str, new_name: str):
    """Changes the friendly name of an existing application."""
    apps = load_apps()
    old_key, new_key = old_name.lower().strip(), new_name.lower().strip()
    if old_key in apps:
        apps[new_key] = apps.pop(old_key)
        save_apps(apps)
        return f"Renamed '{old_name}' to '{new_name}'."
    return f"Error: '{old_name}' not found."

@tool
def register_new_app(friendly_name: str):
    """Opens a file dialog to let the user add a new application to the collection."""
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    
    # We add the 'resolve_links=False' argument here
    file_path = filedialog.askopenfilename(
        title=f"Select the executable for {friendly_name}",
        filetypes=[("Executable Files", "*.exe *.lnk *.app"), ("All Files", "*.*")]
        # Note: some versions of tkinter/Windows might still resolve. 
        # If it does, selecting the file from the Desktop usually works better than the Start Menu.
    )
    root.destroy()

    if file_path:
        # Convert to absolute path to be safe
        file_path = os.path.abspath(file_path)
        current_apps = load_apps()
        current_apps[friendly_name.lower()] = file_path
        save_apps(current_apps)
        return f"Successfully registered '{friendly_name}' at {file_path}"
    return "Registration cancelled."

@tool
def launch_app(app_name: str):
    """Opens a specific application."""
    apps = load_apps()
    app_key = app_name.lower().strip()
    if app_key in apps:
        try:
            path = apps[app_key]
            if platform.system() == "Darwin":
                subprocess.Popen(["open", "-a", path])
            else:
                subprocess.Popen(path, shell=True)
            return f"Opened {app_key}."
        except Exception as e:
            return f"Error: {str(e)}"
    return f"'{app_name}' not in collection."

tools = [launch_app, register_new_app, list_apps, remove_app, rename_app]