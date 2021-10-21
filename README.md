# MMNF-RepSeP
The Reproducible Self Publishing toolkit for the Master Thesis "Multi Modal Generative Learning utilizing Normalizing Flows".

## Dependencies
* [MMVAE_Hub](git@github.com:Jimmy2027/MMVAE_Hub.git)
* [pythontex](https://github.com/gpoore/pythontex) (>=`0.16`)
* [texlive-latex](https://www.tug.org/texlive/)
* [graphviz](https://www.graphviz.org/)

## Usage
### Reproducing the original document
```
git clone git@github.com:Jimmy2027/MMNF_RepSeP.git
cd MMNF_RepSeP
./reproduce.sh
```

### Launch model training and evaluation
The script to launch the model training was written to work on the GPU cluster leomed from ETH Zurich.
- Adapt the paths in the config under `prepare_thesis/conf.json`
- `python prepare_thesis/launch_model_training.py` (this will launch the model training on leomed. This may take while.)
- When all jobs have finished executing, do:
```
./produce.sh
```
