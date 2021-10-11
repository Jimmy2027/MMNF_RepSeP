"""Plot comparison of lr eval and gen coherence for different number of modalities."""
from matplotlib import pyplot as plt

from thesis.scripts.plots.utils import plot_comparisons

plot_comparisons(which='nbr_mods_comp', metric='coherence_eval')
