def deep_analyze_loader(path):
    console.print(f"\n[bold cyan]Análise Avançada do Loader:[/bold cyan] {path}")

    # 1. Headers e Imports
    print_headers(path)
    print_imports(path)

    # 2. Export Table
    check_exports(path)

    # 3. Seções suspeitas
    analyze_sections(path)

    # 4. Entropia
    check_entropy(path)

    # 5. Packers detectados
    detect_packers(path)

    # 6. Code caves
    scan_code_caves(path)

    # 7. EntryPoint fora da .text
    check_entry_point(path)

    # 8. Dump de seções (opcional)
    dump_sections(path)

    # 9. Exportar tudo
    save_full_report(path)