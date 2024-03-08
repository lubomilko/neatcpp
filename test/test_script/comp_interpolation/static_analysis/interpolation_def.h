/***************************************************************************************************
 * ..
 *  Copyright (c) 2024 Danfoss
 *
 *  File name:     interpolation_def.h
 *  Module:        interpolation - declarations
 *  Author:        Martin Madliak
 *
 *  Description:
 *
 * A header file containing user-defined declarations of interpolation functions in the form of declaration
 * macros provided by the interpolation component. The declarations enable the specification of the specific
 * data types needed for a target project where the defined functions are used.
 *
 * The declarations in this file shall correspond to the definitions located in the
 * *interpolation_def.c* source file.
 *
 * .. note::
 *     It is not necessary to declare the required functions in this file from functional point
 *     of view. Using this file is only recommended to facilitate sharing of the of easier sharing of the
 *     defined functions in multiple target project source files and and to ensure clarity brought
 *     by the definition of all functions from the interpolation component in one place.
 ****************************************************************************************************/

#ifndef INTERPOLATION_DEF_H
#define INTERPOLATION_DEF_H

/*--------------------------------------------------------------------------------------------------
 * INCLUDED FILES
 *--------------------------------------------------------------------------------------------------*/
#include "interpolation.h"

/*--------------------------------------------------------------------------------------------------
 * COMPILER DIRECTIVES
 *--------------------------------------------------------------------------------------------------*/
/*--------------------------------------------------------------------------------------------------
 * PUBLIC MACRO CONSTANTS AND FUNCTION-LIKE MACROS
 *--------------------------------------------------------------------------------------------------*/
/*--------------------------------------------------------------------------------------------------
 * PUBLIC TYPE DEFINITIONS
 *--------------------------------------------------------------------------------------------------*/
/*--------------------------------------------------------------------------------------------------
 * PUBLIC FUNCTION DECLARATIONS
 *--------------------------------------------------------------------------------------------------*/
extern SIGNED16 intrpl_s16InterpolationLinear(
    SIGNED16 s16X0,
    SIGNED16 s16Y0,
    SIGNED16 s16X1,
    SIGNED16 s16Y1,
    SIGNED16 s16Xi,
    BOOL8 bExtrapolate,
    BOOL8 bRound);

extern SIGNED16 intrpl_s16DataSetInterpolationLinear(
    SIGNED16 as16PointsX[],
    SIGNED16 as16PointsY[],
    UNSIGNED16 u16PointsNum,
    SIGNED16 s16Xi,
    BOOL8 bExtrapolate,
    BOOL8 bRound);

/*--------------------------------------------------------------------------------------------------
 * PUBLIC CONSTANT DECLARATIONS
 *--------------------------------------------------------------------------------------------------*/
/*--------------------------------------------------------------------------------------------------
 * PUBLIC VARIABLE DECLARATIONS
 *--------------------------------------------------------------------------------------------------*/


#endif /* #ifndef INTERPOLATION_DEF_H */
