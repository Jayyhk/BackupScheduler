import tkinter as tk
from tkinter import filedialog
import shutil
import os
import sys
import ctypes
import webbrowser
import json
import threading
import time
from datetime import datetime, timedelta
import customtkinter
from PIL import Image
import pystray


class BackupScheduler(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("BackupScheduler")
        dpi = ctypes.windll.user32.GetDpiForWindow(customtkinter.CTk().winfo_id())
        ppi = customtkinter.CTk().winfo_fpixels("1i")
        scale = dpi / ppi
        app_width = 784
        app_height = 196
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width / 2 - app_width / 2) * scale)
        y = int((screen_height / 2 - app_height / 2) * scale)
        self.geometry(f"{app_width}x{app_height}+{x}+{y}")
        self.resizable(False, False)

        # configure appearance
        customtkinter.set_appearance_mode("Dark")
        customtkinter.set_default_color_theme("blue")

        # configure sideframe
        self.sidebar_frame = customtkinter.CTkFrame(
            master=self, width=50, corner_radius=0
        )
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(
            master=self.sidebar_frame,
            text="Backup\nScheduler",
            font=customtkinter.CTkFont(size=18, weight="bold"),
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 20))

        # configure github logo
        github_logo = customtkinter.CTkImage(
            dark_image=Image.open(resource_path("config/icons/github.png")),
            size=(42, 42),
        )
        self.github_label = customtkinter.CTkLabel(
            master=self.sidebar_frame,
            image=github_logo,
            width=50,
            height=50,
            text="",
            fg_color="transparent",
        )
        self.github_label.bind(
            "<Button-1>",
            lambda event: webbrowser.open("https://github.com/Jayyhk/BackupScheduler"),
        )
        self.github_label.bind(
            "<Enter>", lambda event: self.github_label.configure(cursor="hand2")
        )
        self.github_label.bind(
            "<Leave>", lambda event: self.github_label.configure(cursor="")
        )
        self.github_label.grid(row=3, column=0, padx=20, pady=(50, 0))

        # configure widgets
        self.source_entry = customtkinter.CTkEntry(
            master=self, placeholder_text="Source Path", width=484
        )
        self.source_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.source_file_button = customtkinter.CTkButton(
            master=self, text="File", width=68, command=self.browse_source_file
        )
        self.source_file_button.grid(row=0, column=2, padx=5, pady=10, sticky="w")
        self.source_folder_button = customtkinter.CTkButton(
            master=self, text="Folder", width=68, command=self.browse_source_folder
        )
        self.source_folder_button.grid(row=0, column=2, padx=5, pady=10, sticky="e")
        self.dest_entry = customtkinter.CTkEntry(
            master=self, placeholder_text="Destination Path", width=484
        )
        self.dest_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        self.browse_dest_button = customtkinter.CTkButton(
            master=self, text="Folder", command=self.browse_dest
        )
        self.browse_dest_button.grid(row=1, column=2, padx=5, pady=10, sticky="")
        self.date_label = customtkinter.CTkLabel(
            master=self, text="Date:", text_color="#DCE4EE", fg_color="transparent"
        )
        self.date_label.grid(row=2, column=1, padx=16, pady=10, sticky="w")
        self.date_entry = customtkinter.CTkEntry(
            master=self, placeholder_text="mm-dd", width=55
        )
        self.date_entry.grid(row=2, column=1, padx=(55, 10), pady=10, sticky="w")
        self.time_label = customtkinter.CTkLabel(
            master=self, text="Time:", text_color="#DCE4EE", fg_color="transparent"
        )
        self.time_label.grid(row=2, column=1, padx=(120, 10), pady=10, sticky="w")
        self.time_entry = customtkinter.CTkEntry(
            master=self, placeholder_text="HH:MM", width=58
        )
        self.time_entry.grid(row=2, column=1, padx=(161, 10), pady=10, sticky="w")

        self.schedule_backup_button = customtkinter.CTkButton(
            master=self, text="Schedule Backup", width=170, command=self.save_changes
        )
        self.schedule_backup_button.grid(
            row=3, column=1, padx=(70, 10), pady=(10, 20), sticky="w"
        )
        self.backup_button = customtkinter.CTkButton(
            master=self,
            text="Backup Now",
            width=170,
            command=lambda: self.add_instant_backup(
                self.source_entry.get(), self.dest_entry.get()
            ),
        )
        self.backup_button.grid(
            row=3, column=1, padx=(10, 70), pady=(10, 20), sticky="e"
        )
        self.clear_button = customtkinter.CTkButton(
            master=self, text="Clear Fields", command=lambda: self.clear_fields()
        )
        self.clear_button.grid(row=2, column=2, padx=5, pady=10, sticky="")
        self.info_label = customtkinter.CTkLabel(
            master=self, text="", text_color="#242424", fg_color="transparent"
        )
        self.info_label.grid(row=3, column=2, padx=5, pady=5, sticky="")

        # configure checkboxes
        daily_var = customtkinter.StringVar(value="off")
        weekly_var = customtkinter.StringVar(value="off")
        monthly_var = customtkinter.StringVar(value="off")
        self.daily = False
        self.weekly = False
        self.monthly = False

        def daily_event():
            print("daily checkbox toggled, current value:", daily_var.get())
            if daily_var.get() == "on":
                self.daily = True
            else:
                self.daily = False

        def weekly_event():
            print("weekly checkbox toggled, current value:", weekly_var.get())
            if weekly_var.get() == "on":
                self.weekly = True
            else:
                self.weekly = False

        def monthly_event():
            print("monthly checkbox toggled, current value:", monthly_var.get())
            if monthly_var.get() == "on":
                self.monthly = True
            else:
                self.monthly = False

        self.daily_checkbox = customtkinter.CTkCheckBox(
            master=self,
            text="Daily",
            text_color="#DCE4EE",
            command=daily_event,
            variable=daily_var,
            onvalue="on",
            offvalue="off",
        )
        self.daily_checkbox.grid(row=2, column=1, padx=(10, 150), pady=10, sticky="e")
        self.weekly_checkbox = customtkinter.CTkCheckBox(
            master=self,
            text="Weekly",
            text_color="#DCE4EE",
            command=weekly_event,
            variable=weekly_var,
            onvalue="on",
            offvalue="off",
        )
        self.weekly_checkbox.grid(row=2, column=1, padx=(10, 80), pady=10, sticky="e")
        self.monthly_checkbox = customtkinter.CTkCheckBox(
            master=self,
            text="Monthly",
            text_color="#DCE4EE",
            command=monthly_event,
            variable=monthly_var,
            onvalue="on",
            offvalue="off",
        )
        self.monthly_checkbox.grid(row=2, column=1, padx=(10, 0), pady=10, sticky="e")

    def clear_fields(self):
        self.source_entry.delete(0, tk.END)
        self.source_entry.configure(placeholder_text="Source Path")
        self.dest_entry.delete(0, tk.END)
        self.dest_entry.configure(placeholder_text="Destination Path")
        self.date_entry.delete(0, tk.END)
        self.date_entry.configure(placeholder_text="mm-dd")
        self.time_entry.delete(0, tk.END)
        self.time_entry.configure(placeholder_text="HH:MM")
        self.daily_checkbox.deselect()
        self.daily = False
        self.weekly_checkbox.deselect()
        self.weekly = False
        self.monthly_checkbox.deselect()
        self.monthly = False

    def change_info(self, text):
        # change info label text
        self.info_label.configure(text=text)
        steps = 80

        # convert start and end colors to RGB format
        start_rgb = tuple(int("242424"[i : i + 2], 16) for i in (0, 2, 4))
        end_rgb = tuple(int("DCE4EE"[i : i + 2], 16) for i in (0, 2, 4))

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
        # add backup now to json file
        add_to_queue(source_path, dest_path, datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.perform_backup(source_path, dest_path)

    def save_changes(self):
        source_paths = self.source_entry.get()
        dest_path = self.dest_entry.get()

        # validate fields
        if all(
            [self.source_entry.get(), self.dest_entry.get(), self.time_entry.get()]
        ) or all(
            [self.source_entry.get(), self.dest_entry.get(), self.date_entry.get()]
        ):
            if not all(
                self.validate_paths(source_path, dest_path)
                for source_path in source_paths.split("*")
            ):
                return
            if not all(
                self.check_storage_space(source_path, dest_path)
                for source_path in source_paths.split("*")
            ):
                return
            self.schedule_backup()
        else:
            print("Please fill in all fields.")
            self.change_info("Please fill in all fields.")

    def schedule_backup(self):
        # store paths
        source_paths = self.source_entry.get()
        dest_path = self.dest_entry.get()

        # validate time format
        try:
            backup_string = self.date_entry.get() + " " + self.time_entry.get()
            backup_string = backup_string.strip()
            year = datetime.now().year
            backup_datetime = datetime.strptime(
                str(year) + "-" + backup_string, "%Y-%m-%d %H:%M"
            )
        except ValueError:
            try:
                backup_datetime = datetime.strptime(
                    str(year) + "-" + backup_string, "$Y-%m-%d"
                )
            except ValueError:
                try:
                    backup_datetime = datetime.strptime(backup_string, "%H:%M")
                    current_date = datetime.now().strftime("%Y-%m-%d")
                    backup_datetime_string = current_date + " " + backup_string
                    backup_datetime = datetime.strptime(
                        backup_datetime_string, "%Y-%m-%d %H:%M"
                    )
                except ValueError:
                    print("Invalid time format. Please use mm-dd and HH:MM.")
                    self.change_info(
                        "Invalid time format.\nPlease use mm-dd and HH:MM."
                    )
                    return

        # calculate backup datetime
        now = datetime.now()
        if now > backup_datetime:
            if now.date() > backup_datetime.date():
                adj_year = now.year % 4
                if adj_year == 0:
                    adj_year += 4
                if (datetime(3, 3, 1) <= now.date().replace(year=adj_year)) and (
                    now.date().replace(year=adj_year) < datetime(4, 2, 29)
                ):
                    backup_datetime += timedelta(days=366)
                else:
                    backup_datetime += timedelta(days=365)
            elif backup_datetime + timedelta(days=1) > now:
                backup_datetime += timedelta(days=1)
        backup_string = backup_datetime.strftime("%Y-%m-%d %H:%M")

        # add backup data to json file
        add_to_queue(source_paths, dest_path, backup_string)

        # wait until backup time and perform backup
        time_until_backup = (backup_datetime - datetime.now()).total_seconds()
        threading.Timer(
            time_until_backup, lambda: self.perform_backup(source_paths, dest_path)
        ).start()

        # show confirmation message
        for source_path in source_paths.split("*"):
            print(
                f"Backup scheduled from {source_path} to {
                    dest_path} for {backup_datetime.strftime('%H:%M')}."
            )
        self.change_info("Backup scheduled!")

    def perform_backup(self, source_paths, dest_path):
        # validate paths
        if not all(
            self.validate_paths(source_path, dest_path)
            for source_path in source_paths.split("*")
        ):
            return
        if not all(
            self.check_storage_space(source_path, dest_path)
            for source_path in source_paths.split("*")
        ):
            return

        # move first backup from queue to history
        move_to_history()

        # create backup name
        timestamp = datetime.now().strftime("%Y-%m-%d %H-%M")

        # remove duplicate if it exists and copy file/folder
        for source_path in source_paths.split("*"):
            basename, extension = os.path.splitext(
                os.path.basename(os.path.normpath(source_path))
            )
            backup_name = f"{basename} - {timestamp}{extension}"
            final_path = os.path.join(dest_path, backup_name)
            try:
                if os.path.isfile(source_path) and os.path.isdir(dest_path):
                    if os.path.exists(final_path):
                        os.remove(final_path)
                    shutil.copy(source_path, final_path)
                    print(f"{source_path} copied to: {final_path}")
                    try:
                        self.change_info("Backup completed!")
                    except Exception as e:
                        print(f"An error occurred while changing info: {str(e)}")
                        pass
                elif os.path.isdir(source_path) and os.path.isdir(dest_path):
                    if os.path.exists(final_path):
                        shutil.rmtree(final_path)
                    shutil.copytree(source_path, final_path)
                    creation_time = datetime.now().timestamp()
                    os.utime(final_path, (creation_time, creation_time))
                    print(f"{source_path} copied to: {final_path}")
                    try:
                        self.change_info("Backup completed!")
                    except Exception as e:
                        print(f"An error occurred while changing info: {str(e)}")
                        pass
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


def move_to_history():
    # remove first backup from json file
    data = load_data()
    backup = data["queue"].pop(0)
    data.setdefault("history", []).append(backup)

    # check if the backup was daily, weekly, or monthly and if so, schedule another
    if backup["daily"]:
        backup_datetime = datetime.strptime(backup["time"], "%Y-%m-%d %H:%M")
        backup_datetime += timedelta(days=1)
        backup["time"] = backup_datetime.strftime("%Y-%m-%d %H:%M")
        data.setdefault("queue", []).append(backup)
    if backup["weekly"]:
        backup_datetime = datetime.strptime(backup["time"], "%Y-%m-%d %H:%M")
        backup_datetime += timedelta(days=7)
        backup["time"] = backup_datetime.strftime("%Y-%m-%d %H:%M")
        data.setdefault("queue", []).append(backup)
    if backup["monthly"]:
        backup_datetime = datetime.strptime(backup["time"], "%Y-%m-%d %H:%M")
        backup_datetime += timedelta(days=30)
        backup["time"] = backup_datetime.strftime("%Y-%m-%d %H:%M")
        data.setdefault("queue", []).append(backup)
    save_data(data)


def add_to_queue(source_entry, dest_entry, backup_time):
    # save data to json file
    data = load_data()
    backup_info = {
        "source": source_entry,
        "destination": dest_entry,
        "time": backup_time,
        "daily": app.daily,
        "weekly": app.weekly,
        "monthly": app.monthly,
    }
    data.setdefault("queue", []).append(backup_info)

    # sort queue by time
    data["queue"] = sorted(data["queue"], key=lambda k: k["time"])
    save_data(data)


def save_data(data):
    # save data to json file
    with open(resource_path("config/data.json"), "w") as file:
        json.dump(data, file, indent=4, default=str)


def load_data():
    # load data from json
    try:
        with open(resource_path("config/data.json"), "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print("No previous backup data found.")
        return None


def resource_path(relative_path):
    if getattr(sys, "frozen", False):
        # we are running in a bundle
        base_path = os.path.dirname(sys.executable)
    else:
        # we are running in a normal python environment
        base_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(base_path, relative_path)


def check_queue():
    # check queue to see if any backup times have passed
    data = load_data()
    if data:
        for backup in data["queue"]:
            backup_datetime = datetime.strptime(backup["time"], "%Y-%m-%d %H:%M")
            if datetime.now() > backup_datetime:
                app.perform_backup(backup["source"], backup["destination"])


def check_queue_periodically():
    # check queue every minute
    while True:
        check_queue()
        print(
            "Checking queue at "
            + (datetime.now() + timedelta(minutes=1)).strftime("%Y-%m-%d %H:%M:%S")
        )
        time.sleep(60)


def on_closing():
    # minimize to tray
    app.withdraw()
    image = Image.open(resource_path("config/icons/tray.ico"))
    icon = pystray.Icon(
        "BackupScheduler",
        image,
        menu=pystray.Menu(
            pystray.MenuItem("Show", on_show), pystray.MenuItem("Quit", on_exit)
        ),
    )
    icon.run()


def on_show(icon, item):
    # show window
    icon.stop()
    app.deiconify()
    app.lift()
    app.focus_force()


def on_exit(icon, item):
    # exit app
    icon.stop()
    app.quit()


if __name__ == "__main__":
    # start app
    app = BackupScheduler()
    print("Running BackupScheduler...")
    queue_thread = threading.Thread(target=check_queue_periodically)
    queue_thread.start()
    app.iconbitmap(resource_path("config/icons/BackupScheduler.ico"))
    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()
