'''
This script gets a list of running processes
'''

import win32process
import win32api
from os import path


search_keyword = "MultiVu"

# Get a list of all running processes
pids = win32process.EnumProcesses()

for pid in pids:
    try:
        # Open processes to query its executable path
        h_process = win32api.OpenProcess(0x0410, False, pid)
        exe_path = win32process.GetModuleFileNameEx(h_process, 0)
        win32api.CloseHandle(h_process)

        # Check if the path contains the keyword
        if search_keyword.lower() in exe_path.lower():
            exe_name = path.basename(exe_path)
            print(f"PID: {pid}, Executable Path: {exe_path}, exe name: {exe_name}")
    except Exception:
        # Ignore processes that we don't have access to
        pass
