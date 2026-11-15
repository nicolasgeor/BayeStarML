#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The oblateness trend of each single model next to the stack's, for the two EB analysis scripts.

The stack (BHS) can be led by a different model from one set-up to another, so the trend of the
residual with oblateness is also computed for BART, HBNN and GP on their own. This needs the
per-model columns that exec_example_prediction.build_prediction_table writes ("rad_pred_BART",
"rad_p16_GP", ...); prediction files written before those columns existed give an empty table.
"""

import numpy as np
import pandas as pd
from scipy import stats

MODELS = ("BHS", "BART", "HBNN", "GP")   # BHS is the stack: the columns without a model suffix


def per_model_table(clean, true_col, prefix):
    """
    One row per model, on the stars of `clean` (the final analysis sample).

    clean: the analysis table, with `true_col` ("R" or "M"), "log10_oblateness" and the prediction
    columns. prefix: "rad" or "mass". Returns an empty table if there are no per-model columns.
    """
    if not all(f"{prefix}_pred_{name}" in clean.columns for name in MODELS[1:]):
        return pd.DataFrame()

    true = clean[true_col].to_numpy(float)
    log_o = clean["log10_oblateness"].to_numpy(float)
    rows = []
    for name in MODELS:
        suffix = "" if name == "BHS" else f"_{name}"
        frac = (clean[f"{prefix}_pred{suffix}"].to_numpy(float) - true) / true
        signed = stats.spearmanr(log_o, frac)
        absolute = stats.spearmanr(log_o, np.abs(frac))
        p16, p84 = clean[f"{prefix}_p16{suffix}"].to_numpy(float), clean[f"{prefix}_p84{suffix}"].to_numpy(float)
        p02_5, p97_5 = clean[f"{prefix}_p02_5{suffix}"].to_numpy(float), clean[f"{prefix}_p97_5{suffix}"].to_numpy(float)
        rows.append({
            "model": name,
            "n": len(clean),
            "MARD_percent": 100 * np.mean(np.abs(frac)),
            "median_abs_frac_residual_percent": 100 * np.median(np.abs(frac)),
            "mean_frac_residual_percent": 100 * np.mean(frac),
            "coverage_68": np.mean((true >= p16) & (true <= p84)),
            "coverage_95": np.mean((true >= p02_5) & (true <= p97_5)),
            "median_half_width_68": np.median((p84 - p16) / 2),
            "spearman_rho_frac_residual": signed.statistic,
            "spearman_p_frac_residual": signed.pvalue,
            "spearman_rho_abs_frac_residual": absolute.statistic,
            "spearman_p_abs_frac_residual": absolute.pvalue,
        })
    return pd.DataFrame(rows)
