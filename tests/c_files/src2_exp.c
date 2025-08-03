#include "multip.h"

/* Define function multiplying two S16 values and returning the S32 result. */
S32 s32Multiply_s16(S16 s16A, S16 s16B)
{
    S32 s32RetVal;

    /* Perform multiplication. */
    s32RetVal = (S32)s16A * (S32)s16B;

    return s32RetVal;
}
