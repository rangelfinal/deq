[Setup]
AppName = CÚlulaDessalinizadora
AppVerName=1.0
DefaultDirName={pf}\PhysisJr
DefaultGroupName=PhysisJr
UninstallDisplayIcon={app}\Desinstalar.exe

[Files]
Source: "Corrente.txt"; DestDir: "{app}"
Source: "pH.txt"; DestDir: "{app}"
Source: "Condutividade.txt"; DestDir: "{app}"
Source: "Manual.docx"; DestDir: "{app}"
Source: "script.exe"; DestDir: "{app}"
Source: "script.ps1"; DestDir: "{app}"
Source: "Script.ahk"; DestDir: "{app}"
Source: "CÚlulaDessalinizadora.vi"; DestDir: "{app}"
Source: "CÚlulaDessalinizadora.ino"; DestDir: "{app}"