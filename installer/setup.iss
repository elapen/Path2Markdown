[Setup]
AppName=Path2Markdown
AppVersion=1.0
DefaultDirName={pf}\Path2Markdown
DefaultGroupName=Path2Markdown
OutputBaseFilename=Path2Markdown_Setup
SetupIconFile=..\resources\icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Tasks]
Name: "desktopicon"; Description: "Create desktop shortcut"; GroupDescription: "Additional icons"; Flags: unchecked
Name: "runapp"; Description: "Run the application after installation"; GroupDescription: "Additional tasks"; Flags: checkedonce

[Files]
Source: "..\\dist\\Path2Markdown.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\\resources\\icon.ico"; DestDir: "{app}\\resources"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\\Path2Markdown"; Filename: "{app}\\Path2Markdown.exe"; IconFilename: "{app}\\resources\\icon.ico"; Tasks: desktopicon
Name: "{commondesktop}\\Path2Markdown"; Filename: "{app}\\Path2Markdown.exe"; IconFilename: "{app}\\resources\\icon.ico"; Tasks: desktopicon

[Run]
Filename: "{app}\\Path2Markdown.exe"; Description: "Launch Path2Markdown"; Flags: nowait postinstall skipifsilent; Tasks: runapp
