#include <WinAPI.au3>

HotKeySet("^!s","AutoDoing") ; �ȼ�����ctrl+Alt+s
;HotKeySet("^x","_Exit")
While 1
    Sleep(1000)
Wend

Func AutoDoing()
	Send("^c")
    If WinExists("[CLASS:TSMMain]") Then
		;WinWait("[CLASS:TSMMain]", '', 10)
		;$winhd=_WinAPI_FindWindow("#32770","")
		;$hNote = WinGetHandle("[CLASS:TSMMain]")
		;Opt('WinTitleMatchMode', 1)
		;$hEdit = ControlGetHandle($hNote, '', 'TPanel')
		;MsgBox(0, "", "Window exists" & $hNote & $winhd)
    	ControlClick("[CLASS:TElWind]","","[CLASS:TPanel; INSTANCE:1]","left",1,22,15)
		;WinActivate($winhd)
		SplashTextOn("", "��ӵ�supermemo...", 200, 40, -1, -1, "", 24)
		Sleep(1000)
		SplashOff()
	Else
		Run(@ScriptDir & "\sm15.exe")
		SplashTextOn("", "����supermemo...", 200, 40, -1, -1, "", 24)
		Sleep(5000)
		SplashOff()
    	ControlClick("[CLASS:TElWind]","","[CLASS:TPanel; INSTANCE:1]","left",1,22,15)
		WinWaitActive("[CLASS:TElWind]","", 10);
		SplashTextOn("", "��ӵ�supermemo...", 200, 40, -1, -1, "", 24)
		Sleep(1000)
		SplashOff()
	EndIf
EndFunc

Func _Exit()
        Exit
EndFunc