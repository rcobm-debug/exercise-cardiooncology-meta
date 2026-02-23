#!/usr/bin/env python3
"""
Reproduce the DerSimonian–Laird random-effects meta-analyses reported in the manuscript.

Inputs (CSV files):
- E7_dataset_net_change.csv
- E7_dataset_post_LVEF.csv
- E7_dataset_post_GLSmag.csv

Output:
- Prints per-study effects, SE (from CI or SD/n), and pooled DL random-effects results.
"""

import pandas as pd
import numpy as np
import math

def meta_random_dl(effects, ses):
    effects = np.asarray(effects, dtype=float)
    ses = np.asarray(ses, dtype=float)
    vi = ses**2
    wi = 1/vi
    fixed = np.sum(wi*effects)/np.sum(wi)
    Q = np.sum(wi*(effects-fixed)**2)
    df = len(effects)-1
    C = np.sum(wi) - (np.sum(wi**2)/np.sum(wi))
    tau2 = max(0.0, (Q-df)/C) if C>0 else 0.0
    wi_re = 1/(vi+tau2)
    re = np.sum(wi_re*effects)/np.sum(wi_re)
    se_re = math.sqrt(1/np.sum(wi_re))
    ci_low = re - 1.96*se_re
    ci_high = re + 1.96*se_re
    I2 = max(0.0, (Q-df)/Q)*100 if Q>0 else 0.0
    return dict(k=len(effects), fixed=fixed, Q=Q, df=df, tau2=tau2, I2=I2,
                re=re, se=se_re, ci_low=ci_low, ci_high=ci_high)

def se_from_ci95(ci_low, ci_high):
    return (ci_high - ci_low) / (2*1.96)

def main():
    net = pd.read_csv("E7_dataset_net_change.csv")
    post_lvef = pd.read_csv("E7_dataset_post_LVEF.csv")
    post_gls = pd.read_csv("E7_dataset_post_GLSmag.csv")

    # Primary FEVI (~4 months): Foulkes Δ4 months + Antunes End of AC
    foulkes = net.query("study_id.str.contains('Foulkes')", engine="python") \
                 .query("outcome_id=='LVEF_net' and timepoint=='Δ 4 months'")
    antunes = net.query("study_id.str.contains('Antunes')", engine="python") \
                 .query("outcome_id=='LVEF_adj_net' and timepoint.str.startswith('End')", engine="python")
    effects = [float(foulkes.iloc[0].effect), float(antunes.iloc[0].effect)]
    ses = [float(foulkes.iloc[0].se_from_ci95), float(antunes.iloc[0].se_from_ci95)]
    print("\nFEVI net change (~4 months)")
    print(pd.DataFrame({"study":["Foulkes 2023","Antunes 2023"],"effect":effects,"se":ses}))
    print(meta_random_dl(effects, ses))

    # Primary GLS magnitude (~4 months): invert raw GLS difference (× -1)
    foulkes = net.query("study_id.str.contains('Foulkes')", engine="python") \
                 .query("outcome_id=='GLS_raw_net' and timepoint=='Δ 4 months'")
    antunes = net.query("study_id.str.contains('Antunes')", engine="python") \
                 .query("outcome_id=='GLS_adj_raw_net' and timepoint.str.startswith('End')", engine="python")
    effects = [-float(foulkes.iloc[0].effect), -float(antunes.iloc[0].effect)]
    ses = [float(foulkes.iloc[0].se_from_ci95), float(antunes.iloc[0].se_from_ci95)]
    print("\nGLS magnitude net change (~4 months) [raw GLS inverted × -1]")
    print(pd.DataFrame({"study":["Foulkes 2023","Antunes 2023"],"effect":effects,"se":ses}))
    print(meta_random_dl(effects, ses))

    # Post-intervention FEVI (k=3)
    effects = post_lvef["effect"].astype(float).tolist()
    ses = post_lvef["se"].astype(float).tolist()
    print("\nFEVI post-intervention (k=3)")
    print(post_lvef[["study_id","timepoint","effect","se"]])
    print(meta_random_dl(effects, ses))

    # Post-intervention GLS magnitude (k=3)
    effects = post_gls["effect"].astype(float).tolist()
    ses = post_gls["se"].astype(float).tolist()
    print("\nGLS magnitude post-intervention (k=3)")
    print(post_gls[["study_id","timepoint","effect","se"]])
    print(meta_random_dl(effects, ses))

if __name__ == "__main__":
    main()
