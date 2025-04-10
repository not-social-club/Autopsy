import pefile
import os
from rich import print
from rich.table import Table
from rich.panel import Panel
from modules.entropy_analysis import calculate_entropy, classify_entropy, predict_packer


def analisar_headers_pe(file_path):
    try:
        pe = pefile.PE(file_path)
        table = Table(title="Headers PE", show_lines=True)
        table.add_column("Campo", style="bold cyan")
        table.add_column("Valor", style="bold white")

        table.add_row("Entrypoint", hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint))
        table.add_row("ImageBase", hex(pe.OPTIONAL_HEADER.ImageBase))
        table.add_row("Número de Seções", str(pe.FILE_HEADER.NumberOfSections))
        table.add_row("Subsystem", str(pe.OPTIONAL_HEADER.Subsystem))
        table.add_row("Tamanho da Image", hex(pe.OPTIONAL_HEADER.SizeOfImage))

        print(table)
    except Exception as e:
        print(f"[red]Erro ao analisar PE: {e}[/red]")


def analisar_secoes(pe):
    table = Table(title="Seções do Executável", show_lines=True)
    table.add_column("Nome", style="bold green")
    table.add_column("Virtual Address", justify="right")
    table.add_column("Size", justify="right")
    table.add_column("Flags", justify="right")

    for section in pe.sections:
        name = section.Name.decode(errors="ignore").strip("\x00")
        vaddr = hex(section.VirtualAddress)
        size = hex(section.Misc_VirtualSize)
        flags = hex(section.Characteristics)
        table.add_row(name, vaddr, size, flags)

    print(table)


def analisar_imports(pe):
    try:
        print("[bold cyan]⮞ Imports:[/bold cyan]")
        for entry in pe.DIRECTORY_ENTRY_IMPORT:
            print(f"[yellow]{entry.dll.decode()}[/yellow]")
            for imp in entry.imports:
                print(f"  └─ {imp.name.decode() if imp.name else 'None'} @ {hex(imp.address)}")
    except AttributeError:
        print("[red]Nenhum import encontrado.[/red]")


def analisar_exports(pe):
    try:
        print("[bold cyan]⮞ Funções Exportadas:[/bold cyan]")
        for exp in pe.DIRECTORY_ENTRY_EXPORT.symbols:
            name = exp.name.decode() if exp.name else "None"
            addr = hex(pe.OPTIONAL_HEADER.ImageBase + exp.address)
            print(f"  └─ {name} @ {addr}")
    except AttributeError:
        print("[red]Nenhum export encontrado.[/red]")


def analisar_entrypoint_entropia(pe):
    entrypoint_rva = pe.OPTIONAL_HEADER.AddressOfEntryPoint
    section = None
    for s in pe.sections:
        if s.VirtualAddress <= entrypoint_rva < s.VirtualAddress + s.Misc_VirtualSize:
            section = s
            break

    if section:
        data = section.get_data()
        entropy = calculate_entropy(data)
        section_name = section.Name.decode().strip("\x00")
        print(f"\n[bold cyan]⮞ Entrypoint e Entropia:[/bold cyan]")
        print(f"Entrypoint na seção: [bold yellow]{section_name}[/bold yellow] com entropia: [bold magenta]{entropy:.2f}[/bold magenta]")
        print(f"Classificação: [green]{classify_entropy(entropy)}[/green]")
        predicted = predict_packer(entropy)
        print(f"Packer provável: [bold red]{predicted}[/bold red]")
    else:
        print("[red]Não foi possível determinar a seção do entrypoint.[/red]")


def analisar_loader(filepath, deep=False):
    print(Panel.fit(f"Iniciando análise do Loader\n{filepath}\nModo: {'DEEP' if deep else 'BÁSICO'}", title=""))
    try:
        pe = pefile.PE(filepath)
    except Exception as e:
        print(f"[red]Erro ao carregar PE: {e}[/red]")
        return

    if deep:
        print(f"\n[bold cyan]⮞ Headers PE:[/bold cyan]")
        analisar_headers_pe(filepath)

    print(f"\n[bold cyan]⮞ Seções encontradas:[/bold cyan]")
    analisar_secoes(pe)

    print(f"\n[bold cyan]⮞ Imports:[/bold cyan]")
    analisar_imports(pe)

    print(f"\n[bold cyan]⮞ Funções Exportadas:[/bold cyan]")
    analisar_exports(pe)

    print(f"\n[bold cyan]⮞ Entrypoint e Entropia:[/bold cyan]")
    analisar_entrypoint_entropia(pe)
