Write-Host "Initializing CyberGuardian REAL SYSTEM MODE..." -ForegroundColor Red
Start-Sleep -Seconds 1

# 1. Install Dependencies
Write-Host "Installing Python requirements..." -ForegroundColor Yellow
pip install -r requirements.txt

# 2. Start Backend Server
Write-Host "Starting Backend Server (server.py)..." -ForegroundColor Green
Start-Process -FilePath "python" -ArgumentList "server.py" -WindowStyle Minimized

# 3. Launch UI
$gamePath = "$PSScriptRoot\CyberSecGame\index.html"
if (Test-Path $gamePath) {
    Write-Host "Launching Interface..." -ForegroundColor Cyan
    Start-Process $gamePath
}

Write-Host "`n[SYSTEM ONLINE]" -ForegroundColor Green
Write-Host "WARNING: The terminal in the web app now executes REAL COMMANDS on your PC." -ForegroundColor Red
Write-Host "Do not expose port 5000 to the internet." -ForegroundColor Red

Read-Host "Press Enter to exit launcher (Server will keep running)..."
