/***************************************************************************************************
 * ..
 *  Copyright (c) 2023 Danfoss
 * 
 *  File name:     coretype.h
 *  Module:        Core data type
 *  Author:        Lubomir Milko
 * 
 *  Description:
 * 
 * A simple header file defining the most essential integer and floating-point data types primarily for
 * all common software components.
 * 
 * .. important::
 *     This file serves as an example of data type definitions required by common software components.
 *     It shall not be used in other projects as it is because the data type sizes are compiler-specific
 *     (e.g. it is not guaranteed that ``short`` will always have 16 bits, it is only the minimum size).
 * 
 *     Each project using common software components shall have its own coretype.h file similar to
 *     this file with appropriately defined integer and floating-point types specific for the
 *     compiler used. The application-specific coretype.h file shall define at least the data types defined
 *     within this file and it shall be included for the use by common software components. It is therefore
 *     possible to include the already existing coretype.h that typically exists in Danfoss valve
 *     applications or to create a new one by copying and modifying (if necessary for the compiler) this
 *     file.
 * 
 * .. note::
 *     The data types in this file are used for the compliance with the MISRA C:2012 directive
 *     *Dir 4.6 (Advisory) - typedefs that indicate size and signedness should be used in the
 *     place of the basic numerical types*.
 ****************************************************************************************************/

#ifndef CORETYPE_H
#define CORETYPE_H

/*--------------------------------------------------------------------------------------------------
 * INCLUDED FILES
 *--------------------------------------------------------------------------------------------------*/
#include <stdint.h>

/*--------------------------------------------------------------------------------------------------
 * COMPILER DIRECTIVES
 *--------------------------------------------------------------------------------------------------*/
/*--------------------------------------------------------------------------------------------------
 * PUBLIC MACRO CONSTANTS AND FUNCTION-LIKE MACROS
 *--------------------------------------------------------------------------------------------------*/
/*--------------------------------------------------------------------------------------------------
 * PUBLIC TYPE DEFINITIONS
 *--------------------------------------------------------------------------------------------------*/
/** 8-bit unsigned integer type. */
typedef uint8_t             UNSIGNED8;
/** 16-bit unsigned integer type. */
typedef uint16_t            UNSIGNED16;
/** 32-bit unsigned integer type. */
typedef uint32_t            UNSIGNED32;
/** 64-bit unsigned integer type. */
typedef uint64_t            UNSIGNED64;

/** 8-bit signed integer type. */
typedef int8_t              SIGNED8;
/** 16-bit signed integer type. */
typedef int16_t             SIGNED16;
/** 32-bit signed integer type. */
typedef int32_t             SIGNED32;
/** 64-bit signed integer type. */
typedef int64_t             SIGNED64;

/** Character type. */
typedef char                CHAR;
/** 32-bit single-precision floating-point type. */
typedef float               FLOAT32;
/** 64-bit double-precision floating-point type. */
typedef double              DOUBLE64;

/*--------------------------------------------------------------------------------------------------
 * PUBLIC FUNCTION DECLARATIONS
 *--------------------------------------------------------------------------------------------------*/
/*--------------------------------------------------------------------------------------------------
 * PUBLIC CONSTANT DECLARATIONS
 *--------------------------------------------------------------------------------------------------*/
/*--------------------------------------------------------------------------------------------------
 * PUBLIC VARIABLE DECLARATIONS
 *--------------------------------------------------------------------------------------------------*/


#endif /* #ifndef CORETYPE_H */
