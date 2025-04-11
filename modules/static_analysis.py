from modules.analysis import static_headers

def analyze_dll(path, console=None):
    if console:
        console.print(f"\n[bold cyan]⮞ Iniciando análise estática da DLL:[/] {path}\n")
    else:
        print(f"\n⮞ Iniciando análise estática da DLL: {path}\n")

    # Corrigido: chama a função correta
    static_headers.parse_pe_headers(path, console)
