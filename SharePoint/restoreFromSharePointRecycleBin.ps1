# Restore item from SharePoint via PS
# See
# https://lazyadmin.nl/powershell/restore-recycle-bin-sharepoint-online-with-powershell/
# https://github.com/joseinazusa/powershell-recursive-folder-restore/blob/master/recursive-recyclebin-restore.ps1
# https://github.com/TheGeorgeDougherty/O365-PS-Scripts/blob/master/SPOnline-Restore-RecycleBin


#Install PnP PowerShell Module
Uninstall-Module PnP.PowerShell -AllVersions -Confirm:$False
Uninstall-Module SharePointPnPPowerShellOnline -AllVersions -Confirm:$False
Get-module -ListAvailable *pnp*
Install-Module PnP.PowerShell



# Connect to SharePoint
Import-Module PnP.PowerShell
Connect-PnPOnline -Url https://xxx/:w:/r/sites/yyy -UseWebLogin
# Connect-PnPOnline -Url https://xxx/:w:/r/sites/yyy -Interactive  

# User that deleted the item(s)
$email = 'alexander.busch@danfoss.com'
Get-PnPRecycleBinItem -FirstStage | ? DeletedByEmail -eq $email | select -last 10 | fl *

# Get numbers of deleted items in Recycle Bins
(Get-PnPRecycleBinItem -firststage).count
(Get-PnPRecycleBinItem -secondstage).count

# Items deleted yesterday or today
$today = (Get-Date)
$restoreDate = $today.date.AddDays(-1)
Get-PnPRecycleBinItem -firststage | ? {($_.DeletedDate -gt $restoreDate) -and ($_.DeletedByEmail -eq $email)} | select -last 10 | fl *
Get-PnPRecycleBinItem -firststage | ? {($_.DeletedDate -gt $restoreDate) -and ($_.DeletedByEmail -eq $email)} | Export-Csv c:\temp\Sharepoint_files_to_restore.csv
Get-PnPRecycleBinItem -firststage | ? {($_.DeletedDate -gt $restoreDate) -and ($_.DeletedByEmail -eq $email)} | Restore-PnpRecycleBinItem -Force

# Items deleted in a specific timeframe
$date1=get-date("16.11.2021 07:00:00")
$date2=get-date("18.11.2021 23:55:00")
Get-PnPRecycleBinItem -firststage | ? {($_.DeletedDate -gt $date2 -and $_.DeletedDate -lt $date1) -and ($_.DeletedByEmail -eq $email)} | select -last 10 | fl *
Get-PnPRecycleBinItem -firststage | ? {($_.DeletedDate -gt $date2 -and $_.DeletedDate -lt $date1) -and ($_.DeletedByEmail -eq $email)} | Export-Csv c:\temp\Sharepoint_files_to_restore.csv
Get-PnPRecycleBinItem -firststage | ? {($_.DeletedDate -gt $date2 -and $_.DeletedDate -lt $date1) -and ($_.DeletedByEmail -eq $email)} | Restore-PnpRecycleBinItem -Force

# File types, e.g., *.docx *.scdoc *.stp
Get-PnPRecycleBinItem -FirstStage | ? LeafName -like '*.scdoc' | select -last 10 | fl *
Get-PnPRecycleBinItem -FirstStage | ? LeafName -like '*.stp' | Export-Csv c:\temp\Sharepoint_files_to_restore.csv
Get-PnPRecycleBinItem -FirstStage | ? LeafName -like '*.stp' | Restore-PnpRecycleBinItem -Force

# Specific file based on filename, an exact file can be found by using the -eq operator, will include folders
Get-PnPRecycleBinItem | ? Title -Like '*someString*' | ft
Get-PnPRecycleBinItem | ? DirName -Like '*someString*' | ft

Get-PnPRecycleBinItem -secondstage | ? Title -Like 'example.docx' | Restore-PnpRecycleBinItem -Force

# As previous, but files only
Get-PnPRecycleBinItem -secondstage | ? {($_.Title -like '*test*') -and ($_.ItemType -eq 'File')} | ft

# In case of two many items to restore: Loop items to restore and restore individually
$restoreItems = import-csv -path "c:\temp\Sharepoint_files_to_restore.csv"
$restoreItemsCount = $restoreItems.Count
foreach( $restoreItem in $restoreItems ){
	Restore-PnpRecycleBinItem -Identity $restoreItem.Id -Force
}



#Get All Items deleted from a specific path or library - sort by most recently deleted
$DeletedItems = Get-PnPRecycleBinItem | Where { $_.DirName -like '*someString*'} | Sort-Object -Property DeletedDate -Descending
 
ForEach($Item in $DeletedItems)
{
    Restore-PnpRecycleBinItem -Identity $Item.Id -Force
}

#Restore all deleted items from the given path to its original location
ForEach($Item in $DeletedItems)
{
    #Get the Original location of the deleted file
    $OriginalLocation = "/"+$Item.DirName+"/"+$Item.LeafName
    If($Item.ItemType -eq "File")
    {
        $OriginalItem = Get-PnPFile -Url $OriginalLocation -AsListItem -ErrorAction SilentlyContinue
    }
    Else #Folder
    {
        $OriginalItem = Get-PnPFolder -Url $OriginalLocation -ErrorAction SilentlyContinue
    }
    #Check if the item exists in the original location
    If($OriginalItem -eq $null)
    {
        #Restore the item
        $Item | Restore-PnpRecycleBinItem -Force
        Write-Host "Item '$($Item.LeafName)' restored Successfully!" -f Green
    }
    Else
    {
        Write-Host "There is another file with the same name.. Skipping $($Item.LeafName)" -f Yellow
    }
}


#Read more: https://www.sharepointdiary.com/2019/02/sharepoint-online-powershell-to-restore-deleted-items-from-recycle-bin.html#ixzz7DJ2ZvDjt

