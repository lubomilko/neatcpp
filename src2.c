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

#define avrg_DEFINE_FUNC_AVERAGE(STRG_CLS, VAL_T, SUM_T) \
    utltype_REF_MACRO_EXP_ARGS(avrg_DIRECT_DEFINE_FUNC_AVERAGE, STRG_CLS, \
        VAL_T, utltype_PRFX_LC(VAL_T), SUM_T, utltype_PRFX_LC(SUM_T))

#define avrg_DIRECT_DEFINE_FUNC_AVERAGE(STRG_CLS, VAL_T, VAL_P, SUM_T, SUM_P) \
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