# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 09:25:20 2024

@author: abusch
"""

import os
from PyPDF2 import PdfReader
import shutil
import re

def rename_files_and_to_etal(directory, modifyFiles):
    """
    Renames files matching the pattern "authorname1 and authorname2 - *"
    to "authorname1 et al - *".
    
    Args:
        directory (str): Directory containing the PDF files.
        modifyFiles (bool): Flag to indicate whether to actually rename files or just log them.
    """
    log_file_path = os.path.join(directory, "rename_files_and_to_etal.txt")

    with open(log_file_path, 'w', encoding='utf-8') as log_file:
        # Loop through all files in the directory
        for filename in os.listdir(directory):
            # Check if the file is a PDF
            if filename.endswith(".pdf"):
                # Use regular expression to check for the pattern "authorname1 and authorname2 - *"
                match = re.match(r"^([a-zA-Z0-9\s]+) and ([a-zA-Z0-9\s]+) - (.*)\.pdf$", filename)

                if match:
                    # Extract author names and the rest of the filename
                    authorname1 = match.group(1).strip()
                    authorname2 = match.group(2).strip()
                    rest_of_filename = match.group(3).strip()
                    
                    # Create the new filename
                    new_filename = f"{authorname1} et al - {rest_of_filename}.pdf"
                    
                    # Log the old and new filenames
                    log_file.write(f"Old Filename: {filename} -> New Filename: {new_filename}\n")
                    
                    if modifyFiles:
                        # Define full file paths
                        old_file_path = os.path.join(directory, filename)
                        new_file_path = os.path.join(directory, new_filename)
                        
                        # Check if the new file already exists
                        if os.path.exists(new_file_path):
                            # Delete the existing file with the new name
                            os.remove(new_file_path)
                            print(f"Deleted existing file: {new_file_path}")
                        
                        # Rename the file
                        os.rename(old_file_path, new_file_path)
                        print(f"Renamed: {filename} -> {new_filename}")
                    else:
                        print(f"Would rename: {filename} -> {new_filename} (not actually renaming because modifyFiles is False)")


def rename_files_remove_dot(directory, modifyFiles):
    """
    Renames files matching the pattern "authorname et al. - *"
    to "authorname et al - *" by removing the period after "et al.".
    
    Args:
        directory (str): Directory containing the PDF files.
        modifyFiles (bool): Flag to indicate whether to actually rename files or just log them.
    """
    log_file_path = os.path.join(directory, "renamed_files_remove_dot.txt")

    with open(log_file_path, 'w', encoding='utf-8') as log_file:
        # Loop through all files in the directory
        for filename in os.listdir(directory):
            # Check if the file is a PDF
            if filename.endswith(".pdf"):
                # Use regular expression to check for the pattern "authorname et al. - *"
                match = re.match(r"^([a-zA-Z0-9\s]+) et al\.\s*-\s*(.*)\.pdf$", filename)

                if match:
                    # Extract author name and the rest of the filename
                    authorname = match.group(1).strip()
                    rest_of_filename = match.group(2).strip()
                    
                    # Create the new filename by removing the period after "et al"
                    new_filename = f"{authorname} et al - {rest_of_filename}.pdf"
                    
                    # Log the old and new filenames
                    log_file.write(f"Old Filename: {filename} -> New Filename: {new_filename}\n")
                    
                    if modifyFiles:
                        # Define full file paths
                        old_file_path = os.path.join(directory, filename)
                        new_file_path = os.path.join(directory, new_filename)
                        
                        # Check if the new file already exists
                        if os.path.exists(new_file_path):
                            # Delete the existing file with the new name
                            os.remove(new_file_path)
                            print(f"Deleted existing file: {new_file_path}")
                        
                        # Rename the file
                        os.rename(old_file_path, new_file_path)
                        print(f"Renamed: {filename} -> {new_filename}")
                    else:
                        print(f"Would rename: {filename} -> {new_filename} (not actually renaming because modifyFiles is False)")


# Example usage
directory = r"D:\turboserver\library\Zotero\pdf"

modifyFiles=True
modifyFiles=False

# Rename files matching the first pattern
rename_files_and_to_etal(directory, modifyFiles)

# Rename files matching the second pattern
rename_files_remove_dot(directory, modifyFiles)









def remove_redundant_filenames(directory, modifyFiles):
    """
    Removes redundant files by checking:
    1. If a file with a number at the end has the same base name and file size as its original version without the number.
    2. If a file name is a substring of another file name and they have the same file size, delete the shorter file name.

    Args:
        directory (str): Directory containing the PDF files.
        modifyFiles (bool): Flag to indicate whether to actually delete the redundant files or just log them.
    """
    log_file_path = os.path.join(directory, "remove_redundant_filenames.txt")

    with open(log_file_path, 'w', encoding='utf-8') as log_file:
        # Get all files in the directory and sort them alphabetically
        files = sorted(os.listdir(directory))
        
        # Loop through all files in the directory
        for filename in files:
            # Check if the file is a PDF
            if filename.endswith(".pdf"):
                log_file.write(f"Processing {filename} \n")
                
                # Debug
                # filename = files[62]
               
                # possibleDuplicates = [entry for entry in files if entry.startswith(filename[:-4]) and len(entry) > len(filename)]
                possibleDuplicates = [entry for entry in files
                                      if entry.startswith(re.sub(r'(\d+)?\.pdf$', '', filename))
                                      and len(entry) > len(filename)]
                
                # debug
                # possibleDuplicate = possibleDuplicates[0]
                
                # Check if the original file exists
                for possibleDuplicate in possibleDuplicates:
                    
                    # Filepaths
                    filename_filepath = os.path.join(directory, filename)                    
                    possibleDuplicate_filepath = os.path.join(directory, possibleDuplicate)

                    if os.path.exists(possibleDuplicate_filepath):
                        try:
                            # Compare the file sizes
                            original_size = os.path.getsize(filename_filepath)
                            possDupl_size = os.path.getsize(possibleDuplicate_filepath)
                            
                            
                            # Calculate the acceptable size range
                            tolerance=0.10
                            min_size = original_size * (1 - tolerance)
                            max_size = original_size * (1 + tolerance)
                            
                            # Detemine file to potentially move
                            if len(filename_filepath) < len(possibleDuplicate_filepath):  # Compare without the ".pdf"
                                file_to_move = filename_filepath
                            else:
                                file_to_move = possibleDuplicate_filepath
                                
                            if original_size == possDupl_size:
                                log_file.write(f"Removing {possibleDuplicate} because {filename} has the same size.\n")
                                
                                if modifyFiles:
                                    try:
                                        #os.remove(os.path.join(directory, possibleDuplicate))
                                        print(f"Deleted: {filename}")
                                        shutil.move(file_to_move, os.path.join(directory, "backup"))
                                        print(f"Moved: {filename} to backup folder")
                                    except FileNotFoundError:
                                        print(f"File {possibleDuplicate} was already deleted or doesn't exist anymore.")
                                        continue
                            elif min_size <= possDupl_size <= max_size:
                                try:
                                    original_reader = PdfReader(filename_filepath)
                                    possDupl_reader = PdfReader(possibleDuplicate_filepath)
                                    if len(original_reader.pages)==len(possDupl_reader.pages):
                                        log_file.write(f"Removing {possibleDuplicate} because files have the same number of pages.\n")
                                        
                                        if modifyFiles:
                                            try:
                                                # os.remove(os.path.join(directory, possibleDuplicate))
                                                # print(f"Deleted: {filename}")
                                                shutil.move(file_to_move, os.path.join(directory, "backup"))
                                                print(f"Moved: {filename} to backup folder")
                                            except FileNotFoundError:
                                                print(f"File {possibleDuplicate} was already deleted or doesn't exist anymore.")
                                                continue
                                except Exception as e:
                                    print(f"pdf not readable")
                                    continue
                            else:
                                print(f"Files are not identical")                            
                        
                        except FileNotFoundError:
                            print(f"File not found during size comparison: {filename} or {possibleDuplicate}. Skipping...")
                            continue
                

# Example usage
directory = r"D:\turboserver\library\Zotero\pdf"  # Change this to your directory
directory = r"\\turboserver\library\Zotero\pdf"  # Change this to your directory

modifyFiles=True
modifyFiles=False

# Remove redundant files
remove_redundant_filenames(directory, modifyFiles)


import os
import re

def count_pdf_filename_lengths(directory, exclude_pattern):
    """
    Count the lengths of filenames for all PDFs in a directory and save the results to a text file.
    Also, identify the shortest filename and its length.

    Args:
        directory (str): Path to the directory containing PDF files.
        exclude_pattern (bool): Flag to exclude specific patterns from the filename length.
    """
    output_file = os.path.join(directory, "filenameLengths.txt")
    
    # Header for the output file
    header = "Filename\tLength\n" + "-" * 40 + "\n"

    # Compile regex for exclusion pattern if required
    pattern = re.compile(r".* - \d{4} -") if exclude_pattern else None

    shortest_filename = None
    shortest_length = float('inf')

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(header)

        # Iterate over files in the directory
        for filename in os.listdir(directory):
            if filename.endswith('.pdf'):
                original_length = len(filename)

                # Adjust length if exclude_pattern is True and pattern matches
                adjusted_length = original_length
                if exclude_pattern and pattern:
                    match = pattern.match(filename)
                    if match:
                        adjusted_length -= len(match.group(0))

                # Write to file
                f.write(f"{filename}\t{adjusted_length}\n")

                # Update shortest filename tracking
                if adjusted_length < shortest_length:
                    shortest_length = adjusted_length
                    shortest_filename = filename

        # Append the shortest filename to the file
        f.write("\n" + "-" * 40 + "\n")
        if shortest_filename is not None:
            f.write(f"Shortest Filename: {shortest_filename}\n")
            f.write(f"Length: {shortest_length}\n")
        else:
            f.write("No PDF files found.\n")

# Example usage
directory = r"\\turboserver\library\Zotero\pdf"
exclude_pattern = False  # Set to True to exclude patterns like " - YYYY -"
count_pdf_filename_lengths(directory, exclude_pattern)
