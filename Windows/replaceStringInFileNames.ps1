# Replace string in file names in all subdirectories

      cd C:\Users\alexabus\OneDrive_NTNU\SWwd\FLUENT\AdWell\Turbulence\archive
      Get-ChildItem -Filter "*string1*" -Recurse | Rename-Item -NewName { $_.name -replace 'string1','string2' }

      Get-ChildItem -Filter "*newt-scaled_mdot=*" -Recurse | Rename-Item -NewName { $_.name -replace 'newt-scaled_mdot=’,'newtonian-scaled_mdot=' }

      Get-ChildItem -Filter "*newt-scaled*" -Recurse | Rename-Item -NewName { $_.name -replace 'newt-scaled’,'newtonian-scaled' }

      Get-ChildItem -Filter "*_dpdl*" -Recurse | Rename-Item -NewName { $_.name -replace '_dpdl’,'_dpdx' }

      Get-ChildItem -Filter "*scaled_m-dot=*" -Recurse | Rename-Item -NewName { $_.name -replace 'scaled_m-dot=’,'scaled_mdot=' }