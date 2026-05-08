#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 15:45:46 2025

@author: LamirelFamily
"""

from pathlib import Path

import numpy as np
import pandas as pd


MISSING_TOKENS = {"", "NA", "nan", "NaN", "None"}

COLUMN_ALIASES = {
    "SIMBAD_ID": ["SIMBAD_ID", "ID"],
    "Meta": ["Meta", "Fe/H"],
    "eMeta1": ["eMeta1", "e1_Fe/H"],
    "eMeta2": ["eMeta2", "e2_Fe/H"],
    "catalog": ["catalog", "source"],
}

NUMERIC_COLUMNS = {
    "Seq",
    "M",
    "eM1",
    "eM2",
    "R",
    "eR1",
    "eR2",
    "Teff",
    "eTeff1",
    "eTeff2",
    "L",
    "eL1",
    "eL2",
    "Meta",
    "eMeta1",
    "eMeta2",
    "logg",
    "elogg1",
    "elogg2",
    "rho",
    "erho1",
    "erho2",
    "e_M",
    "e_R",
    "e_Teff",
    "e_L",
    "orbit_a",
    "eOrbit_a",
    "R/a",
    "database",
    "logg_from_M,R",
    "L_from_SB",
    "oblateness",
    "eoblateness1",
    "eoblateness2",
    "fill_factor",
    "efill_factor1",
    "efill_factor2",
}

ERROR_PERCENT_SPECS = {
    "e_M": ("M", "eM1", "eM2"),
    "e_R": ("R", "eR1", "eR2"),
    "e_Teff": ("Teff", "eTeff1", "eTeff2"),
    "e_L": ("L", "eL1", "eL2"),
}

FEATURE_ERROR_SIDES = {
    "Teff": ("eTeff1", "eTeff2"),
    "Meta": ("eMeta1", "eMeta2"),
    "rho": ("erho1", "erho2"),
}

TARGET_COLUMN = {
    "mass": "M",
    "radius": "R",
}

TARGET_ERROR_SIDES = {
    "mass": ("eM1", "eM2"),
    "radius": ("eR1", "eR2"),
}


def _find_table_header_line(path):
    with open(path, "r", encoding="utf-8-sig") as handle:
        for lineno, line in enumerate(handle):
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                return lineno
    raise ValueError(f"No table header found in {path}.")


def read_stellar_table(data_file):
    """
    Read old or database2026-style tab-separated stellar tables.

    Comment/header text before the real table is ignored by detecting the first
    non-empty, non-comment line. Values are initially read as strings with empty
    strings preserved, then normalized into pandas missing values.
    """
    data_path = Path(data_file)
    header_line = _find_table_header_line(data_path)
    raw = pd.read_csv(
        data_path,
        sep="\t",
        skiprows=header_line,
        dtype=str,
        keep_default_na=False,
    )
    raw.columns = [str(col).strip() for col in raw.columns]
    raw = raw.apply(lambda col: col.str.strip() if col.dtype == object else col)
    return raw.replace(list(MISSING_TOKENS), np.nan)


def _first_present_column(df, candidates):
    for candidate in candidates:
        if candidate in df.columns:
            return candidate
    return None


def _to_numeric(series):
    as_text = series.astype("string").str.strip().str.replace(",", ".", regex=False)
    return pd.to_numeric(as_text, errors="coerce")


def _mean_abs_error(row, err1_col, err2_col):
    values = []
    for col in (err1_col, err2_col):
        if col in row.index and pd.notna(row[col]):
            value = abs(row[col])
            if np.isfinite(value) and value > 0:
                values.append(value)
    if not values:
        return np.nan
    return float(np.mean(values))


def _percentage_error(row, value_col, err1_col, err2_col):
    if value_col not in row.index or pd.isna(row[value_col]):
        return np.nan
    value = row[value_col]
    if not np.isfinite(value) or value == 0:
        return np.nan
    error = _mean_abs_error(row, err1_col, err2_col)
    if pd.isna(error):
        return np.nan
    return 100.0 * error / abs(value)


def standardize_stellar_columns(raw):
    """
    Convert raw table columns to the canonical names expected by the ML code.

    Returns
    -------
    df : pandas.DataFrame
        DataFrame with canonical aliases added and numeric columns converted.
    summary : dict
        Information about mapped and generated columns.
    """
    df = raw.copy()
    mapped_columns = {}
    generated_columns = []

    for canonical, candidates in COLUMN_ALIASES.items():
        if canonical in df.columns:
            continue
        source = _first_present_column(df, candidates)
        if source is not None:
            df[canonical] = df[source]
            mapped_columns[canonical] = source

    for column in sorted(NUMERIC_COLUMNS.intersection(df.columns)):
        df[column] = _to_numeric(df[column])

    for out_col, (value_col, err1_col, err2_col) in ERROR_PERCENT_SPECS.items():
        if out_col not in df.columns and {value_col, err1_col, err2_col}.issubset(df.columns):
            df[out_col] = df.apply(
                _percentage_error,
                axis=1,
                value_col=value_col,
                err1_col=err1_col,
                err2_col=err2_col,
            )
            generated_columns.append(out_col)

    return df, {
        "mapped_columns": mapped_columns,
        "generated_columns": generated_columns,
    }


def _required_columns_for_model(features, target):
    if target not in TARGET_COLUMN:
        raise ValueError(f"Unsupported target {target!r}. Known targets: {sorted(TARGET_COLUMN)}")

    required = ["class", TARGET_COLUMN[target], *TARGET_ERROR_SIDES[target]]
    for feature in features:
        required.append(feature)
        required.extend(FEATURE_ERROR_SIDES.get(feature, ()))
    return list(dict.fromkeys(required))


def _validate_columns(df, required_columns, data_file):
    missing = [column for column in required_columns if column not in df.columns]
    if missing:
        if "cutoff" in missing or "pla" in missing:
            raise ValueError(
                f"{data_file} is missing required columns {missing}. The new database "
                "does not contain cutoff/pla; their derivation must be defined before "
                "they can be used."
            )
        raise ValueError(f"{data_file} is missing required columns: {missing}")


def load_stellar_dataframe(
    data_file,
    *,
    required_features=None,
    target="mass",
    star_class=None,
    drop_invalid=True,
    verbose=True,
):
    """
    Load a stellar table and validate only the columns needed by the model.
    """
    if required_features is None:
        from constants import FEATURES

        required_features = FEATURES

    raw = read_stellar_table(data_file)
    df, mapping_summary = standardize_stellar_columns(raw)
    required_columns = _required_columns_for_model(required_features, target)
    _validate_columns(df, required_columns, data_file)

    rows_loaded = len(df)

    if star_class is not None:
        df = df[df["class"] == star_class].copy()
    rows_after_class_filter = len(df)

    if drop_invalid:
        df = df.dropna(subset=required_columns).copy()
    rows_usable = len(df)

    summary = {
        "file": str(data_file),
        "rows_loaded": rows_loaded,
        "rows_after_class_filter": rows_after_class_filter,
        "rows_usable": rows_usable,
        "required_columns": required_columns,
        **mapping_summary,
    }

    if verbose:
        mapped = ", ".join(
            f"{source}->{target_col}"
            for target_col, source in summary["mapped_columns"].items()
        ) or "none"
        generated = ", ".join(summary["generated_columns"]) or "none"
        print(
            f"Loaded {data_file}: {rows_loaded} rows; "
            f"class={star_class or 'all'} -> {rows_after_class_filter}; "
            f"usable -> {rows_usable}. Mapped: {mapped}. Generated: {generated}."
        )

    return df, summary


def get_dataset(data_file, star_class, *, features=None, target="mass", return_summary=False, verbose=True):
    """
    Load and clean a stellar dataset for the selected model inputs.

    Supports both the old tab-separated format and the database2026 format with
    a leading comment block and decimal commas.
    """
    df, summary = load_stellar_dataframe(
        data_file,
        required_features=features,
        target=target,
        star_class=star_class,
        drop_invalid=True,
        verbose=verbose,
    )

    if return_summary:
        return df, summary
    return df


def find_pointwise_loo(trace):
    """
    Compute pointwise leave-one-out (LOO) log predictive densities.
    """
    import arviz as az

    return az.loo(trace, pointwise=True, scale="log").loo_i.values


def train(model, filename, draw=1000, chains=2, target_accept=0.95):
    """
    Sample from a PyMC model and save the posterior trace.
    """
    import pymc as pm

    print("target_accept=", target_accept)
    trace = pm.sample(
        draws=draw,
        tune=draw,
        chains=chains,
        model=model,
        target_accept=target_accept,
    )
    trace.extend(pm.compute_log_likelihood(trace, model=model, var_names="y"))
    trace.to_netcdf(filename)

    return trace


def mard(y_true, y_pred):
    """
    Compute the mean absolute relative difference (MARD) in percent.
    """
    relative_diff = np.abs((np.array(y_true) - np.array(y_pred)) / np.array(y_true))
    return np.mean(relative_diff) * 100


def mrd(y_true, y_pred):
    """
    Compute the mean relative difference (MRD) in percent.
    """
    relative_diff = (np.array(y_true) - np.array(y_pred)) / np.array(y_true)
    return np.mean(relative_diff) * 100
