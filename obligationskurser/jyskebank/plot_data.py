"""
Plot output from extract_table_data_from_raw_html.py

Usage:

$ python obligationskurser/jyskebank/plot_data.py



"""
from datetime import datetime
from pathlib import Path

import matplotlib
from matplotlib import pyplot
import seaborn
import pandas as pd


def get_parquet_dfs(parquet_basedir):
    dfs = [pd.read_parquet(fpath) for fpath in Path(parquet_basedir).glob("*.parquet")]
    print(f"{len(dfs)} parquet files.")


def get_combined_df(
    parquet_basedir,
    fpattern: str = "*.parquet",
):
    # dfs = [pd.read_parquet(fpath) for fpath in Path(parquet_basedir).glob("*.parquet")]
    # We also need timestamp from filename...
    parquet_files = Path(parquet_basedir).glob(fpattern)
    dfs = []
    for fpath in parquet_files:
        timestamp = datetime.strptime(
            fpath.name.replace("_200.parquet", "").replace("_selenium.parquet", ""),
            r"%Y%m%d-%H%M%S"
        )
        df = pd.read_parquet(fpath)
        df['timestamp'] = timestamp
        dfs.append(df)
    print(f"{len(dfs)} parquet files.")
    return pd.concat(dfs)


def main(
    parquet_basedir: Path | str = "data/jyskebank_erhverv_kurser/bs_pd_parquet", 
    fpattern: str = "*.parquet",
):

    combined_df = get_combined_df(parquet_basedir, fpattern=fpattern)

    print("Columns:")
    print(combined_df.columns.values)

    # Remove bonds that we don't want to consider
    combined_df = combined_df[~combined_df["Løbetid/kuponrente"].str.startswith(r"30 år 1,00 %")]
    print("Løbetid/kuponrente, unikke værdier:")
    print("\n".join(sorted(combined_df["Løbetid/kuponrente"].unique())))

    # Create a shorter version of "Løbetid/kuponrente":
    combined_df["Obligation"] = combined_df["Løbetid/kuponrente"].apply(lambda s: s.split(" - U")[0])

    plot_all_cols_for = {
        # fn, startswith
        "5pct_411.E.OA.56.png": "30 år 5,00 % afdragsfri* 411.E.OA.56",
        "4pct_411.E.OA.56.png": "30 år 4,00 % afdragsfri* 411.E.OA.56",
        "4pct_111.E.56.png": "30 år 4,00 %  111.E.56",
    }

    for plotfn, startswith in plot_all_cols_for.items():
        # Plot all columns for "30 år 5,00 % afdragsfri* 411.E.OA.56"
        selected_df = combined_df[combined_df["Løbetid/kuponrente"].str.startswith(startswith)]
        # print(selected_df)
        fig, ax = pyplot.subplots(figsize=(20, 10))
        selected_df.set_index("timestamp").plot(ax=ax)
        # ax.legend(loc='upper left')
        ax.legend(bbox_to_anchor=(1.25, 1.0))
        fig.tight_layout()
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

    # Create difference plots:
    aktuel_kurs_pivot_df = combined_df.pivot(columns="Obligation", index=["timestamp"], values="Aktuel kurs")
    aktuel_kurs_pivot_diff_df = aktuel_kurs_pivot_df.subtract(aktuel_kurs_pivot_df["30 år 4,00 % afdragsfri* 411.E.OA.56"], axis="index")
    fig, ax = pyplot.subplots(figsize=(15, 10))
    aktuel_kurs_pivot_diff_df.plot(ax=ax)
    ax.legend(bbox_to_anchor=(1.25, 1.0))
    fig.tight_layout()
    plotfn = "Aktuel_kurs_diffplot.png"
    print("Saving plot to file:", plotfn)
    fig.savefig(plotfn)


if __name__ == "__main__":
    main()
