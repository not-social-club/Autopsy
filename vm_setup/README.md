# Autopsy - VM Stealth Setup

Prepara uma VM pra engenharia reversa e análise ofensiva sem deixar rastros.

## Arquivos

- `stealth_vm_setup.ps1`: script PowerShell principal. Faz o trabalho.
- `stealth_bootstrap.bat`: executa o `.ps1` automaticamente com ofuscação. Zero rastros.

---

## O que esse setup faz

- Desliga Defender, telemetria, Sysmon, logs.
- Camufla sinais de máquina virtual.
- Instala ferramentas de análise stealth.
- Renomeia a máquina com nome aleatório.
- Prepara o ambiente pra rodar loader/dll sem ser detectado(anti-anti-dgb).

---

## Como usar

### Opção 1 - Rápido

1. Copie o `stealth_bootstrap.bat` pra VM.
2. Execute como Admin.
3. Ele baixa e roda o `.ps1`. Fim.

### Opção 2 - Manual

1. Copie o `stealth_vm_setup.ps1` pra VM.
2. Rode no PowerShell com Admin:

```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force
.\stealth_vm_setup.ps1
```

Uso é por sua conta.


Not Social Club.
