#define utltype_PRFX_LC_SIGNED8_D                           s8
#define utltype_PRFX_LC_SIGNED16_D                          s16
#define utltype_PRFX_LC_SIGNED32_D                          s32
#define utltype_PRFX_LC_SIGNED64_D                          s64
#define utltype_PRFX_LC_UNSIGNED8_D                         u8
#define utltype_PRFX_LC_UNSIGNED16_D                        u16
#define utltype_PRFX_LC_UNSIGNED32_D                        u32
#define utltype_PRFX_LC_UNSIGNED64_D                        u64
#define utltype_PRFX_LC_FLOAT32_D                           f32
#define utltype_PRFX_LC_FLOAT64_D                           f64
#define utltype_PRFX_LC_FLOAT96_D                           f96
#define utltype_PRFX_LC_FLOAT128_D                          f128
#define utltype_PRFX_LC_DOUBLE32_D                          d32
#define utltype_PRFX_LC_DOUBLE64_D                          d64
#define utltype_PRFX_LC_DOUBLE96_D                          d96
#define utltype_PRFX_LC_DOUBLE128_D                         d128
#define utltype_PRFX_LC_CHAR_D                              c
#define utltype_PRFX_LC_BOOL8_D                             b

#define utltype_PRFX_UC_SIGNED8_D                           S8
#define utltype_PRFX_UC_SIGNED16_D                          S16
#define utltype_PRFX_UC_SIGNED32_D                          S32
#define utltype_PRFX_UC_SIGNED64_D                          S64
#define utltype_PRFX_UC_UNSIGNED8_D                         U8
#define utltype_PRFX_UC_UNSIGNED16_D                        U16
#define utltype_PRFX_UC_UNSIGNED32_D                        U32
#define utltype_PRFX_UC_UNSIGNED64_D                        U64
#define utltype_PRFX_UC_FLOAT32_D                           F32
#define utltype_PRFX_UC_FLOAT64_D                           F64
#define utltype_PRFX_UC_FLOAT96_D                           F96
#define utltype_PRFX_UC_FLOAT128_D                          F128
#define utltype_PRFX_UC_DOUBLE32_D                          D32
#define utltype_PRFX_UC_DOUBLE64_D                          D64
#define utltype_PRFX_UC_DOUBLE96_D                          D96
#define utltype_PRFX_UC_DOUBLE128_D                         D128
#define utltype_PRFX_UC_CHAR_D                              C
#define utltype_PRFX_UC_BOOL8_D                             B

#define utltype_PRFX_LC(TYPE_NAME)                          utltype_PRFX_LC_ ## TYPE_NAME ## _D
#define utltype_PRFX_UC(TYPE_NAME)                          utltype_PRFX_UC_ ## TYPE_NAME ## _D
#define utltype_REF_MACRO_EXP_ARGS(REF_MACRO_NAME, ...)     REF_MACRO_NAME(__VA_ARGS__)

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

#define hstgr_DEFINE_FUNC_UPDATE_HISTOGRAM(STRG_CLS, BIN_TYPE, INPUT_T, BIN_SIZE_T, GET_BIN_IDX_FUNC)\
    utltype_REF_MACRO_EXP_ARGS(DIRECT_DEFINE_FUNC_UPDATE_HISTOGRAM, STRG_CLS, BIN_TYPE_CC(BIN_TYPE),\
        BIN_TYPE, INPUT_T, utltype_PRFX_LC(INPUT_T), utltype_PRFX_UC(INPUT_T), BIN_SIZE_T,\
        utltype_PRFX_LC(BIN_SIZE_T), utltype_PRFX_UC(BIN_SIZE_T), GET_BIN_IDX_FUNC)

#define hstgr_DEFINE_FUNC_GET_EVEN_BIN_IDX(STRG_CLS, INPUT_T, BIN_SIZE_T)\
    utltype_REF_MACRO_EXP_ARGS(DIRECT_DEFINE_FUNC_GET_EVEN_BIN_IDX, STRG_CLS,\
        INPUT_T, utltype_PRFX_LC(INPUT_T), utltype_PRFX_UC(INPUT_T),\
        BIN_SIZE_T, utltype_PRFX_LC(BIN_SIZE_T), utltype_PRFX_UC(BIN_SIZE_T))

#define hstgr_DEFINE_FUNC_GET_EVEN_BIN_ATTRIB(STRG_CLS, INPUT_T, BIN_SIZE_T)\
    utltype_REF_MACRO_EXP_ARGS(DIRECT_DEFINE_FUNC_GET_EVEN_BIN_ATTRIB, STRG_CLS,\
        INPUT_T, utltype_PRFX_LC(INPUT_T), utltype_PRFX_UC(INPUT_T),\
        BIN_SIZE_T, utltype_PRFX_LC(BIN_SIZE_T), utltype_PRFX_UC(BIN_SIZE_T))

#define hstgr_DEFINE_EVEN_HISTOGRAM(STRG_CLS, INPUT_T, BIN_SIZE_T)\
    hstgr_DEFINE_FUNC_UPDATE_HISTOGRAM(STRG_CLS, EVEN, INPUT_T, BIN_SIZE_T, utltype_REF_MACRO_EXP_ARGS(\
        BUILD_GET_BIN_IDX_FUNC_NAME, Even, utltype_PRFX_LC(INPUT_T), utltype_PRFX_LC(BIN_SIZE_T)))\
    hstgr_DEFINE_FUNC_GET_EVEN_BIN_IDX(STRG_CLS, INPUT_T, BIN_SIZE_T)\
    hstgr_DEFINE_FUNC_GET_EVEN_BIN_ATTRIB(STRG_CLS, INPUT_T, BIN_SIZE_T)

hstgr_DEFINE_EVEN_HISTOGRAM(, SIGNED32, UNSIGNED16)