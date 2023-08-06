
import warnings

import numpy as np
import pandas as pd


def extracBLinks_reduce_number(signalData, params):
    '''

    Reduce the number of candidate signals based on these steps
    1) Reduce the number of candidate signals based on the blink amp ratios:
        -params ['params_blinkAmpRange_1'],params ['params_blinkAmpRange_2']
    2) Find the ones that meet the minimum good blink threshold
        -params ['params_goodRatioThreshold']
    3) See if any candidates meet the good blink ratio criteria

    4) Pick the one with the maximum number of good blinks

    '''

    filename = 'extracBLinks_reduce_number.hkl'
    # hkl.dump([signalData, params], filename)
    df = pd.DataFrame(signalData)
    blinkAmpRatios = df[['blinkAmpRatio']].to_numpy()

    params_blinkAmpRange_1 = params['params_blinkAmpRange_1']
    params_blinkAmpRange_2 = params['params_blinkAmpRange_2']
    params_goodRatioThreshold = params['params_goodRatioThreshold']
    params_minGoodBlinks = params['params_minGoodBlinks']
    params_keepSignals = params['params_keepSignals']

    # step 1

    goodIndices = np.logical_and(blinkAmpRatios >= params_blinkAmpRange_1,
                                 blinkAmpRatios <= params_blinkAmpRange_2)

    if sum(goodIndices) == 0 or (len(goodIndices) == 0):
        warnings.warn(f'Blink amplitude ratio too low -- may be noise.')
        status = 'Blink amplitude too low -- may be noise'
        dstatus = dict(status=status, usedSignal='NaN', signalData='NaN', ch='NaN')
        return dstatus

    df = df[goodIndices].reset_index(drop=True)

    goodCandidates = df[df['numberGoodBlinks'] > params_minGoodBlinks].reset_index(drop=True)

    if len(goodCandidates) == 0:
        warnings.warn(f"failure: fewer than '  {str(params_minGoodBlinks)} ' were found'")
        goodCandidates = goodCandidates[
            goodCandidates.numberGoodBlinks == goodCandidates.numberGoodBlinks.max()].reset_index(drop=True)
        ch_ref = goodCandidates['ch'].values.tolist()[0]
        numberGoodBlinks_val = goodCandidates['numberGoodBlinks'].values.tolist()[0]
        warnings.warn(
            f'As an alternative, I feed you channels {ch_ref} whose have the most numberGoodBlink ~ {numberGoodBlinks_val} albeit lower'
            f'than the threshold {params_minGoodBlinks}')
        status = f"failure: fewer than '  {str(params_minGoodBlinks)} ' were found'"
        dstatus = dict(status=status, usedSignal='NaN', signalData=goodCandidates, ch=ch_ref)
        return dstatus

    # Redudent, but just to follow the matlab convention
    signalData = goodCandidates.reset_index(drop=True)

    # Step 3
    # Now see if any candidates meet the good blink ratio criteria
    # warnings.warn(f'Temporary set params_goodRatioThreshold to 0.59 instead of the defaul value {params ["params_goodRatioThreshold"]}')
    # params_goodRatioThreshold = 0.59

    ratioIndices = signalData[signalData['goodRatio'] >= params_goodRatioThreshold].reset_index(drop=True)

    if len(ratioIndices) == 0:
        warnings.warn(f"failure: fewer than {str(params_goodRatioThreshold)}  were found")
        df1 = signalData[signalData.goodRatio == signalData.goodRatio.max()].reset_index(drop=True)
        ch_ref = df1['ch'].values.tolist()[0]
        goodRatio_val = df1['goodRatio'].values.tolist()[0]
        warnings.warn(
            f'As an alternative, I feed you channels {ch_ref} whose have the most numberGoodBlink ~ {goodRatio_val} albeit lower'
            f'than the threshold {params_goodRatioThreshold}')

        status = f"failure: '[Good ratio too low]'"

        dstatus = dict(status=status, usedSignal='NaN', signalData=df1, ch=ch_ref)

        return dstatus

    # Step 4
    # Now pick the one with the maximum number of good blinks
    representative_ch = ratioIndices[ratioIndices['numberGoodBlinks'] == ratioIndices['numberGoodBlinks'].max()]
    ch_ref = representative_ch['ch'].values.tolist()[0]

    return dict(status='success:', usedSignal=ch_ref, signalData=representative_ch, ch=ch_ref)



