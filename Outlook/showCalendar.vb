Sub ShowXXXcalendar()
    Dim objNamespace As Outlook.NameSpace
    Dim objCalendarModule As Outlook.CalendarModule
    Dim objNavPane As Outlook.NavigationPane
    Dim objNavGroup As Outlook.NavigationGroup
    Dim objNavFolder As Outlook.NavigationFolder
    Dim calendarFound As Boolean
    Dim calendarName As String
    Dim calendarFolder As Outlook.Folder

    calendarName = "xxx" ' Change this to your desired calendar name

    Set objNamespace = Application.GetNamespace("MAPI")
    Set objNavPane = Application.ActiveExplorer.NavigationPane
    Set objCalendarModule = objNavPane.Modules.GetNavigationModule(olModuleCalendar)

    calendarFound = False

    ' Search for the "All Group Calendars" group
    For Each objNavGroup In objCalendarModule.NavigationGroups
        If objNavGroup.Name = "All Group Calendars" Then
            ' Look for the calendar inside the group
            For Each objNavFolder In objNavGroup.NavigationFolders
                If objNavFolder.DisplayName = calendarName Then
                    Set calendarFolder = objNavFolder.Folder
                    
                    ' Display the calendar folder and overlay it
                    Application.ActiveExplorer.SelectFolder calendarFolder
                    Application.ActiveExplorer.CurrentFolder.Display
                    calendarFound = True
                    Exit For
                End If
            Next objNavFolder
            Exit For
        End If
    Next objNavGroup

End Sub