# Gerar nome aleatório para a máquina
$chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
$prefix = "SERVER-"
$random = -join ((1..7) | ForEach-Object { $chars | Get-Random })
$machineName = "$prefix$random"

Write-Host "[+] Renomeando máquina para $machineName"
Rename-Computer -NewName $machineName -Force

# Desativar Windows Defender completamente
Write-Host "[+] Desativando Windows Defender..."
Set-MpPreference -DisableRealtimeMonitoring $true
Set-MpPreference -DisableBehaviorMonitoring $true
Set-MpPreference -DisableIOAVProtection $true
Set-MpPreference -DisableScriptScanning $true
Set-MpPreference -SubmitSamplesConsent 2
Set-MpPreference -MAPSReporting 0
Set-MpPreference -PUAProtection 1

# Desabilitar serviços de telemetria
Write-Host "[+] Bloqueando telemetria da Microsoft..."
Stop-Service DiagTrack -Force -ErrorAction SilentlyContinue
Stop-Service dmwappushservice -Force -ErrorAction SilentlyContinue
Set-Service DiagTrack -StartupType Disabled
Set-Service dmwappushservice -StartupType Disabled
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\DataCollection" /v AllowTelemetry /t REG_DWORD /d 0 /f

# Tentar remover Sysmon, se instalado
Write-Host "[+] Verificando e desinstalando Sysmon..."
$sysmonPath = "$env:SystemRoot\Sysmon64.exe"
if (Test-Path $sysmonPath) {
    & "$sysmonPath" -u
    Remove-Item $sysmonPath -Force -ErrorAction SilentlyContinue
}

# Limpando logs do sistema
Write-Host "[+] Limpando logs do sistema..."
wevtutil el | ForEach-Object { wevtutil cl "$_" }

# Desabilitar logging de PowerShell
Write-Host "[+] Desativando logs do PowerShell..."
New-Item -Path "HKLM:\Software\Policies\Microsoft\Windows\PowerShell" -Force | Out-Null
New-ItemProperty -Path "HKLM:\Software\Policies\Microsoft\Windows\PowerShell" -Name EnableTranscripting -Value 0 -PropertyType DWORD -Force | Out-Null
New-ItemProperty -Path "HKLM:\Software\Policies\Microsoft\Windows\PowerShell" -Name EnableModuleLogging -Value 0 -PropertyType DWORD -Force | Out-Null
New-ItemProperty -Path "HKLM:\Software\Policies\Microsoft\Windows\PowerShell" -Name EnableScriptBlockLogging -Value 0 -PropertyType DWORD -Force | Out-Null

# Download de ferramentas essenciais
$tools = @{
    "PE-bear" = "https://github.com/hasherezade/pe-bear/releases/latest/download/pe-bear.zip"
    "x64dbg" = "https://github.com/x64dbg/x64dbg/releases/latest/download/snapshot_64.zip"
    "Detect-It-Easy" = "https://github.com/horsicq/Detect-It-Easy/releases/latest/download/die_win64_portable.zip"
}
$downloadPath = "$env:USERPROFILE\Downloads\RE_Tools"
New-Item -ItemType Directory -Path $downloadPath -Force | Out-Null

Write-Host "[+] Baixando ferramentas para: $downloadPath"
foreach ($tool in $tools.Keys) {
    $url = $tools[$tool]
    $output = "$downloadPath\$tool.zip"
    Invoke-WebRequest -Uri $url -OutFile $output
}

Write-Host "[✔] Setup stealth completo! Reinicie a máquina para aplicar as mudanças."
