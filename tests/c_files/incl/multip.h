#ifndef MULTIP_H
#define MULTIP_H

#include "types.h"
#include "utils.h"


#define DEFINE_FUNC_MULTIPLY(FUNC_STRG_CLS, TYPE)\
    utl_REF_MACRO_EXP_ARGS(DIRECT_DEFINE_FUNC_MULTIPLY, FUNC_STRG_CLS, TYPE, utl_LPRFX(TYPE),\
    utl_HIGHER_TYPE(TYPE), utl_REF_MACRO_EXP_ARGS(utl_LPRFX, utl_HIGHER_TYPE(TYPE)))

#define DIRECT_DEFINE_FUNC_MULTIPLY(FUNC_STRG_CLS, TYPE, A_B_PRFX, RET_TYPE, RET_PRFX)\
    FUNC_STRG_CLS RET_TYPE RET_PRFX ## Multiply_ ## A_B_PRFX(TYPE A_B_PRFX ## A, TYPE A_B_PRFX ## B)\
    {\
        RET_TYPE RET_PRFX ## RetVal;\
        \
        /* Perform multiplication. */\
        RET_PRFX ## RetVal = (RET_TYPE)A_B_PRFX ## A * (RET_TYPE)A_B_PRFX ## B;\
        \
        return RET_PRFX ## RetVal;\
    }

#endif /* #ifndef MULTIP_H */
