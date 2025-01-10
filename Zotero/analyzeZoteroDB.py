# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 21:05:11 2024

@author: alexander.busch@alumni.ntnu.no
"""

import sqlite3
import os


def check_zotero_database(directory_Zotero):
    """
    Check the tables in the Zotero SQLite database to identify the available tables.
    
    Args:
        directory_Zotero (str): directory_Zotero containing the Zotero SQLite database.
    """
    # Path to Zotero SQLite database
    db_path = os.path.join(directory_Zotero, "zotero.sqlite")
    print(f"Checking Zotero DB path: {db_path}")
    
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Query to get all table names in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    
    # Fetch and print all table names
    tables = cursor.fetchall()
    print("Tables in the database:")
    for table in tables:
        print(table[0])
    
    # Close the connection to the database
    conn.close()


def display_first_x_entries(directory_Zotero, numberOfEntries, table_name):
    """
    Display the first 10 entries from a specified table in the Zotero SQLite database.
    
    Args:
        directory_Zotero (str): directory_Zotero containing the Zotero SQLite database.
        table_name (str): The name of the table to query.
    """
    # Path to Zotero SQLite database
    db_path = os.path.join(directory_Zotero, "zotero.sqlite")
    print(f"Zotero DB path: {db_path}")
    
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Query to fetch the first 10 entries from the specified table
    query = f"SELECT * FROM {table_name} LIMIT {numberOfEntries};"
    cursor.execute(query)
    
    # Fetch the results and print each row
    rows = cursor.fetchall()
    print(f"First {numberOfEntries} entries in the '{table_name}' table:")
    for row in rows:
        print(row)
    
    # Close the connection to the database
    conn.close()
    

def list_columns(directory_Zotero, table_name):
    """
    List the columns in a given table in the Zotero SQLite database.
    
    Args:
        directory_Zotero (str): directory_Zotero containing the Zotero SQLite database.
        table_name (str): The name of the table to query.
    """
    # Path to Zotero SQLite database
    db_path = os.path.join(directory_Zotero, "zotero.sqlite")
    print(f"Zotero DB path: {db_path}")
    
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Query to fetch the column names for the specified table
    cursor.execute(f"PRAGMA table_info({table_name});")
    
    # Fetch the results and print each column name
    columns = cursor.fetchall()
    print(f"Columns in the '{table_name}' table:")
    for column in columns:
        print(column[1])  # Column names are in the second index
    
    # Close the connection to the database
    conn.close()


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
    from collections import defaultdict
    groups = defaultdict(list)

    for row in allZoteroAttachments:
        import re
        match = re.match(pattern, row[-1])
        if match:
            # Extract the prefix including 'attachments:'
            prefix = match.group(1)
            
            # If n is provided, extend the prefix to include the next n characters
            if n is not None:
                # Add the next n characters after the initial pattern
                prefix = row[-1][:match.end() + n]
            
            # Remove the 'attachments:' part from the prefix
            cleaned_prefix = prefix.replace("attachments:", "").strip()
            groups[cleaned_prefix].append(row[-1])   

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




""" Usage ---------------------------------------------------------------------------------------------------------------------------------------"""    
directory_Zotero = r"C:\Users\abusch\Zotero"

zoteroDB_tables = check_zotero_database(directory_Zotero)

display_first_x_entries(directory_Zotero, 10, "items")
display_first_x_entries(directory_Zotero, 40, "itemDataValues")
display_first_x_entries(directory_Zotero, 20, "itemData")
display_first_x_entries(directory_Zotero, 10, "items")
display_first_x_entries(directory_Zotero, 40, "itemAttachments")
display_first_x_entries(directory_Zotero, 40, "fulltextItems")

list_columns(directory_Zotero, "itemAttachments")

list_columns(directory_Zotero, "items")
# this is the ParentItem?
# The file is copied to a directory named after the key field from the items table record of the attachment item



""" Query the Zotero database to retrieve and analyze the itemAttachments table --------------------------------------------------------------------"""    

# Path to Zotero SQLite database
db_path = os.path.join(directory_Zotero, "zotero.sqlite")
print(f"Zotero DB path: {db_path}")

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Query all entries in the itemAttachments table
cursor.execute("""
    SELECT itemID, parentItemID, linkMode, path
    FROM itemAttachments
    WHERE path LIKE '%.pdf'
""")

allZoteroAttachments = cursor.fetchall()
multipleAttachments = findPotentiallyRedundantZoteroAttachments(allZoteroAttachments)
# 220 in total
redundantAttachemnts = findPotentiallyRedundantZoteroAttachments(allZoteroAttachments, 10)
# 187 in total



storage_linkMode0 = [tup for tup in allZoteroAttachments if tup[2] == 0]
# 912 in total
# e.g. storage:Peak et al - 2007 - Simulation-Based Design Using SysML Part 1.pdf
# e.g. storage:Patankar - 1967 - Heat and mass transfer in turbulent boundary layer.pdf

storage_linkMode1 = [tup for tup in allZoteroAttachments if tup[2] == 1]
# 309 in total
# e.g. storage:Patel et al. - 1985 - Turbulence models for near-wall and low Reynolds n.pdf
# e.g. storage:Menter - Best Practice Scale-Resolving Simulations in ANSY.pdf

storage_linkMode2 = [tup for tup in allZoteroAttachments if tup[2] == 2]
# 3518
# attachment:Eggers et al - 1995 - Oscillating plate viscometer in the Hz to kHz rang.pdf
# D:\turboserver\library\Zotero\pdf\Oberkampf et al - 1998 - Issues in Computational Fluid Dynamics Code Verification and Validation.pdf

""" linkMode values

https://gist.github.com/pchemguy/19fa69fb4e74ef0cca0026aa0dbf5f42

LINK_MODE_IMPORTED_FILE = 0;
LINK_MODE_IMPORTED_URL = 1;
LINK_MODE_LINKED_FILE = 2;
LINK_MODE_LINKED_URL = 3;
LINK_MODE_EMBEDDED_IMAGE = 4;

The path field encodes the file system path of the attached file. Its value and interpretation depend on the attachment subtype:

LINK_MODE_LINKED_URL
The path field is NULL because the attachment is merely an Internet address
LINK_MODE_LINKED_FILE
If a file is stored within the "Linked Attachment Base Directory" (as defined in "Preferences->Advanced->Files and Folders"), the field contains the prefix "attachments:" followed by the file's relative path. Otherwise, Zotero probably stores absolute paths, but this option should generally be avoided.
LINK_MODE_IMPORTED_FILE, LINK_MODE_IMPORTED_URL, LINK_MODE_EMBEDDED_IMAGE
The file is copied to a directory named after the key field from the items table record of the attachment item. This directory is, in turn, created inside the "storage" directory located inside the "Data Directory" (as defined in "Preferences->Advanced->Files and Folders"). The path includes the prefix "storage:" followed by the file name.

"""





# Investigate a particlar item
indices = find_indices_of_string_in_tuples_list(allZoteroAttachments, 'Salazar-Mendoza et al - 2009')
redundantExample = get_strings_by_list_indices(allZoteroAttachments, indices)
print("Example for redundant PDF attachments in Zotero:")
for i, s in zip(indices, redundantExample):
    print(f"List Index {i}: {s}")        

"""---------------------------------------------------------------------------------------------------------------------------------------"""