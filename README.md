![License](https://img.shields.io/badge/license-NSC%20Confidential-red)

# NSC Reverse Autopsy

Engenharia reversa agressiva e stealth pra analisar DLLs e loaders de cheat/hack.  
Sem rastros, sem sentimentalismo.

---

## O que faz

- Análise estática de DLLs e Loaders (.exe)
- Fingerprint de linguagem e anti-debug
- Dump de strings, PE header, imports, exports, entropy
- Prepara tudo pra análise dinâmica com x64dbg em modo stealth
- Módulo automático de decoding (ex: base64)
- Stealth VM Setup incluso

---

## Requisitos

- Python 3.8+
- `pip`
- Windows (recomenda-se rodar em VM)

```bash
python --version
pip --version
```

## Instalação

`git clone https://github.com/not-social-club/Autopsy.git`
`cd Autopsy`
`pip install -r requirements.txt`

## Ambiente virtual recomendado:

`python -m venv venv`
`venv\Scripts\activate`


## Pra análise segura e indetectável em sandbox/VM.
Vai em vm_stealth_setup/ e segue as instruções no README.md lá dentro.
