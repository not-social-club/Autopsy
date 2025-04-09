import pefile
import os

def analyze_headers_and_sections(dll_path):
    if not os.path.isfile(dll_path):
        print(f"[-] Arquivo não encontrado: {dll_path}")
        return

    try:
        pe = pefile.PE(dll_path)
        print("\n=== HEADERS PRINCIPAIS ===")
        print(f"Magic: {hex(pe.DOS_HEADER.e_magic)}")
        print(f"NT Headers Signature: {hex(pe.NT_HEADERS.Signature)}")
        print(f"Machine: {hex(pe.FILE_HEADER.Machine)}")
        print(f"Número de Seções: {pe.FILE_HEADER.NumberOfSections}")
        print(f"TimeDateStamp: {pe.FILE_HEADER.TimeDateStamp}")
        
        print("\n=== SEÇÕES PE ===")
        for section in pe.sections:
            print(f"[{section.Name.decode(errors='ignore').strip()}]")
            print(f"  Virtual Address: {hex(section.VirtualAddress)}")
            print(f"  Virtual Size   : {hex(section.Misc_VirtualSize)}")
            print(f"  Raw Size       : {hex(section.SizeOfRawData)}")
            print(f"  Flags          : {hex(section.Characteristics)}\n")
    
    except Exception as e:
        print(f"Erro na análise: {e}")
