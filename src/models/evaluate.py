"""Métricas y gráficos de evaluación."""

import matplotlib.pyplot as plt
import numpy as np
from sklearn import metrics


def classification_metrics(y_true: np.ndarray, y_score: np.ndarray) -> dict[str, float]:
    """ROC-AUC, PR-AUC, Brier, log loss (binario)."""
    y_true = np.asarray(y_true).ravel()
    y_score = np.asarray(y_score).ravel()
    out: dict[str, float] = {
        "roc_auc": float(metrics.roc_auc_score(y_true, y_score)),
        "pr_auc": float(metrics.average_precision_score(y_true, y_score)),
        "brier_score": float(metrics.brier_score_loss(y_true, y_score)),
        "log_loss": float(metrics.log_loss(y_true, y_score, labels=[0, 1])),
    }
    return out


def plot_roc_curve(y_true: np.ndarray, y_score: np.ndarray, ax=None):
    """Curva ROC."""
    fpr, tpr, _ = metrics.roc_curve(y_true, y_score)
    if ax is None:
        _, ax = plt.subplots()
    ax.plot(fpr, tpr)
    ax.set_xlabel("FPR")
    ax.set_ylabel("TPR")
    return ax
