"""Predicted vs experimental growth rate across carbon sources and media,
one panel per tool."""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from adjustText import adjust_text

colors = {
    "CataPro": "#CA8ADB",
    "CatPred": "#032138",
    "DLKcat": "#FFDC4C",
    "MMKcat": "#2BA4A6",
    "TurNuP": "#FF8552",
    "UniKP": "#A5C56C",
}

media_styles = {
    "YEP": {"color": "#2255aa", "marker": "D", "label": "Complex media"},
    "MAA": {"color": "#cc3333", "marker": "s", "label": "Minimal media + AA"},
    "Min": {"color": "#e8b93a", "marker": "o", "label": "Minimal media"},
}

carbon_abbr = {
    "D-glucose": "Glu", "D-fructose": "Fru", "sucrose": "Suc", "D-mannose": "Man",
    "maltose": "Mal", "raffinose": "Raf", "D-galactose": "Gal", "glycerol": "Gly",
    "trehalose": "Tre", "ethanol": "Eth", "acetate": "Ace",
}

df = pd.read_csv("../data/geckoplot_data_clean.csv")
tools = sorted(df["tool"].unique())
tool_display_lookup = {k.lower(): k for k in colors}  # e.g. "catpred" -> "CatPred"

nrows, ncols = 3, 2
max_val = max(df["experimental"].max(), df["predicted"].max()) * 1.1

fig, axes = plt.subplots(nrows, ncols, figsize=(9 * ncols, 8 * nrows))
axes = axes.flatten()

for ax, tool in zip(axes, tools):
    sub = df[df["tool"] == tool]
    ax.set_xlim(0, max_val)
    ax.set_ylim(0, max_val)

    texts = []
    for media, style in media_styles.items():
        sub_media = sub[sub["media"] == media]
        ax.scatter(sub_media["experimental"], sub_media["predicted"],
                   color=style["color"], marker=style["marker"], label=style["label"],
                   s=150, edgecolor="black", linewidth=0.8, zorder=3)
        for _, row in sub_media.iterrows():
            abbr = carbon_abbr.get(row["carbon_source"], row["carbon_source"])
            texts.append(ax.text(row["experimental"], row["predicted"], abbr, fontsize=18, zorder=10))

    adjust_text(
        texts, ax=ax,
        arrowprops=dict(arrowstyle="-", color="black", lw=0.6, shrinkA=0, shrinkB=0, zorder=5),
        expand=(1.3, 1.5), force_text=(0.2, 0.3), force_explode=(0.2, 0.5),
        force_pull=(0.05, 0.05), explode_radius=40, max_move=(25, 25),
        iter_lim=500, min_arrow_len=0,
    )

    ax.plot([0, max_val], [0, max_val], linestyle="--", color="gray", zorder=1)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, pos: "" if v == 0 else f"{v:.1f}"))
    ax.set_xlabel(r"$\mu_{max}$ experimental [h$^{-1}$]", fontsize=24)
    ax.set_ylabel(r"$\mu_{max}$ predicted [h$^{-1}$]", fontsize=24)
    ax.tick_params(axis="both", labelsize=16)

    display_name = tool_display_lookup.get(tool.lower(), tool)
    ax.set_title(display_name, fontsize=26, fontweight="bold", color=colors.get(display_name, "black"))

handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc="lower center", ncol=3, bbox_to_anchor=(0.5, -0.07),
           fontsize=15, markerscale=1.0)

fig.subplots_adjust(left=0.08, right=0.98, top=0.95, bottom=0.02, wspace=0.20, hspace=0.20)
plt.savefig("../figures/plot_carbon_sources.png", dpi=300, bbox_inches="tight")
