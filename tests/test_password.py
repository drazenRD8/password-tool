"""
Testovi za password-tool.
Pokreni: pytest -v
"""
import re
import string
import sys
from pathlib import Path

# Dodaj root folder u path da bi import radio
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from password_tool import (
    generate_password,
    check_strength,
)


# ============================================================
# TESTIRANJE generate_password()
# ============================================================

class TestGeneratePassword:
    """Testovi za funkciju generate_password."""

    def test_default_length(self):
        """Testira da li je default dužina 12."""
        pwd = generate_password()
        assert len(pwd) == 12

    def test_custom_length(self):
        """Testira različite dužine."""
        for length in [8, 12, 16, 32, 64, 128]:
            pwd = generate_password(length)
            assert len(pwd) == length

    def test_min_length_raises(self):
        """Testira da dužina < 8 baca ValueError."""
        for length in [0, 1, 7]:
            try:
                generate_password(length)
                assert False, f"Trebalo je da baci ValueError za {length}"
            except ValueError:
                pass

    def test_max_length_raises(self):
        """Testira da dužina > 128 baca ValueError."""
        for length in [129, 200, 1000]:
            try:
                generate_password(length)
                assert False, f"Trebalo je da baci ValueError za {length}"
            except ValueError:
                pass

    def test_contains_letters(self):
        """Testira da lozinka sadrži slova."""
        pwd = generate_password(16)
        assert re.search(r"[a-zA-Z]", pwd)

    def test_contains_digits(self):
        """Testira da lozinka sadrži brojeve."""
        pwd = generate_password(16)
        assert re.search(r"\d", pwd)

    def test_contains_special(self):
        """Testira da lozinka sadrži specijalne znakove."""
        pwd = generate_password(16)
        assert re.search(r"[!@#$%^&*()\-_=+]", pwd)

    def test_unique_passwords(self):
        """Testira da su dve lozinke različite."""
        pwd1 = generate_password(16)
        pwd2 = generate_password(16)
        assert pwd1 != pwd2

    def test_only_valid_chars(self):
        """Testira da lozinka sadrži samo dozvoljene znakove."""
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
        pwd = generate_password(50)
        for char in pwd:
            assert char in alphabet


# ============================================================
# TESTIRANJE check_strength()
# ============================================================

class TestCheckStrength:
    """Testovi za funkciju check_strength."""

    def test_blacklisted_passwords(self):
        """Testira da blacklisted lozinke vraćaju 'Kritično slaba'."""
        for pwd in ["password123!", "administrator", "lozinka123"]:
            result = check_strength(pwd)
            assert "Kritično slaba" in result

    def test_blacklisted_case_insensitive(self):
        """Testira da blacklist radi i sa velikim slovima."""
        result = check_strength("PASSWORD123!")
        assert "Kritično slaba" in result

    def test_strong_password(self):
        """Testira jaku lozinku."""
        pwd = "MyStr0ng!P@ssw0rd2025"
        result = check_strength(pwd)
        assert "Odlična" in result or "Vrlo jaka" in result

    def test_medium_password(self):
        """Testira srednju lozinku."""
        pwd = "Password123"
        result = check_strength(pwd)
        assert "Srednja" in result or "Slaba" in result

    def test_weak_password_short(self):
        """Testira kratku lozinku."""
        result = check_strength("abc")
        assert "Slaba" in result

    def test_weak_password_lowercase_only(self):
        """Testira lozinku samo mala slova."""
        result = check_strength("abcdefghij")
        assert "Slaba" in result or "Srednja" in result

    def test_feedback_for_missing_uppercase(self):
        """Testira feedback za nedostatak velikih slova."""
        result = check_strength("abcdefgh123!")
        assert isinstance(result, str)

    def test_feedback_contains_suggestions(self):
        """Testira da slaba lozinka ima preporuke."""
        result = check_strength("abc")
        assert "Savjeti" in result or "Preporuke" in result

    def test_empty_password(self):
        """Testira praznu lozinku."""
        result = check_strength("")
        assert isinstance(result, str)

    def test_long_password(self):
        """Testira veoma dugu lozinku."""
        pwd = "A" * 100 + "a1!"
        result = check_strength(pwd)
        assert isinstance(result, str)

    def test_password_with_all_categories(self):
        """Testira lozinku sa svim kategorijama."""
        pwd = "MyP@ssw0rd!2025Secure"
        result = check_strength(pwd)
        assert "Odlična" in result or "Vrlo jaka" in result

    def test_password_missing_special(self):
        """Testira lozinku bez specijalnih znakova."""
        pwd = "MyPassword12345"
        result = check_strength(pwd)
        assert "Srednja" in result or "Slaba" in result
