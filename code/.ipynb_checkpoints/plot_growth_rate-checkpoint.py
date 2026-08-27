"""Growth rate comparison across tools, log-norm distribution, BRENDA,
environmental and mean_kcat baselines, with a broken y-axis."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec


# Data

df_long = pd.read_csv("../data/random_boxplot_data.csv", usecols=["type", "growth"])

experimental_value = 0.42
brenda_value = 2.7      # mean_kcat top value (broken axis)
break_start = 2.4
bot_ylim_top = 0.70

tool_colors = {
    "CataPro": "#CA8ADB",
    "CatPred": "#032138",
    "DLKcat": "#FFDC4C",
    "MMKcat": "#2BA4A6",
    "TurNuP": "#FF8552",
    "UniKP": "#A5C56C",
}
gray = "#9c9c9c"
lognorm_hatch = "\\\\"
mean_hatch = "////"

tool_order = ["TurNuP", "DLKcat", "MMKcat", "CatPred", "CataPro", "UniKP"]
tool_growths = [0.6167, 0.3941, 0.3032, 0.2795, 0.2147, 0.2123]

env_val = 0.3442
brenda_val = 0.3404

# x positions
n_tools = len(tool_order)
box_pos = 6      # log-norm
brenda_pos = 7   # BRENDA (normal bar)
env_pos = 8      # environmental (normal bar)
mean_pos = 9     # mean_kcat (broken axis)

all_positions = list(range(n_tools)) + [box_pos, brenda_pos, env_pos, mean_pos]
all_labels = tool_order + ["log-norm", "GECKO / BRENDA", "enviromental", "mean_kcat"]
bar_width = 0.6


# Figure with broken y-axis

fig = plt.figure(figsize=(12, 7))
gs = gridspec.GridSpec(2, 1, height_ratios=[1, 4], hspace=0.08)
ax_top = fig.add_subplot(gs[0])
ax_bot = fig.add_subplot(gs[1])

x_lo, x_hi = -0.5, mean_pos + 0.5
ax_bot.set_xlim(x_lo, x_hi)
ax_top.set_xlim(x_lo, x_hi)

# tool bars
for i, (tool, g) in enumerate(zip(tool_order, tool_growths)):
    ax_bot.bar(i, g, width=bar_width, color=tool_colors[tool],
               edgecolor="black", linewidth=0.5, zorder=10)
    ax_bot.text(i, g, f"{g:.3f}", ha="center", va="bottom", fontsize=16)

# log-norm boxplot
lognorm_growth = df_long[df_long["type"] == "log-norm"]["growth"]
bp = ax_bot.boxplot(
    [lognorm_growth], positions=[box_pos], widths=0.6, patch_artist=True,
    medianprops=dict(color="black", linewidth=2.5),
    whiskerprops=dict(linewidth=1.5), capprops=dict(linewidth=1.5),
    boxprops=dict(linewidth=1.5),
)
for patch in bp["boxes"]:
    patch.set_facecolor(gray)
    patch.set_hatch(lognorm_hatch)
    patch.set_edgecolor("black")
    patch.set_alpha(0.8)

if np.allclose(lognorm_growth, lognorm_growth.iloc[0]):
    ax_bot.hlines(lognorm_growth.iloc[0], box_pos - 0.25, box_pos + 0.25,
                  color="black", linewidth=3, zorder=25)
    ax_bot.scatter(box_pos, lognorm_growth.iloc[0], color="black", s=60, zorder=30)

# BRENDA bar (normal)
ax_bot.bar(brenda_pos, brenda_val, width=bar_width, color=gray, hatch="||||",
           edgecolor="black", linewidth=0.8, zorder=10)
ax_bot.text(brenda_pos, brenda_val, f"{brenda_val:.3f}", ha="center", va="bottom", fontsize=16)

# environmental bar (normal)
ax_bot.bar(env_pos, env_val, width=bar_width, color=gray,
           edgecolor="black", linewidth=0.5, zorder=10)
ax_bot.text(env_pos, env_val, f"{env_val:.3f}", ha="center", va="bottom", fontsize=16)

# mean_kcat bar, split across both panels (broken axis)
rect_bot = mpatches.Rectangle((mean_pos - bar_width / 2, 0), bar_width, bot_ylim_top,
                               facecolor=gray, hatch=mean_hatch, edgecolor="black",
                               linewidth=0.8, zorder=10)
ax_bot.add_patch(rect_bot)

rect_top = mpatches.Rectangle((mean_pos - bar_width / 2, break_start), bar_width,
                               brenda_value - break_start, facecolor=gray,
                               hatch=mean_hatch, edgecolor="black", linewidth=0.8, zorder=10)
ax_top.add_patch(rect_top)
ax_top.text(mean_pos, brenda_value, f"{brenda_value:.3f}", ha="center", va="bottom", fontsize=16)

# experimental reference line
ax_bot.axhline(experimental_value, color="#e6b000", linestyle="--", linewidth=2, zorder=20)
ax_top.plot([], [], color="#e6b000", linestyle="--", linewidth=2, label="Experimental")
ax_top.legend(frameon=True, loc="upper left", fontsize=18)


# Bottom panel axes

ax_bot.set_ylim(-0.02, bot_ylim_top)
ax_bot.set_xticks(all_positions)
ax_bot.set_xticklabels(all_labels, rotation=45, ha="right", fontsize=15)
ax_bot.set_ylabel("Growth rate (h$^{-1}$)", fontsize=20)
ax_bot.tick_params(axis="y", labelsize=16)
ax_bot.tick_params(axis="x", labelsize=17)
ax_bot.grid(False)
ax_bot.spines["top"].set_visible(False)


# Top panel axes

ax_top.set_ylim(break_start, 2.85)
ax_top.set_xticks([])
ax_top.set_yticks([2.5, 2.7])
ax_top.set_yticklabels(["2.5", "2.7"], fontsize=16)
ax_top.grid(False)
ax_top.spines["bottom"].set_visible(False)


# Secondary axes in % deviation from experimental value

def abs_to_pct(v):
    return (v - experimental_value) / experimental_value * 100

ax_bot_right = ax_bot.twinx()
y_lo, y_hi = ax_bot.get_ylim()
ax_bot_right.set_ylim(abs_to_pct(y_lo), abs_to_pct(y_hi))
pct_ticks = np.arange(-100, 60, 20)
pct_ticks = pct_ticks[(pct_ticks >= abs_to_pct(y_lo)) & (pct_ticks <= abs_to_pct(y_hi))]
ax_bot_right.set_yticks(pct_ticks)
ax_bot_right.set_yticklabels([f"{int(t)}%" for t in pct_ticks])
ax_bot_right.spines["top"].set_visible(False)
ax_bot_right.tick_params(axis="y", labelsize=16)
ax_bot_right.grid(False)

ax_top_right = ax_top.twinx()
y_lo_top, y_hi_top = ax_top.get_ylim()
ax_top_right.set_ylim(abs_to_pct(y_lo_top), abs_to_pct(y_hi_top))
pct_ticks_top = np.arange(400, 700, 50)
pct_ticks_top = pct_ticks_top[(pct_ticks_top >= abs_to_pct(y_lo_top)) & (pct_ticks_top <= abs_to_pct(y_hi_top))]
ax_top_right.set_yticks(pct_ticks_top)
ax_top_right.set_yticklabels([f"{int(t)}%" for t in pct_ticks_top])
ax_top_right.spines["bottom"].set_visible(False)
ax_top_right.tick_params(axis="y", labelsize=16)
ax_top_right.grid(False)


# Diagonal break marks

fig.subplots_adjust(left=0.08, right=0.98, top=0.92, bottom=0.15)

d = 0.012
kwargs = dict(transform=fig.transFigure, color="black", clip_on=False, linewidth=1)
bot_pos = ax_bot.get_position()
top_pos = ax_top.get_position()
y_break_bot = bot_pos.y1
y_break_top = top_pos.y0

for x in [bot_pos.x0, bot_pos.x1]:
    fig.add_artist(plt.Line2D([x - d, x + d], [y_break_bot - d, y_break_bot + d], **kwargs))
    fig.add_artist(plt.Line2D([x - d, x + d], [y_break_top - d, y_break_top + d], **kwargs))

plt.savefig("../figures/plot_growth_rate.png", dpi=300, bbox_inches="tight")
