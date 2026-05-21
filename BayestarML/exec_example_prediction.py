#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  5 18:53:33 2025

@author: LamirelFamily
"""

from preprocess import prepare_pred4, prepare_pred3
from predict import predict3, predict4

# For 4 variables
# def main():
#     X, X_er = prepare_pred4("Datasets/dataset_A_trimmed_8cols_NASAFLAG.csv")
#     # will need to change the traces in predict4 if you re-train
#     # trace files aren't included in the github repo due to size
#     _, bhs_pred, w4 = predict4(X, X_er, 'mass', test=True) # disregards X, X_er for test=True / uses test values
#     _, pred, w4 = predict4(X, X_er, 'mass') # make predictions on new data (X, X_er)

#     pred_val = pred.mean(0)
#     pred_err = pred.std(0)



# For 4 variables
def main():
    print("Evaluating Dataset D A-label 4-parameter BHS on 20% holdout test set...")
    # X3, X3_er = prepare_pred3("Datasets/dataset_density_trimmed_6cols_NASAFLAG.csv")
    # will need to change the traces in predict3 if you re-train
    # trace files aren't included in the github repo due to size

    # Benchmark: Evaluates holdout test set, ignores X3, prints MARD/MRD metrics
    # _, bhs_pred, w3 = predict4(X3, X3_er, 'mass', test=True) # disregards X, X_er for test=True / uses test values

    # Inference: Evaluates new dataset, outputs predicted values
    # _, pred, w3 = predict4(X3, X3_er, 'mass') # make predictions on new data (X, X_er)

    # pred_val = pred.mean(0)
    # pred_err = pred.std(0)

    # ChatGPT:
    # Pass None for the data inputs, because test=True overrides them anyway.
    base_preds, bhs_pred_test, bhs_w_test = predict4(None, None, 'mass', test=True)

    print("\n--- Evaluation Complete ---")


    

    
if __name__ == '__main__':
    main()
