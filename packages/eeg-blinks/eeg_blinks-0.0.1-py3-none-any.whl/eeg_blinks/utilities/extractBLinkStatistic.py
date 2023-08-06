# import numpy as np
#
# def extractBLinkStatistic_step_three (params,usedSignal):
#
#     # if debug == True:
#     #     Data_b = loadmat ( f'{self.stored_folder}extracBlinkStatistic_data.mat', squeeze_me=True, struct_as_record=False )
#     #     blinkFits = Data_b ['blinkFits']  # blink fits for usedSignal 5, 'eeg fz-cpz', row 5 of the signalData
#     #
#     #     blinkProperties = Data_b [
#     #         'blinkProperties']  # blink properties for usedSignal 5, 'eeg fz-cpz', row 5 of the signalData
#     #     blinks = Data_b ['blinks']
#     #
#     #     # params = Data_b ['params']
#     #
#     # v = 1
#
#     correlationThreshold = params ['correlationThreshold']
#
#     '''
#     # Make sure enough arguments
#     # if nargin == 0:
#     #     blinkStatistics = getStatisticsStructure()
#     #     return
#     # elif nargin < 3:
#     #     raise ('getSummaryStatistics:NotEnoughArguments',
#     #         'Must be called with at least 3 arguments')
#     # elif nargin < 4:
#     #     correlationThreshold = 0.98
#     # else:
#     #     correlationThreshold = params.correlationThresholdTop;
#     #
#     ### bypass the above argument
#
#     # Check to make sure that the structures are non-empty
#
#     # if isempty(blinks) || isempty(blinkFits) || isempty(blinkProperties) || ...
#     #         length(blinkFits) ~= length(blinkProperties)
#     #     blinkStatistics = [];
#     #     return
#     '''
#
#     ## Now the summary fields
#
#     # if isnan ( blinks_usedSignal ):
#     #     blinkStatistics_status = 'failed'
#     #     raise( 'getSummaryStatistics:NoSignal', 'No blink signal' )
#     #     return
#
#     blinkStatistics = ds.getStatisticsStructure ()
#     blinkStatistics ['fileName'] = blinks.fileName
#     blinkStatistics ['subjectID'] = blinks.subjectID
#     blinkStatistics ['task'] = blinks.task
#     blinkStatistics ['srate'] = blinks.srate
#     blinkStatistics ['startTime'] = blinks.startTime
#     blinkStatistics ['uniqueName'] = blinks.uniqueName
#     blinkStatistics ['usedNumber'] = abs ( blinks.usedSignal )
#     blinkStatistics ['header'] = ds.getHeader ()
#
#     # Now the summary fields
#     # if isnan(blinks.usedSignal):
#     #     blinkStatistics.status = 'failed';
#     #     raise('getSummaryStatistics:NoSignal', 'No blink signal');
#     #     return
#     # end
#
#     '''
#     I believe we can ommit this part, redundent. For sure, the selected signal should be here already
#
#         # signalNumbers = cellfun ( @ double, {sData.signalNumber});
#     # pos = find ( signalNumbers == abs ( blinks.usedSignal ), 1, 'first' );
#     #
#     # if isempty ( pos ):
#     #     blinkStatistics_status = 'failed';
#     #     raise ( 'getSummaryStatistics:NoAcceptableSignal', 'Inconsistent structure' );
#     #     return
#
#     # if blinks.usedSignal < 0:
#     #     blinkStatistics['status'] = 'marginal'
#     # else:
#     #     blinkStatistics['status'] = 'good'
#
#     '''
#     # sData = blinks.signalData
#     # MATLAB USE LABEL 5 (signalNUmber), or atleast in struct in row no 10 of matlab, BUT HERE USE 9 (SINCE PYTHON START COUNTING FROM 0)
#     signalData_temporary_convention = blinks.signalData [
#         9]  # This is temporary approach, better used original file name instead of index, confusing
#
#     # numberBlinks = blinks.signalData [9].numberBlinks
#     theLabel = blinks.usedSignal  # lower ( sData ( pos ).signalLabel )
#     blinkStatistics ['usedLabel'] = theLabel  # IS THIS NECCESARY
#     blinkStatistics ['seconds'] = signalData_temporary_convention.signal.size / blinks.srate
#
#     blinkStatistics ['numberBlinks'] = signalData_temporary_convention.numberBlinks
#     blinkStatistics ['numberGoodBlinks'] = signalData_temporary_convention.numberGoodBlinks
#     blinkStatistics ['goodRatio'] = signalData_temporary_convention.goodRatio
#     '''
#     Equivalent to line 86-100 of extracBlinkStatistic
#     '''
#     leftR2 = np.array ( [conx.leftR2 for conx in blinkFits] )
#     rightR2 = np.array ( [conx.rightR2 for conx in blinkFits] )
#     leftR2_mask = np.isnan ( leftR2 )
#     rightR2_mask = np.isnan ( rightR2 )
#
#     goodBlinkMask = np.logical_and ( np.logical_and ( ~leftR2_mask, ~rightR2_mask ),
#                                      np.logical_and ( leftR2 >= correlationThreshold,
#                                                       rightR2 >= correlationThreshold ) )
#
#     pAVRZ = np.array ( [conx.posAmpVelRatioZero for conx in
#                         blinkProperties] )  # blink properties for usedSignal 5, 'eeg fz-cpz', row 5 of the signalData
#     nAVRZ = np.array ( [conx.negAmpVelRatioZero for conx in
#                         blinkProperties] )  # blink properties for usedSignal 5, 'eeg fz-cpz', row 5 of the signalData
#     durationZ = np.array ( [conx.durationZero for conx in
#                             blinkProperties] )  # blink properties for usedSignal 5, 'eeg fz-cpz', row 5 of the signalData
#     durationB = np.array ( [conx.durationBase for conx in
#                             blinkProperties] )  # blink properties for usedSignal 5, 'eeg fz-cpz', row 5 of the signalData
#     durationT = np.array ( [conx.durationTent for conx in
#                             blinkProperties] )  # blink properties for usedSignal 5, 'eeg fz-cpz', row 5 of the signalData
#     durationHZ = np.array ( [conx.durationHalfZero for conx in
#                              blinkProperties] )  # blink properties for usedSignal 5, 'eeg fz-cpz', row 5 of the signalData
#     durationHB = np.array ( [conx.durationHalfBase for conx in
#                              blinkProperties] )  # blink properties for usedSignal 5, 'eeg fz-cpz', row 5 of the signalData
#     ### SPECIAL CASE
#
#     all_stat = [pAVRZ, nAVRZ, durationZ, durationB, durationT, durationHZ, durationHB]
#     # blink_name=['pAVRZ', 'nAVRZ', 'durationZ', 'durationB,' 'durationT', 'durationHZ', 'durationHB']
#     header_stat = ['mean', 'median', 'std', 'mad', 'goodMean', 'goodMedian', 'goodStd', 'goodMad']
#     all_state_list = []
#     for values in all_stat:
#         goodValues = values [goodBlinkMask]
#         list_detail = [np.nanmean ( values ), np.nanmedian ( values ),
#                        np.nanstd ( values ), mad_matlab ( values ),
#                        np.nanmean ( goodValues ), np.nanmedian ( goodValues ),
#                        np.nanstd ( goodValues ), mad_matlab ( goodValues )]
#         # result = dict ( zip ( header_stat, list_detail ) )
#         all_state_list.append ( dict ( zip ( header_stat, list_detail ) ) )
#
#     #####
#     numberMinutes = signalData_temporary_convention.signal.size / (blinks.srate * 60)
#     goodBlinks = blinkFits [goodBlinkMask].size / numberMinutes
#     allBlinks = blinkFits.size / numberMinutes
#
#     all_zero = np.zeros ( len ( header_stat ) )
#     all_zero [0] = allBlinks
#     all_zero [4] = goodBlinks
#
#     rfinal = dict ( zip ( header_stat, all_zero ) )
#     return rfinal
