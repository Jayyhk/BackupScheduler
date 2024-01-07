# BackupScheduler

BackupScheduler is a Python application built using the [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) UI-library to provide an easy-to-use interface for scheduling and performing backups. You can schedule regular backups of files or folders from a specified source to a destination location. Furthermore, you can perform immediate backups as needed.

## Features

- **🖥️ User-Friendly Interface:** The application provides an intuitive and minimalistizc GUI for users to input source and destination paths, set backup schedules, and perform backups instantly on directories or multiple files at once.

- **🕒 Scheduled Backups:** Users can schedule backups at specific times using the HH:MM (24-hour) format. The application utilizes threading to wait until the scheduled time and then automatically triggers the backup process.

- **🔄 Backup Continuity:** Scheduled backups continue to execute even when the application is closed or minimized to the system tray.

- **⚡Immediate Backup:** Users can perform immediate backups by clicking the "Backup Now" button without inputting a scheduled time.

## Usage

1. **Selecting Paths:**
   - Click the "File" or "Folder" button or enter the source path manually to select individual files for backup.

      - **Multiple Files Support:**
         
         To select multiple individual files at once, separate the file paths with an asterisk (`*`). For example:
         ```
         /path/to/file1.txt*/path/to/file2.txt*/path/to/file3.txt
    - Click the "Folder" button or enter the destination path manually to select the location of the backup. 
    - A backup will only happen if the selected directories exist.

2. **Choosing a Backup Time:**
   - Enter the desired backup time in the "HH:MM" (24-hour) format.

3. **Backing up:**
   - Click the "Schedule Backup" button to schedule the backup for the selected time or click the "Backup Now" button to perform an immediate backup.

4. **Minimizing to Tray:**
   - Click the "X" button on the application window to minimize it to the system tray. **BackupScheduler** will continue to run the background.
   - Right-click the BackupScheduler icon in the system tray to access options to show the window or quit the application.

## Run

1. Run the BackupScheduler application:
```bash
python BackupScheduler.py
```
## To Implement

- **⏳️ Repeated Backups:** Create checkboxes for daily, weekly, monthly, etc. or a custom interval.

- **📊 Backup Tracking:** Develop a separate tab or section that tracks backup history. Provide insights into the date, time, size, and status of each backup operation.

- **🔁 Update Previous Backup:** Add an option to replace an existing backup.

## Additional Notes

Images used in the application are included in the "icons" folder.

Feel free to customize and enhance the application according to your needs. Happy backing up!