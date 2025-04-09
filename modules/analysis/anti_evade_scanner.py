import re
from collections import defaultdict

# Palavras-chave clássicas conhecidas por evasores
KNOWN_ANTI_DEBUG_VM = {
    "Anti-VM": ["vmware", "vbox", "virtualbox", "qemu", "xen", "virtual", "sandbox"],
    "Anti-Debug": ["isdebuggerpresent", "checkremotedebuggerpresent", "ntqueryinformationprocess", "debugactiveprocess"]
}

# Heurística mais sensível
HEURISTIC_PATTERNS = {
    "Anti-VM": [
        (r".*xen.*", "Suspeito"),
        (r".*vmware.*", "Confirmado evasor"),
        (r".*vbox.*", "Confirmado evasor"),
        (r".*qemu.*", "Confirmado evasor"),
        (r".*virtual.*", "Suspeito"),
        (r".*sandbox.*", "Suspeito"),
    ],
    "Anti-Debug": [
        (r".*isdebuggerpresent.*", "Confirmado evasor"),
        (r".*checkremotedebuggerpresent.*", "Confirmado evasor"),
        (r".*ntqueryinformationprocess.*", "Confirmado evasor"),
        (r".*debugactiveprocess.*", "Confirmado evasor"),
        (r".*dbg.*", "Suspeito"),
    ]
}


def detect_anti_debug_vm(pe, strings_list):
    """Detecção clássica baseada em palavras-chave fixas"""
    hits = defaultdict(list)
    for category, keywords in KNOWN_ANTI_DEBUG_VM.items():
        for string in strings_list:
            for keyword in keywords:
                if keyword.lower() in string.lower():
                    hits[category].append(keyword)
    return hits


def detect_anti_debug_vm_heuristic(strings_list, pe, console):
    """Detecção heurística com classificação de confiabilidade"""
    results = defaultdict(list)

    for category, patterns in HEURISTIC_PATTERNS.items():
        for string in strings_list:
            for pattern, confidence in patterns:
                if re.search(pattern, string, re.IGNORECASE):
                    results[category].append((string, confidence))

    if console:
        for category, items in results.items():
            console.print(f"\n[bold cyan]{category}:[/bold cyan]")
            for value, confidence in items:
                if confidence == "Seguro":
                    color = "green"
                elif confidence == "Suspeito":
                    color = "yellow"
                else:
                    color = "red"
                console.print(f"[{color}] → {confidence} → {value}[/{color}]")

    return results
