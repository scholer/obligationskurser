"""
Module for extracting table data from raw HTML pages to Parquet/CSV files.

Usage:

>>> python obligationskurser/jyskebank/extract_table_data_from_raw_html.py



Libraries for parsing html:

- BeautifulSoup
- lxml
- Parsel
  - Based on lxml and cssselect, spun out from Scrapy project.
- Html5lib
- Requests-HTML
  - Javascript support.
- Pyquery
- Pyppeteer
  - Browser automation tool with built-in parsing.

Refs:

- https://www.zenrows.com/alternative/beautifulsoup
- https://www.octoparse.com/blog/best-alternative-to-beautiful-soup-in-web-scraping


"""

from pathlib import Path
import io

from bs4 import BeautifulSoup
import pandas as pd


def get_html_table_elem(html_str):
    div_class = 'component-control id-Z7_2GCC04LUADMC80QC3QGF8M16F7'
    soup = BeautifulSoup(html_str, features="html.parser")
    type(soup.find(class_=div_class))  # bs4.element.Tag
    div_elem = soup.find(class_=div_class)
    assert div_elem is not None
    table_elem = div_elem.find("table")
    # table_elem = soup.find("table")
    return table_elem


def extract_df_from_html_file(html_file):
    """ """
    html_str = Path(html_file).read_text(encoding="utf8")
    if not html_str:
        print(f"HTML file {html_file} is empty!")
        raise ValueError(f"HTML file {html_file} is empty!")
    table_elem = get_html_table_elem(html_str)
    assert table_elem is not None
    assert not isinstance(table_elem, int)
    # print(table_elem.decode())
    # Returns list of Pandas DataFrames. Depends on lxml
    dfs = pd.read_html(io.StringIO(table_elem.decode()), decimal=",", thousands=".")  # type: ignore
    return dfs[0]


def extract_and_save(html_file, output=(("parquet", "{html_dir}/../bs_pd_parquet/"),)):
    """ 
    To save in multiple output formats, use:
    ```python
    extract_and_save(
        html_file, 
        output=(
            ("parquet", "{html_dir}/../bs_pd_parquet/"),
            ("csv", "{html_dir}/../bs_pd_csv/"),
        )
    )
    ```
    """
    if len(output) == 1 and isinstance(output, tuple) and isinstance(output[0], str):
        output = [output]
    html_fpath = Path(html_file)
    html_dir = html_fpath.parent
    df = extract_df_from_html_file(html_file)
    for out_format, output_dir in output:
        out_fpath = Path(output_dir.format(html_dir=html_dir)) / html_fpath.with_suffix(f".{out_format}").name
        out_fpath.parent.mkdir(exist_ok=True, parents=True)
        print(f"Saving {len(df)} rows to: {out_fpath}")
        save_function = getattr(df, f"to_{out_format}")
        save_function(out_fpath, )
        # print(df)


def find_new_html_files(html_dir, processed_file: str | Path = "_processed.txt"):
    """ """
    html_files = Path(html_dir).glob("*_selenium.html")
    try:
        processed = {line.strip() for line in Path(processed_file).open() if line.strip() and line[0] != "#"}
        print(f"{len(processed)} files already processed.")
    except FileNotFoundError:
        print(f"processed_file '{processed_file}' not found, will assume empty set for previously processed files.")
        processed = set()
    new_files = [f for f in html_files if f.name not in processed]
    # print(new_files)
    return new_files


def main():
    # extract_and_save("data/jyskebank_erhverv_kurser/scrape_raw/20231209-191329_200.html")
    # html_dir = "data/jyskebank_erhverv_kurser/scrape_raw"
    html_dir = "data/jyskebank_erhverv_kurser/scrape_selenium"

    processed_file = Path(html_dir) / "_processed.txt"
    processed_file.parent.mkdir(exist_ok=True, parents=False)
    new_files = find_new_html_files(html_dir, processed_file=processed_file)
    if not new_files:
        print("No new HTML files since last run.")
    else:
        print(f"Processing {len(new_files)} new HTML files...")
    # print("\n".join(map(str, new_files)))
    # return
    with open(processed_file, 'a') as processed_fd:
        for html_file in new_files:
            print(html_file)
            extract_and_save(html_file)
            processed_fd.write(f"{html_file.name}\n")


if __name__ == "__main__":
    main()
