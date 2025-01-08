# Activate SharePoint Library export/import
# Requires sharePoint admin privileges

$SiteURL = "https://xxx.sharepoint.com/sites/yyy"

# https://learn.microsoft.com/en-us/sharepoint/troubleshoot/administration/connect-sposervice-error
$creds = Get-Credential
Connect-SPOService -Credential $creds -Url https://tenant-admin.sharepoint.com -ModernAuth $true -AuthenticationUrl https://login.microsoftonline.com/organizations

Set-SPOSite $SiteURL -DenyAddAndCustomizePages $False
