import numpy as np
import pandas as pd
from joblib import Parallel, delayed

from eeg_blinks.utilities.fitBlinks import fitBlinks
from eeg_blinks.utilities.misc import mad_matlab


def _extracBlinks(ch_data, raw, params):
    ch = ch_data['ch']
    print(ch)

    signal_eeg = raw.get_data(picks=ch)

    blinkPositions = ch_data


    blinkFits = fitBlinks(ch=ch, blinkPositions=blinkPositions,
                          signal_eeg=signal_eeg)  # First call in extracBlinks line 56

    df = pd.DataFrame(blinkFits)

    leftR2 = df[['leftR2']].to_numpy()

    leftZero = df[['leftZero']].to_numpy()

    rightR2 = df[['rightR2']].to_numpy()

    rightZero = df[['rightZero']].to_numpy()

    maxValues = df[['maxValues']].to_numpy()

    signal = signal_eeg[0]  # This should be a 1D array

    badIndices = np.isnan(leftZero) | np.isnan(rightZero) | np.isnan(maxValues) | np.isnan(
        leftR2) | np.isnan(rightR2)

    leftZero = leftZero[~badIndices].astype(int)
    rightZero = rightZero[~badIndices].astype(int)
    maxValues = maxValues[~badIndices]

    leftR2 = leftR2[~badIndices]
    rightR2 = np.absolute(rightR2)  # I am not sure required or not
    rightR2 = rightR2[~badIndices]

    blinkMask = np.zeros(signal.size, dtype=bool)

    for leftZero_y, rightZero_x in zip(leftZero - 1, rightZero, ):
        blinkMask[leftZero_y:rightZero_x] = True

    outsideBlink = np.logical_and(signal > 0, ~blinkMask)

    insideBlink = np.logical_and(signal > 0, blinkMask)

    blinkAmpRatio = np.mean(signal[insideBlink]) / np.mean(signal[outsideBlink])  # 2.0629878

    # Now calculate the cutoff ratios -- use default for the values
    goodMaskTop = np.logical_and(leftR2 >= params['correlationThresholdTop'],
                                 rightR2 >= params['correlationThresholdTop'])
    goodMaskBottom = np.logical_and(leftR2 >= params['correlationThresholdBottom'],
                                    rightR2 >= params['correlationThresholdBottom'])

    tt = sum(goodMaskTop)
    if tt < 2:
        pass
    #     print(1)

    bestValues = maxValues[goodMaskTop]
    worstValues = maxValues[~goodMaskBottom]
    goodValues = maxValues[goodMaskBottom]
    allValues = maxValues

    bestMedian = np.nanmedian(bestValues)  # 11.0237731933594
    bestRobustStd = 1.4826 * mad_matlab(bestValues)  # 2.69299754362106
    worstMedian = np.nanmedian(worstValues)  # 10.697759151458740
    worstRobustStd = 1.4826 * mad_matlab(worstValues)  # 2.658969497108459

    cutoff = (bestMedian * worstRobustStd + worstMedian * bestRobustStd) / (
            bestRobustStd + worstRobustStd)  # 10.8597297664580

    all_X = np.sum(np.logical_and(allValues <= bestMedian + 2 * bestRobustStd,
                                  allValues >= bestMedian - 2 * bestRobustStd))  # 162

    if all_X != 0:
        goodRatio = np.sum(np.logical_and(goodValues <= bestMedian + 2 * bestRobustStd,
                                          goodValues >= bestMedian - 2 * bestRobustStd)) / all_X  # 0.253086419753086
    else:
        goodRatio = np.nan
        # numberGoodBlinks = np.sum ( goodMaskBottom )  # 50
    numberGoodBlinks = np.sum(goodMaskBottom)
    ALL_DATA = [ch, blinkAmpRatio, bestMedian, bestRobustStd, cutoff, goodRatio, numberGoodBlinks,
                ch_data['start_blink'], ch_data['end_blink']]
    header_eb_label = ['ch', 'blinkAmpRatio', 'bestMedian', 'bestRobustStd', 'cutoff', 'goodRatio',
                       'numberGoodBlinks', 'start_blink', 'end_blink']
    data_blink = dict(zip(header_eb_label, ALL_DATA))

    return data_blink


def extracBlinks(blinkPositions_list, raw, params, njob):
    '''

    The data are required to be stored in dict style. ndarray with struct/dict inside.
    Refer to MATLAB that open in Python, to get the idea

    blinkPositions_list = all_result
    :return:

    '''

    if njob == 1:

        signalData = [_extracBlinks(ch_data, raw, params) for ch_data in blinkPositions_list]


    else:

        signalData = Parallel(n_jobs=njob, backend='threading', prefer='threads')(
            delayed(_extracBlinks)(ch_data, raw, params) for ch_data in blinkPositions_list)

    return signalData
