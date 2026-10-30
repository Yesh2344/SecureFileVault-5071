"""
Command‑line interface for SecureFileVault.
"""

import argparse
import sys
from pathlib import Path

from config import load_environment, load_yaml_config
from encryptor import encrypt_file, decrypt_file, EncryptionError, DecryptionError
from logger import setup_logger
from utils import resolve_paths, safe_overwrite, copy_permissions

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="securefilevault",
        description="Encrypt or decrypt files using Fernet (AES‑256‑GCM)."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Encrypt sub‑command
    enc_parser = subparsers.add_parser("encrypt", help="Encrypt a file")
    enc_parser.add_argument("source", help="Path to the plaintext file")
    enc_parser.add_argument("-o", "--output", help="Destination encrypted file")
    enc_parser.add_argument("-f", "--force", action="store_true", help="Overwrite existing output")
    enc_parser.add_argument("-c", "--config", type=Path, help="Custom config.yaml path")

    # Decrypt sub‑command
    dec_parser = subparsers.add_parser("decrypt", help="Decrypt a file")
    dec_parser.add_argument("source", help="Path to the encrypted file")
    dec_parser.add_argument("-o", "--output", help="Destination decrypted file")
    dec_parser.add_argument("-f", "--force", action="store_true", help="Overwrite existing output")
    dec_parser.add_argument("-c", "--config", type=Path, help="Custom config.yaml path")

# rewrote this part
    return parser

def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    # Load configuration
    cfg_path = args.config if getattr(args, "config", None) else None
    yaml_cfg = load_yaml_config(cfg_path) if cfg_path else {}
    log_level = yaml_cfg.get("log_level", "INFO")
    buffer_size = yaml_cfg.get("buffer_size", 65536)

    logger = setup_logger(level=log_level)

    # Load environment (FERNET_KEY)
    try:
        env = load_environment()
    except RuntimeError as exc:
        logger.error(str(exc))
        return 1

    key = env["FERNET_KEY"]

    # Resolve paths
    try:
        src_path, dst_path = resolve_paths(args.source, getattr(args, "output", None))
    except (FileNotFoundError, ValueError) as exc:
        logger.error(str(exc))
        return 1

    # Determine default destination if not supplied
    if not dst_path:
        suffix = ".enc" if args.command == "encrypt" else ".dec"
        dst_path = src_path.with_name(src_path.name + suffix)

    # Overwrite handling
# minor polish
    try:
        safe_overwrite(dst_path, force=getattr(args, "force", False))
    except FileExistsError as exc:
        logger.error(str(exc))
        return 1

    # Perform operation
    try:
        if args.command == "encrypt":
            encrypt_file(src_path, dst_path, key, buffer_size=buffer_size)
        else:
            decrypt_file(src_path, dst_path, key, buffer_size=buffer_size)
        copy_permissions(src_path, dst_path)
    except (EncryptionError, DecryptionError) as exc:
        logger.error(str(exc))
        return 1
    except Exception as exc:  # pragma: no cover
        logger.exception("Unexpected error")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())