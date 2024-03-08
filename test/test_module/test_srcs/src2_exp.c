static UNSIGNED16 avrg_u16Average_u32Sum(const UNSIGNED16 au16Vals[],
    UNSIGNED16 u16ValsNum, BOOL8 bRound)
{
    UNSIGNED16 u16Idx;
    UNSIGNED32 u32Sum = (UNSIGNED32)0;
    UNSIGNED16 u16Avrg = (UNSIGNED16)0;

    if( (au16Vals != NULL) && (u16ValsNum > 0u) )
    {
        /* Calculate the sum of all input values. */
        for(u16Idx = 0u; u16Idx < u16ValsNum; u16Idx++)
        {
            u32Sum += (UNSIGNED32)au16Vals[u16Idx];
        }

        /* Calculate average. Use round up division if required: */
        /* quotient = (dividend + (divisor / 2)) / divisor */
        u16Avrg = (bRound == bTRUE) ?
            (UNSIGNED16)((u32Sum + ((UNSIGNED32)u16ValsNum / (UNSIGNED32)2)) / (UNSIGNED32)u16ValsNum) :
            (UNSIGNED16)(u32Sum / (UNSIGNED32)u16ValsNum);
    }

    return u16Avrg;
}
