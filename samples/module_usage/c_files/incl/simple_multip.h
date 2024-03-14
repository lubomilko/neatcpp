#ifndef SIMPLE_MULTIP_H
#define SIMPLE_MULTIP_H


#define DEFINE_MULTIPLY(TYPE, RET_TYPE)\
    RET_TYPE Multiply(TYPE ValA, TYPE ValB)\
    {\
        RET_TYPE RetVal;\
        \
        /* Perform multiplication. */\
        RetVal = (RET_TYPE)ValA * (RET_TYPE)ValB;\
        \
        return RetVal;\
    }

#endif /* #ifndef SIMPLE_MULTIP_H */
