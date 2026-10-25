"""
download_references.py - Download open-access reference PDFs.

Importing this module has no side effects. Run it explicitly:

    python 05_Source_Code/generators/download_references.py

TLS verification is enabled; do not disable certificate checks for scholarly
downloads. Existing non-empty PDFs are skipped.
"""

from __future__ import annotations

import re
import ssl
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

from doc_paths import ADDITIONAL_REFERENCES_DIR, MAIN_REFERENCES_DIR

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
}

DIRECT_PDFS = [
    # Only cited works with a legally available PDF. Filenames match
    # reference_data.py so the manifest can verify every download.
    ("Akiba_2019_Optuna.pdf", "https://arxiv.org/pdf/1907.10902.pdf"),
    ("Bergstra_2011_TPE_Algorithms_for_Hyper-Parameter_Optimization.pdf", "https://proceedings.neurips.cc/paper_files/paper/2011/file/86e8f7ab32cfd12577bc2619bc635690-Paper.pdf"),
    ("Kingma_2014_Adam_Optimizer.pdf", "https://arxiv.org/pdf/1412.6980.pdf"),
    ("Srivastava_2014_Dropout.pdf", "https://jmlr.org/papers/volume15/srivastava14a/srivastava14a.pdf"),
    ("Hochreiter_1997_LSTM.pdf", "https://www.bioinf.jku.at/publications/older/2604.pdf"),
    ("Arlot_2010_Survey_Cross_Validation.pdf", "https://arxiv.org/pdf/0907.4728.pdf"),
    ("Willmott_2005_MAE_vs_RMSE.pdf", "https://www.int-res.com/articles/cr2005/30/c030p079.pdf"),
    ("Breuel_2015_Benchmarking_of_LSTM_Networks.pdf", "https://arxiv.org/pdf/1508.02774.pdf"),
    ("Greff_2017_LSTM_A_Search_Space_Odyssey.pdf", "https://arxiv.org/pdf/1503.04069.pdf"),
    ("Feurer_2019_Hyperparameter_Optimization_Book_Chapter.pdf", "https://www.automl.org/wp-content/uploads/2019/05/AutoML_Book_Chapter1.pdf"),
    ("Bouthillier_2021_Accounting_for_Variance_ML_Benchmarks.pdf", "https://arxiv.org/pdf/2103.03098.pdf"),
    ("Lim_Zohren_2021_Time_Series_Forecasting_with_Deep_Learning_Survey.pdf", "https://arxiv.org/pdf/2004.13408.pdf"),
    ("Gu_2020_Empirical_Asset_Pricing_via_Machine_Learning.pdf", "https://www.nber.org/system/files/working_papers/w25398/w25398.pdf"),
]

# Makridakis dkk. (2018) and Tashman (2000) are paywalled; they are cited
# metadata-only in reference_data.py. Books and online documentation are also
# not downloaded. Empirical papers are normally obtained from their journal
# pages; only the two automated OJS attempts below are configured.
OJS_LIST = [
    ("http://journal-isi.org/index.php/isi/article/view/1228", "Aswadi_2025_JISI_LSTM_Bitcoin_Ethereum.pdf"),
    ("https://journal.universitasbumigora.ac.id/index.php/matrik/article/view/3267", "Ula_2024_MATRIK_LSTM_RandomForest_Bitcoin.pdf"),
]


def is_valid_pdf(data: bytes) -> bool:
    return data[:5] == b"%PDF-" and len(data) > 10_000


def target_is_valid(path: Path) -> bool:
    if not path.exists() or path.stat().st_size <= 10_000:
        return False
    with path.open("rb") as handle:
        return handle.read(5) == b"%PDF-"


def download_direct_pdfs(output_dir: Path, context: ssl.SSLContext) -> None:
    for filename, url in DIRECT_PDFS:
        target = output_dir / filename
        if target_is_valid(target):
            print(f"[SKIP] {filename} ({target.stat().st_size} bytes)")
            continue
        try:
            request = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(request, context=context, timeout=45) as response:
                data = response.read()
            if not is_valid_pdf(data):
                print(f"[INVALID PDF] {filename}: content is not a PDF")
                continue
            target.write_bytes(data)
            print(f"[DOWNLOADED] {filename} ({len(data)} bytes)")
        except Exception as exc:  # network errors are expected for some sources
            print(f"[FAILED] {filename}: {exc}")


def download_ojs_pdf(view_url: str, output_dir: Path, out_filename: str, context: ssl.SSLContext) -> None:
    target = output_dir / out_filename
    if target_is_valid(target):
        print(f"[SKIP OJS] {out_filename} ({target.stat().st_size} bytes)")
        return

    try:
        request = urllib.request.Request(view_url, headers=HEADERS)
        with urllib.request.urlopen(request, context=context, timeout=30) as response:
            html = response.read().decode("utf-8", errors="ignore")

        matches = re.findall(
            r'href=["\']([^"\']*(?:download|article/view/[0-9]+/[0-9]+)[^"\']*)["\']',
            html,
        )
        candidates = [match for match in matches if "pdf" in match.lower() or "download" in match.lower()]
        candidates = candidates or matches
        if not candidates:
            print(f"[OJS NO PDF FOUND] {out_filename}")
            return

        link = candidates[0]
        if link.startswith("/"):
            parsed = urlparse(view_url)
            link = f"{parsed.scheme}://{parsed.netloc}{link}"

        request = urllib.request.Request(link, headers=HEADERS)
        with urllib.request.urlopen(request, context=context, timeout=35) as response:
            content = response.read()

        if is_valid_pdf(content):
            target.write_bytes(content)
            print(f"[DOWNLOADED OJS] {out_filename} ({len(content)} bytes)")
            return

        sub_html = content.decode("utf-8", errors="ignore")
        sub_matches = re.findall(r'href=["\']([^"\']*\.pdf[^"\']*)["\']', sub_html, re.I)
        sub_matches = sub_matches or re.findall(
            r'href=["\']([^"\']*download[^"\']*)["\']', sub_html, re.I
        )
        if not sub_matches:
            print(f"[OJS NO PDF FOUND] {out_filename}")
            return

        sub_link = sub_matches[0]
        if sub_link.startswith("/"):
            parsed = urlparse(view_url)
            sub_link = f"{parsed.scheme}://{parsed.netloc}{sub_link}"
        request = urllib.request.Request(sub_link, headers=HEADERS)
        with urllib.request.urlopen(request, context=context, timeout=35) as response:
            sub_data = response.read()
        if is_valid_pdf(sub_data):
            target.write_bytes(sub_data)
            print(f"[DOWNLOADED OJS NESTED] {out_filename} ({len(sub_data)} bytes)")
        else:
            print(f"[OJS NO PDF FOUND] {out_filename}")
    except Exception as exc:
        print(f"[FAILED OJS] {out_filename}: {exc}")


def main() -> int:
    output_dir = ADDITIONAL_REFERENCES_DIR
    output_dir.mkdir(parents=True, exist_ok=True)
    empirical_dir = MAIN_REFERENCES_DIR
    empirical_dir.mkdir(parents=True, exist_ok=True)
    context = ssl.create_default_context()

    download_direct_pdfs(output_dir, context)
    for url, filename in OJS_LIST:
        download_ojs_pdf(url, empirical_dir, filename, context)

    files = sorted(output_dir.glob("*.pdf"))
    print(f"\nTotal PDF di '{output_dir}': {len(files)}")
    for path in files:
        print(f"  * {path.name} ({path.stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
