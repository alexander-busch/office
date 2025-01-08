# Create a SharePoint library template
# https://sharepoint.handsontek.net/2024/02/12/create-custom-document-library-template-sharepoint/
# Requires sharePoint admin privileges

$listURL = "https://xxx.sharepoint.com/sites/yyy"

Write-Host "Type URL to the document library to be used as a template:"
$listURL = Read-Host 

$tenenatName = $listURL.Split(".")[0].Split("//")[2]

Write-Host "Type a title for the template:"
$templateName = Read-Host 

Write-Host "Type a description for the template:"
$templateDescription = Read-Host 

Write-Host "Type the url to the the thumbnail to be used by the template"
$templateThumbnail = Read-Host 

Connect-SPOService -url ("https://{0}-admin.sharepoint.com" -f $tenenatName)

$listTemplate = Get-SPOSiteScriptFromList -ListUrl $listURL

$siteScript = Add-SPOSiteScript -Title $templateName -Description $templateDescription -Content $listTemplate 

Add-SPOListDesign -Title $templateName -Description $templateDescription -SiteScripts $siteScript.Id -Thumbnail $templateThumbnail