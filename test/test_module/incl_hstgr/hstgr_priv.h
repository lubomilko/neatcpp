#define BIN_TYPE_CC_EVEN_D       Even
#define BIN_TYPE_CC_DIFF_D       Diff
#define BIN_TYPE_CC(BIN_TYPE)    BIN_TYPE_CC_ ## BIN_TYPE ## _D

#define BUILD_GET_BIN_IDX_FUNC_NAME(BIN_TYPE_CC, INPUT_LC_P, BIN_SIZE_LC_P)\
    hstgr_u16Get ## BIN_TYPE_CC ## BinIdx_ ## INPUT_LC_P ## Input_ ## BIN_SIZE_LC_P ## BinSize

#define DIRECT_DEFINE_FUNC_UPDATE_HISTOGRAM(\
    STRG_CLS, BIN_TYPE_CC, BIN_TYPE, INPUT_T, INPUT_LC_P, INPUT_UC_P, BIN_SIZE_T, BIN_SIZE_LC_P, BIN_SIZE_UC_P, GET_BIN_IDX_FUNC)\
    STRG_CLS UNSIGNED16 hstgr_u16Update ## BIN_TYPE_CC ## BinHistogram_ ## INPUT_LC_P ## Input_ ## BIN_SIZE_LC_P ## BinSize(\
        const HSTGR_CFG_ ## BIN_SIZE_UC_P ## _ ## BIN_TYPE ## _BINS_ ## INPUT_UC_P ## _INPUT_T *const psConfig,\
        UNSIGNED16 au16BinVals[],\
        UNSIGNED16 u16BinValsNum,\
        INPUT_T INPUT_LC_P ## Input,\
        BOOL8 bForceInRange)\
    {\
        UNSIGNED16 u16BinIdx = hstgr_BIN_IDX_OUT_OF_RANGE_D;\
        \
        if( (psConfig != NULL) && (au16BinVals != NULL) )\
        {\
            u16BinIdx = GET_BIN_IDX_FUNC(psConfig, INPUT_LC_P ## Input, bForceInRange);\
            \
            if(u16BinIdx < u16BinValsNum)\
            {\
                au16BinVals[u16BinIdx]++;\
            }\
            else\
            {\
                u16BinIdx = hstgr_BIN_IDX_OUT_OF_RANGE_D;\
            }\
        }\
        \
        return u16BinIdx;\
    }

#define DIRECT_DEFINE_FUNC_GET_EVEN_BIN_IDX(\
    STRG_CLS, INPUT_T, INPUT_LC_P, INPUT_UC_P, BIN_SIZE_T, BIN_SIZE_LC_P, BIN_SIZE_UC_P)\
    STRG_CLS UNSIGNED16 hstgr_u16GetEvenBinIdx_ ## INPUT_LC_P ## Input_ ## BIN_SIZE_LC_P ## BinSize(\
        const HSTGR_CFG_ ## BIN_SIZE_UC_P ## _EVEN_BINS_ ## INPUT_UC_P ## _INPUT_T *const psConfig,\
        INPUT_T INPUT_LC_P ## Input,\
        BOOL8 bForceInRange)\
    {\
        UNSIGNED16 u16BinIdx = hstgr_BIN_IDX_OUT_OF_RANGE_D;\
        INPUT_T INPUT_LC_P ## Min;\
        INPUT_T INPUT_LC_P ## Max;\
        \
        if(psConfig != NULL)\
        {\
            INPUT_LC_P ## Min = psConfig->INPUT_LC_P ## Min;\
            INPUT_LC_P ## Max = psConfig->INPUT_LC_P ## Min + ((INPUT_T)psConfig->BIN_SIZE_LC_P ## BinSize *\
                (INPUT_T)psConfig->u16BinsNum);\
            \
            if(psConfig->bInclBinMax == bFALSE)\
            {\
                INPUT_LC_P ## Max--;\
            }\
            else\
            {\
                INPUT_LC_P ## Min++;\
            }\
            \
            if(INPUT_LC_P ## Input < INPUT_LC_P ## Min)\
            {\
                u16BinIdx = (bForceInRange == bTRUE) ? 0u : hstgr_BIN_IDX_OUT_OF_RANGE_D;\
            }\
            else if(INPUT_LC_P ## Input > INPUT_LC_P ## Max)\
            {\
                u16BinIdx = (bForceInRange == bTRUE) ? (psConfig->u16BinsNum - 1u) : hstgr_BIN_IDX_OUT_OF_RANGE_D;\
            }\
            else\
            {\
                u16BinIdx = (UNSIGNED16)((INPUT_LC_P ## Input - INPUT_LC_P ## Min) /\
                    (INPUT_T)psConfig->BIN_SIZE_LC_P ## BinSize);\
            }\
        }\
        \
        return u16BinIdx;\
    }

#define DIRECT_DEFINE_FUNC_GET_EVEN_BIN_ATTRIB(\
    STRG_CLS, INPUT_T, INPUT_LC_P, INPUT_UC_P, BIN_SIZE_T, BIN_SIZE_LC_P, BIN_SIZE_UC_P)\
    STRG_CLS void hstgr_vGetEvenBinAttrib_ ## INPUT_LC_P ## Input_ ## BIN_SIZE_LC_P ## BinSize(\
        const HSTGR_CFG_ ## BIN_SIZE_UC_P ## _EVEN_BINS_ ## INPUT_UC_P ## _INPUT_T *const psConfig,\
        UNSIGNED16 u16BinIdx,\
        INPUT_T *const p ## INPUT_LC_P ## Min,\
        INPUT_T *const p ## INPUT_LC_P ## Max,\
        INPUT_T *const p ## INPUT_LC_P ## Mean)\
    {\
        INPUT_T INPUT_LC_P ## BinMin;\
        INPUT_T INPUT_LC_P ## BinMax;\
        \
        if(psConfig != NULL)\
        {\
            if(u16BinIdx < psConfig->u16BinsNum)\
            {\
                INPUT_LC_P ## BinMin = psConfig->INPUT_LC_P ## Min +\
                    ((INPUT_T)u16BinIdx * (INPUT_T)psConfig->BIN_SIZE_LC_P ## BinSize);\
                INPUT_LC_P ## BinMax = INPUT_LC_P ## BinMin + (INPUT_T)psConfig->BIN_SIZE_LC_P ## BinSize;\
                \
                GET_BIN_ATTRIB_COMMON_CODE(INPUT_T, INPUT_LC_P)\
            }\
        }\
    }

#define GET_BIN_ATTRIB_COMMON_CODE(INPUT_T, INPUT_LC_P)\
    if(p ## INPUT_LC_P ## Mean != NULL)\
    {\
        *p ## INPUT_LC_P ## Mean = (INPUT_LC_P ## BinMin + INPUT_LC_P ## BinMax) / (INPUT_T)2;\
    }\
    \
    if(psConfig->bInclBinMax == bFALSE)\
    {\
        INPUT_LC_P ## BinMax--;\
    }\
    else\
    {\
        INPUT_LC_P ## BinMin++;\
    }\
    \
    if(p ## INPUT_LC_P ## Min != NULL)\
    {\
        *p ## INPUT_LC_P ## Min = INPUT_LC_P ## BinMin;\
    }\
    \
    if(p ## INPUT_LC_P ## Max != NULL)\
    {\
        *p ## INPUT_LC_P ## Max = INPUT_LC_P ## BinMax;\
    }