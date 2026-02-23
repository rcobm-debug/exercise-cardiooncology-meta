#!/usr/bin/env python3
"""Generate forest plots (Figures 4–7) from derived datasets.

Figure provenance (as used in the manuscript):
- Figure 1 (PRISMA): created with PRISMA2020 (web/Shiny) from counts in data/derived/E5_PRISMA_counts.csv.
- Figures 2–3 (RoB 2): created with robvis from data/derived/E8_RoB2_table_LVEF_GLS.csv.
- Figures 4–7 (forest plots): created with this script using datasets in data/derived/.

Outputs are written to outputs/figures/.
"""

from __future__ import annotations

import os
import pandas as pd

from src.meta import meta_random_dl
from src.forestplot import forestplot, StudyCI

import matplotlib.pyplot as plt

FIGDIR = os.path.join("outputs", "figures")
os.makedirs(FIGDIR, exist_ok=True)


def _primary_from_net_change(net: pd.DataFrame):
    # FEVI: Foulkes Δ4 months + Antunes End of AC
    foulkes_lvef = net.query("study_id.str.contains('Foulkes')", engine="python") \
        .query("outcome_id=='LVEF_net' and timepoint=='Δ 4 months'")
    antunes_lvef = net.query("study_id.str.contains('Antunes')", engine="python") \
        .query("outcome_id=='LVEF_adj_net' and timepoint.str.startswith('End')", engine="python")

    fevi = [
        StudyCI("Foulkes 2023", float(foulkes_lvef.iloc[0].effect), float(foulkes_lvef.iloc[0].ci_low), float(foulkes_lvef.iloc[0].ci_high)),
        StudyCI("Antunes 2023", float(antunes_lvef.iloc[0].effect), float(antunes_lvef.iloc[0].ci_low), float(antunes_lvef.iloc[0].ci_high)),
    ]
    fevi_ses = [float(foulkes_lvef.iloc[0].se_from_ci95), float(antunes_lvef.iloc[0].se_from_ci95)]

    # GLS: use magnitude |%| by inverting the raw sign (so higher = better)
    foulkes_gls = net.query("study_id.str.contains('Foulkes')", engine="python") \
        .query("outcome_id=='GLS_raw_net' and timepoint=='Δ 4 months'")
    antunes_gls = net.query("study_id.str.contains('Antunes')", engine="python") \
        .query("outcome_id=='GLS_adj_raw_net' and timepoint.str.startswith('End')", engine="python")

    gls = [
        StudyCI("Foulkes 2023", -float(foulkes_gls.iloc[0].effect), -float(foulkes_gls.iloc[0].ci_high), -float(foulkes_gls.iloc[0].ci_low)),
        StudyCI("Antunes 2023", -float(antunes_gls.iloc[0].effect), -float(antunes_gls.iloc[0].ci_high), -float(antunes_gls.iloc[0].ci_low)),
    ]
    gls_ses = [float(foulkes_gls.iloc[0].se_from_ci95), float(antunes_gls.iloc[0].se_from_ci95)]

    return fevi, fevi_ses, gls, gls_ses


def main() -> None:
    net = pd.read_csv(os.path.join("data", "derived", "E7_dataset_net_change.csv"))
    post_lvef = pd.read_csv(os.path.join("data", "derived", "E7_dataset_post_LVEF.csv"))
    post_gls = pd.read_csv(os.path.join("data", "derived", "E7_dataset_post_GLSmag.csv"))

    # Figures 4–5 (primary)
    fevi, fevi_ses, gls, gls_ses = _primary_from_net_change(net)

    dl = meta_random_dl([s.effect for s in fevi], fevi_ses)
    pooled = StudyCI("Pooled", dl.mu_random, dl.ci95_random[0], dl.ci95_random[1])
    fig = forestplot(fevi, pooled, xlabel="DM (puntos FEVI)", title="Figura 4. FEVI (Δ) fin de antraciclinas (~4 meses)")
    fig.savefig(os.path.join(FIGDIR, "Figura4_FEVI_delta.png"), dpi=300)
    plt.close(fig)

    dl = meta_random_dl([s.effect for s in gls], gls_ses)
    pooled = StudyCI("Pooled", dl.mu_random, dl.ci95_random[0], dl.ci95_random[1])
    fig = forestplot(gls, pooled, xlabel="DM (puntos GLS |%|)", title="Figura 5. GLS magnitud (Δ) fin de antraciclinas (~4 meses)")
    fig.savefig(os.path.join(FIGDIR, "Figura5_GLS_delta.png"), dpi=300)
    plt.close(fig)

    # Figures 6–7 (sensitivity post-intervention)
    studies = [StudyCI(row.study_id.replace('_', ' '), float(row.effect), float(row.ci_low), float(row.ci_high))
               for row in post_lvef.itertuples(index=False)]
    dl = meta_random_dl([s.effect for s in studies], post_lvef["se"].astype(float).tolist())
    pooled = StudyCI("Pooled", dl.mu_random, dl.ci95_random[0], dl.ci95_random[1])
    fig = forestplot(studies, pooled, xlabel="DM post (puntos FEVI)", title="Figura 6. FEVI post-intervención (sensibilidad)")
    fig.savefig(os.path.join(FIGDIR, "Figura6_FEVI_post.png"), dpi=300)
    plt.close(fig)

    studies = [StudyCI(row.study_id.replace('_', ' '), float(row.effect), float(row.ci_low), float(row.ci_high))
               for row in post_gls.itertuples(index=False)]
    dl = meta_random_dl([s.effect for s in studies], post_gls["se"].astype(float).tolist())
    pooled = StudyCI("Pooled", dl.mu_random, dl.ci95_random[0], dl.ci95_random[1])
    fig = forestplot(studies, pooled, xlabel="DM post (puntos GLS |%|)", title="Figura 7. GLS magnitud post-intervención (sensibilidad)")
    fig.savefig(os.path.join(FIGDIR, "Figura7_GLS_post.png"), dpi=300)
    plt.close(fig)

    print(f"OK: forest plots written to {FIGDIR}/")


if __name__ == "__main__":
    main()
