# This is the old file called analyse_eb_oblateness_residuals.py

#!/usr/bin/env python3
"""
Analyse EB mass-prediction residuals versus oblateness and Roche-lobe filling factor.

Expected input: CSV produced by the EB mass-prediction step, containing the original
stellar database columns plus at least:
    mass_pred, mass_sigma, mass_p16, mass_p84, mass_p02_5, mass_p97_5

Main outputs:
    EB_mass_residuals_with_oblateness.csv
    EB_residual_correlation_summary.csv
    EB_residual_binned_by_oblateness.csv
    EB_plot_binned_residuals_vs_log10_oblateness.csv
    EB_top_outliers_by_abs_frac_residual.csv
    plots/*.png

Usage:
    python analyse_eb_oblateness_residuals.py
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

try:
    from scipy import stats
except Exception:  # pragma: no cover
    stats = None


INPUT_CSV = Path("Dataset_D_predictions/EB_oblateness_fill_factor_mass_predictions_4_features_3000_draws_seed_392.csv")
OUTPUT_DIR = Path("Dataset_D_predictions/seed 392_")
MIN_OBLATENESS = 0.0
TOP_N = 30
MASS_MIN = 0.950
MASS_MAX = 1.500
ROBUST = True
N_OBLATENESS_BINS = 12
MIN_BIN_COUNT = 3
REGRESSION_PREDICTORS = ["log10_oblateness", "M", "Teff", "Meta", "logg", "L"]
ROBUST_FEATURE_RANGES = {
    "Teff": (5500.0, 6800.0),
    "logg": (3.750, 4.450),
    "L": (1.000, 11.000),
    "Meta": (-0.500, 0.270),
}

REQUIRED_COLUMNS = ["M", "mass_pred", "mass_sigma", "oblateness"]
OPTIONAL_NUMERIC_COLUMNS = [
    "eM1", "eM2",
    "mass_p16", "mass_p84", "mass_p02_5", "mass_p97_5",
    "eoblateness1", "eoblateness2",
    "fill_factor", "efill_factor1", "efill_factor2",
    "Teff", "eTeff1", "eTeff2",
    "Meta", "eMeta1", "eMeta2",
    "logg", "elogg1", "elogg2",
    "L", "eL1", "eL2",
    "R", "eR1", "eR2",
    "orbit_a", "eOrbit_a",
]


def robust_to_numeric(series: pd.Series) -> pd.Series:
    """Convert common catalogue number strings to float.

    Handles blanks, NA-like strings, decimal comma strings, and occasional thousand
    separators. This is intentionally conservative to avoid silently corrupting IDs.
    """
    s = series.astype("string").str.strip()
    s = s.replace({"": pd.NA, "NA": pd.NA, "NaN": pd.NA, "nan": pd.NA, "None": pd.NA, "NULL": pd.NA})

    # If a value has a comma but no dot, treat comma as decimal separator.
    comma_decimal = s.str.contains(",", na=False) & ~s.str.contains(r"\.", na=False)
    s = s.mask(comma_decimal, s[comma_decimal].str.replace(",", ".", regex=False))

    return pd.to_numeric(s, errors="coerce")


def symmetric_error(df: pd.DataFrame, plus_col: str, minus_col: str, out_col: str) -> None:
    """Create a symmetric error column from two one-sided uncertainty columns."""
    if plus_col in df.columns and minus_col in df.columns:
        a = df[plus_col].abs()
        b = df[minus_col].abs()
        df[out_col] = np.nanmean(np.vstack([a.to_numpy(), b.to_numpy()]), axis=0)
    elif plus_col in df.columns:
        df[out_col] = df[plus_col].abs()
    elif minus_col in df.columns:
        df[out_col] = df[minus_col].abs()
    else:
        df[out_col] = np.nan


def finite_mask(df: pd.DataFrame, columns: Iterable[str]) -> pd.Series:
    mask = pd.Series(True, index=df.index)
    for col in columns:
        mask &= np.isfinite(df[col])
    return mask


def correlation_rows(df: pd.DataFrame, ycols: list[str], xcols: list[str]) -> pd.DataFrame:
    rows = []
    for xcol in xcols:
        for ycol in ycols:
            sub = df[[xcol, ycol]].replace([np.inf, -np.inf], np.nan).dropna()
            n = len(sub)
            row = {"x": xcol, "y": ycol, "n": n}
            if n >= 3 and sub[xcol].nunique() > 1 and sub[ycol].nunique() > 1:
                x = sub[xcol].to_numpy(float)
                y = sub[ycol].to_numpy(float)
                if stats is not None:
                    pearson = stats.pearsonr(x, y)
                    spearman = stats.spearmanr(x, y)
                    row.update({
                        "pearson_r": pearson.statistic,
                        "pearson_p": pearson.pvalue,
                        "spearman_rho": spearman.statistic,
                        "spearman_p": spearman.pvalue,
                    })
                else:
                    row.update({
                        "pearson_r": np.corrcoef(x, y)[0, 1],
                        "pearson_p": np.nan,
                        "spearman_rho": pd.Series(x).rank().corr(pd.Series(y).rank()),
                        "spearman_p": np.nan,
                    })
                slope, intercept = np.polyfit(x, y, deg=1)
                row.update({"linear_slope": slope, "linear_intercept": intercept})
            else:
                row.update({
                    "pearson_r": np.nan, "pearson_p": np.nan,
                    "spearman_rho": np.nan, "spearman_p": np.nan,
                    "linear_slope": np.nan, "linear_intercept": np.nan,
                })
            rows.append(row)
    return pd.DataFrame(rows)


def add_reference_line(ax, horizontal: bool = True, vertical: bool = False) -> None:
    if horizontal:
        ax.axhline(0.0, linestyle="--", linewidth=1, color='red')
    if vertical:
        ax.axvline(0.0, linestyle="--", linewidth=1, color='red')


def scatter_with_fit(df: pd.DataFrame, x: str, y: str, xlabel: str, ylabel: str, title: str, path: Path, color_by: str | None = None) -> None:
    sub_cols = [x, y] + ([color_by] if color_by and color_by in df.columns else [])
    sub = df[sub_cols].replace([np.inf, -np.inf], np.nan).dropna()

    fig, ax = plt.subplots(figsize=(7.2, 5.0), dpi=160)
    if color_by and color_by in sub.columns and sub[color_by].notna().any():
        sc = ax.scatter(sub[x], sub[y], c=sub[color_by], s=28, alpha=0.8)
        cbar = fig.colorbar(sc, ax=ax)
        cbar.set_label(color_by)
    else:
        ax.scatter(sub[x], sub[y], s=28, alpha=0.8, color='black')

    add_reference_line(ax, horizontal=True)

    if len(sub) >= 3 and sub[x].nunique() > 1:
        slope, intercept = np.polyfit(sub[x].to_numpy(float), sub[y].to_numpy(float), deg=1)
        xx = np.linspace(sub[x].min(), sub[x].max(), 200)
        ax.plot(xx, slope * xx + intercept, linewidth=1.5, color='red', label=f"linear fit: slope={slope:.3g}")
        ax.legend(frameon=True, fontsize=12)

    ax.set_xlabel(xlabel, fontsize=14)
    ax.set_ylabel(ylabel, fontsize=14)
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)

def scatter_with_errorbars_and_colormap(df: pd.DataFrame, x: str, y: str, yerr: str, color_by: str, xlabel: str, ylabel: str, cbar_label: str, title: str, path: Path) -> None:
    sub_cols = [x, y, yerr, color_by]
    sub = df[sub_cols].replace([np.inf, -np.inf], np.nan).dropna()

    fig, ax = plt.subplots(figsize=(7.2, 5.0), dpi=160)

    # Plot error bars behind the scatter dots
    ax.errorbar(sub[x], sub[y], yerr=sub[yerr], fmt='none', ecolor='tab:blue', alpha=0.6, elinewidth=1.2, capsize=2, zorder=1)

    # Plot the color-mapped scatter points
    sc = ax.scatter(sub[x], sub[y], c=sub[color_by], cmap='viridis', s=28, edgecolors='0.3', linewidths=0.5, zorder=2)

    cbar = fig.colorbar(sc, ax=ax)
    cbar.set_label(cbar_label, fontsize=14)

    add_reference_line(ax, horizontal=True)

    ax.set_xlabel(xlabel, fontsize=14)
    ax.set_ylabel(ylabel, fontsize=14)
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)

def binned_scatter(
    df: pd.DataFrame,
    x: str,
    y: str,
    xlabel: str,
    ylabel: str,
    title: str,
    path: Path,
    marker_color: str,
    bin_stat: str = "mean",
) -> pd.DataFrame:
    sub = df[[x, y]].replace([np.inf, -np.inf], np.nan).dropna().copy()

    fig, ax = plt.subplots(figsize=(7.2, 5.0), dpi=160)
    ax.scatter(sub[x], sub[y], s=24, alpha=0.55, color="black", edgecolors="none", label="Stars")
    add_reference_line(ax, horizontal=True)

    rows = []
    if len(sub) >= MIN_BIN_COUNT and sub[x].nunique() > 1:
        edges = np.linspace(sub[x].min(), sub[x].max(), N_OBLATENESS_BINS + 1)
        edges = np.unique(edges)
        if len(edges) >= 3:
            sub["x_bin"] = pd.cut(sub[x], bins=edges, include_lowest=True)
            for interval, g in sub.groupby("x_bin", observed=True):
                if len(g) < MIN_BIN_COUNT:
                    continue
                y_values = g[y].to_numpy(float)
                center = 0.5 * (interval.left + interval.right)
                y_center = np.nanmedian(y_values) if bin_stat == "median" else np.nanmean(y_values)
                y_std = np.nanstd(y_values, ddof=1) if len(g) > 1 else np.nan
                rows.append({
                    "plot_file": path.name,
                    "plot_title": title,
                    "x": x,
                    "y": y,
                    "bin": str(interval),
                    "x_center": center,
                    "x_min": interval.left,
                    "x_max": interval.right,
                    "n": len(g),
                    "y_center": y_center,
                    "y_std": y_std,
                    "frac_residual_center": y_center if y == "frac_residual" else np.nan,
                    "frac_residual_std": y_std if y == "frac_residual" else np.nan,
                    "abs_frac_residual_center": y_center if y == "abs_frac_residual" else np.nan,
                    "abs_frac_residual_std": y_std if y == "abs_frac_residual" else np.nan,
                    "statistic": bin_stat,
                })

    binned = pd.DataFrame(rows)
    if not binned.empty:
        label = f"Bin {bin_stat} +/- 1 sigma"
        ax.errorbar(
            binned["x_center"], binned["y_center"],
            yerr=binned["y_std"],
            fmt="s", markersize=5.5,
            color=marker_color, ecolor=marker_color,
            elinewidth=1.4, capsize=3,
            label=label,
        )
        ax.legend(frameon=True, fontsize=12)

    ax.set_xlabel(xlabel, fontsize=14)
    ax.set_ylabel(ylabel, fontsize=14)
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)

    return binned


def save_binned_plot_tables(tables: list[pd.DataFrame], path: Path) -> Path:
    tables = [table for table in tables if table is not None and not table.empty]
    if tables:
        out = pd.concat(tables, ignore_index=True)
    else:
        out = pd.DataFrame(columns=[
            "plot_file", "plot_title", "x", "y", "bin", "x_center", "x_min", "x_max", "n",
            "y_center", "y_std", "frac_residual_center", "frac_residual_std",
            "abs_frac_residual_center", "abs_frac_residual_std", "statistic",
        ])
    out.to_csv(path, index=False)
    return path


def make_plots(df: pd.DataFrame, outdir: Path) -> None:
    plots = outdir / "plots"
    plots.mkdir(parents=True, exist_ok=True)
    plot_bin_tables = []

    # scatter_with_fit(
    #     df, "log10_oblateness", "delta_M",
    #     r"$\log_{10}(o)$", r"$\Delta M = M_{pred}-M_{true}$ [$M_\odot$]",
    #     "Absolute mass residual vs oblateness",
    #     plots / "01_deltaM_vs_log10_oblateness.png",
    #     color_by="fill_factor",
    # )

    plot_bin_tables.append(binned_scatter(
        df, "log10_oblateness", "frac_residual",
        r"$\log_{10}(o)$", r"$(M_{pred}-M_{true})/M_{true}$",
        "Fractional mass residual vs oblateness",
        plots / "02_fractional_residual_vs_log10_oblateness.png",
        marker_color="blue",
        bin_stat="mean",
    ))

    if "abs_frac_residual" in df.columns:
        plot_bin_tables.append(binned_scatter(
            df, "log10_oblateness", "abs_frac_residual",
            r"$\log_{10}(o)$", r"$|(M_{pred}-M_{true})/M_{true}|$",
            "Absolute fractional mass residual vs oblateness",
            plots / "02c_abs_fractional_residual_vs_log10_oblateness.png",
            marker_color="red",
            bin_stat="median",
        ))

    save_binned_plot_tables(plot_bin_tables, outdir / "EB_plot_binned_residuals_vs_log10_oblateness.csv")

    scatter_with_fit(
        df, "oblateness", "frac_residual",
        "Oblateness", r"$(M_{pred}-M_{true})/M_{true}$",
        "Fractional mass residual vs oblateness",
        plots / "02b_fractional_residual_vs_oblateness.png",
        color_by="fill_factor",
    )

    scatter_with_errorbars_and_colormap(
        df,
        x="log10_oblateness",
        y="frac_residual",
        yerr="sigma_frac_residual",
        color_by="M",
        xlabel=r"$\log_{10}(o)$",
        ylabel=r"$(M_{pred}-M_{true})/M_{true}$",
        cbar_label=r"True EB mass ($M_\odot$)",
        title="Fractional mass residual vs oblateness",
        path=plots / "02d_fractional_residual_vs_log10_oblateness_colored_by_M.png"
    )

    # scatter_with_fit(
    #     df, "log10_oblateness", "z_M",
    #     r"$\log_{10}(o)$", r"$z_M$ using mass_sigma",
    #     "Normalized mass residual vs oblateness",
    #     plots / "03_zM_vs_log10_oblateness.png",
    #     color_by="fill_factor",
    # )

    # if "z_M_q68" in df.columns and df["z_M_q68"].notna().sum() >= 3:
    #     scatter_with_fit(
    #         df, "log10_oblateness", "z_M_q68",
    #         r"$\log_{10}(o)$", r"$z_M$ using $(p84-p16)/2$",
    #         "Normalized residual from 68% predictive interval vs oblateness",
    #         plots / "03b_zM_q68_vs_log10_oblateness.png",
    #         color_by="fill_factor",
    #     )

    # if "fill_factor" in df.columns and df["fill_factor"].notna().sum() >= 3:
    #     scatter_with_fit(
    #         df, "fill_factor", "frac_residual",
    #         "Roche-lobe filling factor", r"$(M_{pred}-M_{true})/M_{true}$",
    #         "Fractional mass residual vs filling factor",
    #         plots / "04_fractional_residual_vs_fill_factor.png",
    #         color_by="log10_oblateness",
    #     )

    #     scatter_with_fit(
    #         df, "log10_fill_factor", "frac_residual",
    #         r"$\log_{10}$(filling factor)", r"$(M_{pred}-M_{true})/M_{true}$",
    #         "Fractional mass residual vs log filling factor",
    #         plots / "05_fractional_residual_vs_log10_fill_factor.png",
    #         color_by="log10_oblateness",
    #     )

    # Predicted vs true mass.
    sub = df[["M", "mass_pred", "mass_sigma"]].replace([np.inf, -np.inf], np.nan).dropna()
    fig, ax = plt.subplots(figsize=(6.0, 6.0), dpi=160)
    ax.scatter(sub["M"], sub["mass_pred"], s=28, alpha=0.8, color='black', label='Predictions')
    lo = min(sub["M"].min(), sub["mass_pred"].min())
    hi = max(sub["M"].max(), sub["mass_pred"].max())
    ax.plot([lo, hi], [lo, hi], linestyle="--", linewidth=1, color='red', label='1:1 Line')
    ax.set_xlabel(r"True EB mass [$M_\odot$]", fontsize=14)
    ax.set_ylabel(r"Predicted mass [$M_\odot$]", fontsize=14)
    ax.set_title("Predicted vs true EB masses")
    ax.set_aspect("equal", adjustable="box")
    ax.legend(fontsize=12, frameon=True)
    fig.tight_layout()
    fig.savefig(plots / "07_mass_pred_vs_mass_true.png")
    plt.close(fig)

    scatter_with_fit(
        df, "M", "frac_residual",
        r"True EB mass [$M_\odot$]", r"$(M_{pred}-M_{true})/M_{true}$",
        "Fractional mass residual vs true EB mass",
        plots / "08_fractional_residual_vs_true_mass.png",
        color_by="log10_oblateness",
    )

    for i, xcol in enumerate(["Teff", "Meta", "logg", "L", "log10_L"], start=9):
        if i == 12:
            continue

        if xcol in df.columns and df[xcol].notna().sum() >= 3:
            xlabel = {
                "Teff": r"$T_{eff}$ [K]",
                "Meta": "[Fe/H]",
                "logg": r"$\log g$",
                "L": r"$L$ [$L_\odot$]",
                "log10_L": r"$\log_{10}(L/L_\odot)$",
            }[xcol]
            scatter_with_fit(
                df, xcol, "frac_residual",
                xlabel, r"$(M_{pred}-M_{true})/M_{true}$",
                f"Fractional mass residual vs {xcol}",
                plots / f"{i:02d}_fractional_residual_vs_{xcol}.png",
                color_by="log10_oblateness",
            )

    # Histogram of fractional residuals.
    sub = df[["frac_residual"]].replace([np.inf, -np.inf], np.nan).dropna()
    fig, ax = plt.subplots(figsize=(7.2, 4.5), dpi=160)
    ax.hist(sub["frac_residual"], bins=30, alpha=0.85)
    ax.axvline(0.0, linestyle="--", linewidth=1, color = 'red')
    ax.set_xlabel(r"$(M_{pred}-M_{true})/M_{true}$", fontsize = 14)
    ax.set_ylabel("Number of EB components", fontsize=14)
    ax.set_title("Distribution of fractional mass residuals")
    fig.tight_layout()
    fig.savefig(plots / "13_hist_fractional_residuals.png")
    plt.close(fig)


def make_pretrim_plots(df: pd.DataFrame, outdir: Path) -> None:
    plots = outdir / "plots_before_mass_cut"
    plots.mkdir(parents=True, exist_ok=True)
    plot_bin_tables = []

    plot_bin_tables.append(binned_scatter(
        df, "log10_oblateness", "frac_residual",
        r"$\log_{10}(o)$", r"$(M_{pred}-M_{true})/M_{true}$",
        "Fractional mass residual vs oblateness before mass cut",
        plots / "02_fractional_residual_vs_log10_oblateness_before_mass_cut.png",
        marker_color="black",
        bin_stat="mean",
    ))

    if "abs_frac_residual" in df.columns:
        plot_bin_tables.append(binned_scatter(
            df, "log10_oblateness", "abs_frac_residual",
            r"$\log_{10}(o)$", r"$|(M_{pred}-M_{true})/M_{true}|$",
            "Absolute fractional mass residual vs oblateness before mass cut",
            plots / "02c_abs_fractional_residual_vs_log10_oblateness_before_mass_cut.png",
            marker_color="red",
            bin_stat="median",
        ))

    save_binned_plot_tables(
        plot_bin_tables,
        outdir / "EB_plot_binned_residuals_vs_log10_oblateness_before_mass_cut.csv",
    )

    scatter_with_fit(
        df, "oblateness", "frac_residual",
        "Oblateness", r"$(M_{pred}-M_{true})/M_{true}$",
        "Fractional mass residual vs oblateness before mass cut",
        plots / "02b_fractional_residual_vs_oblateness_before_mass_cut.png",
        color_by="fill_factor",
    )

    scatter_with_errorbars_and_colormap(
        df,
        x="log10_oblateness",
        y="frac_residual",
        yerr="sigma_frac_residual",
        color_by="M",
        xlabel=r"$\log_{10}(o)$",
        ylabel=r"$(M_{pred}-M_{true})/M_{true}$",
        cbar_label=r"True EB mass ($M_\odot$)",
        title="Fractional mass residual vs oblateness before mass cut",
        path=plots / "02d_fractional_residual_vs_log10_oblateness_colored_by_M_before_mass_cut.png"
    )

    # if "fill_factor" in df.columns and df["fill_factor"].notna().sum() >= 3:
    #     scatter_with_fit(
    #         df, "fill_factor", "frac_residual",
    #         "Roche-lobe filling factor", r"$(M_{pred}-M_{true})/M_{true}$",
    #         "Fractional mass residual vs filling factor before mass cut",
    #         plots / "04_fractional_residual_vs_fill_factor_before_mass_cut.png",
    #         color_by="log10_oblateness",
    #     )

    #     scatter_with_fit(
    #         df, "log10_fill_factor", "frac_residual",
    #         r"$\log_{10}$(filling factor)", r"$(M_{pred}-M_{true})/M_{true}$",
    #         "Fractional mass residual vs log filling factor before mass cut",
    #         plots / "05_fractional_residual_vs_log10_fill_factor_before_mass_cut.png",
    #         color_by="log10_oblateness",
    #     )

    sub = df[["M", "mass_pred", "mass_sigma"]].replace([np.inf, -np.inf], np.nan).dropna()
    fig, ax = plt.subplots(figsize=(6.0, 6.0), dpi=160)
    ax.scatter(sub["M"], sub["mass_pred"], s=28, alpha=0.8, color='black', label='Predictions')
    lo = min(sub["M"].min(), sub["mass_pred"].min())
    hi = max(sub["M"].max(), sub["mass_pred"].max())
    ax.plot([lo, hi], [lo, hi], linestyle="--", linewidth=1, color='red', label='1:1 Line')
    ax.set_xlabel(r"True EB mass [$M_\odot$]", fontsize=14)
    ax.set_ylabel(r"Predicted mass [$M_\odot$]", fontsize=14)
    ax.set_title("Predicted vs true EB masses before mass cut")
    ax.set_aspect("equal", adjustable="box")
    ax.legend(fontsize=12, frameon=True)
    fig.tight_layout()
    fig.savefig(plots / "07_mass_pred_vs_mass_true_before_mass_cut.png")
    plt.close(fig)

    scatter_with_fit(
        df, "M", "frac_residual",
        r"True EB mass [$M_\odot$]", r"$(M_{pred}-M_{true})/M_{true}$",
        "Fractional mass residual vs true EB mass before mass cut",
        plots / "08_fractional_residual_vs_true_mass_before_mass_cut.png",
        color_by="log10_oblateness",
    )

    for i, xcol in enumerate(["Teff", "Meta", "logg", "L", "log10_L"], start=9):
        if i == 12: 
            continue

        if xcol in df.columns and df[xcol].notna().sum() >= 3:
            xlabel = {
                "Teff": r"$T_{eff}$ [K]",
                "Meta": "[Fe/H]",
                "logg": r"$\log g$",
                "L": r"$L$ [$L_\odot$]",
                "log10_L": r"$\log_{10}(L/L_\odot)$",
            }[xcol]
            scatter_with_fit(
                df, xcol, "frac_residual",
                xlabel, r"$(M_{pred}-M_{true})/M_{true}$",
                f"Fractional mass residual vs {xcol} before mass cut",
                plots / f"{i:02d}_fractional_residual_vs_{xcol}_before_mass_cut.png",
                color_by="log10_oblateness",
            )


def robust_feature_mask(df: pd.DataFrame) -> pd.Series:
    mask = pd.Series(True, index=df.index)
    missing_cols = [col for col in ROBUST_FEATURE_RANGES if col not in df.columns]
    if missing_cols:
        raise ValueError(f"ROBUST=True requires columns: {missing_cols}")

    for col, (lo, hi) in ROBUST_FEATURE_RANGES.items():
        mask &= np.isfinite(df[col])
        mask &= df[col].between(lo, hi, inclusive="both")

    return mask


def _two_sided_p_value(t_value: float, df_resid: int) -> float:
    if not np.isfinite(t_value) or df_resid <= 0:
        return np.nan
    if stats is not None:
        return 2.0 * stats.t.sf(abs(t_value), df_resid)
    return math.erfc(abs(t_value) / math.sqrt(2.0))


def _critical_value(df_resid: int) -> float:
    if df_resid <= 0:
        return np.nan
    if stats is not None:
        return stats.t.ppf(0.975, df_resid)
    return 1.96


def hc3_regression_table(df: pd.DataFrame, response: str, predictors: list[str]) -> pd.DataFrame:
    cols = [response] + predictors
    sub = df[cols].replace([np.inf, -np.inf], np.nan).dropna().copy()

    rows = []
    n = len(sub)
    if n == 0:
        return pd.DataFrame(rows)

    usable_predictors = []
    standardized = pd.DataFrame(index=sub.index)
    for predictor in predictors:
        mean = sub[predictor].mean()
        std = sub[predictor].std(ddof=0)
        if not np.isfinite(std) or std == 0.0:
            continue
        standardized[predictor] = (sub[predictor] - mean) / std
        usable_predictors.append(predictor)

    if not usable_predictors:
        return pd.DataFrame(rows)

    y = sub[response].to_numpy(float)
    X_pred = standardized[usable_predictors].to_numpy(float)
    X = np.column_stack([np.ones(n), X_pred])
    names = ["intercept"] + usable_predictors

    rank = np.linalg.matrix_rank(X)
    if n <= rank:
        return pd.DataFrame(rows)

    xtx_inv = np.linalg.pinv(X.T @ X)
    beta = xtx_inv @ X.T @ y
    fitted = X @ beta
    resid = y - fitted
    h = np.sum((X @ xtx_inv) * X, axis=1)
    denom = np.clip(1.0 - h, 1e-12, None)
    omega = (resid / denom) ** 2
    cov_hc3 = xtx_inv @ (X.T @ (X * omega[:, None])) @ xtx_inv
    se = np.sqrt(np.clip(np.diag(cov_hc3), 0.0, np.inf))

    df_resid = n - rank
    tcrit = _critical_value(df_resid)
    ss_res = np.sum(resid ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    r_squared = 1.0 - ss_res / ss_tot if ss_tot > 0 else np.nan

    for name, coef, std_err in zip(names, beta, se):
        t_value = coef / std_err if std_err > 0 else np.nan
        rows.append({
            "response": response,
            "predictor": name,
            "coefficient": coef,
            "std_error_HC3": std_err,
            "p_value": _two_sided_p_value(t_value, df_resid),
            "ci95_low": coef - tcrit * std_err if np.isfinite(tcrit) else np.nan,
            "ci95_high": coef + tcrit * std_err if np.isfinite(tcrit) else np.nan,
            "n": n,
            "df_resid": df_resid,
            "r_squared": r_squared,
            "predictors_standardized": name != "intercept",
        })

    return pd.DataFrame(rows)


def multivariable_regression_table(df: pd.DataFrame) -> pd.DataFrame:
    tables = [
        hc3_regression_table(df, "frac_residual", REGRESSION_PREDICTORS),
        hc3_regression_table(df, "abs_frac_residual", REGRESSION_PREDICTORS),
    ]
    tables = [table for table in tables if not table.empty]
    if not tables:
        return pd.DataFrame()
    return pd.concat(tables, ignore_index=True)


def main() -> None:
    input_path = INPUT_CSV
    outdir = OUTPUT_DIR
    outdir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path)

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    numeric_cols = [c for c in REQUIRED_COLUMNS + OPTIONAL_NUMERIC_COLUMNS if c in df.columns]
    for col in numeric_cols:
        df[col] = robust_to_numeric(df[col])

    symmetric_error(df, "eM1", "eM2", "sigma_M_true")
    symmetric_error(df, "eoblateness1", "eoblateness2", "sigma_oblateness")
    symmetric_error(df, "efill_factor1", "efill_factor2", "sigma_fill_factor")

    # Main residual definitions.
    df["delta_M"] = df["mass_pred"] - df["M"]
    df["sigma_delta_M"] = np.sqrt(df["mass_sigma"] ** 2 + df["sigma_M_true"].fillna(0.0) ** 2)
    df["frac_residual"] = df["delta_M"] / df["M"]

    # Alternative predictive uncertainty estimated directly from posterior quantiles.
    # This is often safer than blindly trusting mass_sigma if mass_sigma comes from
    # a model-specific internal scale or has numerical pathologies.
    if "mass_p16" in df.columns and "mass_p84" in df.columns:
        df["sigma_pred_q68"] = 0.5 * (df["mass_p84"] - df["mass_p16"])
        df["sigma_delta_M_q68"] = np.sqrt(df["sigma_pred_q68"] ** 2 + df["sigma_M_true"].fillna(0.0) ** 2)
        df["z_M_q68"] = df["delta_M"] / df["sigma_delta_M_q68"]
        df["ci68_contains_M_true"] = (df["M"] >= df["mass_p16"]) & (df["M"] <= df["mass_p84"])
    else:
        df["sigma_pred_q68"] = np.nan
        df["sigma_delta_M_q68"] = np.nan
        df["z_M_q68"] = np.nan
        df["ci68_contains_M_true"] = False

    if "mass_p02_5" in df.columns and "mass_p97_5" in df.columns:
        df["ci95_contains_M_true"] = (df["M"] >= df["mass_p02_5"]) & (df["M"] <= df["mass_p97_5"])
    else:
        df["ci95_contains_M_true"] = False

    # Linear uncertainty propagation for f = M_pred/M_true - 1.
    df["sigma_frac_residual"] = np.sqrt(
        (df["mass_sigma"] / df["M"]) ** 2
        + ((df["mass_pred"] * df["sigma_M_true"].fillna(0.0)) / (df["M"] ** 2)) ** 2
    )

    df["z_M"] = df["delta_M"] / df["sigma_delta_M"]

    # Credible-interval residuals, if prediction quantiles are present.
    if "mass_p16" in df.columns and "mass_p84" in df.columns:
        df["delta_M_p16"] = df["mass_p16"] - df["M"]
        df["delta_M_p84"] = df["mass_p84"] - df["M"]
        df["frac_residual_p16"] = df["delta_M_p16"] / df["M"]
        df["frac_residual_p84"] = df["delta_M_p84"] / df["M"]
    if "mass_p02_5" in df.columns and "mass_p97_5" in df.columns:
        df["delta_M_p02_5"] = df["mass_p02_5"] - df["M"]
        df["delta_M_p97_5"] = df["mass_p97_5"] - df["M"]
        df["frac_residual_p02_5"] = df["delta_M_p02_5"] / df["M"]
        df["frac_residual_p97_5"] = df["delta_M_p97_5"] / df["M"]

    df["log10_oblateness"] = np.where(df["oblateness"] > MIN_OBLATENESS, np.log10(df["oblateness"]), np.nan)
    if "fill_factor" in df.columns:
        df["log10_fill_factor"] = np.where(df["fill_factor"] > 0, np.log10(df["fill_factor"]), np.nan)
    if "L" in df.columns:
        df["log10_L"] = np.where(df["L"] > 0, np.log10(df["L"]), np.nan)

    # Keep only rows that can answer the core science question.
    core_cols = ["M", "mass_pred", "mass_sigma", "oblateness", "log10_oblateness", "delta_M", "frac_residual", "z_M"]
    clean = df[finite_mask(df, core_cols)].copy()

    clean["abs_delta_M"] = clean["delta_M"].abs()
    clean["abs_frac_residual"] = clean["frac_residual"].abs()
    clean["abs_z_M"] = clean["z_M"].abs()
    clean["flag_abs_z_gt_2"] = clean["abs_z_M"] > 2
    clean["flag_abs_z_gt_3"] = clean["abs_z_M"] > 3

    pretrim_n = len(clean)
    make_pretrim_plots(clean, outdir)

    mass_window_mask = clean["M"].between(MASS_MIN, MASS_MAX, inclusive="both")
    clean = clean[mass_window_mask].copy()
    mass_window_n = len(clean)

    robust_n_before = len(clean)
    robust_n_after = len(clean)
    if ROBUST:
        robust_mask = robust_feature_mask(clean)
        clean = clean[robust_mask].copy()
        robust_n_after = len(clean)

    if clean.empty:
        raise ValueError("No rows remain after the mass-window and robust filters.")

    # Export full residual table.
    residual_path = outdir / "EB_mass_residuals_with_oblateness.csv"
    clean.to_csv(residual_path, index=False)

    # Correlation and linear-fit summaries.
    xcols = ["log10_oblateness"]
    if "fill_factor" in clean.columns:
        xcols += ["fill_factor", "log10_fill_factor"]
    for maybe in ["M", "Teff", "Meta", "logg", "L", "log10_L"]:
        if maybe in clean.columns:
            xcols.append(maybe)

    ycols = ["delta_M", "frac_residual", "z_M", "z_M_q68"]
    corr = correlation_rows(clean, ycols=ycols, xcols=xcols)
    corr.to_csv(outdir / "EB_residual_correlation_summary.csv", index=False)

    regression = multivariable_regression_table(clean)
    regression_path = outdir / "EB_multivariable_regression_HC3.csv"
    regression.to_csv(regression_path, index=False)

    # Bin by oblateness. Quantile bins are more stable than fixed-width bins for skewed o.
    n_bins = min(6, max(2, clean["log10_oblateness"].nunique()))
    clean["oblateness_bin"] = pd.qcut(clean["log10_oblateness"], q=n_bins, duplicates="drop")
    binned = (
        clean.groupby("oblateness_bin", observed=True)
        .agg(
            n=("frac_residual", "size"),
            log10_o_min=("log10_oblateness", "min"),
            log10_o_max=("log10_oblateness", "max"),
            o_median=("oblateness", "median"),
            frac_residual_mean=("frac_residual", "mean"),
            frac_residual_median=("frac_residual", "median"),
            frac_residual_std=("frac_residual", "std"),
            delta_M_mean=("delta_M", "mean"),
            delta_M_median=("delta_M", "median"),
            z_M_median=("z_M", "median"),
            fill_factor_median=("fill_factor", "median") if "fill_factor" in clean.columns else ("M", "median"),
        )
        .reset_index()
    )
    binned.to_csv(outdir / "EB_residual_binned_by_oblateness.csv", index=False)

    # Outlier tables.
    id_cols = [c for c in ["SIMBAD_ID", "catalog", "class", "type", "mode", "detached", "well_detached"] if c in clean.columns]
    core_export_cols = id_cols + [
        "M", "sigma_M_true", "mass_pred", "mass_sigma", "delta_M", "frac_residual",
        "sigma_frac_residual", "z_M", "sigma_pred_q68", "z_M_q68", "ci68_contains_M_true", "ci95_contains_M_true", "oblateness", "log10_oblateness",
        "fill_factor", "Teff", "Meta", "logg", "L",
    ]
    core_export_cols = [c for c in core_export_cols if c in clean.columns]
    clean.sort_values("abs_frac_residual", ascending=False)[core_export_cols].head(TOP_N).to_csv(
        outdir / "EB_top_outliers_by_abs_frac_residual.csv", index=False
    )
    clean.sort_values("abs_z_M", ascending=False)[core_export_cols].head(TOP_N).to_csv(
        outdir / "EB_top_outliers_by_abs_zM.csv", index=False
    )
    if "z_M_q68" in clean.columns:
        clean["abs_z_M_q68"] = clean["z_M_q68"].abs()
        clean.sort_values("abs_z_M_q68", ascending=False)[core_export_cols].head(TOP_N).to_csv(
            outdir / "EB_top_outliers_by_abs_zM_q68.csv", index=False
        )

    make_plots(clean, outdir)
    plot_bins_path = outdir / "EB_plot_binned_residuals_vs_log10_oblateness.csv"
    pretrim_plot_bins_path = outdir / "EB_plot_binned_residuals_vs_log10_oblateness_before_mass_cut.csv"

    # Compact text report.
    summary_lines = []
    summary_lines.append(f"Input file: {input_path}")
    summary_lines.append(f"Input rows: {len(df)}")
    summary_lines.append(f"Rows usable before mass cut: {pretrim_n}")
    summary_lines.append(f"Pre-mass-cut plots directory: {(outdir / 'plots_before_mass_cut').resolve()}")
    summary_lines.append(f"Mass window: {MASS_MIN:.3f} <= M <= {MASS_MAX:.3f} solar masses")
    summary_lines.append(f"Rows after mass window: {mass_window_n}")
    summary_lines.append(f"ROBUST: {ROBUST}")
    if ROBUST:
        summary_lines.append(f"Rows before robust cut: {robust_n_before}")
        summary_lines.append(f"Rows after robust cut: {robust_n_after}")
        for col, (lo, hi) in ROBUST_FEATURE_RANGES.items():
            summary_lines.append(f"  robust {col}: {lo:g} <= {col} <= {hi:g}")
    summary_lines.append(f"Rows used for final residual-vs-oblateness analysis: {len(clean)}")
    summary_lines.append("")
    summary_lines.append("Residual definitions:")
    summary_lines.append("  delta_M = mass_pred - M")
    summary_lines.append("  frac_residual = (mass_pred - M) / M")
    summary_lines.append("  sigma_delta_M = sqrt(mass_sigma^2 + sigma_M_true^2)")
    summary_lines.append("  z_M = delta_M / sigma_delta_M")
    summary_lines.append("")
    for col in ["delta_M", "frac_residual", "z_M", "z_M_q68", "oblateness", "fill_factor", "sigma_pred_q68", "mass_sigma"]:
        if col in clean.columns and clean[col].notna().any():
            s = clean[col].dropna()
            summary_lines.append(
                f"{col}: n={len(s)}, mean={s.mean():.6g}, median={s.median():.6g}, "
                f"std={s.std():.6g}, min={s.min():.6g}, max={s.max():.6g}"
            )
    summary_lines.append("")
    if "ci68_contains_M_true" in clean.columns:
        summary_lines.append(f"68% interval coverage: {clean['ci68_contains_M_true'].mean():.3f}")
    if "ci95_contains_M_true" in clean.columns:
        summary_lines.append(f"95% interval coverage: {clean['ci95_contains_M_true'].mean():.3f}")
    summary_lines.append("")
    summary_lines.append("Most relevant correlations:")
    key_corr = corr[(corr["x"].isin(["log10_oblateness", "fill_factor", "log10_fill_factor"])) & (corr["y"] == "frac_residual")]
    summary_lines.append(key_corr.to_string(index=False))
    summary_lines.append("")
    summary_lines.append("Multivariable regression:")
    summary_lines.append("  Responses: frac_residual and abs_frac_residual")
    summary_lines.append("  Predictors are standardized before fitting; standard errors are HC3 robust.")
    summary_lines.append(f"  Table: {regression_path.resolve()}")
    summary_lines.append("")
    summary_lines.append("Plot-bin statistics:")
    summary_lines.append(f"  Final plot bins: {plot_bins_path.resolve()}")
    summary_lines.append(f"  Pre-mass-cut plot bins: {pretrim_plot_bins_path.resolve()}")

    report_path = outdir / "README_analysis_summary.txt"
    report_path.write_text("\n".join(summary_lines), encoding="utf-8")

    print("Analysis complete.")
    print(f"Output directory: {outdir.resolve()}")
    print(f"Residual table: {residual_path.resolve()}")
    print(f"Regression table: {regression_path.resolve()}")
    print(f"Plot-bin table: {plot_bins_path.resolve()}")
    print(f"Pre-mass-cut plot-bin table: {pretrim_plot_bins_path.resolve()}")
    print(f"Plots directory: {(outdir / 'plots').resolve()}")
    print(f"Pre-mass-cut plots directory: {(outdir / 'plots_before_mass_cut').resolve()}")
    print(f"Usable rows before mass cut: {pretrim_n} / {len(df)}")
    print(f"Rows after {MASS_MIN:.3f}-{MASS_MAX:.3f} solar-mass cut: {mass_window_n}")
    if ROBUST:
        print(f"Rows left by ROBUST=True feature-range cut: {robust_n_after} / {robust_n_before}")
    else:
        print("ROBUST=False; feature-range cut was not applied.")
    print(f"Final usable rows: {len(clean)} / {len(df)}")


if __name__ == "__main__":
    main()
