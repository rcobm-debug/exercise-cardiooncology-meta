from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Optional

import numpy as np
import matplotlib.pyplot as plt

@dataclass
class StudyCI:
    label: str
    effect: float
    ci_low: float
    ci_high: float

def forestplot(studies: List[StudyCI], pooled: Optional[StudyCI] = None, xlabel: str = "Diferencia de medias", title: str = "") -> plt.Figure:
    """Creates a simple forest plot (matplotlib only)."""
    labels = [s.label for s in studies]
    y = np.arange(len(studies), 0, -1)

    fig, ax = plt.subplots(figsize=(7.5, 0.5 + 0.5 * len(studies)))
    ax.axvline(0, linewidth=1)

    for yi, s in zip(y, studies):
        ax.plot([s.ci_low, s.ci_high], [yi, yi], linewidth=2)
        ax.plot([s.effect], [yi], marker="s", markersize=6)

    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.set_xlabel(xlabel)
    ax.set_title(title)

    # pooled (diamond-ish)
    if pooled is not None:
        yi = 0
        ax.plot([pooled.ci_low, pooled.ci_high], [yi, yi], linewidth=3)
        ax.plot([pooled.effect], [yi], marker="D", markersize=8)
        ax.set_yticks(list(y) + [0])
        ax.set_yticklabels(labels + ["Pooled"])

    # nice limits
    all_low = min([s.ci_low for s in studies] + ([pooled.ci_low] if pooled else []))
    all_high = max([s.ci_high for s in studies] + ([pooled.ci_high] if pooled else []))
    pad = (all_high - all_low) * 0.1 if all_high > all_low else 1
    ax.set_xlim(all_low - pad, all_high + pad)
    ax.set_ylim(-1, len(studies) + 1)

    fig.tight_layout()
    return fig
