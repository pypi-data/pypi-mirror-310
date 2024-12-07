import lightgbm as lgb

import optuna


def objective(
    trial,
    X,
    y,
    alpha,
    random_state,
    nfold=5,
    verbose=-1,
    num_threads=0,
    learning_rate=0.1,
):
    train_data = lgb.Dataset(X, label=y)

    params = {
        "objective": "quantile",
        "alpha": alpha,
        "metric": "quantile",
        "num_boost_round": trial.suggest_int("num_boost_round", 10, 200),
        # "max_depth": trial.suggest_int("max_depth", 3, 10),
        "num_leaves": trial.suggest_int("num_leaves", 31, 9100),
        # "learning_rate": trial.suggest_float("learning_rate", 1e-4, 1e-2, log=True),
        "learning_rate": learning_rate,
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
    X,
    y,
    alpha,
    n_trials,
    random_state=42,
    nfold=5,
    verbose=-1,
    num_threads=0,
    learning_rate=0.1,
):
    # Create a study object
    study = optuna.create_study(direction="minimize")

    # Run the optimization process
    optuna.logging.set_verbosity(optuna.logging.WARNING)
    study.optimize(
        lambda trial: objective(
            trial, X, y, alpha, random_state, nfold, verbose, num_threads, learning_rate
        ),
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

    return model, study
