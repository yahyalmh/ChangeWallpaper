Dim win_shell, image_address, args

Set args =WScript.Arguments
bat_address = args(0)
image_address = args(1)

Set objFSO = WScript.CreateObject("Scripting.FileSystemObject")
If not objFSO.FileExists(bat_address) or  not objFSO.FileExists(image_address) Then
	WScript.Quit
End If

Set win_shell = WScript.CreateObject("WScript.Shell")
command = bat_address &" "& image_address
win_shell.Run command,0

Set win_shell = Nothing
Set image_address = Nothing
Set args= Nothing
