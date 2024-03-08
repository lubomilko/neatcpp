# include "utl.h"


#define avrg_DEFINE_FUNC_AVERAGE\
(STRG_CLS, VAL_T, SUM_T) \
    utltype_REF_MACRO_EXP_ARGS(avrg_DIRECT_DEFINE_FUNC_AVERAGE, STRG_CLS, \
        VAL_T, utltype_PRFX_LC(VAL_T), SUM_T, utltype_PRFX_LC(SUM_T))

#define avrg_DIRECT_DEFINE_FUNC_AVERAGE(STRG_CLS, \
    VAL_T, VAL_P, SUM_T, SUM_P\
    ) \
    STRG_CLS VAL_T avrg_ ## VAL_P ## Average_ ## SUM_P ## Sum(const VAL_T a ## VAL_P ## Vals[], \
        UNSIGNED16 u16ValsNum, BOOL8 bRound)\
    {\
        UNSIGNED16 u16Idx;\
        SUM_T SUM_P ## Sum = (SUM_T)0;\
        VAL_T VAL_P ## Avrg = (VAL_T)0;\
        \
        if( (a ## VAL_P ## Vals != NULL) && (u16ValsNum > 0u) )\
        {\
            /* Calculate the sum of all input values. */ \
            for(u16Idx = 0u; u16Idx < u16ValsNum; u16Idx++)\
            {\
                SUM_P ## Sum += (SUM_T)a ## VAL_P ## Vals[u16Idx];\
            }\
            \
            /* Calculate average. Use round up division if required: */\
            /* quotient = (dividend + (divisor / 2)) / divisor */\
            VAL_P ## Avrg = (bRound == bTRUE) ? \
                (VAL_T)((SUM_P ## Sum + ((SUM_T)u16ValsNum / (SUM_T)2)) / (SUM_T)u16ValsNum) : \
                (VAL_T)(SUM_P ## Sum / (SUM_T)u16ValsNum);\
        }\
        \
        return VAL_P ## Avrg;\
    }


avrg_DEFINE_FUNC_AVERAGE(static, UNSIGNED16, UNSIGNED32)