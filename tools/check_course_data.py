"""Check local raw data contracts without estimating course solutions."""
from pathlib import Path
import json
import numpy as np
from scipy.io import loadmat


def check(root):
    files = {
        "Projects/MatlabFiles/exercise1.mat": {"u": (300, 1), "y": (300, 1)},
        "Projects/MatlabFiles/exercise2.mat": {"z1": (200, 2), "z2": (200, 2)},
        "self_study/resources/cascaded_tanks/data/CascadedTanksFiles/dataBenchmark.mat":
            {"uEst": (1024, 1), "yEst": (1024, 1),
             "uVal": (1024, 1), "yVal": (1024, 1), "Ts": (1, 1)}
    }
    result = []
    for rel, expected in files.items():
        d = loadmat(root/rel)
        for key, shape in expected.items():
            assert d[key].shape == shape, (rel, key, d[key].shape)
            assert np.isfinite(d[key]).all(), (rel, key, "nonfinite")
        if "cascaded" in rel:
            assert float(d["Ts"].item()) == 4.
        else:
            assert "Ts" not in d, "Metadata changed: inspect the sampling interval"
        result.append({"path": rel, "variables": {k: list(d[k].shape) for k in expected}})
    print(json.dumps({"status": "passed", "files": result}, ensure_ascii=False, indent=2))
    return result


if __name__ == "__main__":
    check(Path(__file__).resolve().parents[2])
