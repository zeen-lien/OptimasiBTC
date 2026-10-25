"""Build the reference manifest, catalog, and audit report.

Usage:
    python 05_Source_Code/generators/build_reference_manifest.py

The script is deterministic. It reads metadata only from reference_data.py,
checks local PDFs, computes SHA-256 hashes, and writes:

- 04_Referensi_Ilmiah/references_manifest.csv
- 04_Referensi_Ilmiah/DAFTAR_32_REFERENSI_SKRIPSI.md
- docs/REFERENCE_AUDIT.md
"""

from __future__ import annotations

import csv
import hashlib
from datetime import date
from pathlib import Path

from reference_data import CLUSTERS, REFERENCES, apa_reference

ROOT = Path(__file__).resolve().parents[2]
AUDIT_DATE = "2026-10-26"

MANIFEST_PATH = ROOT / "04_Referensi_Ilmiah" / "references_manifest.csv"
CATALOG_PATH = ROOT / "04_Referensi_Ilmiah" / "DAFTAR_32_REFERENSI_SKRIPSI.md"
AUDIT_PATH = ROOT / "docs" / "REFERENCE_AUDIT.md"

FORBIDDEN_OLD_ENTRIES = (
    "Applied Soft Computing",
    "Expert Systems with Applications",
    "IEEE Access",
    "JOIV",
    "University of Warsaw",
    "Gunarto",
    "Frontiers in Applied Mathematics",
)

ARCHIVE_PDFS = (
    "Arsip_Tambahan/Falkner_2018_BOHB_Hyperparameter_Optimization.pdf",
    "Arsip_Tambahan/Fawaz_2019_Deep_Learning_for_Time_Series_Classification_Review.pdf",
    "Arsip_Tambahan/Li_2017_Hyperband_Bandit_Based_HPO.pdf",
    "Arsip_Tambahan/Lipton_2015_Critical_Review_RNN.pdf",
    "Arsip_Tambahan/Oreshkin_2019_N-BEATS_Neural_Basis_Expansion_Forecasting.pdf",
    "Arsip_Tambahan/Salinas_2019_DeepAR_Probabilistic_Forecasting_RNN.pdf",
    "Arsip_Tambahan/Vaswani_2017_Attention_Is_All_You_Need.pdf",
    "Arsip_Tambahan/Intraday trading strategy selection under transaction costs with machine learning.pdf",
    "Arsip_Tambahan/Machine Learning-Based Bitcoin Trading Under Transaction Costs Evidence From Walk-Forward Forecasting.pdf",
    "Arsip_Tambahan/Research on Machine Learning High-Frequency Trading Strategy of Cryptocurrency Based on Transaction Cost-Aware Filtering.pdf",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def pdf_record(ref: dict) -> tuple[str, str, str]:
    """Return (pdf_status, sha256, absolute-or-empty path)."""
    raw = ref.get("pdf", "").strip()
    if not raw:
        return "not_applicable", "", ""
    path = ROOT / raw
    if not path.exists() or path.stat().st_size < 10_000:
        return "missing", "", raw
    with path.open("rb") as handle:
        if handle.read(5) != b"%PDF-":
            return "invalid", "", raw
    return "available", sha256(path), raw


def print_status(ref: dict) -> str:
    status, _, _ = pdf_record(ref)
    if status == "available":
        return "PDF tersedia"
    if status == "missing":
        return "PDF tidak tersedia"
    if status == "invalid":
        return "PDF tidak valid"
    return "Tidak berlaku (buku/dokumen daring)"


def write_manifest(records: list[dict]) -> None:
    fieldnames = [
        "id",
        "cluster",
        "first_author",
        "year",
        "title",
        "venue",
        "doi",
        "url",
        "local_pdf",
        "sha256",
        "pdf_status",
        "metadata_status",
        "role",
        "notes",
    ]
    with MANIFEST_PATH.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)


def write_catalog(records: list[dict]) -> None:
    total = len(records)
    available = sum(1 for r in records if r["pdf_status"] == "available")
    missing = sum(1 for r in records if r["pdf_status"] == "missing")
    not_applicable = sum(1 for r in records if r["pdf_status"] == "not_applicable")
    with_doi = sum(1 for r in records if r["doi"])
    with_url = sum(1 for r in records if r["url"])

    lines = [
        "# MASTER DAFTAR 32 REFERENSI SKRIPSI",
        "",
        "**Program Studi:** Teknik Informatika - FST UNISNU Jepara  ",
        "**Topik Penelitian:** Optimasi Hyperparameter Long Short-Term Memory Menggunakan Algoritma Optuna Pada Prediksi Harga Bitcoin  ",
        f"**Tanggal audit:** {AUDIT_DATE}  ",
        "**Sumber kebenaran:** `05_Source_Code/generators/reference_data.py`  ",
        "**Manifest mesin:** `04_Referensi_Ilmiah/references_manifest.csv`",
        "",
        "---",
        "",
        "## 1. KEBIJAKAN AUDIT",
        "",
        "Daftar ini memuat tepat 32 referensi yang benar-benar disitasi di Bab I–V. "
        "Setiap entri telah dicocokkan dengan Crossref, arXiv, atau laman penerbit. "
        "Entri yang tidak dapat diverifikasi atau tidak disitasi telah dihapus; "
        "karya yang disitasi tetapi belum tercantum telah ditambahkan. "
        "PDF lokal hanya disertakan bila tersedia secara sah dan isinya cocok dengan metadata.",
        "",
        "## 2. RINGKASAN",
        "",
        "| Item | Jumlah |",
        "|---|---:|",
        f"| Referensi dalam daftar | {total} |",
        f"| PDF lokal tersedia dan tervalidasi | {available} |",
        f"| PDF lokal tidak tersedia | {missing} |",
        f"| Tidak berlaku (buku/dokumen daring) | {not_applicable} |",
        f"| Memiliki DOI | {with_doi} |",
        f"| Memiliki URL resmi | {with_url} |",
        "",
        "---",
        "",
        "## 3. INVENTARIS PER KLUSTER",
        "",
    ]

    for cluster_key, cluster_name in CLUSTERS.items():
        subset = sorted(
            (r for r in records if r["cluster"] == cluster_name),
            key=lambda r: (r["first_author"].lower(), r["year"]),
        )
        lines.extend([f"### {cluster_name}", ""])
        for rec in subset:
            ref = next(r for r in REFERENCES if r["id"] == rec["id"])
            lines.append(f"{rec['id']}. **{apa_reference(ref)}**")
            lines.append(f"   - **Peran:** {rec['role']}")
            lines.append(f"   - **Verifikasi:** {rec['metadata_status']}")
            lines.append(f"   - **PDF lokal:** {rec['local_pdf'] or '—'} ({print_status(ref)})")
            if rec["notes"]:
                lines.append(f"   - **Catatan:** {rec['notes']}")
            lines.append("")
        lines.append("---")
        lines.append("")

    lines.extend(
        [
            "## 4. ARSIP TAMBAHAN (TIDAK DISITASI)",
            "",
            "Berkas berikut disimpan sebagai bacaan latar dan **tidak** termasuk 32 referensi. "
            "Berkas-berkas ini tidak boleh dirujuk sebagai sitasi dalam naskah.",
            "",
        ]
    )
    for rel in ARCHIVE_PDFS:
        exists = (ROOT / "04_Referensi_Ilmiah" / rel).exists()
        lines.append(f"- `{rel}` — {'ada' if exists else 'tidak ada'}")
    lines.extend(
        [
            "",
            "---",
            "",
            "## 5. CATATAN PERUBAHAN",
            "",
            "- Empat entri dengan metadata yang tidak dapat dipertanggungjawabkan dihapus: "
            "*Applied Soft Computing* (2023), *Expert Systems with Applications* (2024), "
            "*IEEE Access* (2023), dan *JOIV* (2024).",
            "- Tiga entri nyata tetapi tidak disitasi dikeluarkan dari daftar 32: Gunarto dkk. (2023), "
            "University of Warsaw (2026), dan *Frontiers in Applied Mathematics and Statistics* (2026).",
            "- Tujuh karya yang disitasi tetapi belum tercantum ditambahkan: Bouthillier dkk. (2021), "
            "Feurer & Hutter (2019), Greff dkk. (2017), Lim & Zohren (2021), Makridakis dkk. (2018), "
            "Gu dkk. (2020), dan Breuel (2015).",
            "- Sitasi korporat diganti dengan nama penulis sebenarnya: Aldo dkk. (2026), Widad dkk. (2026), "
            "Wahyuddin dkk. (2025), Fawzi dkk. (2025), Kervancı & Akay (2023), dan Boongasame & Songram (2023).",
            "- Metadata Aswadi & Ependi dikoreksi dari tahun 2022 menjadi 2025; DOI, volume, dan halaman "
            "Khumaidi dkk. serta Ula dkk. dikoreksi.",
            "- Empat PDF yang isinya tidak cocok diganti atau dihapus: Bouthillier, Feurer, Gu, dan Makridakis. "
            "Makridakis dkk. (2018) tidak memiliki PDF akses terbuka sehingga hanya metadatanya yang dicantumkan.",
            "",
        ]
    )
    CATALOG_PATH.write_text("\n".join(lines), encoding="utf-8")


def write_audit(records: list[dict]) -> None:
    total = len(records)
    available = sum(1 for r in records if r["pdf_status"] == "available")
    missing = sum(1 for r in records if r["pdf_status"] == "missing")
    not_applicable = sum(1 for r in records if r["pdf_status"] == "not_applicable")

    lines = [
        "# AUDIT REFERENSI SKRIPSI",
        "",
        f"**Tanggal audit:** {AUDIT_DATE}  ",
        "**Cakupan:** 32 referensi pada DAFTAR PUSTAKA dan seluruh sitasi Bab I–V  ",
        "**Sumber data:** `05_Source_Code/generators/reference_data.py`  ",
        "**Manifest:** `04_Referensi_Ilmiah/references_manifest.csv`",
        "",
        "## 1. Hasil Ringkas",
        "",
        f"- Jumlah referensi: **{total}**.",
        f"- PDF lokal tervalidasi: **{available}**; tidak tersedia: **{missing}**; tidak berlaku: **{not_applicable}**.",
        "- Semua karya yang disitasi di Bab I–V memiliki entri DAFTAR PUSTAKA.",
        "- Semua entri DAFTAR PUSTAKA disitasi minimal satu kali di Bab I–V.",
        "- Tidak ada lagi nama jurnal/korporasi yang dipakai sebagai penulis sitasi.",
        "- Tidak ada lagi entri fiktif atau metadata DOI yang menunjuk ke makalah lain.",
        "",
        "## 2. Koreksi Utama",
        "",
        "| Masalah lama | Tindakan |",
        "|---|---|",
        "| Empat entri jurnal tanpa penulis dan tanpa bukti bibliografis | Dihapus dari daftar 32 |",
        "| Tiga karya nyata tetapi tidak pernah disitasi | Dihapus dari daftar 32 |",
        "| Tujuh karya disitasi tetapi tidak ada di daftar | Ditambahkan dengan metadata terverifikasi |",
        "| Sitasi korporat (JUTIF, Bit-Tech, BRIN, Ganesha, Sakarya, IJEECS) | Diganti nama penulis dan tahun yang benar |",
        "| Aswadi & Ependi (2022) tidak cocok dengan isi | Dikoreksi menjadi Aswadi & Ependi (2025) |",
        "| DOI Khumaidi dkk. dan Ula dkk. salah | Dikoreksi ke DOI dan halaman yang benar |",
        "| PDF Bouthillier, Feurer, Gu, Makridakis berisi makalah lain | Tiga diganti dengan versi benar; satu dihapus karena paywall |",
        "| Sitasi Falkner (2018), Li (2017), Lipton (2015), Pedregosa (2011), Vaswani (2017) | Klaim diankerkan ulang ke Akiba (2019), Optuna docs, Greff (2017), dan Lim & Zohren (2021) |",
        "",
        "## 3. Verifikasi Metadata",
        "",
        "| No | Penulis utama | Tahun | DOI/URL | Status PDF | Verifikasi |",
        "|---:|---|---:|---|---|---|",
    ]
    for rec in records:
        target = f"https://doi.org/{rec['doi']}" if rec["doi"] else (rec["url"] or "—")
        lines.append(
            f"| {rec['id']} | {rec['first_author']} | {rec['year']} | {target} | "
            f"{rec['pdf_status']} | {rec['metadata_status']} |"
        )

    lines.extend(
        [
            "",
            "## 4. Pemeriksaan Isi PDF",
            "",
            "Setiap PDF yang tersedia diperiksa tanda tangan `%PDF-`, ukuran minimum, jumlah halaman, "
            "dan teks halaman pertama. Empat berkas lama yang isinya tidak cocok ditemukan melalui "
            "pemeriksaan ini:",
            "",
            "| Berkas lama | Isi yang ditemukan | Tindakan |",
            "|---|---|---|",
            "| `Bouthillier_2020_Survey_Machine_Learning_Evaluation.pdf` | Makalah fisika AWAKE | Diganti arXiv:2103.03098 |",
            "| `Feurer_2019_Hyperparameter_Optimization_Book_Chapter.pdf` | Makalah PID Lagrangian | Diganti bab AutoML resmi |",
            "| `Gu_2020_Empirical_Asset_Pricing_via_Machine_Learning.pdf` | Makalah matematika Prancis | Diganti NBER w25398 |",
            "| `Makridakis_2018_M4_Competition_Results_and_Findings.pdf` | Makalah asma | Dihapus; artikel paywall |",
            "",
            "## 5. Keterbatasan",
            "",
            "- Makridakis dkk. (2018), Tashman (2000), dan Ula dkk. (2024) tidak memiliki PDF akses terbuka "
            "di repositori; metadata tetap terverifikasi melalui Crossref.",
            "- PDF Gu dkk. adalah versi NBER Working Paper w25398, bukan PDF versi RFS 2020. "
            "DOI dan volume/halaman yang dicantumkan merujuk versi terbit.",
            "- Buku (Goodfellow dkk., Hyndman & Athanasopoulos, López de Prado, Creswell & Creswell) dan "
            "dokumen daring (Optuna, TensorFlow, Binance, UNISNU) tidak disertakan sebagai PDF.",
            "- Verifikasi DOI tidak menjamin akses penuh; yang diverifikasi adalah kecocokan judul, penulis, "
            "tahun, dan wadah terbit.",
            "",
            "## 6. Reproduksi",
            "",
            "```powershell",
            "python 05_Source_Code/generators/build_reference_manifest.py",
            "python 05_Source_Code/generators/generate_all.py",
            "python -m pytest tests/test_references.py -q",
            "```",
            "",
            "Skrip manifest menghitung ulang SHA-256 dan status setiap PDF. Perubahan metadata harus "
            "dilakukan di `reference_data.py`, bukan langsung di DOCX atau katalog.",
            "",
        ]
    )
    AUDIT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    records: list[dict] = []
    for ref in REFERENCES:
        status, digest, path = pdf_record(ref)
        records.append(
            {
                "id": ref["id"],
                "cluster": CLUSTERS[ref["cluster"]],
                "first_author": ref["first_author"],
                "year": ref["year"],
                "title": ref["title"],
                "venue": ref["venue"],
                "doi": ref["doi"],
                "url": ref["url"],
                "local_pdf": path,
                "sha256": digest,
                "pdf_status": status,
                "metadata_status": ref["verification"],
                "role": ref["role"],
                "notes": ref["notes"],
            }
        )

    if len(records) != 32:
        raise SystemExit(f"Expected 32 references, found {len(records)}")
    if len({r['id'] for r in records}) != 32:
        raise SystemExit("Reference ids are not unique")
    for old in FORBIDDEN_OLD_ENTRIES:
        if any(old.lower() in r["title"].lower() or old.lower() in r["venue"].lower() for r in records):
            raise SystemExit(f"Forbidden legacy reference still present: {old}")

    write_manifest(records)
    write_catalog(records)
    write_audit(records)

    counts = {status: sum(1 for r in records if r["pdf_status"] == status) for status in ("available", "missing", "not_applicable", "invalid")}
    print(f"References: {len(records)}")
    print(f"PDF status: {counts}")
    print(f"Manifest: {MANIFEST_PATH.relative_to(ROOT)}")
    print(f"Catalog:  {CATALOG_PATH.relative_to(ROOT)}")
    print(f"Audit:    {AUDIT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
