#!/usr/bin/env python3
"""Write environment/session information for reproducibility."""
import json, os, platform, sys, subprocess
import numpy as np
import pandas as pd
import matplotlib
import scipy

OUTDIR = os.path.join("outputs")
os.makedirs(OUTDIR, exist_ok=True)

def main():
    info = {
        "python_version": sys.version,
        "platform": platform.platform(),
        "numpy": np.__version__,
        "pandas": pd.__version__,
        "matplotlib": matplotlib.__version__,
        "scipy": scipy.__version__,
    }
    # pip freeze
    try:
        freeze = subprocess.check_output([sys.executable, "-m", "pip", "freeze"], text=True)
    except Exception as e:
        freeze = f"Could not run pip freeze: {e}"

    with open(os.path.join(OUTDIR, "session_info.json"), "w", encoding="utf-8") as f:
        json.dump(info, f, indent=2)

    with open(os.path.join(OUTDIR, "session_info.txt"), "w", encoding="utf-8") as f:
        f.write("Session info\n" + "="*40 + "\n")
        for k,v in info.items():
            f.write(f"{k}: {v}\n")
        f.write("\n--- pip freeze ---\n")
        f.write(freeze)

    print("OK: wrote outputs/session_info.*")

if __name__ == "__main__":
    main()
