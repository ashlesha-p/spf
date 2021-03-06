# Import Python packages
import os
import sys
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D


# Set matplotlib font and padding defaults
font = {'family': 'serif',
        'size': 16}
matplotlib.rc('font', **font)
matplotlib.rc('text', usetex=True)
matplotlib.rcParams['axes.titlepad'] = 20
matplotlib.rcParams['axes.labelpad'] = 10


def plot_spf_vs_gpf_teleport_rates(in_files, styles, title, out_file):
    """
        Plots SPF and GPF teleportation channel rates.
        Line colors, styles and labels should be provided in a styles dict.
        Adds title and outputs PNG to out_file
    """
    # Initialise figure
    plt.figure()
    fig, ax = plt.subplots()
    # Plots input datasets
    for (spf_in_file, gpf_in_file), style in zip(in_files, styles):
        # Reads in CSV data into pandas dataframe object
        spf_df = pd.read_csv(spf_in_file, index_col=[0])
        gpf_df = pd.read_csv(gpf_in_file, index_col=[0])
        # Creates x- and y-value arrays and their associated errors
        spf_x_vals = np.array(spf_df.index.values)
        gpf_x_vals = np.array(gpf_df.index.values)
        spf_y_vals = np.array(spf_df.prob_tel)
        gpf_y_vals = np.array(gpf_df.prob_tel)
        diff_y_vals = spf_y_vals - gpf_y_vals
        spf_y_errs = np.array(spf_df.prob_tel_std)
        gpf_y_errs = np.array(gpf_df.prob_tel_std)
        diff_y_errs = (spf_y_errs ** 2 + gpf_y_errs ** 2) ** 0.5
        # Plots SPF and GPF lines with errors and adds difference fill
        ax.plot(spf_x_vals, spf_y_vals, color=style['color'], linewidth=3,
                linestyle='-')
        ax.plot(gpf_x_vals, gpf_y_vals, color=style['color'], linewidth=3,
                linestyle='--')
        ax.fill_between(spf_x_vals, 0, diff_y_vals,
                        facecolor=style['color'], alpha=0.1, linewidth=0.0)
    # Adds channel and PF line labels
    ch_handles = [Line2D([], [], color=style['color'], linestyle='-',
                         linewidth=2, label=style['label'])
                  for style in styles]
    spf_line = Line2D([], [], color='k', linestyle='-', linewidth=2)
    gpf_line = Line2D([], [], color='k', linestyle='--', linewidth=2)
    diff_patch = mpatches.Patch(color='k', alpha=0.1, linewidth=0)
    pf_handles = [spf_line, gpf_line, diff_patch]
    pf_labels = ['SPF', 'GPF', 'Diff.']
    ch_labels = [h.get_label() for h in ch_handles]
    ch_lgd = plt.legend(ch_handles, ch_labels, loc='upper right',
                        framealpha=1)
    pf_lgd = plt.legend(pf_handles, pf_labels, loc=(0.815, 0.295),
                        framealpha=1)
    plt.setp(ch_lgd.get_texts(), fontsize=24)
    plt.setp(pf_lgd.get_texts(), fontsize=24)
    ax.add_artist(pf_lgd)
    ax.add_artist(ch_lgd)
    # Formats axes, adds labels and title
    plt.xlabel('Loss probability (per-qubit), $p_l$', size=24)
    plt.ylabel('Teleportation rate, $T$',  size=24)
    plt.xticks(fontsize=24)
    plt.yticks(fontsize=24)
    ax.set_ylim(0, 1)
    ax.set_xlim(0, 1)
    plt.title(title, fontsize=32)
    # Creates gridlines
    minor_ticks = np.linspace(0, 1, 41)
    ax.set_xticks(minor_ticks, minor=True)
    ax.set_yticks(minor_ticks, minor=True)
    ax.grid(True, ls='--', lw=1, c='k', alpha=0.2, which='major')
    ax.grid(True, ls=':', lw=1, c='k', alpha=0.1, which='minor')
    # Outputs to file
    fig.set_size_inches(11, 7)
    plt.savefig(out_file, bbox_extra_artists=(ch_lgd, pf_lgd,),
                bbox_inches='tight')


if __name__ == '__main__':
    # =================== PLOTS SPF vs GPF TELEPORTATION RATES ================
    if not os.path.exists('pngs'):
        os.makedirs('pngs')
    in_files = \
        [['data/W4xL4_SquareLatticeChannel_MW5_10000MC_SPF_TEL_RATE.csv',
          'data/W4xL4_SquareLatticeChannel_10000MC_GPF_TEL_RATE.csv'],
         ['data/W4xL4_HexagonalLatticeChannel_MW5_10000MC_SPF_TEL_RATE.csv',
          'data/W4xL4_HexagonalLatticeChannel_10000MC_GPF_TEL_RATE.csv'],
         ['data/W4xL4_TriangularLatticeChannel_MW5_10000MC_SPF_TEL_RATE.csv',
          'data/W4xL4_TriangularLatticeChannel_10000MC_GPF_TEL_RATE.csv'],
         ['data/B2xD3_TreeToTreeChannel_MW5_10000MC_SPF_TEL_RATE.csv',
          'data/B2xD3_TreeToTreeChannel_10000MC_GPF_TEL_RATE.csv'],
         ['data/W4xL4_CrazyGraphChannel_MW5_10000MC_SPF_TEL_RATE.csv',
          'data/W4xL4_CrazyGraphChannel_10000MC_GPF_TEL_RATE.csv']]
    styles = [{'color': 'b', 'line': '-', 'label': 'Square Lattice'},
              {'color': 'r', 'line': '-', 'label': 'Hexagonal Lattice'},
              {'color': 'g', 'line': '-', 'label': 'Triangular Lattice'},
              {'color': 'm', 'line': '-', 'label': 'Tree-to-Tree'},
              {'color': 'c', 'line': '-', 'label': 'Crazy Graph'}]
    out_file = 'pngs/SPF_and_GPF_tel_rate_diff_ALL.png'
    title = 'Stabilizer pathfinding performance under heralded loss'

    plot_spf_vs_gpf_teleport_rates(in_files, styles, title, out_file)
