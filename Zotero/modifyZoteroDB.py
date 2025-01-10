# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 10:16:31 2024

@author: abusch
"""

import sys
sys.path.append('D:\OneDrive - ANSYS, Inc\Documents\IT\Zotero\databaseModifications')
import analyzeZoteroDB



def replace_fullPath_with_attachments(directory_Zotero, stringToBeReplaced, modifyFiles):
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

    # Define the replacement
    replacement = r"attachments:"

    # Log file for tracking changes
    log_file_path = os.path.join(directory_Zotero, "replace_fullPath_with_attachments_log.txt")
    print(f"Log file path: {log_file_path}")

    with open(log_file_path, 'w', encoding='utf-8') as log_file:
        # Query all entries in the itemAttachments table
        sqlFilter = stringToBeReplaced
        cursor.execute("""
            SELECT itemID, path FROM itemAttachments WHERE path LIKE ?
        """, (f"%{sqlFilter}%",))
        
        # Debug - Process a single entry
        #allRows = cursor.fetchall()
        #row = allRows[0]
        
        # Process each entry
        for itemID, old_path in cursor.fetchall():
            print(f"Processing itemID {itemID}: {old_path}")
            
            # Replace the target path with the replacement
            new_path = old_path.replace(stringToBeReplaced, replacement)
            log_file.write(f"Old Path: {old_path} -> New Path: {new_path}\n")
            print(f"Updated Path: {new_path}")

            if modifyFiles:
                # Update the database with the new path
                cursor.execute("""
                    UPDATE itemAttachments
                    SET path = ?
                    WHERE itemID = ? AND path = ?
                """, (new_path, itemID, old_path))
                print(f"Database updated for itemID {itemID}")
                
        # Commit changes if modifyFiles is True
        if modifyFiles:
            print("Committing changes to the database.")
            conn.commit()

    # Close the connection
    conn.close()
    print("Database connection closed.")


def replace_storage_with_attachments(directory_Zotero, modifyFiles):
    """
    Query the Zotero database to update paths in the itemAttachments table.

    Args:
        directory_Zotero (str): directory_Zotero containing the Zotero SQLite database.
        modifyFiles (bool): Whether to actually modify the database or just log the changes.
    """
    # Path to Zotero SQLite database
    db_path = os.path.join(directory_Zotero, "zotero.sqlite")
    print(f"Zotero DB path: {db_path}")
    
    # Create a backup copy of the database
    import inspect
    current_function_name = inspect.currentframe().f_code.co_name
    
    # Define the target file name and path
    new_file_name = f"zotero_{current_function_name}.sqlite"
    new_file_path = os.path.join(directory_Zotero, new_file_name)
    
    # Copy the file
    import shutil
    shutil.copy(db_path, new_file_path) 

    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Define the target path and replacement
    stringToBeReplaced = "storage:"
    replacement = r"attachments:"

    # Log file for tracking changes
    log_file_path = os.path.join(directory_Zotero, "replace_storage_with_attachments_log.txt")
    print(f"Log file path: {log_file_path}")

    with open(log_file_path, 'w', encoding='utf-8') as log_file:
        # Query all entries in the itemAttachments table
        sqlFilter = stringToBeReplaced
        cursor.execute("""
            SELECT itemID, path FROM itemAttachments WHERE path LIKE ? AND path LIKE '%.pdf'
        """, (f"%{sqlFilter}%",))
        
        # Debug - Process a single entry
        #allRows = cursor.fetchall()
        #row = allRows[0]
        
        # Process each entry
        for itemID, old_path in cursor.fetchall():
            print(f"Processing itemID {itemID}: {old_path}")
            
            # Replace the target path with the replacement
            new_path = old_path.replace(stringToBeReplaced, replacement)
            log_file.write(f"Old Path: {old_path} -> New Path: {new_path}\n")
            print(f"Updated Path: {new_path}")

            if modifyFiles:
                # Update the database with the new path
                cursor.execute("""
                    UPDATE itemAttachments
                    SET path = ?
                    WHERE itemID = ? AND path = ?
                """, (new_path, itemID, old_path))
                print(f"Database updated for itemID {itemID}")
                
        # Commit changes if modifyFiles is True
        if modifyFiles:
            print("Committing changes to the database.")
            conn.commit()

    # Close the connection
    conn.close()
    print("Database connection closed.")



def replace_AuthorAnd_With_EtAl(directory_Zotero, modifyFiles):
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
    log_file_path = os.path.join(directory_Zotero, "replace_AuthorAnd_With_EtAl_log.txt")
    print(f"Log file path: {log_file_path}")
    
    with open(log_file_path, 'w', encoding='utf-8') as log_file:
        # Query all entries in the itemAttachments table
        sqlFilter = ".pdf"
        cursor.execute("""
            SELECT itemID, path FROM itemAttachments WHERE path LIKE ?
        """, (f"%{sqlFilter}%",))

        # Process each entry
        for itemID, filename in cursor.fetchall():
            # Check for "authorname1 and authorname2 - *" pattern
            match = re.match(r"^(?:attachments:)?([^\d\W_][\w\s\.-]+) and ([^\d\W_][\w\s\.-]+) - (.*)\.pdf$", filename)
            if match:
                # Extract author names and rest of the filename
                authorname1 = match.group(1).strip()
                authorname2 = match.group(2).strip()
                rest_of_filename = match.group(3).strip()
                
                # Only modify the author part, keep the rest intact
                # Replace "and" with "et al" in the author part
                new_filename = f"attachments:{authorname1} et al - {rest_of_filename}.pdf"
                
                # Log the change
                log_file.write(f"Old File Path: {filename} -> New File Path: {new_filename}\n")
                
                # Print for debugging
                print(f"Old File Path: {filename} -> New File Path: {new_filename}")
                
                # Update the file path in the database if modifyFiles is True
                if modifyFiles and filename != new_filename:
                    print(f"Attempting to update path for itemID {itemID}")
                    cursor.execute("""
                        UPDATE itemAttachments SET path = ? WHERE itemID = ? AND path = ?
                    """, (new_filename, itemID, filename))
                    print(f"Updated: {filename} -> {new_filename}")
                
        # Commit changes if modifyFiles is True
        if modifyFiles:
            print("Committing changes to the database.")
            conn.commit()

    # Close the connection
    conn.close()
    print("Database connection closed.")


def remove_dot_from_Author(directory_Zotero, modifyFiles):
    """
    Query the Zotero database to update paths in the itemAttachments table.

    Args:
        directory_Zotero (str): directory_Zotero containing the Zotero SQLite database.
        modifyFiles (bool): Whether to actually modify the database or just log the changes.
    """
    # Path to Zotero SQLite database
    db_path = os.path.join(directory_Zotero, "zotero.sqlite")
    print(f"Zotero DB path: {db_path}")       
        
    # Define the target path and replacement
    stringToBeReplaced = r"et al. - "
    replacement = r"et al - "


    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Log file for tracking changes
    log_file_path = os.path.join(directory_Zotero, "remove_dot_from_Author_log.txt")
    print(f"Log file path: {log_file_path}")
    
    with open(log_file_path, 'w', encoding='utf-8') as log_file:
        # Query all entries in the itemAttachments table
        sqlFilter = stringToBeReplaced
        cursor.execute("""
            SELECT itemID, path FROM itemAttachments WHERE path LIKE ? AND path LIKE '%.pdf'
        """, (f"%{sqlFilter}%",))
        
        
        # Debug - Process a single entry
        # allRows = cursor.fetchall()
        # row = allRows[0]
        # filename = row[1]
        # filtered_list = [item for item in allRows if "Jardiolin" in item[2]]
        
        # Process each entry
        for itemID, filename in cursor.fetchall():
            # print(f"Processing itemID {itemID}: {filename}")
            
            # Check for "authorname et al. - *" pattern
            match = re.match(r"^(?:attachments:)?([^\d\W_][\w\s\.-]+) et al\.\s*-\s*(.*)\.pdf$", filename)
            if match:
                authorname = match.group(1).strip()
                rest_of_filename = match.group(2).strip()
                new_filename = f"attachments:{authorname} et al - {rest_of_filename}.pdf"
                                
                # Log the update in the text file
                log_file.write(f"Old File Path: {filename} -> New File Path: {new_filename}\n")
                
                if modifyFiles and filename != new_filename:
                    print(f"Attempting to update path for itemID {itemID}")
                    # Update the file path in the database
                    cursor.execute("""
                        UPDATE itemAttachments SET path = ? WHERE itemID = ? AND path = ?
                    """, (new_filename, itemID, filename))
                    print(f"Updated: {filename} -> {new_filename}")
                
        # Commit changes if modifyFiles is True
        if modifyFiles:
            print("Committing changes to the database.")
            conn.commit()

    # Close the connection
    conn.close()
    print("Database connection closed.")


def update_linkMode(directory_Zotero, modifyFiles):
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
    log_file_path = os.path.join(directory_Zotero, "update_linkMode_log.txt")
    print(f"Log file path: {log_file_path}")

    with open(log_file_path, 'w', encoding='utf-8') as log_file:
        # Query all entries in the itemAttachments table
        cursor.execute("""
            SELECT itemID, linkMode, path 
            FROM itemAttachments 
            WHERE path LIKE '%.pdf'
        """)

        
        # Debug - Process a single entry
        # allZoteroAttachments = cursor.fetchall()
        # indices = find_indices_of_string_in_tuples_list(allZoteroAttachments, 'Abchiche et al. - 2015')
        # row = allZoteroAttachments[indices[0]]
   
        
        # 'Aase et al - 2013' linkMode = 1
        # 'Abchiche et al. - 2015'
        # 'ABDELRAHIM et al - 1994' linkMode = 0
        
        # Process each entry
        for itemID, linkMode, path in cursor.fetchall():
            print(f"Processing itemID {itemID} - linkMode {linkMode} - {path}")
            
            if linkMode != 2:
                linkMode = 2
                log_file.write(f"Old linkMode: 1 -> New linkMode: {linkMode}\n")
                print(f"New linkMode: {linkMode}")

            if modifyFiles:
                # Update the database with the new path
                cursor.execute("""
                    UPDATE itemAttachments
                    SET linkMode = ?
                    WHERE itemID = ?
                """, (linkMode, itemID))
                print(f"Database updated for itemID {itemID}")
                
        # Commit changes if modifyFiles is True
        if modifyFiles:
            print("Committing changes to the database.")
            conn.commit()

    # Close the connection
    conn.close()
    print("Database connection closed.")











# Example usage

modifyFiles = True
modifyFiles = False


replace_fullPath_with_attachments(directory_Zotero, "D:\\turboserver\\library\\Zotero\\pdf\\", modifyFiles)
replace_storage_with_attachments(directory_Zotero, modifyFiles)


replace_AuthorAnd_With_EtAl(directory_Zotero, modifyFiles)
remove_dot_from_Author(directory_Zotero, modifyFiles)
#update_linkMode(directory_Zotero, modifyFiles)





