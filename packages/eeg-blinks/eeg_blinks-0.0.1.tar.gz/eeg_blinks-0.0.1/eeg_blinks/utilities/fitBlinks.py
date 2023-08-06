
import numpy as np

from eeg_blinks import default_setting as ds


def get_zero_crossing (k, maxFrames, maxValues, outerStarts, outerEnds, candidateSignal, blinkVelocity,
                       baseFraction):

    hhh=ds
    number = k
    maxFrame = maxFrames [k] [0]
    maxValue = maxValues [k]
    leftOuter = outerStarts [k]
    rightOuter = outerEnds [k]

    ## Compute the left and right inner (0 crossing)

    try:
        # aaqw=outerStarts [k]
        theRange = np.arange ( outerStarts [k], maxFrame )
    except ValueError:
        # aaqw = outerStarts [k][0]
        # The problem here is arise as in some instances, the outerStarts contains 2 values.
        # Need to check in previous step, to remove double value outerStarts
        theRange = np.arange ( outerStarts [k] [0], maxFrame )

    minIndex = np.where ( candidateSignal [theRange] == np.amin ( candidateSignal [theRange] ) )
    minFrame = theRange [minIndex]
    theRange = np.arange ( minFrame, maxFrame )

    # The following try-except akin to if else in LIne 68 Matlab
    try:
        sInd = np.argwhere ( candidateSignal [theRange] <= 0 ) [-1]
        leftZero = theRange [sInd]
    except IndexError:  # Take the smallest value before in the interval LINE 70 Matlab
        minValuessig = np.amin ( candidateSignal [theRange] )
        sInd = np.where ( candidateSignal [theRange] == minValuessig )
        leftZero = theRange [sInd]

    # TODO
    # Do something when `a` is empty
    # Start Line 74 Matlab
    try:
        theRange = np.arange ( maxFrame, outerEnds [k] )
        minIndex2 = np.where ( candidateSignal [theRange] == np.amin ( candidateSignal [theRange] ) )
        minFrame = theRange [minIndex2]
        theRange = np.arange ( maxFrame, minFrame )
        sInd = np.argwhere ( candidateSignal [theRange] <= 0 ) [0]
        rightZero = theRange [sInd]

    except (IndexError, ValueError):  # Take the smallest value before in the interval

        sInd = np.where ( candidateSignal [theRange] == np.amin ( candidateSignal [theRange] ) )
        rightZero = theRange [sInd]

    # Compute the place of maximum positive and negative velocities
    ## START FROM LINE 87 MATLAB
    upStroke = np.arange ( leftZero, maxFrame )
    maxPosVelFrame = np.where ( blinkVelocity [upStroke] == np.amax ( blinkVelocity [upStroke] ) )
    maxPosVelFrame = maxPosVelFrame + upStroke [0]

    downStroke = np.arange ( maxFrame, rightZero )
    # maxNegVelFrame = np.where ( blinkVelocity [downStroke] == np.amin ( blinkVelocity [downStroke] ) )
    try:
        AAXX = np.amin ( blinkVelocity [downStroke] )
        AAAA = blinkVelocity [downStroke]
        maxNegVelFrame = np.where ( AAAA == AAXX )
    except (IndexError, ValueError) as e:
        # I did not find any way how to bypass this problem
        # MATLAB LIne 92
        if e.__class__ == ValueError:
            print ( 'Most probably downStroke len is zero.' )
        elif e.__class__ == IndexError:
            print ( 'To investigate' )
        data_blink = dict ( zip ( ds.fit_struc_label, [np.nan] * len ( ds.fit_struc_label ) ) )
        return data_blink

    maxNegVelFrame = maxNegVelFrame + downStroke [0]
    if maxNegVelFrame.size >= 2:
        maxNegVelFrame = maxNegVelFrame [0] [0]
    # Compute the left and right base frames
    try:
        leftBase = np.arange ( leftOuter, maxPosVelFrame )
    except ValueError:
        # Same issue here, in some instances, the leftouter contain two value
        leftBase = np.arange ( leftOuter [0], maxPosVelFrame )
    leftBaseVelocity = np.flip ( blinkVelocity [leftBase] )

    '''
     if leftBaseIndex.size == 0:  # Line 99 Matlab
        leftBaseIndex = 0
    '''
    try:
        leftBaseIndex = np.argwhere ( leftBaseVelocity <= 0 ) [0]  # IDX_1 86
    except IndexError:  # Line 99 Matlab
        leftBaseIndex = 0

    leftBase = maxPosVelFrame - leftBaseIndex

    # Start Line 102 Matlab
    a_tend = np.minimum ( rightOuter, candidateSignal.size - 1 )
    rightBase = np.arange ( maxNegVelFrame, a_tend )  # Line 102 matlab
    # try:
    #     rightBase = np.arange ( maxNegVelFrame, a_tend )  # Line 102 matlab
    # except:
    #     printcc = 1
    rightBaseVelocity = blinkVelocity [rightBase]  # -0.26348615	-0.26243246	-0.25998008	-0.25606441....

    '''
    if rightBaseIndex.size == 0:  # Line 108 Matlab
        rightBaseIndex = 0
    '''
    try:
        rightBaseIndex = np.argwhere ( rightBaseVelocity >= 0 ) [0]
    except IndexError:  # Line 108 Matlab
        rightBaseIndex = 0

    rightBase = maxNegVelFrame + rightBaseIndex

    leftHalfBase = np.arange ( leftBase - 2, maxFrame + 1 )
    ryy = candidateSignal [maxFrame] - candidateSignal [leftBase - 2]  # 11.207063674926758
    blinkHalfHeight = candidateSignal [maxFrame] - (0.5 * (ryy))  # 3.145895004272461

    try:
        leftBaseHalfHeight = leftBase + (np.argwhere ( candidateSignal [leftHalfBase] >= blinkHalfHeight [0] ) [0])
    except ValueError:  # MATLAB Line 121
        leftBaseHalfHeight = np.nan
    # if leftBaseHalfHeight.size == 0:  # MATLAB Line 121
    #     leftBaseHalfHeight = np.nan

    rightHalfBase = np.arange ( maxFrame, rightOuter + 1 )

    '''
    I think this is similar to 
    if rightBaseHalfHeight.size == 0:
        rightBaseHalfHeight = np.nan
    '''
    try:
        rightBaseHalfHeight = np.minimum ( rightOuter, maxFrame +
                                           np.argwhere (
                                               candidateSignal [rightHalfBase] <= blinkHalfHeight [0] ) [
                                               0] )
    except (IndexError, ValueError):
        rightBaseHalfHeight = np.nan

    # Compute the left and right half-height frames from zero
    leftHalfBase = np.arange ( leftZero, maxFrame ) + 1
    blinkHalfHeight = 0.5 * candidateSignal [maxFrame]  # 4.3747134

    '''
    Should this line throw an error:

    if leftZeroHalfHeight.size == 0:
        leftZeroHalfHeight = np.nan

    Please change to

    try:
        leftZeroHalfHeight = leftZero + (np.argwhere ( candidateSignal [leftHalfBase] >= blinkHalfHeight ) [0])  #
    except IndexError:
        leftZeroHalfHeight = np.nan
    '''

    try:
        leftZeroHalfHeight = leftZero + (np.argwhere ( candidateSignal [leftHalfBase] >= blinkHalfHeight ) [0])
    except ValueError:
        leftZeroHalfHeight = np.nan
    # if leftZeroHalfHeight.size == 0:
    #     leftZeroHalfHeight = np.nan

    rightHalfBase = np.arange ( maxFrame, rightZero + 1 )

    '''
    if rightZeroHalfHeight.size == 0:
        rightZeroHalfHeight = np.nan
    '''
    try:
        rightZeroHalfHeight = np.minimum ( rightOuter, maxFrame + np.argwhere (
            candidateSignal [rightHalfBase] <= blinkHalfHeight ) [0] )
    except (IndexError, ValueError):
        rightZeroHalfHeight = np.nan

    # Compute fit ranges
    blinkHeight = candidateSignal [maxFrame] - candidateSignal [leftZero]  # 8.8286028
    blinkTop = candidateSignal [maxFrame] - baseFraction * blinkHeight  # 7.8665667

    blinkBottom = candidateSignal [leftZero] + baseFraction * blinkHeight  # 0.80368418

    blinkRange = np.arange ( leftZero, maxFrame + 1 )
    blinkTopPoint = np.argwhere ( candidateSignal [blinkRange] < blinkTop ) [-1]
    # try:
    #
    #     blinkTopPoint = np.argwhere ( candidateSignal [blinkRange] < blinkTop ) [-1]
    # except ValueError:
    #     # I still believe, the best course of action is
    #     blinkTopPoint = np.argwhere ( candidateSignal [blinkRange] < blinkTop[0] ) [-1]

    blinkBottomPoint = np.argwhere ( candidateSignal [blinkRange] > blinkBottom ) [0]

    xLeft = np.arange ( blinkRange [blinkBottomPoint],
                        blinkRange [blinkTopPoint] + 1 )  # ARE WE SUPPOSE TO TRANSPOSE HERE?
    leftRange = [blinkRange [blinkBottomPoint][0].item(), blinkRange [blinkTopPoint][0].item()]
    # START HERE
    blinkRange = np.arange ( maxFrame, rightZero + 1 )

    blinkTopPoint_ = np.argwhere ( candidateSignal [blinkRange] < blinkTop ) [0]

    blinkBottomPoint_ = np.argwhere ( candidateSignal [blinkRange] > blinkBottom ) [-1]
    rightRange = [blinkRange [blinkTopPoint_][0].item(), blinkRange [blinkBottomPoint_][0].item()]  # LIST: 6210	6288
    '''
    In MATLAB, THE REPRESENTATION IS AS BELOW
    xLeft = np.arange ( leftRange ( 1 ), leftRange ( 2 )) # ARE WE SUPPOSE TO TRANSPOSE HERE?
    xRight = np.arange ( rightRange( 1 ), rightRange ( 2 )) # ARE WE SUPPOSE TO TRANSPOSE HERE?

    TO SIMPLIFY, WE CHANGE TO

    xLeft = np.arange (AXAX, ACAC) # ARE WE SUPPOSE TO TRANSPOSE HERE?
    xRight = np.arange (ARAR, ATAT) # ARE WE SUPPOSE TO TRANSPOSE HERE?

    '''

    xRight = np.arange ( blinkRange [blinkTopPoint_],
                         blinkRange [blinkBottomPoint_] + 1 )  # ARE WE SUPPOSE TO TRANSPOSE HERE?

    # Below and above for types
    if (len ( xLeft ) > 1) & (len ( xRight ) > 1):
        yRight = candidateSignal [xRight]  # do not delete
        yLeft = candidateSignal [xLeft]  # do not delete

        domain_right = np.std ( xRight ) * np.arange ( -1, 2, 2 ) + np.mean ( xRight )
        pRight = np.polynomial.Polynomial.fit ( xRight, yRight, 1, domain=domain_right )
        rightXIntercept = pRight.roots ()  # 6.336226562500000e+03

        domain_left = np.std ( xLeft ) * np.arange ( -1, 2, 2 ) + np.mean ( xLeft )
        pLeft = np.polynomial.Polynomial.fit ( xLeft, yLeft, 1, domain=domain_left )
        leftXIntercept = pLeft.roots ()  # 6.1648716e+03

        left_line = np.polynomial.Polynomial.fit ( xLeft, yLeft, 1, domain=[-1, 1] )
        right_line = np.polynomial.Polynomial.fit ( xRight, yRight, 1, domain=[-1, 1] )
        xIntersect = (left_line - right_line).roots ()  # x0 6.192071289062500e+03
        yIntersect = left_line ( xIntersect )  # y0=9.931675910949707

        leftSlope = yIntersect / (xIntersect - leftXIntercept)  # 0.36513907
        rightSlope = yIntersect / (xIntersect - rightXIntercept)  # -0.068895683
        averLeftVelocity = pLeft.coef [1] / np.std ( xLeft )  # 0.36513701
        averRightVelocity = pRight.coef [1] / np.std ( xRight )  # -0.068895057

        '''
        There are two way to calculate the  corrcoef
        Either
        1) # coefs_left = np.polyfit ( xLeft, yLeft, 1 )
        # ffit_left = np.polyval ( coefs_left, xLeft )

        or 2) 

        ffit_right = np.polyval ( pRight.coef, xRight )
        ffit_left = np.polyval ( pLeft.coef, xLeft )
        '''

        ffit_right = np.polyval ( pRight.coef, xRight )
        ffit_left = np.polyval ( pLeft.coef, xLeft )

        rightR2 = np.corrcoef ( yRight.flatten (), ffit_right.flatten () ) [0, 1]
        leftR2 = np.corrcoef ( yLeft.flatten (), ffit_left.flatten () ) [0, 1]

        try:
            leftBaseHalfHeight=leftBaseHalfHeight[0].item()
        except:
            leftBaseHalfHeight=np.nan

        try:
            leftZero=leftZero.item()

        except AttributeError:
            leftZero=np.nan

        rightZero=rightZero.item()
        leftBase=leftBase[0].item()
        rightBase=rightBase[0].item()

        try:
            rightBaseHalfHeight=rightBaseHalfHeight.item()
        except AttributeError:
            rightBaseHalfHeight=np.nan

        try:
            rightZeroHalfHeight=rightZeroHalfHeight.item()
        except AttributeError:
            rightZeroHalfHeight=np.nan

        leftZeroHalfHeight=leftZeroHalfHeight.item()
        leftSlope=leftSlope.item()
        rightSlope=rightSlope.item()
        xIntersect=xIntersect.item()
        yIntersect=yIntersect.item()
        leftXIntercept=leftXIntercept.item()
        rightXIntercept=rightXIntercept.item()

        slabel = [  'number', 'maxFrame', 'maxValues', 'leftOuter', 'rightOuter', 'leftZero', 'rightZero',
                    'leftBase','rightBase', 'leftBaseHalfHeight', 'rightBaseHalfHeight', 'rightZeroHalfHeight','leftZeroHalfHeight',
                    'leftRange' ,'rightRange','leftSlope','rightSlope', 'averLeftVelocity', 'averRightVelocity',
                    'leftR2', 'rightR2', 'xIntersect', 'yIntersect', 'leftXIntercept', 'rightXIntercept']

        data = [number, maxFrame, maxValue, leftOuter, rightOuter, leftZero, rightZero,
                leftBase, rightBase, leftBaseHalfHeight, rightBaseHalfHeight, rightZeroHalfHeight,leftZeroHalfHeight,
                leftRange,rightRange, leftSlope, rightSlope, averLeftVelocity, averRightVelocity,
                leftR2, rightR2, xIntersect, yIntersect, leftXIntercept, rightXIntercept]

        data_blink = dict ( zip ( slabel, data ) )

        return data_blink


def fitBlinks (signal_eeg=None, ch='No_channel', blinkPositions=None):

    candidateSignal = signal_eeg [0]
    startBlinks = blinkPositions ['start_blink']
    endBlinks = blinkPositions ['end_blink']

    maxValues = []
    maxFrames = []
    #############
    for idx in range ( 0, startBlinks.size ):
        blinkRange = np.arange ( startBlinks [idx], endBlinks [idx] )
        dff = candidateSignal [startBlinks [idx]:endBlinks [idx]]
        maxInd = np.where ( dff == np.amax ( dff ) )
        maxValues.append ( np.amax ( dff ) )
        maxFrames.append ( blinkRange [maxInd] )

    ## Calculate the fits

    baseFraction = 0.1  # Fraction from top and bottom
    maxFrames = np.array ( maxFrames )
    maxValues = np.array ( maxValues )
    outerStarts = np.append ( 0, maxFrames [0:-1] )
    outerEnds = np.append ( maxFrames [1:], candidateSignal.size )

    blinkVelocity = np.diff ( candidateSignal, axis=0 )

    all_data_blink = []

    for k in range ( 0, maxFrames.size ):
        # Find the zero crossing or the minimum between blinks
        data_blink = get_zero_crossing ( k, maxFrames, maxValues, outerStarts, outerEnds,
                                              candidateSignal, blinkVelocity, baseFraction )

        if data_blink is not None:
            all_data_blink.append ( data_blink )

    return all_data_blink