Sub RemoveAllFavorites()

    Dim favGroup As NavigationGroup
    Dim favFldrs As NavigationFolders

    Set favGroup = Application.ActiveExplorer.NavigationPane.Modules.GetNavigationModule(olModuleMail).NavigationGroups.GetDefaultNavigationGroup(olFavoriteFoldersGroup)
    Set favFldrs = favGroup.NavigationFolders

    Do While favFldrs.Count > 0
        favFldrs.Remove favFldrs.item(1)
    Loop

End Sub