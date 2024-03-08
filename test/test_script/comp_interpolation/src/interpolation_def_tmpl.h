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
 *
 * .. important::
 *     This file is only a template. The actual definition file shall be created by creating
 *     a copy of this template file, removing the *_tmpl* suffix from the file name and removing
 *     this "important" comment. Then the required interpolation function declaration macros shall
 *     be added instead of the provided examples within the ``EXAMPLES`` compilation condition.
 *
 *     This file can be stored in any suitable location within the target project. However, it is
 *     recommended to store it in the same location as the main *interpolation.h* component file
 *     to make the relation with the main component file obvious and easier to understand.
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
#ifdef EXAMPLES
/* Generate the function declaration of the linear interpolation. */
/* Declare function:
extern SIGNED16 intrpl_s16InterpolationLinear(
    SIGNED16 s16X0,
    SIGNED16 s16Y0,
    SIGNED16 s16X1,
    SIGNED16 s16Y1,
    SIGNED16 s16Xi,
    BOOL8 bExtrapolate,
    BOOL8 bRound);
*/
intrpl_DECLARE_FUNC_INTERPOLATION_LINEAR(extern, SIGNED16);

/* Generate the function declaration of the linear interpolation of a non-equidistant data set. */
/* Declare function:
extern SIGNED16 intrpl_s16DataSetInterpolationLinear(
    SIGNED16 as16PointsX[],
    SIGNED16 as16PointsY[],
    UNSIGNED16 u16PointsNum,
    SIGNED16 s16Xi,
    BOOL8 bExtrapolate,
    BOOL8 bRound);
*/
intrpl_DECLARE_FUNC_DATA_SET_INTERPOLATION_LINEAR(extern, SIGNED16);

/* Generate the function declaration of the linear interpolation of a data set with equidistant coordinates. */
/* Declare function:
extern SIGNED16 intrpl_s16DataSetEqdistInterpolationLinear(
    SIGNED16 s16X0,
    SIGNED16 s16X_AbsStep,
    BOOL8 bX_Ascending,
    SIGNED16 as16PointsY[],
    UNSIGNED16 u16PointsNum,
    SIGNED16 s16Xi,
    BOOL8 bExtrapolate,
    BOOL8 bRound);
*/
intrpl_DECLARE_FUNC_DATA_SET_EQDIST_INTERPOLATION_LINEAR(extern, SIGNED16);
#endif /* #ifdef EXAMPLES */

/*--------------------------------------------------------------------------------------------------
 * PUBLIC CONSTANT DECLARATIONS
 *--------------------------------------------------------------------------------------------------*/
/*--------------------------------------------------------------------------------------------------
 * PUBLIC VARIABLE DECLARATIONS
 *--------------------------------------------------------------------------------------------------*/


#endif /* #ifndef INTERPOLATION_DEF_H */
