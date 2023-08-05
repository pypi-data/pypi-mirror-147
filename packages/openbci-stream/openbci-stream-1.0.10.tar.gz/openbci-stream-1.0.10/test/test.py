from openbci_stream.utils import HDF5Reader
from matplotlib import pyplot as plt
import numpy as np


filename = 'record-02_28_22-10_43_36.c.h5'

with HDF5Reader(filename) as reader:

    eeg = reader.eeg
    aux = reader.aux
    timestamp = reader.timestamp
    aux_timestamp = reader.aux_timestamp
    header = reader.header
    markers = reader.markers

    print(reader)


data, cls = reader.get_data(
    tmax=4.5, tmin=-0.5, ref='Cz', markers=['Left', 'Up', 'Bottom', 'INC', 'Right'])

rises = reader.get_rises(aux[0], aux_timestamp[0], lower=200, upper=850)
reader.fix_markers(['Left', 'Up', 'Bottom', 'INC', 'Right'], rises, 3000)

epochs = reader.get_epochs(tmax=4.5, tmin=-0.5, ref='Cz', markers=[
                           'Left_fixed', 'Up_fixed', 'Bottom_fixed', 'INC_fixed', 'Right_fixed'])


