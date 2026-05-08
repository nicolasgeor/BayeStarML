from pathlib import Path
import sys

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils import load_stellar_dataframe, read_stellar_table


def main():
    tmp_dir = Path(__file__).resolve().parent / "_tmp_loader"
    tmp_dir.mkdir(exist_ok=True)
    path = tmp_dir / "database2026_sample.txt"
    try:
        path.write_text(
            "\n".join(
                [
                    "# comment line",
                    "# another comment",
                    "",
                    "ID\tM\teM1\teM2\tR\teR1\teR2\tTeff\teTeff1\teTeff2\tFe/H\te1_Fe/H\te2_Fe/H\tclass\ttype\tmode\trho\terho1\terho2",
                    "Star_A\t1,20\t0,02\t0,03\t1,10\t0,01\t0,02\t6000,0\t100,0\t90,0\t-0,10\t0,02\t0,03\tMS\tG\tEB\t0,90\t0,04\t0,05",
                    "Star_B\t1,00\tNA\tNA\t1,00\t0,01\t0,01\t5800,0\t80,0\t80,0\t0,00\t0,01\t0,01\tMS\tG\tEB\t1,00\t0,02\t0,02",
                ]
            ),
            encoding="utf-8",
        )

        raw = read_stellar_table(path)
        assert raw.columns[0] == "ID"
        assert raw.loc[0, "M"] == "1,20"
        assert pd.isna(raw.loc[1, "eM1"])

        df, summary = load_stellar_dataframe(
            path,
            required_features=["Teff", "Meta", "rho"],
            target="mass",
            star_class="MS",
            drop_invalid=False,
            verbose=False,
        )
        assert summary["rows_loaded"] == 2
        assert summary["mapped_columns"]["Meta"] == "Fe/H"
        assert summary["generated_columns"] == ["e_M", "e_R", "e_Teff"]
        assert df.loc[0, "M"] == 1.2
        assert df.loc[0, "Meta"] == -0.1
        assert round(df.loc[0, "e_M"], 6) == round(100.0 * 0.025 / 1.2, 6)
    finally:
        if path.exists():
            path.unlink()
        if tmp_dir.exists():
            tmp_dir.rmdir()

    print("new database loader smoke check passed")


if __name__ == "__main__":
    main()
