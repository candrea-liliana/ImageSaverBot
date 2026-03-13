# 🖼️ Bing Image Scraper Bot

A lightweight Python bot that automatically scrapes images from Bing based on configurable search terms. Runs on a schedule via GitHub Actions — no server or local machine required.

---

## ✨ Features

- 🔍 Scrapes images from **Bing Images** — no API key needed
- 🔁 **Automated hourly runs** via GitHub Actions cron
- 🧹 **Duplicate detection** — skips already downloaded images using MD5 hashing
- 🖼️ **Filters low-quality images** — ignores images smaller than 100×100px
- 📦 **Artifact export** — images saved and downloadable from GitHub Actions for 30 days
- ⚙️ **Fully configurable** via GitHub Variables — no code changes needed

---

## 📁 Project Structure

```
├── .github/
│   └── workflows/
│       └── scraper.yml   # GitHub Actions workflow
├── main.py               # Scraper logic
├── requirements.txt      # Python dependencies
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### 1. Fork or clone this repository

```bash
git clone https://github.com/your-username/image-scraper-bot.git
cd image-scraper-bot
```

### 2. Configure GitHub Variables

Go to **Settings → Variables → Actions** and add:

| Variable | Description | Example |
|---|---|---|
| `SEARCH_TERMS` | Comma-separated search terms | `pizza,cats,nature` |
| `IMAGES_PER_SEARCH` | Number of images per term | `10` |

### 3. Run manually (first test)

Go to **Actions → Image Scraper Bot → Run workflow**.

### 4. Download images

After each run, go to **Actions → [run] → Artifacts** and download the zip.

---

## ⚙️ Local Development

```bash
pip install -r requirements.txt

SEARCH_TERMS=pizza,cats IMAGES_PER_SEARCH=5 python main.py
```

Images are saved to `scraped_images/<term>/`.

---

## 🕐 Schedule

The bot runs **every hour** automatically via GitHub Actions cron:

```yaml
- cron: '0 * * * *'
```

To change the frequency, edit `.github/workflows/scraper.yml`.

### Stopping the bot

- **Temporarily**: Actions → Image Scraper Bot → `...` → **Disable workflow**
- **Permanently**: delete `.github/workflows/scraper.yml`

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `requests` | HTTP requests |
| `beautifulsoup4` | HTML parsing |
| `pillow` | Image processing |

---

## ⚠️ Disclaimer

This project is intended for **personal and educational use only**. Scraping websites may violate their Terms of Service. Use responsibly.
