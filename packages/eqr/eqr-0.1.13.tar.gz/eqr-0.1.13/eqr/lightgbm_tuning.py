import lightgbm as lgb
import numpy as np

import optuna


# 1. Define an objective function to be maximized.
def objective(trial, X, y, alpha, random_state, nfold=5, verbose=-1, num_threads=0):
    train_data = lgb.Dataset(X, label=y)

    params = {
        "objective": "quantile",
        "alpha": alpha,
        "metric": "quantile",
        "num_boost_round": trial.suggest_int("num_boost_round", 100, 400),
        # "max_depth": trial.suggest_int("max_depth", 3, 10),
        "num_leaves": trial.suggest_int("num_leaves", 31, 3100),
        # "learning_rate": trial.suggest_float("learning_rate", 1e-4, 1e-2, log=True),
        "verbose": verbose,
        "min_data_in_leaf": trial.suggest_int("min_data_in_leaf", 1, 100),
        "seed": random_state,
        "num_threads": num_threads,
    }

    cv_results = lgb.cv(
        params=params,
        train_set=train_data,
        nfold=nfold,
        stratified=False,  # needed for regression?
        # shuffle=False,
    )

    score = cv_results["valid quantile-mean"][-1]  # is this correct?

    return score


def optimise_quantile_regressor(
    X, y, alpha, n_trials, random_state=42, nfold=5, verbose=-1, num_threads=0
):
    # Create a study object
    study = optuna.create_study(direction="minimize")

    # Run the optimization process
    optuna.logging.set_verbosity(optuna.logging.WARNING)
    study.optimize(
        lambda trial: objective(trial, X, y, alpha, random_state, nfold, verbose),
        n_trials=n_trials,
        show_progress_bar=True,
        # n_jobs=4,
    )

    # Print the best hyperparameters and score
    # print("Best hyperparameters:", study.best_params)
    # print("Best score:", study.best_value)

    # train model with all data and best parameters

    train_data = lgb.Dataset(X, label=y)

    params = study.best_params.copy()
    params.update(
        {
            "objective": "quantile",
            "alpha": alpha,
            "metric": "quantile",
            "seed": random_state,
            "verbose": verbose,
            "num_threads": num_threads,
        }
    )

    # Train the model
    model = lgb.train(
        params=params,
        train_set=train_data,
    )

    # return model, study
    return model
