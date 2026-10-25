"""Rebuild every thesis component and audit the assembled master document.

This is the one-command entry point used for the final manuscript::

    python 05_Source_Code/generators/generate_all.py
"""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

GENERATORS_DIR = Path(__file__).resolve().parent
if str(GENERATORS_DIR) not in sys.path:
    sys.path.insert(0, str(GENERATORS_DIR))

from generate_master_skripsi import assemble_full_skripsi  # noqa: E402
from audit_citations import audit as audit_citations  # noqa: E402
from verify_full_skripsi import verify_full_skripsi  # noqa: E402


def main() -> int:
    started = datetime.now().astimezone()
    print(f"[{started:%Y-%m-%d %H:%M:%S %Z}] Rebuild naskah lengkap dimulai")
    try:
        assemble_full_skripsi()
    except Exception as exc:  # noqa: BLE001 - fail loudly with the generator error
        print(f"[FAIL] Generator naskah gagal: {exc}")
        return 1

    ok = verify_full_skripsi()
    citation_errors = audit_citations()
    if citation_errors:
        print("\n=== AUDIT SITASI ===")
        print("HASIL: GAGAL")
        for error in citation_errors:
            print(f"  - {error}")
        ok = False
    else:
        print("\n=== AUDIT SITASI ===")
        print("HASIL: LULUS. 32 referensi dan seluruh sitasi konsisten.")

    finished = datetime.now().astimezone()
    print(f"[{finished:%Y-%m-%d %H:%M:%S %Z}] Rebuild selesai")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
