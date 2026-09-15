import string
import secrets
import re
import getpass
import argparse
import sys
import time
import threading

try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False


def clear_clipboard_delayed(delay=30):
    """Prazni clipboard nakon definisanog broja sekundi."""
    time.sleep(delay)
    if CLIPBOARD_AVAILABLE:
        try:
            pyperclip.copy("")
            print("\n[i] Sadržaj lozinke je automatski obrisan iz memorije (Clipboard) radi bezbednosti.")
        except Exception:
            pass


def generate_password(length=12):
    if length < 8:
        raise ValueError("Dužina mora biti najmanje 8.")
    if length > 128:
        raise ValueError("Maksimalna dužina je 128 karaktera.")
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def check_strength(password):
    score = 0
    feedback = []

    if password.lower() in ["password123!", "administrator", "lozinka123"]:
        return "Kritično slaba lozinka! Nalazi se na javnim listama hakovanih lozinki. ⚠️"

    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        feedback.append("Lozinka je prekratka.")

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

    if score >= 6:
        return "Odlična / Vrlo jaka lozinka! 🔥"
    elif score >= 4:
        return f"Srednja jačina. Preporuke: {', '.join(feedback)}"
    return f"Slaba lozinka! ⚠️ Savjeti: {', '.join(feedback)}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Profesionalni alat za lozinke")
    parser.add_argument("--gen", type=int, metavar="DUŽINA", help="Generiši lozinku direktno iz terminala")
    parser.add_argument("--check", action="store_true", help="Pokreni bezbednu interaktivnu proveru")
    args = parser.parse_args()

    if args.gen:
        try:
            pwd = generate_password(args.gen)
            print(f"[+] Nova lozinka: {pwd}")
            if CLIPBOARD_AVAILABLE:
                pyperclip.copy(pwd)
                print("[i] Kopirano u clipboard! Biće obrisano za 30 sekundi.")
                threading.Thread(target=clear_clipboard_delayed, daemon=True).start()
                time.sleep(0.5)
        except ValueError as e:
            print(f"[-] Greška: {e}")
        sys.exit(0)

    if args.check:
        pwd = getpass.getpass("Unesi lozinku za provjeru: ")
        print(f"[REZULTAT]: {check_strength(pwd)}")
        sys.exit(0)

    print("</> PASSWORD TOOL (PRO)")
    choice = input("1. Generiši | 2. Provjeri: ").strip()

    if choice == "1":
        try:
            length = int(input("Unesi dužinu lozinke: "))
            pwd = generate_password(length)
            print(f"[+] Nova lozinka: {pwd}")
            if CLIPBOARD_AVAILABLE:
                pyperclip.copy(pwd)
                print("[i] Kopirano u Clipboard! Čisti se automatski za 30s.")
                threading.Thread(target=clear_clipboard_delayed, daemon=True).start()
                print("[i] Nemoj gasiti terminal dok se memorija ne očisti...")
                time.sleep(31)
        except ValueError as e:
            print(f"[-] Greška: {e}")
    elif choice == "2":
        pwd = getpass.getpass("Unesi lozinku za provjeru: ")
        print(f"[REZULTAT]: {check_strength(pwd)}")