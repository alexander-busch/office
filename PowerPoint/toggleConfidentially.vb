Sub ToggleConfidentiality()
    Dim slideMaster As Master
    Dim layout As CustomLayout
    Dim shape As shape
    Dim currentText As String
    Dim updatedText As String
    Dim changedToProprietary As Boolean
    Dim removedProprietary As Boolean

    ' Get the current year
    'Dim currentYear As String
    'currentYear = Year(Date)

    ' Define the two text states dynamically with the current year
    Dim textState1 As String
    Dim textState2 As String

    'textState1 = "©" & currentYear & " ANSYS, Inc."
    'textState2 = "©" & currentYear & " ANSYS, Inc. / Proprietary. Do Not Share."
    
    textState1 = "ANSYS, Inc."
    textState2 = "ANSYS, Inc. / Proprietary. Do Not Share."

    ' Initialize flags
    changedToProprietary = False
    removedProprietary = False

    ' Access the Slide Master
    Set slideMaster = ActivePresentation.Designs(1).slideMaster

    ' Check and update text on the Slide Master
    For Each shape In slideMaster.Shapes
        If shape.HasTextFrame Then
            If shape.TextFrame.HasText Then
                currentText = shape.TextFrame.TextRange.Text
                If InStr(currentText, textState2) > 0 Then
                    updatedText = Replace(currentText, textState2, textState1)
                    shape.TextFrame.TextRange.Text = updatedText
                    removedProprietary = True
                ElseIf InStr(currentText, textState1) > 0 Then
                    updatedText = Replace(currentText, textState1, textState2)
                    shape.TextFrame.TextRange.Text = updatedText
                    changedToProprietary = True
                End If
            End If
        End If
    Next shape

    ' Check and update text on each layout of the Slide Master
    For Each layout In slideMaster.CustomLayouts
        For Each shape In layout.Shapes
            If shape.HasTextFrame Then
                If shape.TextFrame.HasText Then
                    currentText = shape.TextFrame.TextRange.Text
                    If InStr(currentText, textState2) > 0 Then
                        updatedText = Replace(currentText, textState2, textState1)
                        shape.TextFrame.TextRange.Text = updatedText
                        removedProprietary = True
                    ElseIf InStr(currentText, textState1) > 0 Then
                        updatedText = Replace(currentText, textState1, textState2)
                        shape.TextFrame.TextRange.Text = updatedText
                        changedToProprietary = True
                    End If
                End If
            End If
        Next shape
    Next layout

    ' Display the appropriate message
    If changedToProprietary And Not removedProprietary Then
        MsgBox "Changed to Proprietary. Do Not Share!"
    ElseIf removedProprietary And Not changedToProprietary Then
        MsgBox "Removed label Proprietary. Do Not Share!"
    ElseIf changedToProprietary And removedProprietary Then
        MsgBox "Both changes were applied on different elements."
    Else
        MsgBox "No changes were made."
    End If
End Sub

