from __future__ import annotations
import math
from dataclasses import dataclass
from typing import Iterable, Tuple, Dict, Any, List

import numpy as np
from scipy import stats

@dataclass
class MetaResult:
    k: int
    mu_fixed: float
    mu_random: float
    se_random: float
    ci95_random: Tuple[float, float]
    tau2: float
    Q: float
    df: int
    I2: float

    # Hartung-Knapp adjustment (a.k.a. scale estimation / HKSJ-style CI)
    hk_se: float | None = None
    hk_ci95: Tuple[float, float] | None = None
    hk_q: float | None = None

def se_from_ci95(ci_low: float, ci_high: float) -> float:
    return (ci_high - ci_low) / (2 * 1.96)

def meta_random_dl(effects: Iterable[float], ses: Iterable[float]) -> MetaResult:
    effects = np.asarray(list(effects), dtype=float)
    ses = np.asarray(list(ses), dtype=float)
    k = len(effects)
    if k < 2:
        raise ValueError("Se requieren al menos 2 estudios para metaanálisis.")

    vi = ses ** 2
    wi = 1 / vi
    mu_fixed = float(np.sum(wi * effects) / np.sum(wi))

    Q = float(np.sum(wi * (effects - mu_fixed) ** 2))
    df = k - 1
    C = float(np.sum(wi) - (np.sum(wi ** 2) / np.sum(wi)))
    tau2 = max(0.0, (Q - df) / C) if C > 0 else 0.0

    wi_re = 1 / (vi + tau2)
    mu_random = float(np.sum(wi_re * effects) / np.sum(wi_re))
    se_random = math.sqrt(1 / float(np.sum(wi_re)))
    ci95 = (mu_random - 1.96 * se_random, mu_random + 1.96 * se_random)
    I2 = max(0.0, (Q - df) / Q) * 100 if Q > 0 else 0.0

    return MetaResult(
        k=k,
        mu_fixed=mu_fixed,
        mu_random=mu_random,
        se_random=se_random,
        ci95_random=ci95,
        tau2=tau2,
        Q=Q,
        df=df,
        I2=I2
    )

def hartung_knapp_ci(effects: Iterable[float], ses: Iterable[float], tau2: float) -> Tuple[float, float, Tuple[float, float], float]:
    """Hartung-Knapp adjustment for the random-effects mean.

    Returns: (mu, hk_se, (ci_low, ci_high), q)

    Notes
    -----
    - Uses weights 1/(vi + tau2)
    - q = sum(wi*(yi-mu)^2)/(k-1)
    - CI uses t_{k-1, 0.975}
    """
    effects = np.asarray(list(effects), dtype=float)
    ses = np.asarray(list(ses), dtype=float)
    k = len(effects)
    vi = ses ** 2
    wi = 1 / (vi + tau2)
    mu = float(np.sum(wi * effects) / np.sum(wi))
    q = float(np.sum(wi * (effects - mu) ** 2) / (k - 1))
    hk_se = math.sqrt(q / float(np.sum(wi)))
    tcrit = float(stats.t.ppf(0.975, df=k - 1))
    return mu, hk_se, (mu - tcrit * hk_se, mu + tcrit * hk_se), q
