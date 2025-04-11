import pefile
from rich.table import Table

def parse_pe_headers(path, console):
    try:
        pe = pefile.PE(path)

        table = Table(title="PE Headers")
        table.add_column("Campo", style="cyan", no_wrap=True)
        table.add_column("Valor", style="magenta")

        table.add_row("Machine", hex(pe.FILE_HEADER.Machine))
        table.add_row("NumberOfSections", str(pe.FILE_HEADER.NumberOfSections))
        table.add_row("TimeDateStamp", hex(pe.FILE_HEADER.TimeDateStamp))
        table.add_row("Characteristics", hex(pe.FILE_HEADER.Characteristics))
        table.add_row("EntryPoint", hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint))
        table.add_row("ImageBase", hex(pe.OPTIONAL_HEADER.ImageBase))

        console.print(table)

    except Exception as e:
        console.print(f"[bold red]Erro ao analisar PE:[/] {e}")
