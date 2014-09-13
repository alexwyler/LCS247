; IMPORTANT INFO ABOUT GETTING STARTED: Lines that start with a
; semicolon, such as this one, are comments.  They are not executed.

; This script has a special filename and path because it is automatically
; launched when you run the program directly.  Also, any text file whose
; name ends in .ahk is associated with the program, which means that it
; can be launched simply by double-clicking it.  You can have as many .ahk
; files as you want, located in any folder.  You can also run more than
; one ahk file simultaneously and each will get its own tray icon.

; SAMPLE HOTKEYS: Below are two sample hotkeys.  The first is Win+Z and it
; launches a web site in the default browser.  The second is Control+Alt+N
; and it launches a new Notepad window (or activates an existing one).  To
; try out these hotkeys, run AutoHotkey again, which will load this file.#

;#IfWinExist, League of Legends (TM) Client

#Persistent
#SingleInstance force

	msgbox start %1% - %2%
	
	while !isLeagueOpen()
	{
		Sleep 1000
	}
	
	;msgbox league is open
	
	;5 second wait
	Sleep 2000
	
	while isInLoadingScreen()
	{
		Sleep 1000
	}
	
	;msgbox out of spectating
	
	;small wait
	Sleep 1000

	index = %2%
	if 1 contains true
	{
		Send {F1 down}{F1 up}
		selectTwice( index + 1 )
	} else {
		Send {F2 down}{F2 up}
		if index = 0 
		{
			Loop, 10 
			{
				Send {q down}{q up}
				Sleep 50
				Send {q down}{q up}
			}
		}
		else if index = 1
		{
			Loop, 10 
			{
				Send {w down}{w up}
				Sleep 50
				Send {w down}{w up}
			}
		}
		else if index = 2
		{
			Loop, 10 
			{
				Send {e down}{e up}
				Sleep 50
				Send {e down}{e up}
			}
		}
		else if index = 3
		{
			Loop, 10 
			{
				Send {r down}{r up}
				Sleep 50
				Send {r down}{r up}
			}
		}
		else if index = 4
		{
			Loop, 10 
			{
				Send {t down}{t up}
				Sleep 50
				Send {t down}{t up}
			}
		}
	}
return

isLeagueOpen()
{
	if( WinExist("League of Legends (TM) Client") )
	{
		return true
	} else {
		return false
	}
}

isInLoadingScreen()
{
	PixelGetColor, color, 0, 0
	if color contains 0x000000
	{
		return true
	}
	else
	{
		return false
	}
}
return

selectTwice(key)
{
	Loop, 10 
	{
		Send {%key% down}{%key% up}
		Sleep 50
		Send {%key% down}{%key% up}
	}
}