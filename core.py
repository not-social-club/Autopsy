import os
import time
import pefile
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from modules.static_analysis import analyze_dll
from modules.analysis import static_headers
from modules.static_strings import show_all_strings, show_suspect_strings
from modules.analysis.anti_evade_scanner import detect_anti_debug_vm

console = Console()

selected_dll = None
selected_loader = None


def banner():
    console.clear()
    console.print(Panel("""                                                                                  
              ##                                                                      
           /####                                                                      
          /  ###                        #                                             
             /##                       ##                                             
            /  ##                      ##                                             
            /  ##     ##   ####      ######## /###     /###     /###   ##   ####      
           /    ##     ##    ###  / ######## / ###  / / ###  / / #### / ##    ###  /  
           /    ##     ##     ###/     ##   /   ###/ /   ###/ ##  ###/  ##     ###/   
          /      ##    ##      ##      ##  ##    ## ##    ## ####       ##      ##    
          /########    ##      ##      ##  ##    ## ##    ##   ###      ##      ##    
         /        ##   ##      ##      ##  ##    ## ##    ##     ###    ##      ##    
         #        ##   ##      ##      ##  ##    ## ##    ##       ###  ##      ##    
        /####      ##  ##      /#      ##  ##    ## ##    ##  /###  ##  ##      ##    
       /   ####    ## / ######/ ##     ##   ######  #######  / #### /    #########    
      /     ##      #/   #####   ##     ##   ####   ######      ###/       #### ###   
      #                                             ##                           ###  
       ##                                           ##                    #####   ### 
        [bold red]v0.1[/bold red] - [italic cyan]Not Social Club[/italic cyan]                      ##                  /#######  /#  
                                                    ##                /      ###/    
    """))

def main_menu():
    global selected_dll, selected_loader

    while True:
        console.print("\n[bold green]MENU PRINCIPAL[/bold green]", style="bold underline")
        console.print("[1] Selecionar DLL (Payload)")
        console.print("[2] Selecionar Loader (EXE)")
        console.print("[3] Executar Análise Estática")
        console.print("[4] Ver TODAS as Strings da DLL")
        console.print("[5] Ver STRINGS SUSPEITAS da DLL")
        console.print("[6] Detectar Anti-Debug / Anti-VM")
        console.print("[0] Sair")

        choice = Prompt.ask("\nEscolha uma opção", choices=["0", "1", "2", "3", "4", "5", "6"])

        if choice == "1":
            selected_dll = input("Digite o caminho da DLL: ")
            console.print(f"[green]DLL selecionada:[/green] {selected_dll}")

        elif choice == "2":
            selected_loader = input("Digite o caminho do Loader EXE: ")
            console.print(f"[green]Loader selecionado:[/green] {selected_loader}")

        elif choice == "3":
            if not selected_dll:
                console.print("[red]Selecione uma DLL primeiro![/red]")
                continue
            analyze_dll(selected_dll)

        elif choice == "4":
            if not selected_dll:
                console.print("[red]Selecione uma DLL primeiro![/red]")
                continue
            show_all_strings(selected_dll, console)

        elif choice == "5":
            if not selected_dll:
                console.print("[red]Selecione uma DLL primeiro![/red]")
                continue
            show_suspect_strings(selected_dll, console)

        elif choice == "6":
            if not selected_dll:
                console.print("[red]Selecione uma DLL primeiro![/red]")
                continue

            try:
                pe = pefile.PE(selected_dll)
                with open(selected_dll, 'rb') as f:
                    raw_data = f.read()
                all_strings = set([s.decode(errors='ignore') for s in raw_data.split(b'\x00') if len(s) > 4])

                anti_hits = detect_anti_debug_vm(pe, all_strings)
                if anti_hits:
                    console.print("[bold red][!] Técnicas suspeitas de Anti-Debug ou Anti-VM detectadas:[/bold red]")
                    for h in anti_hits:
                        console.print(f" → {h}")
                else:
                    console.print("[green]Nenhuma técnica suspeita detectada.[/green]")

            except Exception as e:
                console.print(f"[red]Erro ao analisar DLL:[/red] {e}")

        elif choice == "0":
            console.print("[bold red]Saindo...[/bold red]")
            break

        else:
            console.print("[yellow]Opção inválida.[/yellow]")

if __name__ == "__main__":
    banner()
    main_menu()
