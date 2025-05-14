# Connect to SharePoint
Connect-PnPOnline -Url https://xxx.sharepoint.com/sites/xxx -UseWebLogin

# Get today's date
$today = Get-Date -Format "yyMMdd"

# Concanate path to .csv export 
$pathToFileExport = -join("xxx", $today, ".csv");

# queery all members and export as .csv
Get-PnPGroup | Get-PnPGroupMember | Export-Csv $pathToFileExport