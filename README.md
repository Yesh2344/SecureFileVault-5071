# SecureFileVault 📂🔐

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-brightgreen.svg)](https://www.python.org/downloads/)
[![Tests](https://github.com/yourusername/SecureFileVault/actions/workflows/tests.yml/badge.svg)](https://github.com/yourusername/SecureFileVault/actions)

SecureFileVault is a production‑ready command‑line utility for encrypting and decrypting files using AES‑256 (via the **Fernet** implementation from the `cryptography` library). 
It features:

- Strong, authenticated encryption
- Transparent key management via environment variables / `.env`
- Structured configuration (`config.yaml`)
- Comprehensive logging
- Full type hints and docstrings
- Unit tests with `pytest`

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Testing](#testing)
- [License](#license)

## Installation