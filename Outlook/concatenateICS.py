# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 12:57:19 2025

@author: abusch
"""

import os

def concatenate_ics_in_directory(directory):
    """Concatenate all .ics files in a directory into one."""
    combined_events = []
    header = None
    footer = "END:VCALENDAR"

    # Get all .ics files in the directory
    files = [f for f in os.listdir(directory) if f.endswith(".ics")]
    if not files:
        print("No .ics files found in the directory.")
        return

    # Process each .ics file
    for file in files:
        file_path = os.path.join(directory, file)
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        # Separate header and footer from events
        if not header:
            header = []
            for line in lines:
                stripped_line = line.strip()
                if stripped_line == "BEGIN:VEVENT":
                    break
                header.append(stripped_line)
        
        # Extract events
        in_event = False
        for line in lines:
            stripped_line = line.strip()
            if stripped_line == "BEGIN:VEVENT":
                in_event = True
                combined_events.append(stripped_line)
            elif stripped_line == "END:VEVENT":
                combined_events.append(stripped_line)
                in_event = False
            elif in_event:
                combined_events.append(stripped_line)
    
    # Combine all parts into a single file
    output_file = os.path.join(directory, "all.ics")
    with open(output_file, 'w') as f:
        f.write("\n".join(header) + "\n")
        f.write("\n".join(combined_events) + "\n")
        f.write(footer + "\n")
    
    print(f"Combined ICS file created at {output_file}")

# Usage
directory = r"C:\Users\abusch\Downloads"
concatenate_ics_in_directory(directory)

