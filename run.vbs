Dim win_shell, main_path, current_dir, python3_path

current_dir= left(WScript.ScriptFullName,(Len(WScript.ScriptFullName))-(len(WScript.ScriptName)))

main_path = current_dir & "Main.py"
main_path = Replace(main_path, "\", "\\")

set win_shell = WScript.CreateObject("WScript.Shell")
return=win_shell.Run("cmd /c where python3 > output.txt", 0, true)

set objFSO  = CreateObject("Scripting.FileSystemObject")
set file = objFSO.OpenTextFile("output.txt", 1)
python3_path = file.ReadAll
file.Close

python3_path = Replace(python3_path,"\","\\")
python3_path = Replace(python3_path,vbCr,"")
python3_path = Replace(python3_path,vbLf,"")
python3_path = CStr(Trim(python3_path))


If  not objFSO.FileExists(main_path) Then
	WScript.Echo "Main.py file not found"
	WScript.Quit
End If
If  not objFSO.FileExists(python3_path) Then
	WScript.Echo "python3.exe not found"
		WScript.Quit
End If

command= python3_path &" "& main_path
win_shell.Run command,0

Set win_shell = Nothing
set main_path = Nothing
set current_dir = Nothing
set python3_path = Nothing