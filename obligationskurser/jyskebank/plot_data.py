
from datetime import datetime
from pathlib import Path

import matplotlib
from matplotlib import pyplot
import pandas as pd


def get_parquet_dfs(parquet_basedir):
    dfs = [pd.read_parquet(fpath) for fpath in Path(parquet_basedir).glob("*.parquet")]
    print(f"{len(dfs)} parquet files.")


def get_combined_df(parquet_basedir):
    # dfs = [pd.read_parquet(fpath) for fpath in Path(parquet_basedir).glob("*.parquet")]
    # We also need timestamp from filename...
    parquet_files = Path(parquet_basedir).glob("*.parquet")
    dfs = []
    for fpath in parquet_files:
        timestamp = datetime.strptime(fpath.name.replace("_200.parquet", ""), r"%Y%m%d-%H%M%S")
        df = pd.read_parquet(fpath)
        df['timestamp'] = timestamp
        dfs.append(df)
    print(f"{len(dfs)} parquet files.")
    return pd.concat(dfs)


def main():
    parquet_basedir = "data/jyskebank_erhverv_kurser/bs_pd_parquet"

    combined_df = get_combined_df(parquet_basedir)
    print(combined_df.columns)
    selected_df = combined_df[combined_df["Løbetid/kuponrente"].str.startswith(r"30 år 5,00 % afdragsfri* 411.E.OA.56")]
    print(selected_df)

    fig, ax = pyplot.subplots(figsize=(20, 10))
    plotax = selected_df.set_index("timestamp").plot(ax=ax)

    # ax.legend(loc='upper left')
    ax.legend(bbox_to_anchor=(1.25, 1.0))
    fig.tight_layout()

    plotfn = "5pct_411.E.OA.56.png"
    print("Saving plot to file:", plotfn)
    plotax.figure.savefig(plotfn)


# help(pd.Series.str)

if __name__ == "__main__":
    main()
