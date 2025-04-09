# modules/static_strings.py

import re
from rich.text import Text

# Lista de palavras suspeitas
SUSPECT_KEYWORDS = [
    # Networking
    "http", "https", "url", "tcp", "udp", "socket", "connect", "host", "port", "dns", "ip",
    # Cripto
    "key", "aes", "rsa", "xor", "encrypt", "decrypt", "hash", "md5", "sha", "token",
    # Debug / evasão
    "debug", "isdebuggerpresent", "antidebug", "sandbox", "vmware", "virtualbox", "hook", "patch", "trace",
    # Arquivos
    "file", "write", "read", "temp", "save", "log", "dump", "config", ".exe", ".dll", ".txt", ".json",
    # WinAPI
    "CreateProcess", "OpenProcess", "WriteProcessMemory", "ReadProcessMemory", "GetProcAddress", "LoadLibrary",
    "VirtualAlloc", "NtQuery", "ZwQuery", "registry", "regedit", "autorun", "shell",
    # Injeção
    "inject", "shellcode", "payload", "stager", "dropper", "bypass", "rootkit", "stealth", "syscall",
    # Hacking de jogo
    "aimbot", "esp", "wallhack", "trigger", "noclip", "recoil", "cheat", "overlay", "dxhook", "directx", "anti-cheat"
]

def contains_suspect_keyword(s):
    return any(keyword.lower() in s.lower() for keyword in SUSPECT_KEYWORDS)

def extract_strings(file_path, min_length=4):
    """Extrai strings ASCII de um binário."""
    try:
        with open(file_path, "rb") as f:
            data = f.read()
            pattern = rb"[\x20-\x7E]{%d,}" % min_length
            found = re.findall(pattern, data)
            return [s.decode("ascii", errors="ignore") for s in found]
    except Exception as e:
        return [f"[ERRO] Falha ao extrair strings: {str(e)}"]

def show_all_strings(file_path, console, return_list=False):
    try:
        with open(file_path, "rb") as f:
            data = f.read()

        strings = re.findall(rb"[\x1f-\x7e]{4,}", data)
        decoded_strings = [s.decode("utf-8", errors="ignore") for s in strings]

        if return_list:
            return decoded_strings

        console.print("[bold green]Todas as strings encontradas:[/bold green]")
        for s in decoded_strings:
            console.print(f"- {s}")

    except Exception as e:
        console.print(f"[red]Erro ao extrair strings:[/red] {e}")

def show_suspect_strings(file_path, console):
    """Mostra apenas strings com palavras-chave suspeitas"""
    console.print(f"\n[bold yellow]Strings suspeitas encontradas em:[/bold yellow] {file_path}\n")
    strings = extract_strings(file_path)
    filtered = [s for s in strings if contains_suspect_keyword(s)]

    if not filtered:
        console.print("[green]Nenhuma string suspeita encontrada.[/green]")
        return

    for s in filtered:
        console.print(f"[white]- {s}[/white]")

    console.print(f"\n[bold magenta]Total de strings suspeitas:[/bold magenta] {len(filtered)}")
