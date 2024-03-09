/***************************************************************************************************
 * ..
 *  Copyright (c) 2024 Danfoss
 *
 *  File name:     interpolation_def.c
 *  Module:        interpolation - definitions
 *  Author:        Martin Madliak
 *
 *  Description:
 *
 * A source file containing user-defined definitions of interpolation functions in the form of definition
 * macros provided by the interpolation component. The declarations enable the specification of the specific
 * data types needed for a target project where the defined functions are used.
 *
 * The definitions in this file shall correspond to the declarations located in the
 * *interpolation_def.h* header file.
 *
 * .. note::
 *     It is not necessary to define the required functions in this file from the functional point
 *     of view. Using this file is only recommended to facilitate sharing of the defined functions in
 *     multiple target project source files and to ensure clarity brought by the definition of all functions
 *     from the interpolation component in one place.
 ****************************************************************************************************/

/*--------------------------------------------------------------------------------------------------
 * INCLUDED FILES
 *--------------------------------------------------------------------------------------------------*/
#include "interpolation_def.h"

/*--------------------------------------------------------------------------------------------------
 * COMPILER DIRECTIVES
 *--------------------------------------------------------------------------------------------------*/
/*--------------------------------------------------------------------------------------------------
 * PRIVATE MACRO CONSTANTS AND FUNCTION-LIKE MACROS
 *--------------------------------------------------------------------------------------------------*/
/*--------------------------------------------------------------------------------------------------
 * PRIVATE TYPE DEFINITIONS
 *--------------------------------------------------------------------------------------------------*/
/*--------------------------------------------------------------------------------------------------
 * PUBLIC CONSTANT DEFINITIONS
 *--------------------------------------------------------------------------------------------------*/
/*--------------------------------------------------------------------------------------------------
 * PUBLIC VARIABLE DEFINITIONS
 *--------------------------------------------------------------------------------------------------*/
/*--------------------------------------------------------------------------------------------------
 * PRIVATE FUNCTION DECLARATIONS
 *--------------------------------------------------------------------------------------------------*/
/*--------------------------------------------------------------------------------------------------
 * PRIVATE CONSTANT DEFINITIONS
 *--------------------------------------------------------------------------------------------------*/
/*--------------------------------------------------------------------------------------------------
 * PRIVATE VARIABLE DEFINITIONS
 *--------------------------------------------------------------------------------------------------*/
/*--------------------------------------------------------------------------------------------------
 * PUBLIC FUNCTION DEFINITIONS
 *--------------------------------------------------------------------------------------------------*/
SIGNED16 intrpl_s16InterpolationLinear(
    SIGNED16 s16X0,
    SIGNED16 s16Y0,
    SIGNED16 s16X1,
    SIGNED16 s16Y1,
    SIGNED16 s16Xi,
    BOOL8 bExtrapolate,
    BOOL8 bRound)
{
    SIGNED32 s32Yo = (SIGNED32)0;
    SIGNED32 s32DeltaY1Y0;
    SIGNED32 s32DeltaXiX0;
    SIGNED32 s32DeltaX1X0;
    UNSIGNED8 u8Sign = 0u;

    if( (bExtrapolate == 0x00u) &&
        (((s16X0 < s16X1) && (s16Xi <= s16X0)) ||
        ((s16X0 > s16X1) && (s16Xi >= s16X0))) )
    {
        s32Yo = (SIGNED32)s16Y0;
    }
    else if( (bExtrapolate == 0x00u) &&
        (((s16X0 < s16X1) && (s16Xi >= s16X1)) ||
        ((s16X0 > s16X1) && (s16Xi <= s16X1))) )
    {
        s32Yo = (SIGNED32)s16Y1;
    }
    else
    {
        /* Calculate absolute values from deltas and determine the final sign of the expression. */
        if(((s16Y1) - (s16Y0)) < 0)
        {
            (u8Sign) ^= 1u;
            (s32DeltaY1Y0) = (s16Y0) - (s16Y1);
        }
        else
        {
            (s32DeltaY1Y0) = (s16Y1) - (s16Y0);
        };
        if(((s16Xi) - (s16X0)) < 0)
        {
            (u8Sign) ^= 1u;
            (s32DeltaXiX0) = (s16X0) - (s16Xi);
        }
        else
        {
            (s32DeltaXiX0) = (s16Xi) - (s16X0);
        };
        if(((s16X1) - (s16X0)) < 0)
        {
            (u8Sign) ^= 1u;
            (s32DeltaX1X0) = (s16X0) - (s16X1);
        }
        else
        {
            (s32DeltaX1X0) = (s16X1) - (s16X0);
        };

        if(s32DeltaX1X0 != (SIGNED32)0)
        {
            if(bRound == 0xFFu)
            {
                /* Calculate part of the interpolation expression with rounding to the closest value: */
                /* (((Y1 - Y0) * (Xi - X0)) + ((X1 - X0) / 2)) / (X1 - X0)). */
                s32Yo = ((s32DeltaY1Y0 * s32DeltaXiX0) +
                    (s32DeltaX1X0 / (SIGNED32)2)) /
                        s32DeltaX1X0;
            }
            else
            {
                /* Calculate part of the interpolation expression: ((Y1 - Y0) * (Xi - X0)) / (X1 - X0). */
                s32Yo = (s32DeltaY1Y0 * s32DeltaXiX0) /
                    s32DeltaX1X0;
            }

            /* Calculate interpolated coordinate. */
            s32Yo = ((u8Sign & 0x01u) == 1u) ?
                ((SIGNED32)s16Y0 - s32Yo) :
                ((SIGNED32)s16Y0 + s32Yo);
        }
    }

    return (SIGNED16)s32Yo;
}

SIGNED16 intrpl_s16DataSetInterpolationLinear(
    SIGNED16 as16PointsX[],
    SIGNED16 as16PointsY[],
    UNSIGNED16 u16PointsNum,
    SIGNED16 s16Xi,
    BOOL8 bExtrapolate,
    BOOL8 bRound)
{
    SIGNED16 s16Yo = (SIGNED16)0;
    UNSIGNED16 u16High = u16PointsNum - 1u;
    UNSIGNED16 u16Low = 0u;
    UNSIGNED16 u16Mid;
    BOOL8 bIsAsc;

    if( (as16PointsX != ((void *)0)) && (as16PointsY != ((void *)0)) && (u16PointsNum > 1u) )
    {
        bIsAsc = (as16PointsX[0u] <= as16PointsX[u16High]) ? 0xFFu : 0x00u;

        /* Find the X0 coordinate for Xi using a binary search algorithm. */
        while((u16High - u16Low) > 1u)
        {
            u16Mid = (u16High + u16Low) >> 1u;

            if( ((bIsAsc == 0xFFu) && (as16PointsX[u16Mid] > s16Xi)) ||
                ((bIsAsc == 0x00u) && (as16PointsX[u16Mid] < s16Xi)) )
            {
                u16High = u16Mid;
            }
            else
            {
                u16Low = u16Mid;
            }
        }

        /* Perform linear interpolation. */
        s16Yo = intrpl_s16InterpolationLinear(
            as16PointsX[u16Low],
            as16PointsY[u16Low],
            as16PointsX[u16Low + 1u],
            as16PointsY[u16Low + 1u],
            s16Xi,
            bExtrapolate,
            bRound);
    }

    return s16Yo;
};

/*--------------------------------------------------------------------------------------------------
 * PRIVATE FUNCTION DEFINITIONS
 *--------------------------------------------------------------------------------------------------*/
