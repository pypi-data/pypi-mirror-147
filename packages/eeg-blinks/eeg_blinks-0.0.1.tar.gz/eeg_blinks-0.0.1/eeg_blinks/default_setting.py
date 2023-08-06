import numpy as np

params = {'srate': 1024, 'stdThreshold': 1.50,
          'minEventLen': 0.05,
          'minEventSep': 0.05,
          'correlationThresholdTop': 0.980,
          'correlationThresholdBottom': 0.90,
          'params_blinkAmpRange_1': 0,
          'params_blinkAmpRange_2': 4,
          'params_goodRatioThreshold': 0.7,
          'params_minGoodBlinks': 10,
          'params_keepSignals': 0,
          'correlationThreshold': 0.98}



def getHeader ():
    header = ['mean', 'median', 'std',
              'mad', 'goodMean', 'goodMedian',
              'goodStd', 'goodMad']
    return dict ( zip ( header, [np.nan] * len ( header ) ) )


def getStatisticsStructure ():
    list_detail = ['subjectID', 'task', 'uniqueName',
                   'srate', 'startTime', 'usedNumber',
                   'usedLabel', 'status', 'seconds',
                   'numberBlinks','numberGoodBlinks',
                   'goodRatio', 'header', 'pAVRZ',
                   'nAVRZ', 'durationZ', 'durationB',
                   'durationT', 'durationHZ',
                   'durationHB', 'blinksPerMin']
    return dict ( zip ( list_detail, [np.nan] * len ( list_detail ) ) )