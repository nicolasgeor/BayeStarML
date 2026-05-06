#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  5 18:53:33 2025

@author: LamirelFamily
"""

from constants import TARGET
from predict import predict3


def main():
    print("Evaluating BHS on 20% holdout test set...")
    base_preds, bhs_pred_test, bhs_w_test = predict3(None, None, TARGET, test=True)

    print("\n--- Evaluation Complete ---")


    

    
if __name__ == '__main__':
    main()
