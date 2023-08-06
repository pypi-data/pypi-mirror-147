import logging

from joblib import Parallel, delayed

from . import default_setting
from eeg_blinks.utilities.extractBlinks import extracBlinks
from eeg_blinks.utilities.extractBlinks_reduceNumber import extracBLinks_reduce_number
from eeg_blinks.utilities.getBlinkPositions import getBlinkPosition
from eeg_blinks.utilities.misc import create_annotation

logging.getLogger().setLevel(logging.INFO)


# class blinker_eeg:

def BlinkPosition(raw, include=None, **kwargs):
    """
    Parameters
    ----------


    raw : instance of Raw

        The raw data.


    include : list of str
        List of channels to include (if None include all available).

        .. note:: This is to be treated as a set. The order of this list
           is not used or maintained in ``sel``.



    Returns
    -------

        annot: instance of Annotations

            The annotations.

        ch: The channel representative

        nGoodBlinks:

            The number of good blinks obtained from the representative channel
        """

    params = default_setting.params
    annot_description = kwargs.get('annot_label', 'eye_blink')
    njob = kwargs.get('njob', 1)

    ch_list=raw.ch_names if include is None else include
    sfreq = raw.info['sfreq']


    if njob == 1:

        all_result = [getBlinkPosition(params, sfreq, signal_eeg=raw.get_data(picks=ch), ch=ch) for ch in ch_list]

    else:

        all_result = Parallel(n_jobs=-1, backend='threading', prefer='threads')(
            delayed(getBlinkPosition)(params, sfreq,
                                   signal_eeg=raw.get_data(picks=ch),
                                   ch=ch) for ch in ch_list)

    signalData = extracBlinks(all_result, raw, params, njob)
    usedSignal = extracBLinks_reduce_number(signalData, params)

    annot, Ch, nGoodBlinks = create_annotation(usedSignal, sfreq, annot_description)

    return annot, Ch, nGoodBlinks

