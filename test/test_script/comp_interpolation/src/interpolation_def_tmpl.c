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
 *
 * .. important::
 *     This file is only a template. The actual definition file shall be created by creating
 *     a copy of this template file, removing the *_tmpl* suffix from the file name and removing
 *     this "important" comment. Then the required interpolation function definition macros shall
 *     be added instead of the provided examples within the ``EXAMPLES`` compilation condition.
 *
 *     This file can be stored in any suitable location within the target project. However, it is
 *     recommended to store it in the same location as the main *interpolation.h* component file
 *     to make the relation with the main component file obvious and easier to understand.
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
#ifdef EXAMPLES
/* Generate the function definition of the linear interpolation. */
/* Define function:
SIGNED16 intrpl_s16InterpolationLinear(
    SIGNED16 s16X0,
    SIGNED16 s16Y0,
    SIGNED16 s16X1,
    SIGNED16 s16Y1,
    SIGNED16 s16Xi,
    BOOL8 bExtrapolate,
    BOOL8 bRound){...}
*/
intrpl_DEFINE_FUNC_INTERPOLATION_LINEAR(, SIGNED16);

/* Generate the function definition of the linear interpolation of a non-equidistant data set. */
/* Define function:
SIGNED16 intrpl_s16DataSetInterpolationLinear(
    SIGNED16 as16PointsX[],
    SIGNED16 as16PointsY[],
    UNSIGNED16 u16PointsNum,
    SIGNED16 s16Xi,
    BOOL8 bExtrapolate,
    BOOL8 bRound){...}
*/
intrpl_DEFINE_FUNC_DATA_SET_INTERPOLATION_LINEAR(, SIGNED16, intrpl_s16InterpolationLinear);

/* Generate the function definition of the linear interpolation of a data set with equidistant coordinates. */
/* Define function:
SIGNED16 intrpl_s16DataSetEqdistInterpolationLinear(
    SIGNED16 s16X0,
    SIGNED16 s16X_AbsStep,
    BOOL8 bX_Ascending,
    SIGNED16 as16PointsY[],
    UNSIGNED16 u16PointsNum,
    SIGNED16 s16Xi,
    BOOL8 bExtrapolate,
    BOOL8 bRound){...}
*/
intrpl_DEFINE_FUNC_DATA_SET_EQDIST_INTERPOLATION_LINEAR(, SIGNED16, intrpl_s16InterpolationLinear);
#endif /* #ifdef EXAMPLES */

/*--------------------------------------------------------------------------------------------------
 * PRIVATE FUNCTION DEFINITIONS
 *--------------------------------------------------------------------------------------------------*/
