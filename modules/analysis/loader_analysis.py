import os
import pefile
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from modules.analysis.static_headers import parse_pe_headers

console = Console()

def analyze_loader(path, mode="basic"):
    if not os.path.isfile(path):
        console.print(f"[red]Arquivo não encontrado:[/red] {path}")
        return

    try:
        pe = pefile.PE(path)
        console.print(Panel(f"[bold green]Iniciando análise do Loader[/bold green]\n[cyan]{path}[/cyan]\nModo: [yellow]{mode.upper()}[/yellow]"))

        # Análise básica
        console.print("\n[bold cyan]⮞ Headers PE:[/bold cyan]")
        parse_pe_headers(pe, console)

        console.print("\n[bold cyan]⮞ Seções encontradas:[/bold cyan]")
        table = Table(title="Seções do Executável")
        table.add_column("Nome", style="magenta")
        table.add_column("Virtual Address", justify="right")
        table.add_column("Size", justify="right")
        table.add_column("Flags", justify="right")

        for section in pe.sections:
            table.add_row(
                section.Name.decode(errors="ignore").strip("\x00"),
                hex(section.VirtualAddress),
                hex(section.Misc_VirtualSize),
                hex(section.Characteristics)
            )

        console.print(table)

        # Modo profundo
        if mode == "deep":
            console.print("\n[bold cyan]⮞ Imports:[/bold cyan]")
            if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
                for entry in pe.DIRECTORY_ENTRY_IMPORT:
                    console.print(f"[green]{entry.dll.decode()}[/green]")
                    for imp in entry.imports:
                        addr = hex(imp.address) if imp.address else "N/A"
                        name = imp.name.decode() if imp.name else "N/A"
                        console.print(f"  └─ {name} @ {addr}")
            else:
                console.print("[yellow]Nenhuma entrada de import encontrada.[/yellow]")

            console.print("\n[bold cyan]⮞ Funções Exportadas:[/bold cyan]")
            if hasattr(pe, 'DIRECTORY_ENTRY_EXPORT'):
                for exp in pe.DIRECTORY_ENTRY_EXPORT.symbols:
                    name = exp.name.decode() if exp.name else "N/A"
                    console.print(f"  └─ {name} @ {hex(pe.OPTIONAL_HEADER.ImageBase + exp.address)}")
            else:
                console.print("[yellow]Nenhuma exportação encontrada.[/yellow]")

            console.print("\n[bold cyan]⮞ Entrypoint e Entropia:[/bold cyan]")
            entrypoint = pe.OPTIONAL_HEADER.AddressOfEntryPoint
            entrypoint_section = None
            for section in pe.sections:
                if section.VirtualAddress <= entrypoint < section.VirtualAddress + section.Misc_VirtualSize:
                    entrypoint_section = section
                    break

            if entrypoint_section:
                entropy = entrypoint_section.get_entropy()
                name = entrypoint_section.Name.decode().strip("\x00")
                console.print(f"Entrypoint na seção: [bold]{name}[/bold] com entropia: [red]{entropy:.2f}[/red]")
            else:
                console.print("[red]Não foi possível determinar a seção do entrypoint.[/red]")

    except Exception as e:
        console.print(f"[red]Erro ao analisar loader:[/red] {e}")
