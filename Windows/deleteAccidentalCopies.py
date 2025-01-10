# -*- coding: utf-8 -*-
"""
Reccursively deletes accidental copies

@author: alexander.busch@alumni.ntnu.no

"""

import os
import shutil

directory = r'D:\aaa'
backup_directory = r'D:\bbb'

def delete_copy_files(directory, backup_directory):
    
    # create backup directory if it does not exist
    if not os.path.exists(backup_directory):
        os.makedirs(backup_directory)
    
    # Recursively foll all files/folders in the directory and subdirectory
    for filename in os.listdir(directory):
        
        filepath = os.path.join(directory, filename)
        
        # If filepath is another directory recursively call this function
        if os.path.isdir(filepath):
            delete_copy_files(filepath)
        
        # Alternatively, check for file ending and delete in case this file is a copy
        elif filename.endswith('- copy'):
            backup_filepath = os.path.join(backup_directory, filename)
            shutil.copy2(filepath, backup_filepath)
            os.remove(filepath)

# Usage:
delete_copy_files(directory)