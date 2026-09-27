@echo off
setlocal
set "MVNW_ROOT=%~dp0"
set "MVNW_CACHE=%MVNW_ROOT%.mvn\wrapper\dists"
set "MVNW_MAVEN_HOME=%MVNW_CACHE%\apache-maven-3.9.16"
set "MVNW_ARCHIVE=%MVNW_CACHE%\apache-maven-3.9.16-bin.zip"
set "MVNW_URL=https://repo.maven.apache.org/maven2/org/apache/maven/apache-maven/3.9.16/apache-maven-3.9.16-bin.zip"
set "MVNW_SHA512=ed41650d42485cfc243fad22158caf9cbb5dc408ce7a09ddb94dd42a019de929ca43065bfa450612cf12bf78b5cafa3884b96c090de326ff590448c933454af3"

if defined JAVA_HOME if not exist "%JAVA_HOME%\bin\java.exe" set "JAVA_HOME="

if exist "%MVNW_MAVEN_HOME%\bin\mvn.cmd" goto run
if not exist "%MVNW_CACHE%" mkdir "%MVNW_CACHE%"

powershell.exe -NoProfile -ExecutionPolicy Bypass -Command ^
  "$ErrorActionPreference='Stop';" ^
  "if (-not (Test-Path -LiteralPath '%MVNW_ARCHIVE%')) { Invoke-WebRequest -UseBasicParsing -Uri '%MVNW_URL%' -OutFile '%MVNW_ARCHIVE%' };" ^
  "$actual=(Get-FileHash -Algorithm SHA512 -LiteralPath '%MVNW_ARCHIVE%').Hash.ToLowerInvariant();" ^
  "if ($actual -ne '%MVNW_SHA512%') { throw 'Checksum inválido para a distribuição Maven.' };" ^
  "Expand-Archive -LiteralPath '%MVNW_ARCHIVE%' -DestinationPath '%MVNW_CACHE%' -Force"
if errorlevel 1 exit /b 1

:run
call "%MVNW_MAVEN_HOME%\bin\mvn.cmd" %*
exit /b %errorlevel%
