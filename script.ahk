ifWinExist ET-2077/2232 Interface Program Ver 3.03(x64)
{
}
else
{
	Run C:\Program Files (x86)\DMM\ET-2077_2232\ET_2077_2232.exe
	WinWait ET-2077/2232 Interface Program Ver 3.03(x64)
}
ControlClick x275 y280, ET-2077/2232 Interface Program Ver 3.03(x64),,,, NA
WinWait, ahk_class #32770
ControlClick Edit1
Send C:\physis\data.txt
ControlClick ComboBox3
Send {Down 3}
ControlClick x600 y390, ET-2077/2232 Interface Program Ver 3.03(x64),,,, NA
Loop 5
{	
	ifWinExist Confirmar Salvar como
	{
		ControlClick x230 y100, ET-2077/2232 Interface Program Ver 3.03(x64),,,, NA
	}
	ifWinExist Information
	{
		ControlClick x330 y130, ET-2077/2232 Interface Program Ver 3.03(x64),,,, NA
		break
	}
	ControlClick x600 y390, ET-2077/2232 Interface Program Ver 3.03(x64),,,, NA
}