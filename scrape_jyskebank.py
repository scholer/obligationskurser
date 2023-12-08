"""

The page is protected by Cloudflare bot prevention.

Use one of these packages:

- https://pypi.org/project/cloudscraper/  (most up to date)
- https://pypi.org/project/cfscrape/      (last relese 2020)

"""
from pathlib import Path
import requests
import time
from datetime import datetime

import cloudscraper


scrape_url = "https://www.jyskebank.dk/erhverv/ejendomsfinansiering/kurser"
sleep_duration = 60*60  # 1 hour.

user_agents = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

output_folder = "data/jyskebank_erhverv_kurser/scrape_raw"


def main():
    """ """

    while True:
        Path(output_folder).mkdir(exist_ok=True, parents=True)
        scraper = cloudscraper.create_scraper()
        res = scraper.get(scrape_url, headers={"User-Agent": user_agents})
        txt = res.text
        fname = f"{datetime.now():%Y%m%d-%H%M%S}_{res.status_code}.html"
        fpath = Path(output_folder) / fname
        print(f"Writing {len(txt)} chars to file: {fpath}")
        Path(fpath).write_text(txt)
        time.sleep(sleep_duration)


if __name__ == "__main__":
    main()
