UNSIGNED16 hstgr_u16UpdateEvenBinHistogram_s32Input_u16BinSize(
    const HSTGR_CFG_U16_EVEN_BINS_S32_INPUT_T *const psConfig,
    UNSIGNED16 au16BinVals[],
    UNSIGNED16 u16BinValsNum,
    SIGNED32 s32Input,
    BOOL8 bForceInRange)
{
    UNSIGNED16 u16BinIdx = hstgr_BIN_IDX_OUT_OF_RANGE_D;

    if( (psConfig != NULL) && (au16BinVals != NULL) )
    {
        u16BinIdx = hstgr_u16GetEvenBinIdx_s32Input_u16BinSize(psConfig, s32Input, bForceInRange);

        if(u16BinIdx < u16BinValsNum)
        {
            au16BinVals[u16BinIdx]++;
        }
        else
        {
            u16BinIdx = hstgr_BIN_IDX_OUT_OF_RANGE_D;
        }
    }

    return u16BinIdx;
}
UNSIGNED16 hstgr_u16GetEvenBinIdx_s32Input_u16BinSize(
    const HSTGR_CFG_U16_EVEN_BINS_S32_INPUT_T *const psConfig,
    SIGNED32 s32Input,
    BOOL8 bForceInRange)
{
    UNSIGNED16 u16BinIdx = hstgr_BIN_IDX_OUT_OF_RANGE_D;
    SIGNED32 s32Min;
    SIGNED32 s32Max;

    if(psConfig != NULL)
    {
        s32Min = psConfig->s32Min;
        s32Max = psConfig->s32Min + ((SIGNED32)psConfig->u16BinSize *
            (SIGNED32)psConfig->u16BinsNum);

        if(psConfig->bInclBinMax == bFALSE)
        {
            s32Max--;
        }
        else
        {
            s32Min++;
        }

        if(s32Input < s32Min)
        {
            u16BinIdx = (bForceInRange == bTRUE) ? 0u : hstgr_BIN_IDX_OUT_OF_RANGE_D;
        }
        else if(s32Input > s32Max)
        {
            u16BinIdx = (bForceInRange == bTRUE) ? (psConfig->u16BinsNum - 1u) : hstgr_BIN_IDX_OUT_OF_RANGE_D;
        }
        else
        {
            u16BinIdx = (UNSIGNED16)((s32Input - s32Min) /
                (SIGNED32)psConfig->u16BinSize);
        }
    }

    return u16BinIdx;
}
void hstgr_vGetEvenBinAttrib_s32Input_u16BinSize(
    const HSTGR_CFG_U16_EVEN_BINS_S32_INPUT_T *const psConfig,
    UNSIGNED16 u16BinIdx,
    SIGNED32 *const ps32Min,
    SIGNED32 *const ps32Max,
    SIGNED32 *const ps32Mean)
{
    SIGNED32 s32BinMin;
    SIGNED32 s32BinMax;

    if(psConfig != NULL)
    {
        if(u16BinIdx < psConfig->u16BinsNum)
        {
            s32BinMin = psConfig->s32Min +
                ((SIGNED32)u16BinIdx * (SIGNED32)psConfig->u16BinSize);
            s32BinMax = s32BinMin + (SIGNED32)psConfig->u16BinSize;

            if(ps32Mean != NULL)
            {
                *ps32Mean = (s32BinMin + s32BinMax) / (SIGNED32)2;
            }

            if(psConfig->bInclBinMax == bFALSE)
            {
                s32BinMax--;
            }
            else
            {
                s32BinMin++;
            }

            if(ps32Min != NULL)
            {
                *ps32Min = s32BinMin;
            }

            if(ps32Max != NULL)
            {
                *ps32Max = s32BinMax;
            }
        }
    }
}
