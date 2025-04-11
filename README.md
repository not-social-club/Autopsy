![License](https://img.shields.io/badge/license-NSC%20Confidential-red)

# Not Social Club Autopsy

Ferramenta stealth de engenharia reversa para análise de loaders e DLLs.  
Realiza análise estática, detecção de linguagem, fingerprint de verificações e prepara terreno para análise dinâmica com x64dbg.

---

## Pré-requisitos

Certifique-se de ter o Python instalado.

- Python 3.8 ou superior
- pip (gerenciador de pacotes)

Execute no CMD para verificar:

python --version
pip --version

## Instalação
1. Clone o projeto ou baixe os arquivos:

- git clone https://github.com/not-social-club/Autopsy.git
- cd autopsy
- pip install -r requirements.txt

2. Crie um ambiente virtual (opcional mas recomendado):

- python -m venv venv
- venv\Scripts\activate

1. Configuração do Sistema
Renomear a máquina com um nome aleatório (estilo DESKTOP-XXXXXXX)

Desativar atualizações automáticas

Desativar o Windows Defender (AntiSpyware e AntiVirus)

Desativar Telemetria da Microsoft (via serviços, agendamentos, policies)

Desabilitar Sysmon, PowerShell Logging, Event Tracing

Modo de energia: performance máxima

Remover serviços que geram logs ou fazem upload de dados

🧰 2. Instalar Ferramentas
Baixar e instalar:

x64dbg (com stealth plugin)

PE-bear

CFF Explorer

Ghidra (opcional)

Python 3.12 + pip

Git

Visual Studio Code

Ferramentas auxiliares: sigcheck, procexp, procdump, etc

Criar aliases úteis no PowerShell

3. Evasão
Alterar UID de rede (MAC spoofing)

Alterar hostname

Spoofar manufacturer (WMI)

Inserir chaves fake no registro (como se fosse uma instalação OEM normal)

Set-ExecutionPolicy Bypass -Scope Process -Force
.\NSC_VM_StealthSetup.ps1


Criado por @fbreseghello
