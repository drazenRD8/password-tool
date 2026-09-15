import string
import secrets
import re
import getpass
import argparse
import sys

try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False


def generate_password(length=12):
    """Generiše jaku nasumičnu lozinku."""
    if length < 8:
        raise ValueError("Dužina mora biti najmanje 8.")
    if length > 128:
        raise ValueError("Maksimalna dužina je 128 karaktera.")

    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def check_strength(password):
    """Analizira jačinu unijete lozinke."""
    score = 0
    feedback = []

    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        feedback.append("Lozinka je prekratka (minimum 8, preporučeno 12).")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Fale velika slova.")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Fale mala slova.")

    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("Fale brojevi.")

    if re.search(r"[!@#$%^&*()\-_=+]", password):
        score += 1
    else:
        feedback.append("Fale specijalni znakovi.")

    if re.search(r"(.)\1{2,}", password):
        score -= 1
        feedback.append("Ima previše ponavljanja istog znaka.")

    if score >= 6:
        return "Odlična / Vrlo jaka lozinka! 🔥"
    elif score >= 4:
        return f"Srednja jačina. Preporuke: {', '.join(feedback)}"
    else:
        return f"Slaba lozinka! ⚠️ Savjeti: {', '.join(feedback)}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Profesionalni alat za lozinke")
    parser.add_argument("--gen", type=int, metavar="DUŽINA", help="Generiši lozinku direktno iz terminala")
    parser.add_argument("--check", type=str, metavar="LOZINKA", help="Provjeri jačinu lozinke direktno iz terminala")
    args = parser.parse_args()

    if args.gen:
        try:
            pwd = generate_password(args.gen)
            print(f"[+] Nova lozinka: {pwd}")
            if CLIPBOARD_AVAILABLE:
                pyperclip.copy(pwd)
                print("[i] Automatski kopirano u clipboard! (Ctrl+V)")
        except ValueError as e:
            print(f"[-] Greška: {e}")
        sys.exit(0)

    if args.check:
        print(f"[REZULTAT]: {check_strength(args.check)}")
        sys.exit(0)

    print("</> PASSWORD TOOL (PRO)")
    print("1. Generiši novu lozinku")
    print("2. Provjeri jačinu postojeće lozinke")

    choice = input("\nIzaberi opciju (1 ili 2): ").strip()

    if choice == "1":
        try:
            length = int(input("Unesi dužinu lozinke (preporučeno 12+): "))
            pwd = generate_password(length)
            print(f"\n[+] Nova lozinka: {pwd}")

            if CLIPBOARD_AVAILABLE:
                pyperclip.copy(pwd)
                print("[i] Lozinka je automatski kopirana u memoriju (Clipboard)! Možeš je zalijepiti sa Ctrl+V.")
            else:
                print("[i] Savjet: Instaliraj 'pyperclip' (`pip install pyperclip`) za automatsko kopiranje.")
        except ValueError as e:
            print(f"[-] Greška: {e}")

    elif choice == "2":
        pwd = getpass.getpass("Unesi lozinku za provjeru: ")
        print(f"\n[REZULTAT]: {check_strength(pwd)}")
    else:
        print("[-] Nepoznata opcija.")