#!/usr/bin/env python3
"""
EB residuals against oblateness, split by source catalogue.

Reads the per-star tables written by analyse_eb_radius_oblateness_residuals.py and
analyse_eb_mass_oblateness_residuals.py (stacked prediction, "res" = (pred - true) / true),
and the holdout prediction tables of the radius noise-floor runs. Nothing is retrained.

Checks:
  1. Size (radius only): on the holdout (single) stars, does the fractional residual depend
     on R as it does on the EBs? Removing the holdout relation, what is left of the
     oblateness trend?
  2. Signed residual and absolute residual against log10 oblateness, for all EBs, Xiong23
     (the largest catalogue), the other catalogues, inside catalogues (ranks centred within
     each catalogue with >= MIN_STARS stars, p from shuffling inside catalogues) and leaving
     out one of the other catalogues at a time.
  3. Inside Xiong23 and the other catalogues: does the absolute residual survive at fixed R
     (and R, Teff, logg)? Do the catalogue's reported errors and the model's sigma grow with
     oblateness? Does |z| = |pred - true| / sqrt(model sigma^2 + catalogue sigma^2) still grow?

Outputs in OUTPUT_DIR: report.txt, correlations.csv, catalogue_means.csv.

Usage (from the BayestarML folder):
    python analyse_eb_residuals_by_catalogue.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

PRED_DIR = Path("Dataset_D_different_predictions")
HOLDOUT_DIR = Path("Dataset_D_v4_training")
OUTPUT_DIR = PRED_DIR / "catalogue_checks"
BIG_CATALOGUE = "Xiong23"
MIN_STARS = 3
N_PERM = 2000

# label, target, folder with EB_<target>_residuals_with_oblateness.csv, (draws, seed) of the holdout tables or None
CASES = [
    ("radius seed 665 floor", "radius", "seed_665_radius_residuals_floor", (1000, 665)),
    ("radius seed 145 floor", "radius", "seed_145_radius_residuals_floor", (3000, 145)),
    ("radius seed 146 floor", "radius", "seed_146_radius_residuals_floor", (3000, 146)),
    ("mass seed 648", "mass", "v4_seed_648_mass_residuals", None),
    ("mass seed 38 (v3)", "mass", "v3_seed_38_mass_residuals", None),
]
TARGETS = {"radius": ("R", "rad"), "mass": ("M", "mass")}


def spearman(x, y) -> tuple[float, float]:
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    s = stats.spearmanr(x[ok], y[ok])
    return float(s.statistic), float(s.pvalue)


def partial_spearman(df: pd.DataFrame, x: str, y: str, controls: list[str]) -> tuple[float, float]:
    """Rank correlation of x and y after removing a linear fit on the ranks of the controls."""
    df = df.dropna(subset=[x, y, *controls])
    ranks = lambda c: stats.rankdata(df[c])
    design = np.column_stack([np.ones(len(df))] + [ranks(c) for c in controls])
    resid = lambda v: v - design @ np.linalg.lstsq(design, v, rcond=None)[0]
    r = float(np.corrcoef(resid(ranks(x)), resid(ranks(y)))[0, 1])
    dof = len(df) - 2 - len(controls)
    t = r * np.sqrt(dof / (1 - r ** 2))
    return r, float(2 * stats.t.sf(abs(t), dof))


def within_catalogue(df: pd.DataFrame, x: str, y: str) -> tuple[float, float, int]:
    """Rank correlation inside catalogues (ranks centred within each catalogue with >= MIN_STARS
    stars); permutation p from shuffling y inside each catalogue."""
    rng = np.random.default_rng(0)
    big = df.groupby("catalog").filter(lambda g: len(g) >= MIN_STARS)
    groups = big["catalog"]

    def centred(values: pd.Series) -> pd.Series:
        return values.groupby(groups).rank() - values.groupby(groups).transform(lambda v: (len(v) + 1) / 2)

    cx = centred(big[x])
    r = float(np.corrcoef(cx, centred(big[y]))[0, 1])
    null = [np.corrcoef(cx, centred(big[y].groupby(groups).transform(lambda v: rng.permutation(v.to_numpy()))))[0, 1]
            for _ in range(N_PERM)]
    return r, float(np.mean(np.abs(null) >= abs(r))), len(big)


def load(folder: str, target: str) -> pd.DataFrame:
    true_col, prefix = TARGETS[target]
    d = pd.read_csv(PRED_DIR / folder / f"EB_{target}_residuals_with_oblateness.csv")
    d = d.dropna(subset=[f"{prefix}_pred", true_col, "oblateness"]).copy()
    d["log_o"] = np.log10(d["oblateness"])
    d["res"] = (d[f"{prefix}_pred"] - d[true_col]) / d[true_col]
    d["abs_res"] = d["res"].abs()
    d["model_sigma_rel"] = d[f"{prefix}_sigma"] / d[true_col]
    d["abs_z"] = d[f"abs_z_{true_col}"]
    d["ci68"] = d[f"ci68_contains_{true_col}_true"].astype(float)
    for col, base in (("R", "R"), ("M", "M"), ("Teff", "Teff")):
        d[f"err_{col}_rel"] = 0.5 * (d[f"e{col}1"].abs() + d[f"e{col}2"].abs()) / d[base]
    d["err_logg"] = 0.5 * (d["elogg1"].abs() + d["elogg2"].abs())
    return d


def fmt(r: float, p: float) -> str:
    return f"{r:+.2f} (p={p:.2g})"


def size_check(d: pd.DataFrame, draws: int, seed: int, out: list[str], rows: list[dict], label: str) -> None:
    R_eb = d["R"].to_numpy(float)
    for model, tsv, col in (("GP", f"radius_prediction_results_GP_{draws}_seed_{seed}.tsv", "rad_pred_GP"),
                            ("HBNN", f"radius_prediction_results_HBNN_floor_{draws}_seed_{seed}.tsv", "rad_pred_HBNN")):
        h = pd.read_csv(HOLDOUT_DIR / tsv, sep="\t")
        R_h = h["R_true"].to_numpy(float)
        f_h = (h["R_pred"].to_numpy(float) - R_h) / R_h
        common = (R_h >= R_eb.min()) & (R_h <= R_eb.max())
        fit_h = np.polyfit(R_h[common], f_h[common], 1)
        f_eb = (d[col].to_numpy(float) - R_eb) / R_eb
        slope_eb = np.polyfit(R_eb, f_eb, 1)[0]
        observed = spearman(d["log_o"], f_eb)
        left = spearman(d["log_o"], f_eb - np.polyval(fit_h, R_eb))
        out.append(f"  {model:4s} residual slope vs R: holdout {100 * fit_h[0]:+.2f} %/Rsun (n={common.sum()} in the EB R range), "
                   f"EBs {100 * slope_eb:+.2f} %/Rsun | EB residual vs log o: {fmt(*observed)}, "
                   f"after removing the holdout size relation {fmt(*left)}")
        rows.append(dict(case=label, check="size", group=f"EBs, {model}", n=len(d), rho=left[0], p=left[1],
                         note=f"holdout slope {100 * fit_h[0]:+.2f} %/Rsun, EB slope {100 * slope_eb:+.2f} %/Rsun"))


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out: list[str] = [__doc__.strip().split("\n\n")[0], ""]
    rows: list[dict] = []
    means: list[pd.DataFrame] = []

    for label, target, folder, holdout in CASES:
        d = load(folder, target)
        out.append(f"##### {label} (stacked prediction, {len(d)} EB stars; {folder})")

        if holdout is not None:
            out.append("1. Size")
            size_check(d, *holdout, out, rows, label)

        out.append("2. Residual vs log10 oblateness: signed | absolute")
        split = {"all EBs": d, BIG_CATALOGUE: d[d["catalog"] == BIG_CATALOGUE],
                 "other catalogues": d[d["catalog"] != BIG_CATALOGUE]}
        for name, g in split.items():
            s, a = spearman(g["log_o"], g["res"]), spearman(g["log_o"], g["abs_res"])
            out.append(f"  {name:34s} n={len(g):3d}, median log o {g['log_o'].median():+.2f}, mean |res| {100 * g['abs_res'].mean():.1f}% "
                       f"| signed {fmt(*s)} | absolute {fmt(*a)}")
            rows.append(dict(case=label, check="signed", group=name, n=len(g), rho=s[0], p=s[1]))
            rows.append(dict(case=label, check="absolute", group=name, n=len(g), rho=a[0], p=a[1]))
        for name, g in ((f"inside catalogues, incl. {BIG_CATALOGUE}", d),
                        (f"inside catalogues, excl. {BIG_CATALOGUE}", d[d["catalog"] != BIG_CATALOGUE])):
            rs, ps, n = within_catalogue(g, "log_o", "res")
            ra, pa, _ = within_catalogue(g, "log_o", "abs_res")
            out.append(f"  {name:34s} n={n:3d} | signed {rs:+.2f} (perm p={ps:.2g}) | absolute {ra:+.2f} (perm p={pa:.2g})")
            rows.append(dict(case=label, check="signed", group=name, n=n, rho=rs, p=ps, note="permutation p"))
            rows.append(dict(case=label, check="absolute", group=name, n=n, rho=ra, p=pa, note="permutation p"))
        others = d[d["catalog"] != BIG_CATALOGUE]
        loco = [spearman(others.loc[others["catalog"] != c, "log_o"], others.loc[others["catalog"] != c, "res"])[0]
                for c in others["catalog"].unique()]
        out.append(f"  signed, other catalogues leaving one catalogue out: rho {min(loco):+.2f} to {max(loco):+.2f}")
        rows.append(dict(case=label, check="signed", group="other catalogues, leave one catalogue out", n=len(others),
                         rho=max(loco), note=f"range {min(loco):+.2f} to {max(loco):+.2f}; rho = weakest"))

        t = (d.groupby("catalog")
              .agg(n=("log_o", "size"), median_log_o=("log_o", "median"),
                   mean_signed_res_percent=("res", lambda v: 100 * v.mean()),
                   mean_abs_res_percent=("abs_res", lambda v: 100 * v.mean())))
        t = t[t["n"] >= MIN_STARS].sort_values("median_log_o").round(2)
        out.append(f"  catalogues with >= {MIN_STARS} stars, by median log o:")
        out.extend("    " + line for line in t.to_string().splitlines())
        means.append(t.reset_index().assign(case=label))

        out.append("3. Absolute residual, catalogue errors and model sigma vs log10 oblateness")
        for name in (BIG_CATALOGUE, "other catalogues"):
            g = split[name]
            checks = {
                "absolute residual": spearman(g["log_o"], g["abs_res"]),
                "absolute residual at fixed R": partial_spearman(g, "log_o", "abs_res", ["R"]),
                "absolute residual at fixed R, Teff, logg": partial_spearman(g, "log_o", "abs_res", ["R", "Teff", "logg"]),
                "catalogue error on R (relative)": spearman(g["log_o"], g["err_R_rel"]),
                "catalogue error on M (relative)": spearman(g["log_o"], g["err_M_rel"]),
                "catalogue error on Teff (relative)": spearman(g["log_o"], g["err_Teff_rel"]),
                "catalogue error on logg": spearman(g["log_o"], g["err_logg"]),
                "model sigma (relative)": spearman(g["log_o"], g["model_sigma_rel"]),
                "|z| = |residual| / combined sigma": spearman(g["log_o"], g["abs_z"]),
            }
            out.append(f"  {name} (n={len(g)}; absolute residual vs R {fmt(*spearman(g['R'], g['abs_res']))}; "
                       f"68% coverage {g['ci68'].mean():.2f}; median catalogue error R {100 * g['err_R_rel'].median():.1f}%, "
                       f"M {100 * g['err_M_rel'].median():.1f}%; median model sigma {100 * g['model_sigma_rel'].median():.1f}%)")
            for what, (r, p) in checks.items():
                out.append(f"    {what:42s} {fmt(r, p)}")
                rows.append(dict(case=label, check=what, group=name, n=len(g), rho=r, p=p))
        out.append("")

    (OUTPUT_DIR / "report.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
    pd.DataFrame(rows).to_csv(OUTPUT_DIR / "correlations.csv", index=False, float_format="%.4g")
    pd.concat(means)[["case", "catalog", "n", "median_log_o", "mean_signed_res_percent", "mean_abs_res_percent"]] \
        .to_csv(OUTPUT_DIR / "catalogue_means.csv", index=False)
    print("\n".join(out))
    print(f"Written to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
