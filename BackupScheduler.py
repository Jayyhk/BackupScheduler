import tkinter as tk
from tkinter import filedialog
import customtkinter
from PIL import Image
import pystray
import shutil
import os
import sys
import ctypes
import webbrowser
import json
from datetime import datetime, timedelta

class BackupScheduler(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("BackupScheduler")
        dpi = ctypes.windll.user32.GetDpiForWindow(customtkinter.CTk().winfo_id())
        ppi = customtkinter.CTk().winfo_fpixels('1i')
        scale = dpi/ppi
        app_width = 700
        app_height = 196
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width/2 - app_width/2)*scale)
        y = int((screen_height/2 - app_height/2)*scale)
        self.geometry(f"{app_width}x{app_height}+{x}+{y}")
        self.resizable(False, False)

        # configure appearance
        customtkinter.set_appearance_mode("Dark")
        customtkinter.set_default_color_theme("blue")

        # configure sideframe
        self.sidebar_frame = customtkinter.CTkFrame(self, width=50, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Backup\nScheduler", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 20))

        # configure github logo
        github_logo = customtkinter.CTkImage(dark_image = Image.open(resource_path('config/icons/github.png')), size = (42, 42))
        self.github_label = customtkinter.CTkLabel(self.sidebar_frame, image=github_logo, width=50, height=50, text="", fg_color="transparent")
        self.github_label.bind("<Button-1>", lambda event: webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ"))
        self.github_label.bind("<Enter>",  lambda event: self.github_label.configure(cursor="hand2"))
        self.github_label.bind("<Leave>", lambda event: self.github_label.configure(cursor=""))
        self.github_label.grid(row=3, column=0, padx=20, pady=(50,0))
        
        # configure widgets
        self.source_entry = customtkinter.CTkEntry(self, placeholder_text="Source Path", width=400)
        self.source_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.source_file_button = customtkinter.CTkButton(self, text="File", width=68, command=self.browse_source_file)
        self.source_file_button.grid(row=0, column=2, padx=5, pady=10, sticky="w")
        self.source_folder_button = customtkinter.CTkButton(self, text="Folder", width=68, command=self.browse_source_folder)
        self.source_folder_button.grid(row=0, column=2, padx=5, pady=10, sticky="e")
        self.dest_entry = customtkinter.CTkEntry(self, placeholder_text="Destination Path", width=400)
        self.dest_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        self.browse_dest_button = customtkinter.CTkButton(self, text="Folder", command=self.browse_dest)
        self.browse_dest_button.grid(row=1, column=2, padx=5, pady=10)
        self.time_entry = customtkinter.CTkEntry(self, placeholder_text="HH:MM", width=58)
        self.time_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        self.schedule_backup_button = customtkinter.CTkButton(self, text="Schedule Backup", width=170, command=self.save_changes)
        self.schedule_backup_button.grid(row=3, column=1, padx=10, pady=(10,20), sticky="w")
        self.backup_button = customtkinter.CTkButton(self, text="Backup Now", width=170, command=lambda: self.add_instant_backup(self.source_entry.get(), self.dest_entry.get()))
        self.backup_button.grid(row=3, column=1, padx=10, pady=(10,20), sticky="e")
        self.info_label = customtkinter.CTkLabel(self, text="", text_color="#242424", fg_color="transparent")
        self.info_label.grid(row=3, column=2, padx=5, pady=5, sticky="")

    def change_info(self, text):
        # change info label text
        self.info_label.configure(text=text)
        steps = 80

        # convert start and end colors to RGB format
        start_rgb = tuple(int("242424"[i:i+2], 16) for i in (0, 2, 4))
        end_rgb = tuple(int("DCE4EE"[i:i+2], 16) for i in (0, 2, 4))

        # calculate color differences for each channel (R, G, B)
        delta_rgb = [(end_rgb[i] - start_rgb[i]) / steps for i in range(3)]

        # fade in
        for step in range(steps + 1):
            current_rgb = [int(start_rgb[i] + step * delta_rgb[i]) for i in range(3)]
            current_color = "#{:02X}{:02X}{:02X}".format(*current_rgb)
            self.info_label.configure(text_color=current_color)
            self.info_label.update()
            self.info_label.after(10)

        # fade out
        for step in range(steps + 1):
            current_rgb = [int(end_rgb[i] - step * delta_rgb[i]) for i in range(3)]
            current_color = "#{:02X}{:02X}{:02X}".format(*current_rgb)
            self.info_label.configure(text_color=current_color)
            self.info_label.update()
            self.info_label.after(10)
        
        self.info_label.configure(text="")
    
    def browse_source_file(self):
    # select source files
        file_paths = filedialog.askopenfilenames()
        if file_paths:
            # Clear previous entry and insert selected file paths
            self.source_entry.delete(0, tk.END)
            self.source_entry.insert(0, "*".join(file_paths))

    def browse_source_folder(self):
        # select source folder
        folder_path = filedialog.askdirectory()
        self.source_entry.delete(0, tk.END)
        self.source_entry.insert(0, folder_path)

    def browse_dest(self):
        # select destination folder
        dest_path = filedialog.askdirectory()
        self.dest_entry.delete(0, tk.END)
        self.dest_entry.insert(0, dest_path)

    def validate_paths(self, source_path, dest_path):
        # check if paths exist
        if not os.path.exists(source_path):
                print(f"Source path '{source_path}' not found.")
                self.change_info("Source not found.")
                return False
        if not os.path.exists(dest_path):
            print(f"Destination path '{dest_path}' not found.")
            self.change_info("Destination not found.")
            return False
        return True

    def check_storage_space(self, source_path, dest_path):
        # calculate source size
        total_size = 0
        if os.path.isfile(source_path):
            total_size = os.path.getsize(source_path)
        elif os.path.isdir(source_path):
            for dirpath, dirnames, filenames in os.walk(source_path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    total_size += os.path.getsize(fp)

        # calculate destination free space
        dest_drive, _ = os.path.splitdrive(dest_path)
        dest_free_space = shutil.disk_usage(dest_drive).free

        # compare sizes
        if total_size > dest_free_space:
            print("Not enough storage space to make a backup.")
            self.change_info("Not enough\nstorage space.")
            return False
        return True

    def add_instant_backup(self, source_path, dest_path):
        add_data(source_path, dest_path, datetime.now().strftime("%H:%M"))
        print(datetime.now().strftime("%H:%M"))
        self.perform_backup(source_path, dest_path)

    def save_changes(self):
        source_paths = self.source_entry.get()
        dest_path = self.dest_entry.get()

        # validate fields
        if all([self.source_entry.get(), self.dest_entry.get(), self.time_entry.get()]):
            if not all(self.validate_paths(source_path, dest_path) for source_path in source_paths.split("*")):
                return
            if not all(self.check_storage_space(source_path, dest_path) for source_path in source_paths.split("*")):
                return
            self.schedule_backup()
        else:
            print(f"Please fill in all fields.")
            self.change_info("Please fill in all fields.")
    
    def schedule_backup(self):
        # validate time format
        try:
            backup_string = self.time_entry.get()
            backup_time = datetime.strptime(backup_string, "%H:%M")
        except ValueError:
            print(f"Invalid time format. Please use HH:MM.")
            self.change_info("Invalid time format.\nPlease use HH:MM.")
            return

        # calculate time until backup
        current_time = datetime.now().time()
        backup_datetime = datetime.combine(datetime.now().date(), backup_time.time())
        if current_time > backup_time.time():
            backup_datetime += timedelta(days=1)
        time_until_backup = (backup_datetime - datetime.now()).total_seconds()

        # add data to json file
        add_data(self.source_entry.get(), self.dest_entry.get(), backup_string)

        # wait until backup time and perform backup
        source_paths = self.source_entry.get()
        dest_path = self.dest_entry.get()
        import threading
        threading.Timer(time_until_backup, lambda: self.perform_backup(source_paths, dest_path)).start()

        # show confirmation message
        for source_path in source_paths.split("*"):
            print(f"Backup scheduled from {source_path} to {dest_path} for {backup_datetime.strftime('%H:%M')}.")
        self.change_info("Backup scheduled!")

    def perform_backup(self, source_paths, dest_path):
        # validate paths
        if not all(self.validate_paths(source_path, dest_path) for source_path in source_paths.split("*")):
            return
        if not all(self.check_storage_space(source_path, dest_path) for source_path in source_paths.split("*")):
            return

        # remove previous backup data
        remove_data()

        # create backup name
        timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")

        # remove duplicate if it exists and copy file/folder
        for source_path in source_paths.split("*"):
            basename, extension = os.path.splitext(os.path.basename(os.path.normpath(source_path)))
            backup_name = f"{basename} - {timestamp}{extension}"
            final_path = os.path.join(dest_path, backup_name)

            try:
                if os.path.isfile(source_path) and os.path.isdir(dest_path):
                    if os.path.exists(final_path):
                        os.remove(final_path)
                    shutil.copy(source_path, final_path)
                    print(f"{source_path} copied to: {final_path}")
                    self.change_info("Backup completed!")
                elif os.path.isdir(source_path) and os.path.isdir(dest_path):
                    if os.path.exists(final_path):
                        shutil.rmtree(final_path)
                    shutil.copytree(source_path, final_path)
                    creation_time = datetime.now().timestamp()
                    os.utime(final_path, (creation_time, creation_time))
                    print(f"{source_path} copied to: {final_path}")
                    self.change_info("Backup completed!")

            except FileExistsError:
                print(f"Destination folder '{final_path}' already exists.")
                self.change_info("Destination already\nexists.")
            except PermissionError:
                print("Permission error. Please check file permissions.")
                self.change_info("Please check file\npermissions.")
            except shutil.Error as e:
                print(f"Backup failed: {str(e)}")
                self.change_info("Backup failed.")
            except Exception as e:
                print(f"An unexpected error occurred: {str(e)}")
                self.change_info("An unexpected\nerror occurred.")

def remove_data():
    # remove first backup from json file
    data = load_data()
    data['backups'].pop(0)
    save_data(data)

def add_data(source_entry, dest_entry, backup_time):
    # save data to json file
    data = load_data()

    backup_info = {
        'source': source_entry,
        'destination': dest_entry,
        'time': backup_time
    }

    data.setdefault("backups", []).append(backup_info)
    save_data(data)

def save_data(data):
    # save data to json file
    with open(resource_path('config/data.json'), 'w') as file:
        json.dump(data, file, indent=4, default=str)

def load_data():
    # load data from json
    try:
        with open(resource_path('config/data.json'), 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print("No previous backup data found.")
        return None

def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
    # we are running in a bundle
        base_path = os.path.dirname(sys.executable)
    else:
    # we are running in a normal Python environment
        base_path = os.path.dirname(os.path.realpath(__file__))

    return os.path.join(base_path, relative_path)

def on_closing():
    # minimize to tray
    app.withdraw()
    image = Image.open(resource_path('config/icons/tray.ico'))
    icon = pystray.Icon("BackupScheduler", image, menu=pystray.Menu(
        pystray.MenuItem("Show", on_show),
        pystray.MenuItem("Quit", on_exit)))
    icon.run()

def on_show(icon, item):
    # show window
    icon.stop()
    app.deiconify()

def on_exit(icon, item):
    # exit app
    icon.stop()
    ctypes.windll.kernel32.ReleaseMutex(mutex)
    app.quit()

def enforce_single_instance():
    # create a mutex
    global mutex
    mutex = ctypes.windll.kernel32.CreateMutexW(None, False, "BackupScheduler_mutex")
    
    # if the mutex already exists, exit the program
    if ctypes.windll.kernel32.GetLastError() == 183:  # ERROR_ALREADY_EXISTS
        print("BackupScheduler is already running.")
        sys.exit(0)

if __name__ == "__main__":
    # check if app is already running
    # enforce_single_instance()
    app = BackupScheduler()
    print("Running BackupScheduler...")
    app.iconbitmap(resource_path('config/icons/BackupScheduler.ico'))
    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()