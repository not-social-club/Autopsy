def detect_anti_debug_vm(pe, strings):
    """
    Detecta técnicas comuns de anti-debug e anti-VM baseadas em strings presentes no binário.
    Retorna uma lista de técnicas suspeitas detectadas.
    """
    hits = []

    # Técnicas comuns de Anti-Debug
    anti_debug_keywords = [
        "IsDebuggerPresent", "CheckRemoteDebuggerPresent", "NtQueryInformationProcess",
        "OutputDebugString", "DebugActiveProcess", "UnhandledExceptionFilter",
        "GetTickCount", "QueryPerformanceCounter"
    ]

    # Técnicas comuns de Anti-VM
    anti_vm_keywords = [
        "VBox", "VMware", "vboxservice.exe", "vmtoolsd.exe", "QEMU", "VirtualBox",
        "Xen", "Hyper-V", "Parallels", "Sandboxie", "HARDWARE\\ACPI\\DSDT\\VBOX__",
        "SOFTWARE\\VMware, Inc.", "SystemBiosVersion", "VideoBiosVersion"
    ]

    # Normaliza as strings para comparação (case-insensitive)
    normalized_strings = [s.lower() for s in strings]

    # Busca por correspondências
    for keyword in anti_debug_keywords + anti_vm_keywords:
        for s in normalized_strings:
            if keyword.lower() in s:
                hits.append(keyword)
                break  # evita duplicatas desnecessárias

    return list(set(hits))  # remove duplicatas finais
