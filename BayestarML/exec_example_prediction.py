#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  5 18:53:33 2025

@author: LamirelFamily
"""

from pathlib import Path

import pandas as pd

from constants import BHS_MASS_PRED_PATH, BHS_MASS_WEIGHTS_PATH, TARGET
from predict import predict3


def main():
    print("Evaluating BHS on 20% holdout test set...")
    base_preds, bhs_pred_test, bhs_w_test = predict3(None, None, TARGET, test=True)

    output_dir = Path(BHS_MASS_PRED_PATH).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    pd.DataFrame({
        "bhs_mean": bhs_pred_test.mean(0),
        "bhs_std": bhs_pred_test.std(0),
    }).to_csv(BHS_MASS_PRED_PATH, index=False)

    pd.DataFrame(
        bhs_w_test.mean(0),
        columns=["w_bart", "w_hbnn", "w_gp"],
    ).to_csv(BHS_MASS_WEIGHTS_PATH, index=False)

    print(f"Saved BHS predictions to {BHS_MASS_PRED_PATH}")
    print(f"Saved BHS weights to {BHS_MASS_WEIGHTS_PATH}")
    print("\n--- Evaluation Complete ---")


    

    
if __name__ == '__main__':
    main()
