
import numpy as np
import mne

def mad_matlab(arr, axis=None, keepdims=True):
    median = np.median(arr, axis=axis, keepdims=True)
    mad = np.median(np.abs(arr - median), axis=axis, keepdims=keepdims)[0]
    return mad


def create_annotation(usedSignal,sfreq,label):
    # sfreq=150

    sblink = usedSignal['signalData']

    d_s = ((sblink['end_blink'] - sblink['start_blink']) / sfreq).tolist()[0].tolist()
    onset_s = (sblink['start_blink'] / sfreq).tolist()[0].tolist()

    des_s = [label] * len(onset_s)

    annot = mne.Annotations(onset=onset_s,  # in seconds
                               duration=d_s,  # in seconds, too
                               description=des_s)
    numberGoodBlinks = sblink['numberGoodBlinks'].head().tolist()
    Ch = sblink['ch'].head().tolist()[0]
    nblinks = len(sblink['start_blink'].tolist()[0].tolist())

    return annot, Ch,numberGoodBlinks