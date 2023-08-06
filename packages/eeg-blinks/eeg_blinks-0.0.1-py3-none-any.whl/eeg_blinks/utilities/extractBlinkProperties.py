"""

function [blinkProps, blinkFits] = extractBlinkProperties(signalData, params)
% Return a structure with blink shapes and properties for individual blinks
%
% Parameters:
%     signalData    signalData structure
%     params        params structure with parameters
    %     blinkProps    (output) structure with the blink properties
%     blinkFits     (output) structure with the blink landmarks
%
% BLINKER extracts blinks and ocular indices from time series.
% Copyright (C) 2016  Kay A. Robbins, Kelly Kleifgas, UTSA
%
% This program is free software: you can redistribute it and/or modify
% it under the terms of the GNU General Public License as published by
% the Free Software Foundation, either version 3 of the License, or
% (at your option) any later version.
%
% This program is distributed in the hope that it will be useful,
% but WITHOUT ANY WARRANTY; without even the implied warranty of
% MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
% GNU General Public License for more details.
    %
% You should have received a copy of the GNU General Public License
% along with this program.  If not, see <http://www.gnu.org/licenses/>.

%% Compute the fits

"""
import numpy as np
import pandas as pd

from eeg_blinks.utilities.fitBlinks import fitBlinks




def extractBlinkProperties(raw, srate, params, sData):


    srate = params['srate'];
    df = sData['signalData']
    df_data = df[df['ch'] == sData['usedSignal']]
    start_b = df_data['start_blink'].to_numpy()[0]
    end_b = df_data['end_blink'].to_numpy()[0]
    signal = raw.get_data(picks=sData['usedSignal'])
    # # signal = signalData.signal;
    blinkPositions = dict(start_blink=start_b, end_blink=end_b, ch=sData['usedSignal'])
    blinkFits = fitBlinks(ch=sData['usedSignal'], blinkPositions=blinkPositions,
                          signal_eeg=signal)

    bestMedian = df_data['bestMedian']
    bestRobustStd = df_data['bestRobustStd']
    # ##First reduce on the basis of blink maximum amplitude
    zThresholds = [0.90, 2, 0.98, 5]  # also availabe at getGOodBlinkMask
    #
    from eeg_blinks.utilities.getGoodBlinkMask import getGoodBlinkMask

    # # SLice only good blink. Expect lesser selection number
    blinkFits = getGoodBlinkMask(blinkFits, bestMedian, bestRobustStd, zThresholds)

    # srate = 150

    # blinkFits = loadmat ( '../blink_dev1.mat' )['blinkFits']
    # signal = loadmat('../signal_blink_prop.mat')['signal']
    # signal = np.array(signal).reshape((1, -1))

    signal_l = signal.shape[1]

    ## Compute the fits

    # blinkVelocity = diff(signalData.signal); # A matlab build in function
    blinkVelocity = np.diff(signal, axis=1)

    blinkFits.reset_index(drop=True, inplace=True)

    ## Blink durations
    blinkFits['durationBase'] = (blinkFits['rightBase'] - blinkFits['leftBase']) / srate
    blinkFits['durationTent'] = (blinkFits['rightXIntercept'] - blinkFits['leftXIntercept']) / srate
    blinkFits['durationZero'] = (blinkFits['rightZero'] - blinkFits['leftZero']) / srate
    blinkFits['durationHalfBase'] = (blinkFits['rightBaseHalfHeight'] - blinkFits['leftBaseHalfHeight'] + 1) / srate
    blinkFits['durationHalfZero'] = (blinkFits['rightZeroHalfHeight'] - blinkFits['leftZeroHalfHeight'] + 1) / srate

    ## Blink amplitude-velocity ratio from zero to max
    blinkFits['peaksPosVelZero'] = blinkFits.apply(
        lambda x: x['leftZero'] + np.argmax(blinkVelocity[0][x['leftZero']:x['maxFrame'] + 1]), axis=1)

    # TODO TO remove the minus 1 >> blinkFits['maxFrame']-1
    blinkFits['RRC'] = signal[0][blinkFits['maxFrame'] - 1] / blinkVelocity[0][blinkFits['peaksPosVelZero']]
    blinkFits['posAmpVelRatioZero'] = (100 * abs(blinkFits['RRC'])) / srate

    blinkFits['downStrokevelFrame_del'] = blinkFits.apply(
        lambda x: x['maxFrame'] + np.argmin(blinkVelocity[0][x['maxFrame']:x['rightZero'] + 1]), axis=1)

    blinkFits['TTT'] = signal[0][blinkFits['maxFrame'] - 1] / blinkVelocity[0][blinkFits['downStrokevelFrame_del']]
    blinkFits['negAmpVelRatioZero'] = (100 * abs(blinkFits['TTT'])) / srate

    ## Blink amplitude-velocity ratio from base to max

    blinkFits['peaksPosVelBase'] = blinkFits.apply(
        lambda x: x['leftBase'] + np.argmax(blinkVelocity[0][x['leftBase']:x['maxFrame'] + 1]), axis=1)
    blinkFits['KKK'] = signal[0][blinkFits['maxFrame'] - 1] / blinkVelocity[0][blinkFits['peaksPosVelBase']]
    blinkFits['posAmpVelRatioBase'] = (100 * abs(blinkFits['KKK'])) / srate

    blinkFits['downStroke_del'] = blinkFits.apply(
        lambda x: x['maxFrame'] + np.argmin(blinkVelocity[0][x['maxFrame']:x['rightBase'] + 1]), axis=1)
    blinkFits['KKK'] = signal[0][blinkFits['maxFrame'] - 1] / blinkVelocity[0][blinkFits['downStroke_del']]
    blinkFits['negAmpVelRatioBase'] = (100 * abs(blinkFits['KKK'])) / srate

    ## Blink amplitude-velocity ratio estimated from tent slope

    # TODO TO remove the minus 1 >> blinkFits['maxFrame']-1
    blinkFits['pop'] = signal[0][blinkFits['maxFrame'] - 1] / blinkFits['averRightVelocity']
    blinkFits['negAmpVelRatioTent'] = (100 * abs(blinkFits['pop'])) / srate

    blinkFits['opi'] = signal[0][blinkFits['maxFrame'] - 1] / blinkFits['averLeftVelocity']
    blinkFits['WE'] = (100 * abs(blinkFits['opi']))
    blinkFits['posAmpVelRatioTent'] = blinkFits['WE'] / srate

    ## Time zero shut
    shutAmpFraction = 0.9
    blinkFits['closingTimeZero'] = (blinkFits['maxFrame'] - blinkFits['leftZero']) / srate

    blinkFits['reopeningTimeZero'] = (blinkFits['rightZero'] - blinkFits['maxFrame']) / srate

    blinkFits['ampThreshhold'] = shutAmpFraction * blinkFits['maxValues']
    blinkFits['start_shut_tzs'] = blinkFits.apply(
        lambda x: np.argmax(signal[0][x['leftZero']:x['rightZero'] + 1] >= x['ampThreshhold']), axis=1)

    blinkFits['endShut_tzs'] = blinkFits.apply(
        lambda x: np.argmax(signal[0][x['leftZero']:x['rightZero'] + 1][x['start_shut_tzs'] + 1:-1] <
                            shutAmpFraction * x['maxValues']), axis=1)

    # leftZero = blinkFits.loc[0, 'leftZero']
    # rightZero = blinkFits.loc[0, 'rightZero']

    ## PLease expect error here, some value maybe zero or lead to empty cell
    blinkFits['endShut_tzs'] = blinkFits['endShut_tzs'] + 1  ## temporary  to delete
    blinkFits['timeShutZero'] = blinkFits.apply(
        lambda x: 0 if x['endShut_tzs'] == np.isnan else x['endShut_tzs'] / srate, axis=1)

    ## Time base shut
    shutAmpFraction = 0.9
    blinkFits['ampThreshhold_tbs'] = shutAmpFraction * blinkFits['maxValues']
    blinkFits['start_shut_tbs'] = blinkFits.apply(
        lambda x: np.argmax(signal[0][x['leftBase']:x['rightBase'] + 1] >= x['ampThreshhold_tbs']), axis=1)

    blinkFits['endShut_tbs'] = blinkFits.apply(
        lambda x: np.argmax(signal[0][x['leftBase']:x['rightBase'] + 1][x['start_shut_tbs']:-1] <
                            shutAmpFraction * x['maxValues']), axis=1)

    ## PLease expect error here, some value maybe zero or lead to empty cell
    ### PLease note the diffrent name here >> timeShutBase
    blinkFits['timeShutBase'] = blinkFits.apply(
        lambda x: 0 if x['endShut_tbs'] == np.isnan else (x['endShut_tbs'] / srate), axis=1)

    ## Time shut tent
    blinkFits['closingTimeTent'] = (blinkFits['xIntersect'] - blinkFits['leftXIntercept']) / srate
    blinkFits['reopeningTimeTent'] = (blinkFits['rightXIntercept'] - blinkFits['xIntersect']) / srate

    blinkFits['ampThreshhold_tst'] = shutAmpFraction * blinkFits['maxValues']

    blinkFits[['leftXIntercept_int', 'rightXIntercept_int']] = blinkFits[['leftXIntercept', 'rightXIntercept']].astype(
        int)
    blinkFits['start_shut_tst'] = blinkFits.apply(
        lambda x: np.argmax(signal[0][x['leftXIntercept_int']:x['rightXIntercept_int'] + 1] >= x['ampThreshhold']),
        axis=1)

    blinkFits['endShut_tst'] = blinkFits.apply(
        lambda x: np.argmax(signal[0][x['leftXIntercept_int']:x['rightXIntercept_int'] + 1][x['start_shut_tst']:-1] <
                            shutAmpFraction * x['maxValues']), axis=1)

    ## PLease expect error here, some value maybe zero or lead to empty cell
    ### PLease note the diffrent name here >> timeShutTent
    blinkFits['timeShutTent'] = blinkFits.apply(
        lambda x: 0 if x['endShut_tst'] == np.isnan else (x['endShut_tst'] / srate), axis=1)

    ## Other times
    blinkFits['peakMaxBlink '] = blinkFits['maxValues']
    blinkFits['peakMaxTent'] = blinkFits['yIntersect']
    blinkFits['peakTimeTent'] = blinkFits['xIntersect'] / srate
    blinkFits['peakTimeBlink'] = blinkFits['maxFrame'] / srate

    dfcal = blinkFits[['maxFrame', 'peaksPosVelBase', 'peaksPosVelZero']]

    df_t = pd.DataFrame.from_records([[signal_l] * 3], columns=['maxFrame', 'peaksPosVelBase', 'peaksPosVelZero'])

    dfcal = pd.concat([dfcal, df_t]).reset_index(drop=True)

    dfcal['ibmx'] = dfcal.maxFrame.diff().shift(-1)

    dfcal['interBlinkMaxAmp'] = dfcal['ibmx'] / srate

    dfcal['ibmvb'] = 1 - dfcal['peaksPosVelBase']
    dfcal['interBlinkMaxVelBase'] = dfcal['ibmvb'] / srate  # peaksPosVelBase == velFrame

    dfcal['ibmvz'] = 1 - dfcal['peaksPosVelZero']
    dfcal['interBlinkMaxVelZero'] = dfcal['ibmvz'] / srate

    dfcal.drop(dfcal.tail(1).index, inplace=True)  # drop last n rows# peaksPosVelZero == velFrame
    dfnew = blinkFits[['maxValues', 'posAmpVelRatioZero']]

    pAVRThreshold = 3
    R1 = dfnew['posAmpVelRatioZero'] < pAVRThreshold
    bestMedian, bestRobustStd = 94.156208105121580, 28.368641236303578
    th_bm_brs = bestMedian - bestRobustStd
    R2 = dfnew['maxValues'] < th_bm_brs
    pMask = pd.concat([R1, R2], axis=1)
    pMasks = pMask.all(1)
    df_res = pd.concat([blinkFits, dfcal], axis=1)
    df_res = df_res[~pMasks]
    kk = 1
    return df_res


