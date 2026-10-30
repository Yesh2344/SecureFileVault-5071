"""
Integration tests for encryptor module.
"""

import os
import tempfile
from pathlib import Path

import pytest

from encryptor import encrypt_file, decrypt_file, EncryptionError, DecryptionError
from cryptography.fernet import Fernet

@pytest.fixture
def fernet_key() -> bytes:
    return Fernet.generate_key()

def test_encrypt_decrypt_roundtrip(fernet_key: bytes):
    # Create a temporary plaintext file
    with tempfile.TemporaryDirectory() as td:
        src = Path(td) / "plain.txt"
        encrypted = Path(td) / "plain.txt.enc"
        decrypted = Path(td) / "plain.txt.dec"

        plaintext = b"The quick brown fox jumps over the lazy dog." * 1000  # large payload
        src.write_bytes(plaintext)

        # Encrypt
        encrypt_file(src, encrypted, fernet_key)
        assert encrypted.is_file()
        assert encrypted.stat().st_size > 0

        # Decrypt
        decrypt_file(encrypted, decrypted, fernet_key)
        assert decrypted.read_bytes() == plaintext

def test_decrypt_with_wrong_key(fernet_key: bytes):
    with tempfile.TemporaryDirectory() as td:
        src = Path(td) / "data.txt"
        encrypted = Path(td) / "data.txt.enc"
        decrypted = Path(td) / "data.txt.dec"

        src.write_bytes(b"secret data")
        encrypt_file(src, encrypted, fernet_key)

        wrong_key = Fernet.generate_key()
        with pytest.raises(DecryptionError):
            decrypt_file(encrypted, decrypted, wrong_key)

def test_encrypt_nonexistent_source():
    with tempfile.TemporaryDirectory() as td:
        src = Path(td) / "does_not_exist.txt"
        dst = Path(td) / "out.enc"
        with pytest.raises(EncryptionError):
            encrypt_file(src, dst, Fernet.generate_key())