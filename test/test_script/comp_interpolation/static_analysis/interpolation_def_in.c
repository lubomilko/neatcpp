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
intrpl_DEFINE_FUNC_INTERPOLATION_LINEAR(, SIGNED16)

// intrpl_DEFINE_FUNC_DATA_SET_INTERPOLATION_LINEAR(, SIGNED16, intrpl_s16InterpolationLinear);

/*--------------------------------------------------------------------------------------------------
 * PRIVATE FUNCTION DEFINITIONS
 *--------------------------------------------------------------------------------------------------*/
