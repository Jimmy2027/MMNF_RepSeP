"""Plot comparison over epochs for latent space eval and coherence eval."""

from thesis.scripts.plots.utils import plot_comparisons

plot_comparisons(which='epoch_comp', metric='coherence_eval')
