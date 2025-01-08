# Update PowerShell https://www.pdq.com/blog/how-to-update-powershell/

$PSVersionTable

winget search Microsoft.PowerShell
winget install --id Microsoft.PowerShell --source winget

Get-Module -ListAvailable
Get-Module -ListAvailable *pnp*

Install-Module -Name Microsoft.Online.SharePoint.PowerShell
Install-Module PnP.PowerShell
Install-Module SharePointPnPPowerShellOnline