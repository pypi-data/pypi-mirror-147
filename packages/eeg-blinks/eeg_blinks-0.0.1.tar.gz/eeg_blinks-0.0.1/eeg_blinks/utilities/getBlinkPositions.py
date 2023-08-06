import logging

import numpy as np
from tqdm import tqdm

from eeg_blinks.utilities.misc import mad_matlab

logging.getLogger().setLevel(logging.INFO)





def getBlinkPosition(params, sfreq,signal_eeg=None, ch='No_channel'):


    blinkComp = signal_eeg[0]
    mu = np.mean(blinkComp, dtype=np.float64)

    mad_val = mad_matlab(blinkComp)
    robustStdDev = 1.4826 * mad_val

    minBlink = params['minEventLen'] * sfreq # minimum blink frames
    threshold = mu + params['stdThreshold'] * robustStdDev  # actual threshold

    '''
    % The return structure.  Initially there is room for an event at every time
    % tick, to be trimmed later
    '''

    inBlink = False
    startBlinks = []
    endBlinks = []
    for index in tqdm(range(0, blinkComp.size), desc=f"Get blink start and end for channel {ch}"):
        Drule=~inBlink and (blinkComp[index] > threshold)
        if Drule:
            start = index
            inBlink = np.ones((1), dtype=bool)

        # if previous point was in a blink and signal retreats below threshold and duration greater than discard
        # threshold
        krule=inBlink==True and (blinkComp[index] < threshold)
        if krule:
            if (index - start) > minBlink:
                startBlinks.append(start)  # t_up
                endBlinks.append(index)  # t_dn

            inBlink = False

    arr_startBlinks = np.array(startBlinks) + 1  # Plus 1 to get similar result as in MATLAB
    arr_endBlinks = np.array(endBlinks) + 1

    positionMask = np.ones(arr_endBlinks.size,
                           dtype=bool)  # arr_endBlinks.size remove redundency using  numBlinks counter
    x = (arr_startBlinks[1:] - arr_endBlinks[:-1]) / params['srate']
    y = np.argwhere(x <= 0.05)
    positionMask[y] = np.zeros((1), dtype=bool)
    positionMask[y + 1] = np.zeros((1), dtype=bool)

    blink_position = {'start_blink': arr_startBlinks[positionMask],
                      'end_blink': arr_endBlinks[positionMask],
                      'ch': ch}

    return blink_position
