# Search all folders/files in folder and delete them

$source="D:\aaa"
$source="D:\bbb"

# $source=pwd

# Define the file types to be removed
# $strings_in_sim=@( "*.ar","*.bak", "*.bat", "*.cc", "*.ccdyn", "*.ccnodes", "*.csv", "*.err", "*.for", "*.inp*", "*.loadt", "*.k*", "*.log", "*.out", "*.pacj", "*.pp", "*.rck", "*.sav", "*.savPCS", "*.savx", "*.sym", "*.txt")
# $strings_in_post=@("*.avi", "*.csv", "*.ezp*", "*.mp4", "*.png", "*.xls*")
# $strings_in = $strings_in_sim + $strings_in_post
$strings_in=@("local.lnk", "oneDrive.lnk")

# Define specific files to be excluded
$strings_ex=@("")

# Change to directory
cd ($source)

# Remove all the files defined, keep the ones to be excluded
get-childitem -Include ($strings_in) -Exclude ($strings_ex) -Recurse -force | Remove-Item -Force -Recurse

# Function declaration: recursively delete empty folders starting from the lowest level in the folder hierarchy
function Remove-EmptyFolders {
    param (
        [string]$path
    )

    # Get a list of all subdirectories in the current directory
    $subdirectories = Get-ChildItem -Path $path -Directory

    # Loop through each subdirectory
    foreach ($subdirectory in $subdirectories) {
        # Recursively call the function on the subdirectory
        Remove-EmptyFolders -path $subdirectory.FullName

        # Check if the current subdirectory is empty
        if ((Get-ChildItem -Path $subdirectory.FullName).Count -eq 0) {
            # If it's empty, remove it
            Remove-Item -Path $subdirectory.FullName -Force
        }
    }
	
	# Check if the current directory is named "FluidPropertyWorkDir"
    if ($path -like "*FluidPropertyWorkDir*") {
        Remove-Item -Path $path -Force -Recurse
    }
}

# Call the function to remove empty folders
Remove-EmptyFolders -path $source

# Pause to keep the PowerShell window open until a key is pressed
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')