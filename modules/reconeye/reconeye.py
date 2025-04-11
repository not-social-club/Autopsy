import re
import json
from collections import defaultdict

# === CATEGORIAS E PADRÕES ===
CATEGORIES = {
    "Cryptography": [r"AES", r"RSA", r"MD5", r"SHA1", r"SHA256", r"XOR", r"key", r"HASH"],
    "Execution": [r"ShellExecute[AaWw]?", r"CreateProcess", r"WinExec", r"LoadLibrary[AaWw]?", r"GetProcAddress"],
    "AntiDebug": [r"IsDebuggerPresent", r"CheckRemoteDebuggerPresent", r"NtQueryInformationProcess", r"OutputDebugString"],
    "Evasion/VM": [r"VBox", r"VMware", r"Sandbox", r"QEMU", r"XEN", r"rdtsc"],
    "FileAccess": [r"CreateFile", r"ReadFile", r"WriteFile", r"MapViewOfFile"],
    "Obfuscation": [r"[a-zA-Z0-9]{6,}ip", r"vM\\*kEy", r"ip\|Se", r"[a-zA-Z0-9]{10,}"],
    "Suspicious": [r"api-ms-win", r"vcruntime", r"msvcp", r"dll", r".exe", r"GetSystemTimeAsFileTime", r"UnloadUserProfile"]
}

# === FUNÇÃO DE DETECÇÃO ===
def classify_strings(strings):
    result = defaultdict(list)
    for s in strings:
        for category, patterns in CATEGORIES.items():
            for pattern in patterns:
                if re.search(pattern, s, re.IGNORECASE):
                    result[category].append(s)
                    break  # Evita múltiplas classificações para a mesma categoria
    return result

# === FUNÇÃO PRINCIPAL ===
def main(input_file, output_txt, output_json):
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        raw_strings = [line.strip() for line in f.readlines() if line.strip()]

    classified = classify_strings(raw_strings)

    # Salva relatório TXT
    with open(output_txt, 'w', encoding='utf-8') as f:
        for category, items in classified.items():
            f.write(f"=== {category} ({len(items)} matches) ===\n")
            for item in items:
                f.write(f"{item}\n")
            f.write("\n")

    # Salva JSON
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(classified, f, indent=4)

    print(f"[+] Análise concluída. Resultados salvos em {output_txt} e {output_json}.")

# === EXEMPLO DE USO ===
if __name__ == '__main__':
    main('strings_dump.txt', 'reconeye_output.txt', 'reconeye_output.json')
