Sub TotalVol()

For Each ws In Worksheets

'-------------------
'Easy Part
'-------------------

  'Set Variable for ticker
    Dim Ticker As String
    
    'Set variable for volume
    Dim Volume As LongLong
    Volume = 0
        
        
    ws.Range("I1").Value = "Ticker"
    ws.Range("J1").Value = "Total Volume"
    
    'Keep track of location of each ticker in the summary table
    Dim Summary_Table As Long
    Summary_Table = 2
    
    'Variable for last row
    Dim LastRow As Long
    LastRow = Range("A" & Rows.Count).End(xlUp).Row
    
    'Loop through ticker
    For i = 2 To LastRow
    
    'Check if we are still within same ticker, if not...
    If ws.Cells(i + 1, 1).Value <> ws.Cells(i, 1).Value Then
    
        'set ticker name
        Ticker = ws.Cells(i, 1).Value
    
        'add to volume total
        Volume = Volume + ws.Cells(i, 7).Value
    
        'print the ticker name in summary table
        ws.Range("I" & Summary_Table).Value = Ticker
    
        'print added volume in summary table
        ws.Range("J" & Summary_Table).Value = Volume
    
        'add one to summary table
        Summary_Table = Summary_Table + 1
    
        'reset ticker
        Volume = 0
    
        'if cells immediate following a row is the same ticker
        Else
    
        'add to the volume total
        Volume = Volume + ws.Cells(i, 7).Value
    
    End If
    
    Next i
    
'----------------------------
'Moderate Part
'----------------------------

    ws.Range("K1").Value = "Yearly Change"
    ws.Range("L1").Value = "Percent Change"
    
    For i = 2 To LastRow
    
    'Check if we are still within same ticker, if not...
    If ws.Cells(i + 1, 1).Value <> ws.Cells(i, 1).Value Then
    
    'Grab opening value of the year for the same ticker
    OpeningVal
    
    'Grab closing value of the year for the same ticker
    ClosingVal
    
    'add row to summary table
    Summary_Table = Summary_Table + 1
    
    'Calculate Yearly Change and print in summary table
    YearlyChange = ClosingVal - OpeningVal
    ws.Range("K" & Summary_Table).Value = YearlyChange
    
    
    
    
    
    
    
    
    

Next ws
    
End Sub
