# BackupScheduler

BackupScheduler is a Python application built using the [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) UI-library to provide an easy-to-use interface for scheduling and performing backups.

![](https://i.imgur.com/BtlJR8P.png)

## Features

- **🖥️ User-Friendly Interface:** BackupScheduler provides an intuitive and minimalistic GUI for users to input source and destination paths, set backup schedules, and perform backups instantly on directories or multiple files at once.

- **🕒 Schedule Backups:** Users can schedule backups at specific times using the `mm-dd` date format and/or `HH:MM` (24-hour) time format. Backups can be scheduled daily, weekly, monthly, or none of those.

- **🔄 Backup Continuity:** Scheduled backups continue to execute even when BackupScheduler is minimized to the system tray or closed.

- **⚡ Immediate Backup:** Users can perform immediate backups by clicking the "Backup Now" button without inputting a scheduled time.

- **📊 Backup Tracking:** Data from previous backups as well as the current queue can be found in the `data.json` file in the `config` folder.

## Requirements
- Python 3.12
- Tkinter
- CustomTkinter
- Pillow (PIL)
- pystray

## Installation

1. Install the required libraries from the command line:

   ```bash
   pip install tk customtkinter pillow pystray 
   ```

2. Execute the BackupScheduler application:
   ```bash
   py BackupScheduler.py
   ```

   - Also be sure to update the existing installation of CustomTkinter as often as possible because the library is under active development.

      ```bash
      pip install customtkinter --upgrade
      ```
> [!IMPORTANT]
> Make sure the `config folder` is in the same directory as the script when running the script through the command line or through an executable compiled with PyInstaller.

## Usage

1. **Selecting Paths:**
   - Click the "File" or "Folder" button or enter the source and destination paths manually to select individual files for backup.

> [!NOTE]
> To select multiple individual files at once, separate the file paths with an asterisk (`*`). For example:
> ```
> /path/to/file1.txt*/path/to/file2.txt*/path/to/file3.txt
> ```

2. **Backing Up:**
   - Enter the desired backup time in the `mm-dd` date format and/or `HH:MM` (24-hour) time format.
   - Choose a daily, weekly, or monthly backup, or none of the above. 
   - Click the "Schedule Backup" button to schedule the backup for the selected time or click the "Backup Now" button to perform an immediate backup with your configurations applied to that backup.

3. **Minimizing to Tray:**
   - Click the "X" button on the application window to minimize it to the system tray. BackupScheduler will continue to run the background.
   - Right-click the BackupScheduler icon in the system tray to access options to show the window or quit the application.

## Additional Notes

Images used in the application are included in the `icons` folder in the `config` folder.

Feel free to open an issue if you spot a bug and customize and enhance the application according to your needs. Happy backing up!