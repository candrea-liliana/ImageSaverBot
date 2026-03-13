import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import os
import re
import json
import hashlib

# ===== CONFIG =====

SEARCH_TERMS      = os.environ.get("SEARCH_TERMS", "pizza,cats,nature").split(",")
IMAGES_PER_SEARCH = int(os.environ.get("IMAGES_PER_SEARCH", "10"))
OUTPUT_DIR        = os.environ.get("OUTPUT_DIR", "scraped_images")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

# ===== HELPERS =====

def clean_filename(name):
    return re.sub(r'[<>:"/\\|?!*\n\r]', '', name).strip()[:80]

def image_hash(content):
    return hashlib.md5(content).hexdigest()

def load_seen_hashes(folder):
    path = os.path.join(folder, ".seen_hashes")
    if os.path.exists(path):
        with open(path) as f:
            return set(line.strip() for line in f if line.strip())
    return set()

def save_hash(folder, h):
    with open(os.path.join(folder, ".seen_hashes"), "a") as f:
        f.write(h + "\n")

# ===== BING SCRAPER =====

def get_bing_urls(search):
    r = requests.get(
        "https://www.bing.com/images/search",
        params={"q": search, "form": "HDRSC2"},
        headers=HEADERS,
        timeout=10
    )
    soup = BeautifulSoup(r.text, "html.parser")
    urls = []
    for item in soup.find_all("a", {"class": "iusc"}):
        try:
            m = json.loads(item["m"])
            urls.append((m["murl"], m.get("t", "image")))
        except:
            continue
    return urls

# ===== DOWNLOAD =====

def download_images(urls, search):
    folder = os.path.join(OUTPUT_DIR, search.strip().replace(" ", "_"))
    os.makedirs(folder, exist_ok=True)
    seen = load_seen_hashes(folder)
    saved = 0

    for i, (url, title) in enumerate(urls):
        if saved >= IMAGES_PER_SEARCH:
            break
        try:
            r = requests.get(url, headers=HEADERS, timeout=8)
            r.raise_for_status()

            h = image_hash(r.content)
            if h in seen:
                print(f"  ~ Jump duplicate")
                continue

            img = Image.open(BytesIO(r.content)).convert("RGB")
            if img.width < 100 or img.height < 100:
                continue

            name = clean_filename(title.replace(" ", "_")) or f"image_{i}"
            filepath = os.path.join(folder, f"{name}.jpg")
            if os.path.exists(filepath):
                filepath = os.path.join(folder, f"{name}_{i}.jpg")

            img.save(filepath, "JPEG", quality=90)
            seen.add(h)
            save_hash(folder, h)
            saved += 1
            print(f"  ✓ {os.path.basename(filepath)}")

        except Exception as e:
            print(f"  ✗ {e}")
            continue

    return saved

# ===== MAIN =====

def run():
    total = 0
    for term in SEARCH_TERMS:
        term = term.strip()
        print(f"\n[BING] Search for: '{term}'")
        urls = get_bing_urls(term)
        print(f"  Found: {len(urls)} URLs")
        saved = download_images(urls, term)
        print(f"  Save: {saved} images")
        total += saved
    print(f"\n✓ Total: {total} saved images '{OUTPUT_DIR}/'")

if __name__ == "__main__":
    run()