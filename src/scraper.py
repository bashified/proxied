import os
import requests
import time

INPUT_DIR = "input"
OUTPUT_DIR = "output"

def getp(loggerfunction):
    sources = {
        "http.txt": [
            "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=5000&country=all",
            "https://www.proxy-list.download/api/v1/get?type=http"
        ],
        "https.txt": [
            "https://api.proxyscrape.com/v2/?request=getproxies&protocol=https&timeout=5000&country=all",
            "https://www.proxy-list.download/api/v1/get?type=https"
        ],
        "socks.txt": [
            "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=5000&country=all",
            "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=5000&country=all",
            "https://www.proxy-list.download/api/v1/get?type=socks4",
            "https://www.proxy-list.download/api/v1/get?type=socks5"
        ]
    }

    os.makedirs(INPUT_DIR, exist_ok=True)

    for filename, urls in sources.items():
        all_proxies = set()
        for url in urls:
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    proxies = response.text.strip().split("\n")
                    all_proxies.update([p.strip() for p in proxies if p.strip()])
                    loggerfunction("info", f"Fetched {len(proxies)} proxies from {url}")
                else:
                    loggerfunction("invalid", f"Failed to fetch from {url} : {response.status_code}")
                time.sleep(2)
            except Exception as e:
                loggerfunction("invalid", f"Error fetching from {url}: {e}")

        output_path = os.path.join(INPUT_DIR, filename)
        with open(output_path, "w") as f:
            f.write("\n".join(sorted(all_proxies)))

        loggerfunction("info", f"Saved {len(all_proxies)} proxies to {output_path}")
