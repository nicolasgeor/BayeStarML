#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
One-button pipeline for the 4-feature Dataset D models.

Edit the SETTINGS block below and run:   python run_pipeline.py

Steps, in this order:
    train_gp      Train the GP on the asteroseismic (mode A) stars; holdout TSV + plots.
    train_hbnn    Same for the HBNN.
    holdout_eval  (optional) Train BART and stack the three models on the holdout set; prints MARD/MRD.
    predict       Train BART, stack GP + HBNN + BART with BHS and predict the EB stars -> CSV.
    analysis      Residuals vs oblateness of those predictions -> tables and plots.

Every file name is built from the settings by RunConfig, so nothing has to be renamed by hand.
To redo only some steps (e.g. re-run the analysis of an earlier run), switch the others off:
the remaining steps then read the files written earlier with the same settings.
"""

import os
import time
from dataclasses import asdict, dataclass

import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

from constants import MU, SIGMA
from preprocess import return_train_test, TARGET_COLUMNS
from utils import get_dataset
import analyse_eb_mass_oblateness_residuals
import analyse_eb_radius_oblateness_residuals
import exec_example_prediction
import exec_example_train

#######################################################################################
# SETTINGS
#######################################################################################
TARGET_VAR = "radius"   # "radius" or "mass"

SEED = 146             # MCMC seed for GP, HBNN and BART; it is the "seed_N" in every file name
SPLIT_SEED = 146      # train/test split seed (seed 239 used 4159; seeds 2805 and 2695 used 5732).
                        # Not part of the file names, so it is stored in the GP/HBNN traces and
                        # checked before they are reused
DRAWS = 3000            # draws per chain (and as many tuning steps) for GP, HBNN and BART
CHAINS = 4

HBNN_NODES = 15
GP_N_INDUCING_MEAN = 100
GP_N_INDUCING_VAR = 50
BHS_DRAWS = 3000         # per chain; the stacked predictions use BHS_DRAWS * BHS_CHAINS draws
BHS_CHAINS = 4

NOISE_MODEL = "floor"   # How BART and the HBNN treat the noise of the target. The GP is the same in all three.
                        #   "floor": inferred, but never below the measurement error of each star:
                        #            sqrt(inferred² + measurement error of the target²). The HBNN draws include their noise.
                        #   "fixed": radius only, as in the original code: HBNN noise fixed at 0.15 (HBNN_R4) and
                        #            BART noise fixed at 0.3 (BART_R), in normalised units. Nothing is inferred.
                        #   "free":  as in the runs up to October 2026: HBNN noise inferred with no lower limit
                        #            (for radius its chains do not converge); BART inferred for mass, 0.3 for radius.
                        # Files carry "floor" or "fixed" in their names; "free" keeps the names of the earlier runs.
                        # Decided 2026-11-15: use "floor" for radius and "free" for mass.

# Steps to run. A step that is off is skipped, and later steps use the files it wrote before.
RUN_TRAIN_GP = False
RUN_TRAIN_HBNN = True
RUN_HOLDOUT_EVAL = True
RUN_PREDICT = True
RUN_ANALYSIS = True

SHOW_PLOTS = False      # True pops up plots and pauses the run until each window is closed

# Data and output locations 
DATABASE = "Datasets/database_D_merged.txt"             # training stars: class MS, mode A
PREDICTION_DATABASE = "Datasets/database_D_merged.txt"  # stars to predict
PREDICTION_MODE = "EB"          # e.g. "A", "EB", or None for all modes
PREDICTION_STAR_CLASS = None    # e.g. "MS", "RGB", or None for all classes
TRAINING_DIR = "Dataset_D_v4_training"
PREDICTIONS_DIR = "Dataset_D_different_predictions"
#######################################################################################

STEP_ORDER = ("train_gp", "train_hbnn", "holdout_eval", "predict", "analysis")


@dataclass(frozen=True)
class RunConfig:
    """All settings of one run, plus the file names every step shares."""
    target: str
    seed: int
    split_seed: int
    draws: int
    chains: int
    hbnn_nodes: int
    gp_n_inducing_mean: int
    gp_n_inducing_var: int
    bhs_draws: int
    bhs_chains: int
    noise_model: str
    show_plots: bool
    database: str
    prediction_database: str
    prediction_mode: str | None
    prediction_star_class: str | None
    training_dir: str
    predictions_dir: str

    @property
    def abbr(self):
        return 'rad' if self.target == 'radius' else 'mass'

    @property
    def noise_floor(self):
        return self.noise_model == 'floor'

    @property
    def noise_tag(self):
        """In the name of every file that depends on NOISE_MODEL, so a run never overwrites one made with another setting."""
        return '' if self.noise_model == 'free' else f'_{self.noise_model}'

    def model_string(self, model):
        """Base name of a GP/HBNN trace and of its plots."""
        if model == 'GP':
            return (f"GP_{self.abbr}_4param_L_{self.draws}_draws_{self.chains}_chains_"
                    f"{self.gp_n_inducing_mean}_{self.gp_n_inducing_var}_seed_{self.seed}")
        if model == 'HBNN':
            # "sig_015" is only a label kept so names match the earlier ("free") runs, whose HBNN inferred its noise.
            # The other two settings use their own name as the label
            noise_label = 'sig_015' if self.noise_model == 'free' else self.noise_model
            return (f"HBNN_{self.abbr}_4param_L_{self.draws}_draws_{self.chains}_chains_"
                    f"{self.hbnn_nodes}_nodes_{noise_label}_seed_{self.seed}")
        raise ValueError("model must be 'GP' or 'HBNN'")

    def trace_path(self, model):
        return f"{self.training_dir}/{self.model_string(model)}.nc"

    def test_results_path(self, model):
        tag = self.noise_tag if model == 'HBNN' else ''   # the GP does not depend on NOISE_MODEL
        return f"{self.training_dir}/{self.target}_prediction_results_{model}{tag}_{self.draws}_seed_{self.seed}.tsv"

    # stage is "prediction" (stars of PREDICTION_DATABASE) or "holdout" (test set)
    def bart_trace_path(self, stage):
        return (f"{self.training_dir}/BART_{self.abbr}_4param_L_{stage}_{self.draws}_draws_{self.chains}_chains"
                f"{self.noise_tag}_seed_{self.seed}.nc")

    def bart_predictions_path(self, stage):
        return (f"{self.training_dir}/BART_{self.abbr}_4param_L_{stage}_{self.draws}_draws_{self.chains}_chains_"
                f"predictions{self.noise_tag}_seed_{self.seed}.nc")

    def bhs_trace_path(self, stage):
        # Named after DRAWS like earlier runs, although BHS itself samples BHS_DRAWS per chain
        return (f"{self.training_dir}/BHS_{self.abbr}_4param_L_{stage}_{self.draws}_draws_{self.chains}_chains"
                f"{self.noise_tag}_seed_{self.seed}.nc")

    def holdout_plot_base(self, model):
        return f"{self.training_dir}/{model}_{self.abbr}_4param_L_holdout{self.noise_tag}_seed_{self.seed}"

    @property
    def eb_predictions_path(self):
        return (f"{self.predictions_dir}/EB_oblateness_fill_factor_{self.target}_predictions_4_features_"
                f"{self.draws}_draws{self.noise_tag}_seed_{self.seed}.csv")

    @property
    def analysis_dir(self):
        return f"{self.predictions_dir}/seed_{self.seed}_{self.target}_residuals{self.noise_tag}"


def build_config():
    if TARGET_VAR not in ("radius", "mass"):
        raise ValueError("TARGET_VAR must be 'radius' or 'mass'")
    if NOISE_MODEL not in ("floor", "fixed", "free"):
        raise ValueError("NOISE_MODEL must be 'floor', 'fixed' or 'free'")
    if NOISE_MODEL == "fixed" and TARGET_VAR != "radius":
        raise ValueError("NOISE_MODEL = 'fixed' exists only for radius: the original code has no fixed-noise mass models")
    return RunConfig(
        target=TARGET_VAR, seed=SEED, split_seed=SPLIT_SEED, draws=DRAWS, chains=CHAINS,
        hbnn_nodes=HBNN_NODES, gp_n_inducing_mean=GP_N_INDUCING_MEAN, gp_n_inducing_var=GP_N_INDUCING_VAR,
        bhs_draws=BHS_DRAWS, bhs_chains=BHS_CHAINS, noise_model=NOISE_MODEL, show_plots=SHOW_PLOTS,
        database=DATABASE, prediction_database=PREDICTION_DATABASE,
        prediction_mode=PREDICTION_MODE, prediction_star_class=PREDICTION_STAR_CLASS,
        training_dir=TRAINING_DIR, predictions_dir=PREDICTIONS_DIR,
    )


def check_trace_split(path, split_seed, noise_model=None):
    """
    Stop if a saved GP/HBNN trace was trained on a different train/test split or, for the HBNN
    (noise_model given), with another NOISE_MODEL setting.
    """
    with xr.open_dataset(path, group="posterior") as posterior:
        recorded = posterior.attrs.get("split_seed")
        recorded_noise = posterior.attrs.get("noise_model")
        if recorded_noise is None:
            # Older traces: the first "floor" runs stored noise_floor = 1; before that nothing was stored ("free")
            recorded_noise = 'floor' if int(posterior.attrs.get("noise_floor", 0)) else 'free'
    if recorded is None:
        print(f"WARNING: {path} does not record its split seed (it was trained before run_pipeline.py). "
              f"Make sure it was trained with SPLIT_SEED = {split_seed}.")
    elif int(recorded) != split_seed:
        raise ValueError(f"{path} was trained with SPLIT_SEED = {recorded}, but SPLIT_SEED = {split_seed} now. "
                         f"Use the same split seed, or retrain that model.")
    if noise_model is not None and recorded_noise != noise_model:
        raise ValueError(f"{path} was trained with NOISE_MODEL = '{recorded_noise}', but NOISE_MODEL = '{noise_model}' now. "
                         f"Use the same setting, or retrain that model.")


def preflight(cfg, steps):
    """Fail fast, before hours of sampling, if a step needs a file that no earlier step will write."""
    needed = []
    if "holdout_eval" in steps or "predict" in steps:
        for model, train_step in (("GP", "train_gp"), ("HBNN", "train_hbnn")):
            if train_step not in steps:
                needed.append(cfg.trace_path(model))
    if "analysis" in steps and "predict" not in steps:
        needed.append(cfg.eb_predictions_path)

    missing = [path for path in needed if not os.path.exists(path)]
    if missing:
        raise FileNotFoundError("These files are needed but do not exist (switch on the step that "
                                "writes them, or check the settings):\n  " + "\n  ".join(missing))

    for path in needed:
        if path.endswith(".nc"):
            is_hbnn = path == cfg.trace_path("HBNN")
            check_trace_split(path, cfg.split_seed, noise_model=cfg.noise_model if is_hbnn else None)


def set_target_normalisation(cfg):
    """
    Set the target's mean/std (constants.MU / SIGMA, used to turn predictions back into solar
    units) to those of this run's training split, so they always match SPLIT_SEED.
    Same calculation as in preprocess.return_train_test.
    """
    df = get_dataset(cfg.database, "MS")
    df = df[df["mode"] == "A"]
    _, _, Y_train, _ = return_train_test(df, normalised=False, random_state=cfg.split_seed)
    y = Y_train[TARGET_COLUMNS[cfg.target][0]]
    MU[cfg.target] = np.mean(y)
    SIGMA[cfg.target] = np.std(y)
    print(f"Target normalisation from the training split (SPLIT_SEED = {cfg.split_seed}): "
          f"{cfg.target} mean = {MU[cfg.target]}, std = {SIGMA[cfg.target]}")


def run_analysis(cfg):
    analysis = (analyse_eb_radius_oblateness_residuals if cfg.target == "radius"
                else analyse_eb_mass_oblateness_residuals)
    analysis.main(input_path=cfg.eb_predictions_path, output_dir=cfg.analysis_dir)


def main(only=None):
    """Run every switched-on step in order; `only` limits the run to some of the steps."""
    cfg = build_config()
    switched_on = {
        "train_gp": RUN_TRAIN_GP,
        "train_hbnn": RUN_TRAIN_HBNN,
        "holdout_eval": RUN_HOLDOUT_EVAL,
        "predict": RUN_PREDICT,
        "analysis": RUN_ANALYSIS,
    }
    steps = [step for step in STEP_ORDER if switched_on[step] and (only is None or step in only)]
    if not steps:
        print("Nothing to run: the requested steps are all switched off in run_pipeline.py.")
        return

    if not cfg.show_plots:
        plt.switch_backend("Agg")

    print("Settings:")
    for key, value in asdict(cfg).items():
        print(f"  {key} = {value}")
    print("Steps:", ", ".join(steps))

    preflight(cfg, steps)
    set_target_normalisation(cfg)

    actions = {
        "train_gp": lambda: exec_example_train.train_and_evaluate(cfg, "GP"),
        "train_hbnn": lambda: exec_example_train.train_and_evaluate(cfg, "HBNN"),
        "holdout_eval": lambda: exec_example_prediction.run_holdout_evaluation(cfg),
        "predict": lambda: exec_example_prediction.run_eb_predictions(cfg),
        "analysis": lambda: run_analysis(cfg),
    }
    pipeline_start = time.time()
    for step in steps:
        print(f"\n{'=' * 30} {step} {'=' * 30}")
        step_start = time.time()
        actions[step]()
        print(f"--- {step} finished in {(time.time() - step_start) / 60:.1f} min")
    print(f"\nPipeline finished in {(time.time() - pipeline_start) / 60:.1f} min.")


if __name__ == "__main__":
    main()
