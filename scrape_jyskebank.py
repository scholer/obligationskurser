"""

The page is protected by Cloudflare bot prevention.

Use one of these packages:

- https://pypi.org/project/cloudscraper/  (most up to date)
- https://pypi.org/project/cfscrape/      (last relese 2020)

"""
from pathlib import Path
import time
import random
from datetime import datetime

import cloudscraper


output_folder = "data/jyskebank_erhverv_kurser/scrape_raw"
scrape_url = "https://www.jyskebank.dk/erhverv/ejendomsfinansiering/kurser"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Wait period config:
minute = 60
hour = 60 * minute
day = 24 * hour
sleep_duration_base = 1*hour
sleep_random_extra_max = 1*hour
sleep_weekend_extra_min = 4*hour
sleep_weekend_extra_max = 12*hour
sleep_offhour_extra_min = 1*hour
sleep_offhour_extra_max = 6*hour


def main():
    """ """
    Path(output_folder).mkdir(exist_ok=True, parents=True)
    scraper = cloudscraper.create_scraper()
    while True:
        res = scraper.get(scrape_url, headers={"User-Agent": user_agent})
        txt = res.text
        fname = f"{datetime.now():%Y%m%d-%H%M%S}_{res.status_code}.html"
        fpath = Path(output_folder) / fname
        print(f"Writing {len(txt)} chars to file: {fpath}")
        Path(fpath).write_text(txt)
        loop_sleep_duration = sleep_duration_base + random.randint(0, sleep_random_extra_max)
        if 4 < datetime.now().weekday():
            loop_sleep_duration += random.randint(sleep_weekend_extra_min, sleep_weekend_extra_max)
        if 16 < datetime.now().hour:
            loop_sleep_duration += random.randint(sleep_offhour_extra_min, sleep_offhour_extra_max)
        print(f" - sleeping for {loop_sleep_duration/hour:.01f} hours...")
        try:
            time.sleep(loop_sleep_duration)
        except KeyboardInterrupt:
            print("Exiting...")
            return


if __name__ == "__main__":
    main()
