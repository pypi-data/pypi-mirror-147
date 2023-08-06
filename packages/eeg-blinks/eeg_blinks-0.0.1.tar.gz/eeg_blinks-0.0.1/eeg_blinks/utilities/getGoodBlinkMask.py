import pandas as pd


def get_mask(df,indicesNaN,specifiedMedian,specifiedStd,correlationThreshold,zScoreThreshold):
    R1=~indicesNaN
    R2=df['leftR2']>=correlationThreshold
    R3=df['rightR2']>=correlationThreshold
    R4=df['maxValues']>= max(0, specifiedMedian - zScoreThreshold*specifiedStd)
    R5=df['maxValues']<=specifiedMedian + zScoreThreshold*specifiedStd
    df1 = pd.concat([R1,R2,R3,R4,R5],axis=1)
    return df1


def getGoodBlinkMask(blinkFits, specifiedMedian, specifiedStd, zThresholds):
    goodBlinkMask = [];
    if blinkFits == None:
        return;
    # elseif nargin < 4
    # zThresholds = [0.90, 2, 0.98, 5];
    # end
    correlationThreshold, zScoreThreshold = zThresholds[0], zThresholds[1]
    df = pd.DataFrame(blinkFits)
    df['rightR2']=df['rightR2'].abs()
    df_data=df[['leftR2','rightR2','maxValues']]

    indicesNaN =df_data.isnull().any(1)

    specifiedMedian=94.156208105121580
    specifiedStd=28.368641236303578


    correlationThreshold_s1=0.9
    zScoreThreshold_s1=2



    df1 =get_mask(df_data,indicesNaN,specifiedMedian,specifiedStd,correlationThreshold_s1,zScoreThreshold_s1)
    goodBlinkMask_s1 =df1.all(1)
    #####

    correlationThreshold_s2=0.98
    zScoreThreshold_s2=5

    df_s2=get_mask(df_data,indicesNaN,specifiedMedian,specifiedStd,correlationThreshold_s2,zScoreThreshold_s2)


    ff_s2 =df_s2.all(1)
    df_s2a = pd.concat([goodBlinkMask_s1,ff_s2],axis=1)
    goodBlinkMask=df_s2a.any(1)

    # return goodBlinkMask, specifiedMedian, specifiedStd
    blinkFits=df[goodBlinkMask]
    return blinkFits