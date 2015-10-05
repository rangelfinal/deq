ifWinExist ET-2077/2232 Interface Program Ver 3.03(x64)
{
	WinActivate
}
else
{
	Run C:\Program Files (x86)\DMM\ET-2077_2232\ET_2077_2232.exe
	WinWait ET-2077/2232 Interface Program Ver 3.03(x64)
	WinActivate
}
Click 275,280
WinWait, ahk_class #32770
ControlClick Edit1
Send C:\physis\data.txt
ControlClick ComboBox3
Send {Down 3}
Click 600,390
Loop 5
{	
	ifWinExist Confirmar Salvar como
	{
		Click 230,100
	}
	ifWinExist Information
	{
		Click 330,130
		break
	}
	Click 600,390
}