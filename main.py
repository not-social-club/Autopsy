import os
import sys

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    print(r"""                                                                                  
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
                Not Social Club ©               ##                  /#######  /#  
                                                 ##                /      ###/    
""")

def submenu_analise_dll():
    while True:
        clear()
        print("╔══════════════════════════════════╗")
        print("║     Submenu: Análise de DLL      ║")
        print("╠══════════════════════════════════╣")
        print("║ [1] Strings Suspeitas            ║")
        print("║ [2] Entropia de Seções           ║")
        print("║ [3] Imports / Exports            ║")
        print("║ [4] Detectar Packing             ║")
        print("║ [0] Voltar                       ║")
        print("╚══════════════════════════════════╝")
        choice = input(">> Escolha uma opção: ").strip()
        if choice == "0":
            break
        else:
            print("→ Em construção.")
            input("Pressione Enter para voltar...")

def submenu_analise_loader():
    while True:
        clear()
        print("╔══════════════════════════════════╗")
        print("║    Submenu: Análise de Loader    ║")
        print("╠══════════════════════════════════╣")
        print("║ [1] Strings Suspeitas            ║")
        print("║ [2] Seções PE                    ║")
        print("║ [3] EntryPoint                   ║")
        print("║ [4] Entropia & Imports           ║")
        print("║ [0] Voltar                       ║")
        print("╚══════════════════════════════════╝")
        choice = input(">> Escolha uma opção: ").strip()
        if choice == "0":
            break
        else:
            print("→ Em construção.")
            input("Pressione Enter para voltar...")

def submenu_antidebug_vm():
    while True:
        clear()
        print("╔══════════════════════════════════╗")
        print("║     Submenu: Anti-Debug / VM     ║")
        print("╠══════════════════════════════════╣")
        print("║ [1] Check API Suspicious         ║")
        print("║ [2] Artefatos de VM              ║")
        print("║ [3] Técnicas Anti-Debug          ║")
        print("║ [0] Voltar                       ║")
        print("╚══════════════════════════════════╝")
        choice = input(">> Escolha uma opção: ").strip()
        if choice == "0":
            break
        else:
            print("→ Em construção.")
            input("Pressione Enter para voltar...")

def print_menu():
    clear()
    print_banner()
    print("╔════════════════════════════════════════════╗")
    print("║       Analysis Toolkit v2.0 - MAIN MENU    ║")
    print("╠════════════════════════════════════════════╣")
    print("║ [1] Selecionar DLL                         ║")
    print("║ [2] Selecionar Loader                      ║")
    print("║ [3] Análise DLL                            ║")
    print("║ [4] Análise Loader                         ║")
    print("║ [5] Anti-Debug / VM Check                  ║")
    print("║ [0] Sair                                   ║")
    print("╚════════════════════════════════════════════╝")

def main():
    while True:
        print_menu()
        choice = input(">> Escolha uma opção: ").strip()
        
        if choice == "1":
            print("→ [Selecionar DLL] Módulo em construção.")
            input("Pressione Enter para voltar...")
        elif choice == "2":
            print("→ [Selecionar Loader] Módulo em construção.")
            input("Pressione Enter para voltar...")
        elif choice == "3":
            submenu_analise_dll()
        elif choice == "4":
            submenu_analise_loader()
        elif choice == "5":
            submenu_antidebug_vm()
        elif choice == "0":
            print("Encerrando...")
            sys.exit(0)
        else:
            print("Opção inválida.")
            input("Pressione Enter para continuar...")

if __name__ == "__main__":
    main()
