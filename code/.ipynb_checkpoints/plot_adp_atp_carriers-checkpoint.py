"""ADP/ATP carrier plots: (1) predicted kcat spread per isoenzyme vs the
experimental range, and (2) growth rate gained by opening each isoenzyme."""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.legend import Legend

tool_colors = {
    "CatPred": "#032138",
    "CataPro": "#CA8ADB",
    "MMKcat": "#2BA4A6",
    "UniKP": "#A5C56C",
    "DLKcat": "#FFDC4C",
    "TurNuP": "#FF8552",
}


# Figure 1: predicted kcat per isoenzyme (log scale) vs experimental range

kcat_data = {
    "YBL030C": {"CatPred": 4319.4635, "DLKcat": 352415.5200, "CataPro": 3470.7357,
                "MMKcat": 10831.7706, "TurNuP": 192828.4452, "UniKP": 9500.1019},
    "YBR085W": {"CatPred": 7577.3872, "DLKcat": 93393.7200, "CataPro": 1878.4842,
                "MMKcat": 4503.4026, "TurNuP": 103198.3848, "UniKP": 12024.6101},
    "YMR056C": {"CatPred": 4641.6898, "DLKcat": 481741.2000, "CataPro": 2017.4290,
                "MMKcat": 1858.7290, "TurNuP": 123196.5504, "UniKP": 11089.9101},
}
enzymes = list(kcat_data.keys())
positions = list(range(len(enzymes)))

fig = plt.figure(figsize=(8, 5))
ax = fig.add_axes([0.1, 0.09, 0.85, 0.75])  # [left, bottom, width, height]

for pos, (enzyme, tools) in zip(positions, kcat_data.items()):
    log_values = [np.log10(v) for v in tools.values()]
    tool_names = list(tools.keys())

    ax.boxplot([log_values], vert=True, patch_artist=False, widths=0.35,
               medianprops=dict(color="black", linewidth=2),
               boxprops=dict(color="black"), whiskerprops=dict(color="black"),
               capprops=dict(color="black"), showfliers=False,
               positions=[pos], manage_ticks=False)

    jitter = np.linspace(-0.12, 0.12, len(log_values))
    for j, (tool, lv) in enumerate(zip(tool_names, log_values)):
        ax.scatter(pos + jitter[j], lv, color=tool_colors[tool], s=90, zorder=4,
                   edgecolors="white", linewidths=0.5)

    # experimental range, converted from min to h^-1 (mean +/- std)
exp_values = [(1538 * 60, 214 * 60), (1424 * 60, 101 * 60)]
log_mins = [np.log10(m - s) for m, s in exp_values]
log_maxs = [np.log10(m + s) for m, s in exp_values]
band_lo, band_hi = min(log_mins), max(log_maxs)
mean_combined = np.log10(np.mean([1538 * 60, 1424 * 60]))

ax.axhspan(band_lo, band_hi, color="steelblue", alpha=0.15, zorder=0, label="Experimental range")
ax.axhline(mean_combined, color="steelblue", linewidth=1.2, linestyle="--", alpha=0.6, zorder=1)

ax.set_xticks(positions)
ax.set_xticklabels(enzymes, fontsize=12)
ax.set_xlim(-0.6, len(enzymes) - 0.4)
ax.set_ylabel("$k_{cat}$ (h$^{-1}$)", fontsize=13)
ax.axhline(0, color="grey", linewidth=0.8, linestyle="--", alpha=0.5)
ax.grid(axis="y", alpha=0.3)

    # crop to the relevant range (10^3 to 10^6)
ax.set_ylim(3, 6)
yticks = [3, 4, 5, 6]
ax.set_yticks(yticks)
ax.set_yticklabels([f"$10^{{{y}}}$" for y in yticks], fontsize=11)

    # legend on its own invisible axis
ax_leg = fig.add_axes([0.1, 0.82, 0.85, 0.15])
ax_leg.set_axis_off()
handles = [mpatches.Patch(color=tool_colors[t], label=t) for t in tool_colors]
legend1 = Legend(ax_leg, handles, list(tool_colors), loc="upper center",
                  ncol=len(tool_colors), fontsize=9, frameon=False,
                  bbox_to_anchor=(0.5, 0.6))
ax_leg.add_artist(legend1)

plt.savefig("../figures/plot_adp_atp_kcat_spread.png", dpi=300, bbox_inches="tight")


# Figure 2: growth rate gained by opening each isoenzyme (baseline + increment)

tools = ["CataPro", "CatPred", "DLKcat", "MMKcat", "TurNuP", "UniKP"]
baseline = [0.2147, 0.2795, 0.3941, 0.3032, 0.6167, 0.2123]
skipped = [0.5627, 0.4599, 0.3975, 0.4381, 0.6380, 0.2364]  # with YBL030C opened
experimental_value = 0.42

increment = [s - b for s, b in zip(skipped, baseline)]

fixed_order = ["TurNuP", "DLKcat", "MMKcat", "CatPred", "CataPro", "UniKP"]
order = [tools.index(t) for t in fixed_order]
tools_sorted = [tools[i] for i in order]
baseline_sorted = [baseline[i] for i in order]
increment_sorted = [increment[i] for i in order]

def lighten(hex_color, factor=0.45):
    """Blend a hex color with white."""
    hex_color = hex_color.lstrip("#")
    r, g, b = [int(hex_color[i:i + 2], 16) for i in (0, 2, 4)]
    r = int(r + (255 - r) * factor)
    g = int(g + (255 - g) * factor)
    b = int(b + (255 - b) * factor)
    return f"#{r:02x}{g:02x}{b:02x}"

base_colors = [tool_colors[t] for t in tools_sorted]
inc_colors = [lighten(tool_colors[t]) for t in tools_sorted]

fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(len(tools_sorted))
bar_width = 0.6

ax.bar(x, baseline_sorted, width=bar_width, color=base_colors, edgecolor="black",
       linewidth=0.7, zorder=10)
ax.bar(x, increment_sorted, width=bar_width, bottom=baseline_sorted, color=inc_colors,
       edgecolor="black", linewidth=0.7, linestyle="--", hatch="////", zorder=10)

    # baseline value label inside the base bar
for i, b in enumerate(baseline_sorted):
    if b > 0.05:
        ax.text(x[i], b / 2, f"{b:.3f}", ha="center", va="center", fontsize=10,
                color="white" if base_colors[i] == "#032138" else "black")

ax.axhline(experimental_value, color="#e6b000", linestyle="--", linewidth=2, zorder=20)

    # secondary axis in % deviation from experimental value
def abs_to_pct(v):
    return (v - experimental_value) / experimental_value * 100

ax_right = ax.twinx()
y_lo, y_hi = ax.get_ylim()
ax_right.set_ylim(abs_to_pct(y_lo), abs_to_pct(y_hi))
pct_ticks = np.arange(-100, 80, 20)
pct_ticks = pct_ticks[(pct_ticks >= abs_to_pct(y_lo)) & (pct_ticks <= abs_to_pct(y_hi))]
ax_right.set_yticks(pct_ticks)
ax_right.set_yticklabels([f"{int(t)}%" for t in pct_ticks])
ax_right.tick_params(axis="y", labelsize=11)
ax_right.spines["top"].set_visible(False)
ax_right.grid(False)

ax.set_ylim(-0.02, 0.75)
ax.set_xticks(x)
ax.set_xticklabels(tools_sorted, rotation=45, ha="right", fontsize=12)
ax.set_ylabel("Growth rate (h$^{-1}$)", fontsize=13)
ax.spines["top"].set_visible(False)
ax.tick_params(axis="both", labelsize=11)
ax.grid(False)

legend_base = mpatches.Patch(facecolor="#aaaaaa", edgecolor="black", linewidth=0.7, label="Baseline")
legend_inc = mpatches.Patch(facecolor="#dddddd", edgecolor="black", linewidth=0.7,
                             linestyle="--", hatch="////", label="YMR056C opened")
exp_line = plt.Line2D([0], [0], color="#e6b000", linestyle="--", linewidth=2, label="Experimental")
ax.legend(handles=[legend_base, legend_inc, exp_line], loc="upper right", fontsize=11, frameon=True)

plt.tight_layout()
plt.savefig("../figures/plot_adp_atp_growth_gain.png", dpi=300, bbox_inches="tight")
