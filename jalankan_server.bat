@echo off
cd /d "%~dp0"
title SERVER UPLOAD BABI - MODE ADMIN
color 0A

:: === CEK APAKAH SCRIPT INI DIJALANKAN SEBAGAI ADMIN ===
>nul 2>&1 net session
if %errorLevel% NEQ 0 (
    echo [PERINGATAN] Script ini butuh akses ADMIN, goblok!
    echo [ACTION] Nyalain ulang sebagai ADMIN...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

echo ====================================================
echo [INFO] Akses admin terdeteksi. Mulai pengaturan firewall dan server.
echo ====================================================
echo.

:: === CARI PATH PYTHON.EXE YANG DIPAKAI ===
where python > temp_path.txt
set /p PYEXE=<temp_path.txt
del temp_path.txt

echo [PYTHON] Ketemu: %PYEXE%

:: === CEK RULE FIREWALL ADA GAK ===
netsh advfirewall firewall show rule name="Flask Upload Python" | findstr /i "Rule Name" >nul
if %errorlevel% NEQ 0 (
    echo [FIREWALL] Python belum dapet izin. Nambahin rule sekarang...
    netsh advfirewall firewall add rule name="Flask Upload Python" ^
    dir=in action=allow program="%PYEXE%" enable=yes profile=any protocol=TCP localport=5000
) else (
    echo [FIREWALL] Rule untuk Python udah ada, mantap.
)

:: === DETEKSI WARP/VPN ===
echo.
echo [CHECK] Lagi cek apakah WARP / VPN aktif...
for /f "tokens=2 delims=:" %%a in ('netsh interface show interface ^| findstr /i "cloudflare warp"') do (
    echo [ERROR] KETEMU WARP, ANJING! Matikan dulu itu VPN goblok.
    echo [FIX] Buka Settings > Network & Internet > VPN atau matiin Cloudflare WARP
    pause
    exit /b
)

:: === CEK MODUL PYTHON ===
echo.
echo [INFO] Cek modul Flask, QRCode, Pillow...
python -c "import flask" 2>NUL || (
    echo [INSTALL] Flask kagak ada, installing dulu...
    pip install flask
)
python -c "import qrcode" 2>NUL || (
    echo [INSTALL] QRCode ilang, installing dulu...
    pip install qrcode
)
python -c "from PIL import Image" 2>NUL || (
    echo [INSTALL] Pillow ngilang, installing dulu...
    pip install pillow
)

:: === MULAI SERVER ===
echo.
echo ====================================================
echo [GAS] Semua siap tempur. Server mulai sekarang!
echo ====================================================
python app.py
pause
