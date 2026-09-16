# Password Tool

Mali Python alat za generisanje jakih lozinki i proveru njihove jačine.

**Verzija:** v2.0.0

## Instalacija

pip install -r requirements.txt

## Pokretanje

python password_tool.py

## CLI upotreba

# Generiši lozinku od 16 karaktera
python password_tool.py --gen 16

# Proveri jačinu lozinke
python password_tool.py --check

## Primer

</> PASSWORD TOOL (PRO)
1. Generiši | 2. Provjeri: 1
Unesi dužinu lozinke: 16

[+] Nova lozinka: aB3!xY9@kLmN2pQr
[i] Kopirano u Clipboard! Čisti se automatski za 30s.

## Funkcije

- **Generator lozinki**: Koristi `secrets` modul (kriptografski siguran).
- **Provera jačine**: Analizira dužinu, velika/mala slova, brojeve, specijalne znakove.
- **Provera poznatih lozinki**: Hvata lozinke sa javnih lista (npr. `password123!`).
- **Auto-clear clipboarda**: Briše lozinku iz memorije posle 30 sekundi.
- **CLI podrška**: Može se pozvati iz terminala (`--gen`, `--check`).

## Napomena

Ovaj alat je napravljen za edukaciju.