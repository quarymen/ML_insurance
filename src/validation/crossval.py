from __future__ import annotations

import logging
from typing import Any, Callable

import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.metrics import get_scorer
from sklearn.model_selection import StratifiedKFold, KFold

logger = logging.getLogger(__name__)


def _make_splitter(y: pd.Series | np.ndarray, k_folds: int, seed: int):
    is_classification = (
        pd.api.types.is_integer_dtype(pd.Series(y))
        and pd.Series(y).nunique() <= 50
    )
    if is_classification:
        return StratifiedKFold(n_splits=k_folds, shuffle=True, random_state=seed)
    return KFold(n_splits=k_folds, shuffle=True, random_state=seed)


def cross_validate_model(
    model: Any,
    X: pd.DataFrame | np.ndarray,
    y: pd.Series | np.ndarray,
    k_folds: int = 3,
    seed: int = 42,
    metric: str = "roc_auc",
    return_oof: bool = False,
) -> dict:
    y_series = pd.Series(y).reset_index(drop=True)
    X_arr = X.reset_index(drop=True) if isinstance(X, pd.DataFrame) else X

    splitter = _make_splitter(y_series, k_folds, seed)
    scorer = get_scorer(metric)

    scores: list[float] = []
    oof_pred = np.full(len(y_series), np.nan, dtype=float)

    for fold_idx, (train_idx, val_idx) in enumerate(splitter.split(X_arr, y_series)):
        X_tr, X_val = X_arr.iloc[train_idx], X_arr.iloc[val_idx]
        y_tr, y_val = y_series.iloc[train_idx], y_series.iloc[val_idx]

        # clone — чтобы каждый фолд обучался с нуля, не таща состояние с прошлого.
        fold_model = clone(model)
        fold_model.fit(X_tr, y_tr)

        score = scorer(fold_model, X_val, y_val)
        scores.append(float(score))
        logger.info("Fold %d/%d: %s=%.5f", fold_idx + 1, k_folds, metric, score)

        if return_oof:
            if hasattr(fold_model, "predict_proba"):
                oof_pred[val_idx] = fold_model.predict_proba(X_val)[:, 1]
            else:
                oof_pred[val_idx] = fold_model.predict(X_val)

    result = {
        "metric": metric,
        "scores": scores,
        "mean": float(np.mean(scores)),
        "std": float(np.std(scores)),
    }
    logger.info(
        "CV %d-fold: %s = %.5f ± %.5f", k_folds, metric, result["mean"], result["std"]
    )

    if return_oof:
        result["oof_predictions"] = oof_pred
    return result