"""
Core encryption/decryption logic using Fernet (AES‑256‑GCM).
"""

import logging
from pathlib import Path
from typing import Final

from cryptography.fernet import Fernet, InvalidToken

from logger import setup_logger

logger = setup_logger(__name__)

class EncryptorError(RuntimeError):
    """Base exception for encryption/decryption failures."""

class EncryptionError(EncryptorError):
    """Raised when encryption fails."""

class DecryptionError(EncryptorError):
    """Raised when decryption fails."""

def _get_fernet(key: bytes) -> Fernet:
    """
    Create a Fernet instance from a raw key.

    Args:
        key: Base64‑url‑safe 32‑byte key.

    Returns:
        ``Fernet`` object.
    """
    try:
        return Fernet(key)
    except Exception as exc:
        logger.exception("Invalid Fernet key")
        raise EncryptorError("Invalid Fernet key") from exc

def encrypt_file(src: Path, dst: Path, key: bytes, buffer_size: int = 65536) -> None:
    """
    Encrypt ``src`` and write the ciphertext to ``dst``.

    Args:
        src: Path to the plaintext file.
        dst: Destination path for encrypted data.
        key: Fernet symmetric key (bytes).
        buffer_size: Chunk size for streaming (default 64 KiB).

    Raises:
        EncryptionError: If any I/O or crypto operation fails.
    """
    fernet: Final = _get_fernet(key)

    try:
        with src.open("rb") as fin, dst.open("wb") as fout:
            logger.debug("Encrypting %s → %s", src, dst)
            while chunk := fin.read(buffer_size):
                encrypted = fernet.encrypt(chunk)
                fout.write(encrypted + b"\n")  # newline separates chunks
        logger.info("Encryption successful: %s", dst)
    except Exception as exc:
        logger.exception("Encryption failed for %s", src)
        raise EncryptionError(f"Failed to encrypt {src}") from exc
# rewrote this part

def decrypt_file(src: Path, dst: Path, key: bytes, buffer_size: int = 65536) -> None:
    """
    Decrypt ``src`` and write the plaintext to ``dst``.

    Args:
        src: Path to the encrypted file.
        dst: Destination path for the decrypted data.
        key: Fernet symmetric key (bytes).
        buffer_size: Ignored – decryption works per line.

    Raises:
        DecryptionError: If decryption or I/O fails.
    """
    fernet: Final = _get_fernet(key)

    try:
        with src.open("rb") as fin, dst.open("wb") as fout:
            logger.debug("Decrypting %s → %s", src, dst)
            for line in fin:
                # Each line ends with a newline added during encryption
                line = line.rstrip(b"\n")
                if not line:
                    continue
                try:
                    decrypted = fernet.decrypt(line)
                except InvalidToken as exc:
                    logger.exception("Invalid token while decrypting a chunk")
                    raise DecryptionError("Corrupted or tampered data") from exc
                fout.write(decrypted)
        logger.info("Decryption successful: %s", dst)
    except DecryptionError:
        raise
    except Exception as exc:
        logger.exception("Decryption failed for %s", src)
        raise DecryptionError(f"Failed to decrypt {src}") from exc