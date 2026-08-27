"""BRENDA-derived vs EnzyExtract (independent) evaluation, per tool:
(1) R2 and (2) RMSE."""

import numpy as np
import matplotlib.pyplot as plt

colors = {
    "CataPro": "#CA8ADB",
    "CatPred": "#032138",
    "DLKcat": "#FFDC4C",
    "MMKcat": "#2BA4A6",
    "TurNuP": "#FF8552",
    "UniKP": "#A5C56C",
}
models = ["CatPred", "CataPro", "MMKcat", "UniKP", "DLKcat"]  # TurNuP not in EnzyExtract


def plot_brenda_vs_enzyextract(brenda_vals, enzy_vals, ylabel, tick_step, tick_mode, out_name):
    """Shared plotting logic for the R2 and RMSE comparisons.
    tick_mode is 'ceil' (R2) or 'floor' (RMSE), matching the original figures.
    out_name sets the output filename, since both calls share this function."""
    fig, ax = plt.subplots(figsize=(5, 5))
    x_brenda, x_enzy = 0, 1

    for model in models:
        y1, y2 = brenda_vals[model], enzy_vals[model]
        color = colors[model]
        ax.plot([x_brenda, x_enzy], [y1, y2], color=color, linewidth=1.8, zorder=2)
        ax.scatter(x_brenda, y1, color=color, s=80, zorder=3)
        ax.scatter(x_enzy, y2, color=color, s=80, zorder=3)

    if ylabel == "R\u00b2":
        ax.axhline(0.0, color="gray", linestyle="--", linewidth=1, zorder=1)

    all_vals = list(brenda_vals.values()) + list(enzy_vals.values())
    y_min, y_max = min(all_vals), max(all_vals)

    if tick_mode == "ceil":
        margin = (y_max - y_min) * 0.12
        ax.set_ylim(y_min - margin, y_max + margin)
        yticks = np.arange(np.ceil(y_min / tick_step) * tick_step,
                            np.ceil(y_max / tick_step) * tick_step + tick_step / 2, tick_step)
    else:
        ax.set_ylim(y_min - 0.05, y_max + 0.05)
        yticks = np.arange(np.floor(y_min / tick_step) * tick_step,
                            np.floor(y_max / tick_step) * tick_step + tick_step / 2, tick_step)

    ax.set_yticks(np.round(yticks, 2))
    ax.tick_params(axis="y", labelsize=14)

    ax.set_xlim(-0.25, 1.6)
    ax.set_xticks([x_brenda, x_enzy])
    ax.set_xticklabels(["BRENDA", "EnzyExtract"], fontsize=16)
    ax.set_ylabel(ylabel, fontsize=16)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # spread out model labels next to the EnzyExtract points so they don't overlap
    min_gap = 0.04
    sorted_models = sorted(models, key=lambda m: enzy_vals[m])
    positions = [enzy_vals[m] for m in sorted_models]
    for _ in range(100):
        for i in range(1, len(positions)):
            if positions[i] - positions[i - 1] < min_gap:
                mid = (positions[i] + positions[i - 1]) / 2
                positions[i - 1] = mid - min_gap / 2
                positions[i] = mid + min_gap / 2

    for model, pos in zip(sorted_models, positions):
        ax.text(x_enzy + 0.08, pos, model, color=colors[model], fontsize=16, va="center")

    plt.tight_layout()
    plt.savefig(f"../figures/{out_name}.png", dpi=300, bbox_inches="tight")



# R2 values from the heatmaps

brenda_r2 = {"CatPred": 0.59, "CataPro": 0.42, "MMKcat": 0.28, "UniKP": 0.27, "DLKcat": 0.07}
enzyextract_r2 = {"CataPro": 0.20, "UniKP": 0.18, "MMKcat": 0.08, "CatPred": 0.06, "DLKcat": -0.03}
plot_brenda_vs_enzyextract(brenda_r2, enzyextract_r2, ylabel="R\u00b2", tick_step=0.2, tick_mode="ceil",
                            out_name="plot_brenda_vs_enzyextract_r2")


# RMSE values from the heatmaps

brenda_rmse = {"CatPred": 0.93, "CataPro": 1.10, "MMKcat": 1.23, "UniKP": 1.24, "DLKcat": 1.40}
enzyextract_rmse = {"CataPro": 1.29, "UniKP": 1.30, "MMKcat": 1.38, "CatPred": 1.40, "DLKcat": 1.47}
plot_brenda_vs_enzyextract(brenda_rmse, enzyextract_rmse, ylabel="RMSE", tick_step=0.2, tick_mode="floor",
                            out_name="plot_brenda_vs_enzyextract_rmse")
