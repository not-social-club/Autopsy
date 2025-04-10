import os
import re
import time
import pefile
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from modules.analysis.loader_analysis import analyze_loader
from modules.static_analysis import analyze_dll
from modules.analysis import static_headers
from modules.static_strings import show_all_strings, show_suspect_strings
from modules.analysis.anti_evade_scanner import detect_anti_debug_vm, detect_anti_debug_vm_heuristic

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
           /    ##     ##    ###  / ######## / ###  / / ###  / / #### / ##    ###/   
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
        console.print("[3] Análise Estática da DLL")
        console.print("[4] Analisar Strings da DLL")
        console.print("[5] Detectar Anti-Debug / Anti-VM")
        console.print("[6] Análise do Loader")
        console.print("[0] Sair")

        choice = Prompt.ask("\nEscolha uma opção", choices=["0", "1", "2", "3", "4", "5", "6"])

        if choice == "1":
            selected_dll = input("Digite o caminho da DLL: ").strip('"').strip()
            console.print(f"[green]DLL selecionada:[/green] {selected_dll}")

        elif choice == "2":
            selected_loader = input("Digite o caminho do Loader EXE: ").strip('"').strip()
            console.print(f"[green]Loader selecionado:[/green] {selected_loader}")

        elif choice == "3":
            if not selected_dll:
                console.print("[red]Selecione uma DLL primeiro![/red]")
                continue
            analyze_dll(selected_dll, console)

        elif choice == "4":
            if not selected_dll:
                console.print("[red]Selecione uma DLL primeiro![/red]")
                continue

            while True:
                console.print("\n[bold yellow]Análise de Strings da DLL[/bold yellow]")
                console.print("[1] Ver TODAS as Strings")
                console.print("[2] Ver STRINGS SUSPEITAS")
                console.print("[0] Voltar")

                string_choice = Prompt.ask("\nEscolha uma opção", choices=["0", "1", "2"])

                if string_choice == "1":
                    show_all_strings(selected_dll, console)
                elif string_choice == "2":
                    show_suspect_strings(selected_dll, console)
                elif string_choice == "0":
                    break

        elif choice == "5":
            if not selected_dll:
                console.print("[red]Selecione uma DLL primeiro![/red]")
                continue

            console.print("\n[bold yellow]Modo de Detecção[/bold yellow]")
            console.print("[1] Detecção Clássica")
            console.print("[2] Heurística com confiabilidade")
            console.print("[3] Mostrar as duas")

            sub_choice = Prompt.ask("\nEscolha o modo de detecção", choices=["1", "2", "3"], default="3")
            all_strings = show_all_strings(selected_dll, console, return_list=True)

            pe = pefile.PE(selected_dll)
            hits = {}

            if sub_choice in ["1", "3"]:
                hits.update(detect_anti_debug_vm(pe, all_strings))
            if sub_choice in ["2", "3"]:
                heuristic = detect_anti_debug_vm_heuristic(all_strings, pe, console)    
                for cat, values in heuristic.items():
                    if cat in hits:
                        hits[cat].extend(values)
                    else:
                        hits[cat] = values

            if hits:
                console.print("[bold red]\n[!] Técnicas suspeitas de Anti-Debug ou Anti-VM detectadas:[/bold red]")
                for category, items in hits.items():
                    console.print(f"\n[bold cyan]{category}:[/bold cyan]")
                    for item in items:
                        if isinstance(item, tuple):
                            level, value = item
                        else:
                            level, value = "Suspeito", item
                        color = "green" if level == "Seguro" else ("yellow" if level == "Suspeito" else "red")
                        console.print(f" → [{color}]{level}[/{color}] → {value}")
            else:
                console.print("[green]Nenhuma técnica suspeita detectada.[/green]")

        elif choice == "6":
            if not selected_loader:
                console.print("[red]Selecione um Loader primeiro![/red]")
                continue

            console.print("\n[bold yellow]Modo de Análise do Loader[/bold yellow]")
            console.print("[1] Análise Básica")
            console.print("[2] Análise Profunda")

            mode_choice = Prompt.ask("Escolha o modo de análise", choices=["1", "2"], default="1")
            mode = "deep" if mode_choice == "2" else "basic"

            analyze_loader(selected_loader, mode=mode)

        elif choice == "0":
            console.print("[bold red]Saindo...[/bold red]")
            break

        else:
            console.print("[yellow]Opção inválida.[/yellow]")

if __name__ == "__main__":
    banner()
    main_menu()
