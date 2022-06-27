# Copyright (c) 2021 brainlife.io
#
# This file is a MNE python-based brainlife.io App
#


# set up environment
import os
import json
import mne
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image

# Current path
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

# Load brainlife config.json
with open(__location__+'/config.json') as config_json:
    config = json.load(config_json)

# == LOAD DATA ==
fname = config['fif']
raw = mne.io.read_raw_fif(fname, verbose=False).crop(tmax=60)



ecg_projs, ecg_events = mne.preprocessing.compute_proj_ecg(raw, n_grad=1, n_mag=1, n_eeg=0,
                                                           average=True)

eog_projs, eog_events = mne.preprocessing.compute_proj_eog(raw, n_grad=1, n_mag=1,
                                                           n_eeg=1, average=True)
projs = eog_projs + ecg_projs

raw.add_proj(projs)
raw_cleaned = raw.copy().apply_proj()
#raw.plot()

# == SAVE FILE ==
raw_cleaned.save(os.path.join('out_dir','raw_cleaned.fif'))
mne.write_proj('out_dir/heartbeat-proj.fif', ecg_projs)
mne.write_proj('out_dir/blink-proj.fif', eog_projs)

mne.write_events('out_dir/ecg-events.fif', ecg_events)
mne.write_events('out_dir/eog-events.fif', eog_events)
#check the save
# # # == FIGURES ==
plt.figure(1)
raw.plot()
plt.savefig(os.path.join('out_figs','meg_epoch.png'))