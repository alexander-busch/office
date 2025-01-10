# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 07:42:37 2024

@author: abusch
"""

import sqlite3
import os
import re
from PyPDF2 import PdfReader
import shutil

directory_Zotero = r"C:\Users\abusch\Zotero"
directory_pdf = r"\\turboserver\library\Zotero\pdf"  # Change this to your direc







def findPotentiallyRedundantZoteroAttachments(allZoteroAttachments, n=None):
    """
    Find potentially redundant Zotero attachments by identifying files with common prefixes.
    
    Args:
        allZoteroAttachments (list): List of tuples where the second element is the file name.
        n (int, optional): Number of characters after the prefix to include in the identification process. Defaults to None (use entire prefix).
    
    Returns:
        dict: A dictionary of redundant entries where the key is the cleaned prefix and the value is the list of matching entries.
    """
    # Find similar items in allZoteroAttachments based on "author(s) - YYYY -"
    pattern = r"^(attachments:.*?-\s\d{4}\s-)"

    # Use a defaultdict to group files by their common prefix
    groups = defaultdict(list)

    for row in allZoteroAttachments:
        match = re.match(pattern, row[1])
        if match:
            # Extract the prefix including 'attachments:'
            prefix = match.group(1)
            
            # If n is provided, extend the prefix to include the next n characters
            if n is not None:
                # Add the next n characters after the initial pattern
                prefix = row[1][:match.end() + n]
            
            # Remove the 'attachments:' part from the prefix
            cleaned_prefix = prefix.replace("attachments:", "").strip()
            groups[cleaned_prefix].append(row[1])   

    # Identify redundant entries: groups with more than one file
    redundant_entries = {prefix: group for prefix, group in groups.items() if len(group) > 1}

    # Output the redundant entries
    for prefix, group in redundant_entries.items():
        print(f"Redundant group '{prefix}':")
        for entry in group:
            print(f"  {entry}")
    
    return redundant_entries

def find_indices_of_string_in_tuples_list(tuples_list, search_string):
    """
    Find the indices of tuples where the last element contains the search string as a substring.

    Args:
        tuples_list (list): List of tuples with two or three elements.
        search_string (str): Substring to search for in the last element of the tuples.

    Returns:
        list: List of indices where the substring is found, or an empty list if no matches.
    """
    indices = []  # List to store matching indices

    for index, item in enumerate(tuples_list):
        *_, string = item  # Dynamically extract the last element of the tuple
        if search_string in string:  # Check if search_string is a substring of the last element
            indices.append(index)

    return indices  # Return list of indices of matches




def get_strings_by_list_indices(data, indices):
    """
    Get the last element (string) of tuples in the list, given a list of indices.
    The tuples can have two or three elements, and the string is always the last element.

    Args:
        data (list): List of tuples (with either two or three elements).
        indices (list): List of indices for which strings should be retrieved.

    Returns:
        list: List of strings corresponding to the specified indices, or an error message for invalid indices.
    """
    result_strings = []
    
    for index in indices:
        if 0 <= index < len(data):  # Check if the index is valid
            # Extract the last element (string) of the tuple, regardless of its length
            result_strings.append(data[index][-1])  
        else:
            result_strings.append("Index out of range")  # Handle invalid indices
    
    return result_strings


def find_possible_matches(zoteroAttachmentName, allPDFfiles, n=None):
    """
    Find possible matches for a Zotero filename based on the pattern "Author(s) - YYYY -".
    Optionally include the next 'n' characters after the pattern.

    Args:
        zoteroAttachmentName (tuple or string): A tuple or string containing file details, with the filename as the second element.
        allPDFfiles (list): List of all PDF filenames to compare against.
        n (int, optional): Number of additional characters to include after the pattern.

    Returns:
        list: List of filenames from allPDFfiles that match the pattern (and optional additional characters).
    """
    # Convert zoteroAttachmentName to a string if it’s a tuple
    if isinstance(zoteroAttachmentName, tuple):
        zoteroAttachmentName = zoteroAttachmentName[1]
    elif not isinstance(zoteroAttachmentName, str):
        raise ValueError("Input must be a tuple or a string.")

    # Match the pattern "Author(s) - YYYY -"
    result = re.match(r"^(.*?-\s\d{4}\s-)", zoteroAttachmentName)

    if result:
        # Extract base prefix
        authorYear = result.group(1).strip()

        # Optionally include the next 'n' characters after the pattern
        if n:
            # Extract 'n' characters following the matched prefix
            start_index = len(authorYear)
            extended_authorYear = authorYear + zoteroAttachmentName[start_index:start_index + n]
        else:
            extended_authorYear = authorYear

        # Find possible matches in allPDFfiles
        possibleMatches = [
            entry for entry in allPDFfiles 
            if entry.startswith(extended_authorYear.replace("attachments:", "", 1))
        ]

        return possibleMatches

    # Return an empty list if no match is found
    return []



def sync_zoteroDBfilenames_with_pdfFilenames(directory_Zotero, directory_pdf, modifyFiles):
    """
    Query the Zotero database to update paths in the itemAttachments table.

    Args:
        directory_Zotero (str): directory_Zotero containing the Zotero SQLite database.
        modifyFiles (bool): Whether to actually modify the database or just log the changes.
    """
    # Path to Zotero SQLite database
    db_path = os.path.join(directory_Zotero, "zotero.sqlite")
    print(f"Zotero DB path: {db_path}")

    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Log file for tracking changes
    log_file_path = os.path.join(directory_Zotero, "sync_zoteroDBfilenames_with_pdfFilenames.txt")
    print(f"Log file path: {log_file_path}")

    with open(log_file_path, 'w', encoding='utf-8') as log_file:
        # Query all entries in the itemAttachments table
        cursor.execute("""
            SELECT itemID, path FROM itemAttachments WHERE path LIKE '%.pdf'
        """)
        
        
        # Additionally checks for the first n characters after "authors(s) - YYYY -"
        addNchar = 10
        
        # Debug - Process a single entry
# =============================================================================
#         allZoteroAttachments = cursor.fetchall()
#         redundant_entries = findPotentiallyRedundantZoteroAttachments(allZoteroAttachments)
#         redundant_entries = findPotentiallyRedundantZoteroAttachments(allZoteroAttachments,addNchar)
#         indices = find_indices_of_string_in_tuples_list(allZoteroAttachments, 'Salazar-Mendoza et al - 2009')
#         redundantExample = get_strings_by_list_indices(allZoteroAttachments, indices)
#         print("Example for redundant PDF attachments in Zotero:")
#         for i, s in zip(indices, redundantExample):
#             print(f"List Index {i}: {s}")        
#         zoteroAttachmentName = allZoteroAttachments[indeces[1]][1]
# =============================================================================
        
        # Get all pdf files
        allPDFfiles = sorted(os.listdir(directory_pdf))
        
        
        # Process each entry
        for itemID, zoteroAttachmentName in cursor.fetchall():
            
            # Debug itemID = 1234
                        
            # Log
            stringToPrint = f"Processing itemID {itemID}: {zoteroAttachmentName}"
            log_file.write(stringToPrint + "\n")
            print(stringToPrint)
            
            possibleMatches = find_possible_matches(zoteroAttachmentName, allPDFfiles, addNchar)
            
            for possibleMatch in possibleMatches:
                # Debug
                # possibleMatch = possibleMatches[0]
                
                zoteroFileName = zoteroAttachmentName.replace("attachments:", "", 1)
                
                if possibleMatch == zoteroFileName:
                    # Log
                    stringToPrint = f"Zotero Attachment file name {zoteroFileName} matchess file name on disk {possibleMatch}"
                    log_file.write(stringToPrint + "\n")
                    print(stringToPrint)
                else: 
                    # change the Zotero database string such that it conforms to the pdf on disk
                    newAttachmentName = f"attachments:{possibleMatch}"
                    # Log
                    stringToPrint = f"Zotero Attachment file name {zoteroFileName} will be modified to {newAttachmentName} to match file name on disk {possibleMatch}"
                    log_file.write(stringToPrint + "\n")
                    print(stringToPrint)
                    
                    if modifyFiles:
                        # Update the database with the new path
                        cursor.execute("""
                            UPDATE itemAttachments
                            SET path = ?
                            WHERE itemID = ? AND path = ?
                        """, (newAttachmentName, itemID, zoteroAttachmentName))
                        print(f"Database updated for itemID {itemID}")
                
        # Commit changes if modifyFiles is True
        if modifyFiles:
            print("Committing changes to the database.")
            conn.commit()

    # Close the connection
    conn.close()
    print("Database connection closed.")
    

modifyFiles  = True
modifyFiles  = False

sync_zoteroDBfilenames_with_pdfFilenames(directory_Zotero, directory_pdf, modifyFiles)
