# 🕵️ Proxied

A multithreaded Python tool that scrapes fresh proxies from multiple sources and checks their validity across several protocols using different methods like `requests`, `socket`, `httpx`, and `websocket`. Results are logged in real-time with color-coded output and saved to output files per category.

---

## 💡 Features

- ✅ Scrape HTTP, HTTPS, SOCKS4/5 proxies from public APIs
- ⚙️ Check proxies with:
  - `requests` (HTTP)
  - `socket` (TCP)
  - `httpx` (high-performance client)
  - `websocket` (WS echo test)
- 🌈 Color-coded terminal logging
- ⏱ Shows response time (in ms)
- 💾 Saves working proxies instantly to `output/` folder
- 🧵 Threaded proxy checking (adjustable with `MAX_THREADS` and user input)
- 📂 Organized I/O via `input/` and `output/` folders

---
## 📁 Folder Structure
```
project/
├── input/                  # Input proxies go here
│   ├── http.txt
│   ├── https.txt
│   └── socks.txt
├── output/                 # Working proxies are saved here
│   ├── http_working.txt
│   └── https_working.txt
├── src/                    # Source code for scraping and checking
│   ├── checkers.py         # Proxy checking logic (requests, socket, etc.)
│   └── scraper.py          # Proxy scraping logic from APIs
├── install.sh              # Shell script to install dependencies (Linux/macOS)
├── proxied.py              # Main launcher script (menu: scrape/check/exit)
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation (this file)

```
---

## 🚀 Getting Started

1. Install Requirements

```bash
pip install -r requirements.txt
```
or run the install.sh file

2. Run the Script

```bash
python proxy_checker.py
```

# 📌 Notes

- Working proxies are appended to output/ files as soon as they are verified.

- SOCKS proxies and HTTPS proxies are harder to find in large volumes — not all sources support them consistently.

# ✨ Credits

- Proxies from:

    - ProxyScrape
    - Proxy List Download