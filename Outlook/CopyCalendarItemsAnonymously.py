# -*- coding: utf-8 -*-
"""
@date: 30.01.25
@author: alexander.busch@alumni.ntnu.no
@description: A script to copy items from an Outlook Exchange source calendar anonomously to a target calendar
"""

# Requires the win32com library that provides access to many of the Windows APIs from Python >> pip install pywin32

import win32com.client
from datetime import datetime, timedelta, timezone
import os

# Initialize Outlook Application
outlook = win32com.client.Dispatch("Outlook.Application")
namespace = outlook.GetNamespace("MAPI")

# Define the source and target calendar
# outlook = win32com.client.Dispatch('Outlook.Application').GetNamespace('MAPI')
# source_calendar = outlook.getDefaultFolder(9).Items
source_calendar = namespace.Folders["someEmailAdress"].Folders["Calendar"]
target_calendar = namespace.Folders["someOtherEmailAdress"].Folders["Calendar"]
print(f"Source: {source_calendar}")
print(f"Target: {target_calendar}")

for folder in namespace.Folders["someEmailAdress"].Folders:
    print(folder.Name)

# Set start and end time
start_time = datetime.now(timezone.utc)
end_time = start_time + timedelta(days=30)
log = True

# Prepare to write logs to file
if log:
    log_directory = "D:\\logs"
    log_file_path = os.path.join(log_directory, "calendar_items_log.txt")
    
    # Ensure the directory exists
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    
    # Check if the log file exists
    if os.path.exists(log_file_path):
        # Delete the log file
        os.remove(log_file_path)
        print(f"Existing log file '{log_file_path}' deleted.")
    else:
        print(f"Log file '{log_file_path}' does not exist.")
    
    # Open the log file in write mode (UTF-8 encoding to handle special characters)
    #with open(log_file_path, "w", encoding="utf-8") as log_file:
    log_file = open(log_file_path, "a")  # Open the log file in append mode
    log_file.write("Calendar Item Information Log\n")
    log_file.write(f"Start Time: {start_time}\n")
    log_file.write(f"End Time: {end_time}\n\n")
    log_file.write("---------------------------------------------------------------------\n")

# Access the target calendar and delete all occurences of xxx appointments
try:    
    if target_calendar is None:
        print("Target calendar not found")
        if log:
            log_file.write("Target calendar not found\n")
        exit()

except Exception as e:
    print(f"Error accessing calendar: {e}")
    exit()

# Delete all items labeled "xxx" from the target calendar
if log:
    log_file.write("Deleting all old items in target calendar\n")

items = target_calendar.Items
item_count = items.Count
deleted_count = 0

for i in range(item_count, 0, -1):  # Loop through the items in reverse order
    item = items.Item(i)
    if item.Class == 26:  # Check if it's an appointment (Class 26 is AppointmentItem in Outlook)
        if item.Subject == "xxx":
            item.Delete()
            deleted_count += 1



# Get source calendar items, apply restriction, and sort them
calendar = source_calendar.Items
calendar.IncludeRecurrences = True
calendar.Sort('[Start]')

# Loop calendar items and write to target calendar
for item in calendar:
    if item.Start < start_time:
        continue
    
    if item.Start >= start_time:
        print(f"Subject: {item.Subject}, Start: {item.Start}, End: {item.End}")
        
        try:
            # Adding a new item to the target calendar
            new_item = target_calendar.Items.Add()  # Use Items.Add() without the argument
            
            # Setting the properties of the new item
            new_item.Subject = "xxx"
            # Use the actual 'Start' and 'End' properties from the current item
            new_item.Start = item.Start
            new_item.End = item.End
            
            # Copy other properties if needed
            new_item.BusyStatus = item.BusyStatus
            new_item.ReminderSet = False
            
            new_item.Save()  # Save the new item
            if log:
                log_file.write(f"Created entry {new_item.Subject} target calendar from {new_item.Start} to {new_item.End}\n")
        
        except Exception as e:
            print(f"Error creating item: {e}")

    # Stop the loop if the end time of an event exceeds the end_time
    if item.Start >= end_time:
        print(f"Subject: {item.Subject}, Start: {item.Start}, End: {item.End}")
        break


# Close the log file at the end of the script and open it in an editor
if log and log_file is not None:
    log_file.close()
    import subprocess
    # Launch Notepad with the log file
    subprocess.Popen(["notepad.exe", log_file_path])