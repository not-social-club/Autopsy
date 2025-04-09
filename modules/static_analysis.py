from modules.analysis import static_headers

def analyze_dll(dll_path):
    print(f"Iniciando análise estática da DLL: {dll_path}\n")
    static_headers.analyze_headers_and_sections(dll_path)
