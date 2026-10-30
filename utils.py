"""
Utility helpers for file handling and path validation.
"""

import shutil
from pathlib import Path
from typing import Tuple

def resolve_paths(source: str, output: str | None) -> Tuple[Path, Path]:
    """
    Resolve and validate source and destination paths.

    Args:
        source: Path to the input file (string).
        output: Optional path to the output file. If ``None``, a default
            name is derived (``.enc`` for encryption, ``.dec`` for decryption).

    Returns:
        Tuple of (source_path, destination_path).

    Raises:
        FileNotFoundError: If the source does not exist.
        ValueError: If the destination already exists and overwriting is not allowed.
    """
    src_path = Path(source).expanduser().resolve()
    if not src_path.is_file():
        raise FileNotFoundError(f"Source file not found: {src_path}")

    dst_path = Path(output).expanduser().resolve() if output else None
    return src_path, dst_path

def safe_overwrite(dst: Path, force: bool = False) -> None:
    """
    Ensure that ``dst`` can be written.

    Args:
        dst: Destination path.
        force: If ``True`` existing files are overwritten.

    Raises:
        FileExistsError: If the file exists and ``force`` is ``False``.
    """
    if dst.exists():
        if force:
            dst.unlink()
        else:
            raise FileExistsError(f"Destination already exists: {dst}")

def copy_permissions(src: Path, dst: Path) -> None:
    """
    Replicate the file permission bits from ``src`` to ``dst``.
    """
    shutil.copymode(src, dst)