import base64
import re
from rich import print
from rich.panel import Panel
from rich.table import Table

def is_base64(s):
    s = s.strip()
    if len(s) % 4 != 0:
        return False
    return re.fullmatch(r'[A-Za-z0-9+/=]+', s) is not None

def decode_base64_strings(strings):
    decoded_results = []
    for s in strings:
        s_clean = s.strip()
        if is_base64(s_clean):
            try:
                decoded = base64.b64decode(s_clean).decode('utf-8', errors='replace')
                decoded_results.append((s_clean, decoded, "success"))
            except Exception as e:
                decoded_results.append((s_clean, str(e), "error"))
    return decoded_results

def analisar_strings_com_base64(path):
    print(Panel.fit(f"Analisando strings com possível codificação Base64 em:\n{path}", title="Base64 Decoder"))

    try:
        with open(path, 'rb') as f:
            data = f.read()
    except Exception as e:
        print(f"[red]Erro ao ler arquivo: {e}[/red]")
        return

    ascii_data = data.decode('latin1', errors='ignore')
    strings = re.findall(r'[A-Za-z0-9+/=]{8,}', ascii_data)
    results = decode_base64_strings(strings)

    if not results:
        print("[yellow]Nenhuma string Base64 detectada.[/yellow]")
        return

    table = Table(title="Resultados de Decodificação Base64", show_lines=True)
    table.add_column("String Base64", style="cyan")
    table.add_column("Decodificado", style="white")
    table.add_column("Status", style="green")

    for base64_str, decoded, status in results:
        table.add_row(base64_str[:30] + ("..." if len(base64_str) > 30 else ""), decoded[:50] + ("..." if len(decoded) > 50 else ""), status)

    print(table)
