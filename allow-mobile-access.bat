@echo off
:: Run this file ONCE as Administrator (right-click -> Run as administrator)
:: Opens ports 3000 (frontend) and 8000 (backend) so your phone can reach this PC on Wi-Fi.
net session >nul 2>&1
if %errorlevel% neq 0 (
  echo Please right-click this file and choose "Run as administrator".
  pause
  exit /b 1
)
netsh advfirewall firewall delete rule name="Search-Want Dev (3000,8000)" >nul 2>&1
netsh advfirewall firewall add rule name="Search-Want Dev (3000,8000)" dir=in action=allow protocol=TCP localport=3000,8000 profile=private,public
echo.
echo Done. On your phone (same Wi-Fi) open:
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do echo    http://%%a:3000
pause
