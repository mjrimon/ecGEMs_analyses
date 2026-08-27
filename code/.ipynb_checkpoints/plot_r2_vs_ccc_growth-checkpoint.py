"""Concordance (CCC) of predicted growth rate across experimental carbon
sources vs each tool's kcat benchmark R2, with bootstrap 95% CI."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.legend import Legend
from scipy import stats

colors = {
    "CataPro": "#CA8ADB",
    "CatPred": "#032138",
    "DLKcat": "#FFDC4C",
    "MMKcat": "#2BA4A6",
    "TurNuP": "#FF8552",
    "UniKP": "#A5C56C",
}

tools = ["CatPred", "CataPro", "MMKcat", "UniKP", "TurNuP", "DLKcat"]
name_to_key = {
    "CatPred": "catpred", "CataPro": "catapro", "MMKcat": "mmkcat",
    "UniKP": "unikp", "TurNuP": "turnup", "DLKcat": "dlkcat",
}
benchmark_r2 = {
    "CatPred": 0.59, "CataPro": 0.42, "MMKcat": 0.28,
    "UniKP": 0.27, "TurNuP": 0.22, "DLKcat": 0.07,
}

df = pd.read_csv("../data/geckoplot_data_clean.csv")


def concordance_correlation_coefficient(y_true, y_pred):
    y_true, y_pred = np.asarray(y_true, dtype=float), np.asarray(y_pred, dtype=float)
    mean_true, mean_pred = y_true.mean(), y_pred.mean()
    var_true, var_pred = y_true.var(), y_pred.var()
    covariance = np.mean((y_true - mean_true) * (y_pred - mean_pred))
    return (2 * covariance) / (var_true + var_pred + (mean_true - mean_pred) ** 2)


def bootstrap_ccc(y_true, y_pred, n_boot=10000, seed=None):
    """Non-parametric bootstrap of the CCC, resampling matched
    experimental-predicted pairs with replacement."""
    rng = np.random.default_rng(seed)
    y_true, y_pred = np.asarray(y_true, dtype=float), np.asarray(y_pred, dtype=float)
    n = len(y_true)

    idx = rng.integers(0, n, size=(n_boot, n))
    yt, yp = y_true[idx], y_pred[idx]
    mean_t, mean_p = yt.mean(axis=1), yp.mean(axis=1)
    var_t, var_p = yt.var(axis=1), yp.var(axis=1)
    cov = ((yt - mean_t[:, None]) * (yp - mean_p[:, None])).mean(axis=1)
    boot = (2 * cov) / (var_t + var_p + (mean_t - mean_p) ** 2)

    point = concordance_correlation_coefficient(y_true, y_pred)  # on the original data
    lo, hi = np.percentile(boot, [2.5, 97.5])
    return point, lo, hi


# CCC(growth) per tool + bootstrap 95% CI
growth_ccc = {}
growth_ccc_ci = {}
for tool in tools:
    sub = df[df["tool"] == name_to_key[tool]]
    point, lo, hi = bootstrap_ccc(sub["experimental"].values, sub["predicted"].values, seed=42)
    growth_ccc[tool] = point
    growth_ccc_ci[tool] = (lo, hi)

x = np.array([benchmark_r2[t] for t in tools])
y = np.array([growth_ccc[t] for t in tools])
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

fig, ax = plt.subplots(figsize=(6.5, 5.5))

for tool in tools:
    ccc = growth_ccc[tool]
    lo, hi = growth_ccc_ci[tool]
    yerr = np.array([[ccc - lo], [hi - ccc]])  # asymmetric, CCC CI is not symmetric

    ax.errorbar(benchmark_r2[tool], ccc, yerr=yerr, fmt="o", markersize=11,
                color=colors[tool], markeredgecolor="white", markeredgewidth=0.6,
                ecolor=colors[tool], elinewidth=1.8, capsize=5, zorder=3)

ax.set_xlabel(r"$R^2$ benchmark ($k_{cat}$ prediction)", fontsize=14)
ax.set_ylabel("CCC growth (experimental C-sources)", fontsize=14)
ax.set_ylim(0, 1)
ax.spines[["top", "right"]].set_visible(False)

# legend on its own invisible axis
ax_leg = fig.add_axes([0.1, 0.85, 0.85, 0.15])
ax_leg.set_axis_off()
handles = [mpatches.Patch(color=colors[t], label=t) for t in colors]
legend1 = Legend(ax_leg, handles, list(colors), loc="upper center", ncol=len(colors),
                  fontsize=9, frameon=False, handletextpad=0.45, columnspacing=0.8,
                  bbox_to_anchor=(0.5, 0.5))
ax_leg.add_artist(legend1)

plt.savefig("../figures/ccc_vs_r2.png", dpi=300, bbox_inches="tight")

