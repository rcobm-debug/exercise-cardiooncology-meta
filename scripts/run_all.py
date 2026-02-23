#!/usr/bin/env python3
"""Run all analyses and write outputs for reproducibility.

This script reproduces the DerSimonian–Laird random-effects meta-analyses (primary and sensitivity)
and Hartung–Knapp CIs as reported in the manuscript.

Inputs:
  - data/derived/E7_dataset_net_change.csv
  - data/derived/E7_dataset_post_LVEF.csv
  - data/derived/E7_dataset_post_GLSmag.csv

Outputs (created under outputs/):
  - outputs/meta_results.json
  - outputs/meta_results.csv
"""

from __future__ import annotations
import json
import os
import pandas as pd
from src.meta import meta_random_dl, hartung_knapp_ci

OUTDIR = os.path.join("outputs")
os.makedirs(OUTDIR, exist_ok=True)

def main():
    net = pd.read_csv(os.path.join("data","derived","E7_dataset_net_change.csv"))
    post_lvef = pd.read_csv(os.path.join("data","derived","E7_dataset_post_LVEF.csv"))
    post_gls = pd.read_csv(os.path.join("data","derived","E7_dataset_post_GLSmag.csv"))

    results = []

    # Primary FEVI (~4 months): Foulkes Δ4 months + Antunes End of AC
    foulkes = net.query("study_id.str.contains('Foulkes')", engine="python") \
                 .query("outcome_id=='LVEF_net' and timepoint=='Δ 4 months'")
    antunes = net.query("study_id.str.contains('Antunes')", engine="python") \
                 .query("outcome_id=='LVEF_adj_net' and timepoint.str.startswith('End')", engine="python")

    effects = [float(foulkes.iloc[0].effect), float(antunes.iloc[0].effect)]
    ses = [float(foulkes.iloc[0].se_from_ci95), float(antunes.iloc[0].se_from_ci95)]
    dl = meta_random_dl(effects, ses)
    mu_hk, hk_se, hk_ci, hk_q = hartung_knapp_ci(effects, ses, dl.tau2)
    results.append({
        "analysis": "FEVI net change (~4 months)",
        "k": dl.k,
        "mu_random": dl.mu_random,
        "ci95_random_low": dl.ci95_random[0],
        "ci95_random_high": dl.ci95_random[1],
        "I2": dl.I2,
        "tau2": dl.tau2,
        "hk_ci95_low": hk_ci[0],
        "hk_ci95_high": hk_ci[1],
    })

    # Primary GLS magnitude (~4 months): invert raw GLS difference (× -1)
    foulkes = net.query("study_id.str.contains('Foulkes')", engine="python") \
                 .query("outcome_id=='GLS_raw_net' and timepoint=='Δ 4 months'")
    antunes = net.query("study_id.str.contains('Antunes')", engine="python") \
                 .query("outcome_id=='GLS_adj_raw_net' and timepoint.str.startswith('End')", engine="python")

    effects = [-float(foulkes.iloc[0].effect), -float(antunes.iloc[0].effect)]
    ses = [float(foulkes.iloc[0].se_from_ci95), float(antunes.iloc[0].se_from_ci95)]
    dl = meta_random_dl(effects, ses)
    mu_hk, hk_se, hk_ci, hk_q = hartung_knapp_ci(effects, ses, dl.tau2)
    results.append({
        "analysis": "GLS magnitude net change (~4 months)",
        "k": dl.k,
        "mu_random": dl.mu_random,
        "ci95_random_low": dl.ci95_random[0],
        "ci95_random_high": dl.ci95_random[1],
        "I2": dl.I2,
        "tau2": dl.tau2,
        "hk_ci95_low": hk_ci[0],
        "hk_ci95_high": hk_ci[1],
    })

    # Sensitivity: FEVI post-intervention (k=3)
    effects = post_lvef["effect"].astype(float).tolist()
    ses = post_lvef["se"].astype(float).tolist()
    dl = meta_random_dl(effects, ses)
    mu_hk, hk_se, hk_ci, hk_q = hartung_knapp_ci(effects, ses, dl.tau2)
    results.append({
        "analysis": "FEVI post-intervention (k=3)",
        "k": dl.k,
        "mu_random": dl.mu_random,
        "ci95_random_low": dl.ci95_random[0],
        "ci95_random_high": dl.ci95_random[1],
        "I2": dl.I2,
        "tau2": dl.tau2,
        "hk_ci95_low": hk_ci[0],
        "hk_ci95_high": hk_ci[1],
    })

    # Sensitivity: GLS post-intervention (k=3)
    effects = post_gls["effect"].astype(float).tolist()
    ses = post_gls["se"].astype(float).tolist()
    dl = meta_random_dl(effects, ses)
    mu_hk, hk_se, hk_ci, hk_q = hartung_knapp_ci(effects, ses, dl.tau2)
    results.append({
        "analysis": "GLS magnitude post-intervention (k=3)",
        "k": dl.k,
        "mu_random": dl.mu_random,
        "ci95_random_low": dl.ci95_random[0],
        "ci95_random_high": dl.ci95_random[1],
        "I2": dl.I2,
        "tau2": dl.tau2,
        "hk_ci95_low": hk_ci[0],
        "hk_ci95_high": hk_ci[1],
    })

    out_json = os.path.join(OUTDIR, "meta_results.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    pd.DataFrame(results).to_csv(os.path.join(OUTDIR, "meta_results.csv"), index=False)

    print(f"OK: outputs written to {OUTDIR}/")

if __name__ == "__main__":
    main()
