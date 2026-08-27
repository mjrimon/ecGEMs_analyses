"""Decline in predictive performance (delta R2) vs decline in training
data match (delta I_match), per tool."""

import matplotlib.pyplot as plt
from adjustText import adjust_text

colors = {
    "CataPro": "#CA8ADB",
    "CatPred": "#032138",
    "DLKcat": "#FFDC4C",
    "MMKcat": "#2BA4A6",
    "TurNuP": "#FF8552",
    "UniKP": "#A5C56C",
}

delta_data = {
    "DLKcat": {"delta_I": 23.85 - 14.94, "delta_R2": 0.07 - (-0.03)},
    "UniKP": {"delta_I": 23.85 - 14.94, "delta_R2": 0.27 - 0.18},
    "MMKcat": {"delta_I": 40.40 - 19.35, "delta_R2": 0.28 - 0.08},
    "CataPro": {"delta_I": 78.48 - 23.50, "delta_R2": 0.42 - 0.20},
    "CatPred": {"delta_I": 75.95 - 26.21, "delta_R2": 0.59 - 0.06},
}

xs = [vals["delta_I"] / 100 for vals in delta_data.values()]
ys = [vals["delta_R2"] for vals in delta_data.values()]
max_val = max(max(xs), max(ys)) * 1.15
offset = max_val * 0.02  # label offset from each point

fig, ax = plt.subplots(figsize=(6.5, 6.5))
texts = []
for tool, vals in delta_data.items():
    x, y = vals["delta_I"] / 100, vals["delta_R2"]
    color = colors.get(tool, "black")
    ax.scatter(x, y, color=color, s=180, zorder=3)
    texts.append(ax.text(x + offset, y + offset, tool, fontsize=14, color=color))

ax.plot([0, max_val], [0, max_val], "--", color="gray", zorder=1)
ax.set_xlim(0, max_val)
ax.set_ylim(0, max_val)
ax.set_aspect("equal", adjustable="box")
ax.set_xlabel(r"$\Delta I_{match}$", fontsize=16)
ax.set_ylabel(r"$\Delta R^2$", fontsize=16)
ax.tick_params(axis="both", labelsize=16)

adjust_text(texts, ax=ax)  # spreads overlapping labels automatically

plt.tight_layout()
plt.savefig("../figures/plot_decline_performance.png", dpi=300, bbox_inches="tight")
