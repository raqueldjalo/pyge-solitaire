#define Version '1.1'
[Files]
Source: *; DestDir: {app}
Source: Resources\fonts\*; DestDir: {app}\Resources\fonts
;Source: Resources\images\*; DestDir: {app}\Resources\images
Source: Resources\text\*; DestDir: {app}\Resources\text
[Setup]
AppCopyright=Annan Yearian
AppName=Pyge
AppVerName=Pyge {#Version}
LicenseFile=COPYING.txt
PrivilegesRequired=none
DefaultDirName={pf}\Pyge\
DefaultGroupName=Pyge
SetupIconFile=icon.ico
UsePreviousGroup=false
AlwaysShowGroupOnReadyPage=true
OutputDir=\H\Planning and Peg\source\binaries\iss
OutputBaseFilename=pyge_installer_{#Version}
SourceDir=\H\Planning and Peg\source\binaries\py2exe
[Icons]
Name: {group}\{cm:UninstallProgram, Pyge}; Filename: {uninstallexe}
Name: {group}\Pyge; Filename: {app}\Pyge.exe








