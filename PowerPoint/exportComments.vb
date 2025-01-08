' Export all comments from a .pptx file
' https://answers.microsoft.com/en-us/msoffice/forum/all/in-powerpoint-is-there-a-way-to-export-all-review/3e38dd7d-c2b8-4a75-81ce-b22c68a236d8

Sub ExportComments()

   Dim oSl As Slide
   Dim oSlides As Slides
   Dim sText As String
   Dim sFilename As String
   Dim R As Long
   Dim C As Long

   Set oSlides = ActivePresentation.Slides
   For Each oSl In oSlides
      sText = sText & "Slide: " & oSl.SlideIndex & vbCrLf
      sText = sText & "======================================" & vbCrLf
      For C = 1 To oSl.Comments.Count
         sText = sText & "On " & oSl.Comments(C).DateTime & " "
         sText = sText & oSl.Comments(C).Author & " said " & Chr(34)
         sText = sText & oSl.Comments(C).Text & Chr(34) & vbCrLf
         If oSl.Comments(C).Replies.Count > 0 Then

            For R = 1 To oSl.Comments(C).Replies.Count
               sText = sText & vbTab & oSl.Comments(C).Replies(R).Author & " replied" _
                       & " on " & oSl.Comments(C).Replies(R).DateTime & " " & Chr(34)
               sText = sText & oSl.Comments(C).Replies(R).Text & Chr(34) & vbCrLf
            Next R

         End If
         sText = sText & "--------------" & vbCrLf

      Next C
   Next oSl

   sFilename = InputBox("Full path to output file:", "Output file")
   If Len(sFilename) > 0 Then
      WriteStringToFile sFilename, sText
      SendFileToNotePad sFilename
   End If

End Sub

Sub WriteStringToFile(pFileName As String, pString As String)
' this writes the text out to a file

    Dim intFileNum As Integer

    intFileNum = FreeFile
    Open pFileName For Output As intFileNum
    Print #intFileNum, pString
    Close intFileNum

End Sub

Sub SendFileToNotePad(pFileName As String)
' This opens the file in notepad

    Dim lngReturn As Long
    lngReturn = Shell("NOTEPAD.EXE " & pFileName, vbNormalFocus)

End Sub