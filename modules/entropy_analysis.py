import math

def calculate_entropy(data):
    if not data:
        return 0.0
    entropy = 0
    byte_counts = [0] * 256
    for byte in data:
        byte_counts[byte] += 1
    for count in byte_counts:
        if count == 0:
            continue
        p = count / len(data)
        entropy -= p * math.log2(p)
    return entropy

def classify_entropy(entropy):
    if entropy < 3.5:
        return "Baixa"
    elif 3.5 <= entropy < 6.5:
        return "Média"
    else:
        return "Alta"

def predict_packer(entropy):
    if entropy > 7.0:
        return "Provavelmente Packed (ex: UPX, Themida, etc)"
    elif entropy > 6.0:
        return "Possivelmente Packed"
    else:
        return "Pouco provável"
