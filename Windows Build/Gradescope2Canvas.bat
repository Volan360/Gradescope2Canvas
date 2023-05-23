ECHO OFF
pushd %~dp0
start server.exe
pushd %~dp0\UI
start index.html