@echo off
echo Starting web chat...

REM Navigate to the project directory using pushd
pushd \\hzdemfs01.fas.local\DEM\RedirFolders\k.kostyuk\Desktop\VSCode\LilKrizis\LilKrizisTZ

REM Build Docker images
docker-compose build --pull

REM Start Docker containers
docker-compose up -d

REM Wait for the containers to start
timeout /t 30 /nobreak >nul

REM Open the browser to the web chat
start http://localhost:8080

echo Web chat is running. Open your browser and navigate to http://localhost:8080