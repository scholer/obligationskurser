"""

# Selenium-based scraper

## Installation and requirements, package dependencies:


1. Create a virtual environment.
2. Install `cloudscraper` package.
3. Download this using one of the following:
   - `git clone git@github.com:scholer/obligationskurser.git`


## Usage:

Just run `scrape_jyskebank.py` in your shell ("Command prompt", "Terminal", "bash", "zsh", "fish", etc.)

```shell
python scrape_jyskebank.py
```


## Further info

To fix this HTTP 403 Error message: "The page is protected by Cloudflare bot prevention."

Use one of these packages:

- https://pypi.org/project/cloudscraper/  (most up to date, used here)
- https://pypi.org/project/cfscrape/      (last relese 2020)


"""
from pathlib import Path
import time
import random
from datetime import datetime, timedelta

# import cloudscraper
import selenium.webdriver


output_folder = "data/jyskebank_erhverv_kurser/scrape_selenium"
scrape_url = "https://www.jyskebank.dk/erhverv/ejendomsfinansiering/kurser"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Wait period config:
minute = 60
hour = 60 * minute
day = 24 * hour
sleep_duration_base = hour//4
sleep_random_extra_max = hour//2
sleep_weekend_extra_min = 4*hour
sleep_weekend_extra_max = 12*hour
sleep_offhour_extra_min = 1*hour
sleep_offhour_extra_max = 6*hour


def main():
    """ """
    Path(output_folder).mkdir(exist_ok=True, parents=True)
    driver = selenium.webdriver.Chrome()
    while True:
        try:
            print(f"\n{datetime.now():%Y%m%d-%H%M%S} Fetching {scrape_url}")
            driver.get(scrape_url)
            # OBS: Selenium webdriver does not support status codes:
            # https://github.com/seleniumhq/selenium-google-code-issue-archive/issues/141
            time.sleep(6)
            txt = driver.page_source
            fname = f"{datetime.now():%Y%m%d-%H%M%S}_selenium.html"
            fpath = Path(output_folder) / fname
            print(f" - Writing {len(txt)} chars to file: {fpath} ", end="")
            Path(fpath).write_text(txt, encoding="utf8")
            print("OK.")

            # time.sleep is paused during hybernation.
            # Instead, calcualte the datetime of the next acquisition, and then keep sleeping in smaller loops until then.
            loop_sleep_duration = sleep_duration_base + random.randint(0, sleep_random_extra_max)
            # Add additional sleep time over the weekend and during off-hours (after 4pm).
            if 4 < datetime.now().weekday():
                loop_sleep_duration += random.randint(sleep_weekend_extra_min, sleep_weekend_extra_max)
            if 16 < datetime.now().hour:
                loop_sleep_duration += random.randint(sleep_offhour_extra_min, sleep_offhour_extra_max)
            next_acq_time = datetime.now() + timedelta(seconds=loop_sleep_duration)
            print(f" - sleeping for {loop_sleep_duration/hour:.01f} hours until {next_acq_time:%H:%M:%S}...")
            while datetime.now() < next_acq_time:
                time.sleep(61)
        except KeyboardInterrupt:
            print("Exiting...")
            break
        except Exception as exc:
            print("Exception:", exc)
            print("Looping in 15 seconds...")
            time.sleep(15)
    driver.quit()
    time.sleep(2)


if __name__ == "__main__":
    main()
