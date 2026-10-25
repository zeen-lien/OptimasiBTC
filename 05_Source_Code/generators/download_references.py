import os
import re
import ssl
import urllib.request
from urllib.parse import urlparse

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
}

OUTPUT_DIR = os.path.join('referensi', 'referensi tambahan')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# List of direct PDF downloads
direct_pdfs = [
    # Seminal & Theoretical Foundation
    ('Akiba_2019_Optuna.pdf', 'https://arxiv.org/pdf/1907.10902.pdf'),
    ('Bergstra_2011_TPE_Algorithms_for_Hyper-Parameter_Optimization.pdf', 'https://proceedings.neurips.cc/paper_files/paper/2011/file/86e8f7ab32cfd12577bc2619bc635690-Paper.pdf'),
    ('Kingma_2014_Adam_Optimizer.pdf', 'https://arxiv.org/pdf/1412.6980.pdf'),
    ('Srivastava_2014_Dropout.pdf', 'https://jmlr.org/papers/volume15/srivastava14a/srivastava14a.pdf'),
    ('Hochreiter_1997_LSTM.pdf', 'https://www.bioinf.jku.at/publications/older/2604.pdf'),
    ('Arlot_2010_Survey_Cross_Validation.pdf', 'https://arxiv.org/pdf/0907.4728.pdf'),
    ('Willmott_2005_MAE_vs_RMSE.pdf', 'https://www.int-res.com/articles/cr2005/30/c030p079.pdf'),
    
    # Additional prominent open access papers
    ('Hyndman_2006_Another_Look_at_Measures_of_Forecast_Accuracy.pdf', 'https://robjhyndman.com/papers/mase.pdf'),
    ('Breuel_2015_Benchmarking_of_LSTM_Networks.pdf', 'https://arxiv.org/pdf/1508.02774.pdf'),
    ('Greff_2017_LSTM_A_Search_Space_Odyssey.pdf', 'https://arxiv.org/pdf/1503.04069.pdf'),
    ('Lipton_2015_Critical_Review_RNN.pdf', 'https://arxiv.org/pdf/1506.00019.pdf'),
    ('Feurer_2019_Hyperparameter_Optimization_Book_Chapter.pdf', 'https://arxiv.org/pdf/2007.03964.pdf'),
    ('Bouthillier_2020_Survey_Machine_Learning_Evaluation.pdf', 'https://arxiv.org/pdf/1905.07406.pdf'),
    ('Fawaz_2019_Deep_Learning_for_Time_Series_Classification_Review.pdf', 'https://arxiv.org/pdf/1809.04356.pdf'),
    ('Lim_Zohren_2021_Time_Series_Forecasting_with_Deep_Learning_Survey.pdf', 'https://arxiv.org/pdf/2004.13408.pdf')
]

for filename, url in direct_pdfs:
    target_path = os.path.join(OUTPUT_DIR, filename)
    if os.path.exists(target_path) and os.path.getsize(target_path) > 10000:
        print(f"[ALREADY EXISTS] {filename} ({os.path.getsize(target_path)} bytes)")
        continue
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
            data = resp.read()
            if data[:4] == b'%PDF' or len(data) > 10000:
                with open(target_path, 'wb') as f:
                    f.write(data)
                print(f"[DOWNLOADED] {filename} ({len(data)} bytes)")
            else:
                print(f"[INVALID CONTENT] {filename}: not a valid PDF")
    except Exception as e:
        print(f"[FAILED] {filename}: {e}")

# Function to resolve OJS article pages
def download_ojs_pdf(view_url, out_filename):
    target_path = os.path.join(OUTPUT_DIR, out_filename)
    if os.path.exists(target_path) and os.path.getsize(target_path) > 10000:
        print(f"[ALREADY EXISTS] {out_filename} ({os.path.getsize(target_path)} bytes)")
        return
    try:
        req = urllib.request.Request(view_url, headers=HEADERS)
        with urllib.request.urlopen(req, context=ctx, timeout=20) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
        
        # Look for download link
        matches = re.findall(r'href=["\']([^"\']*(?:download|article/view/[0-9]+/[0-9]+)[^"\']*)["\']', html)
        candidates = [m for m in matches if 'pdf' in m.lower() or 'download' in m.lower()]
        if not candidates:
            candidates = matches
        
        if candidates:
            link = candidates[0]
            if link.startswith('/'):
                parsed = urlparse(view_url)
                link = f"{parsed.scheme}://{parsed.netloc}{link}"
            
            # If it links to another viewer, fetch it
            req_c = urllib.request.Request(link, headers=HEADERS)
            with urllib.request.urlopen(req_c, context=ctx, timeout=25) as resp_c:
                content = resp_c.read()
                if content[:4] == b'%PDF':
                    with open(target_path, 'wb') as f:
                        f.write(content)
                    print(f"[DOWNLOADED OJS] {out_filename} ({len(content)} bytes)")
                    return
                else:
                    # Might be an intermediate html viewer page
                    sub_html = content.decode('utf-8', errors='ignore')
                    sub_matches = re.findall(r'href=["\']([^"\']*\.pdf[^"\']*)["\']', sub_html, re.I)
                    if not sub_matches:
                        sub_matches = re.findall(r'href=["\']([^"\']*download[^"\']*)["\']', sub_html, re.I)
                    if sub_matches:
                        sub_link = sub_matches[0]
                        if sub_link.startswith('/'):
                            parsed = urlparse(view_url)
                            sub_link = f"{parsed.scheme}://{parsed.netloc}{sub_link}"
                        req_sub = urllib.request.Request(sub_link, headers=HEADERS)
                        with urllib.request.urlopen(req_sub, context=ctx, timeout=25) as resp_sub:
                            sub_data = resp_sub.read()
                            if sub_data[:4] == b'%PDF':
                                with open(target_path, 'wb') as f:
                                    f.write(sub_data)
                                print(f"[DOWNLOADED OJS NESTED] {out_filename} ({len(sub_data)} bytes)")
                                return
        print(f"[OJS NO PDF FOUND] {out_filename}")
    except Exception as e:
        print(f"[FAILED OJS] {out_filename}: {e}")

# Try OJS Indonesian journals
ojs_list = [
    ('https://jurnal.atmaluhur.ac.id/index.php/sisfokom/article/view/1554', 'Gunarto_2023_Sisfokom_Crypto_RNN_LSTM.pdf'),
    ('https://jurnal.iaii.or.id/index.php/RESTI/article/view/3630', 'Rizkilloh_2022_RESTI_LSTM_Cryptocurrency.pdf'),
    ('http://journal-isi.org/index.php/isi/article/view/1228', 'Aswadi_2025_JISI_LSTM_Bitcoin_Ethereum.pdf'),
    ('https://journal.universitasbumigora.ac.id/index.php/matrik/article/view/3267', 'Ula_2024_MATRIK_LSTM_RandomForest_Bitcoin.pdf')
]

for url, fname in ojs_list:
    download_ojs_pdf(url, fname)

print("\n--- Summary of referensi tambahan folder ---")
files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith('.pdf')]
print(f"Total PDFs in 'referensi tambahan': {len(files)}")
for f in sorted(files):
    size_kb = os.path.getsize(os.path.join(OUTPUT_DIR, f)) // 1024
    print(f"  * {f} ({size_kb} KB)")
