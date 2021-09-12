"""Plot comparison of lr eval and gen coherence for different number of modalities."""

from thesis.scripts.plots.utils import plot_comparisons

plot_comparisons(which='nbr_mods_comp', metric='lat_eval')
