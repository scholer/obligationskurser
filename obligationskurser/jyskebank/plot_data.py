
from datetime import datetime
from pathlib import Path

import matplotlib
from matplotlib import pyplot
import seaborn
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

    print("Columns:")
    print(combined_df.columns.values)

    # Remove 
    combined_df = combined_df[~combined_df["Løbetid/kuponrente"].str.startswith(r"30 år 1,00 %")]
    print("Løbetid/kuponrente, unikke værdier:")
    print("\n".join(sorted(combined_df["Løbetid/kuponrente"].unique())))

    # Plot all columns for "30 år 5,00 % afdragsfri* 411.E.OA.56"
    selected_df = combined_df[combined_df["Løbetid/kuponrente"].str.startswith(r"30 år 5,00 % afdragsfri* 411.E.OA.56")]
    # print(selected_df)
    fig, ax = pyplot.subplots(figsize=(20, 10))
    selected_df.set_index("timestamp").plot(ax=ax)
    # ax.legend(loc='upper left')
    ax.legend(bbox_to_anchor=(1.25, 1.0))
    fig.tight_layout()
    plotfn = "5pct_411.E.OA.56.png"
    print("Saving plot to file:", plotfn)
    fig.savefig(plotfn)

    # Plot all columns for "30 år 5,00 % afdragsfri* 411.E.OA.56"
    selected_df = combined_df[combined_df["Løbetid/kuponrente"].str.startswith(r"30 år 4,00 % afdragsfri* 411.E.OA.56")]
    # print(selected_df)
    fig, ax = pyplot.subplots(figsize=(20, 10))
    selected_df.set_index("timestamp").plot(ax=ax)
    # ax.legend(loc='upper left')
    ax.legend(bbox_to_anchor=(1.25, 1.0))
    fig.tight_layout()
    plotfn = "4pct_411.E.OA.56.png"
    print("Saving plot to file:", plotfn)
    fig.savefig(plotfn)

    # Plot all rows for a specific column ('Tilbudskurs'):
    fig, ax = pyplot.subplots(figsize=(15, 10))
    seaborn.lineplot(data=combined_df, x="timestamp", y="Tilbudskurs", hue="Løbetid/kuponrente")
    ax.legend(bbox_to_anchor=(1.0, 1.0))
    fig.tight_layout()
    plotfn = 'Tilbudskurs.png'
    print("Saving plot to file:", plotfn)
    fig.savefig(plotfn)

    # Plot all rows for a specific column ('Aktuel kurs'):
    fig, ax = pyplot.subplots(figsize=(15, 10))
    seaborn.lineplot(data=combined_df, x="timestamp", y="Aktuel kurs", hue="Løbetid/kuponrente")
    ax.legend(bbox_to_anchor=(1.0, 1.0))
    fig.tight_layout()
    plotfn = 'Aktuel_kurs.png'
    print("Saving plot to file:", plotfn)
    fig.savefig(plotfn)

    # Plot all "Udbetalingskurs Fastkursaftale":
    fastkurs_cols = [col for col in combined_df.columns.values if "Udbetalingskurs Fastkursaftale" in col]



if __name__ == "__main__":
    main()
