/***************************************************************************************************
 * ..
 *  Copyright (c) 2023 Danfoss
 * 
 *  File name:     base_data_types.h
 *  Module:        Base data types
 *  Author:        Lubomir Milko
 * 
 *  Description:
 * 
 * A simple header file defining the null pointer value and boolean data type as well as true/false
 * boolean values primarily for all common software components.
 ****************************************************************************************************/

#ifndef BASE_DATA_TYPES_H
#define BASE_DATA_TYPES_H

/*--------------------------------------------------------------------------------------------------
 * INCLUDED FILES
 *--------------------------------------------------------------------------------------------------*/
#include "coretype.h"

/*--------------------------------------------------------------------------------------------------
 * COMPILER DIRECTIVES
 *--------------------------------------------------------------------------------------------------*/
/*--------------------------------------------------------------------------------------------------
 * PUBLIC MACRO CONSTANTS AND FUNCTION-LIKE MACROS
 *--------------------------------------------------------------------------------------------------*/
#ifndef NULL
    /** 
     * Macro representing the null pointer value.
     * 
     * .. note::
     *     The macro name intentionally deviates from the Danfoss naming convention requiring the
     *     use of the ``_D`` suffix to improve the readability and shorten the code lines since
     *     this macro is going to be commonly used in many source files and also for clarity, since
     *     ``NULL`` is a generally accepted constant name representing the null pointer.
     * 
     *     Furthermore, the ``NULL`` macro is used as a null pointer type definition instead of other
     *     definitions typically used in Danfoss valve applications because the application-specific
     *     definitions are not aligned across all applications, e.g. ``NULL_D`` or ``NULL_VPS``are used
     *     in different applications together with potentially other definitions coming from external
     *     software libraries (e.g., SYS TEC COP stack). The definition in this file allows the components
     *     to always use the same null pointer type definition without any potential ambiguity or issues
     *     relating to missing or duplicate definitions when relying on the definition provided by the
     *     application using the component.
     */
    #define NULL    ((void *)0)
#endif

#ifndef bTRUE
/** 
 * Macro defining the boolean value "true".
 * 
 * .. note::
 *     The macro name intentionally deviates from the Danfoss naming convention requiring the
 *     use of the ``_D`` suffix to improve the readability and shorten the code lines since
 *     this macro is going to be commonly used in many source files.
 *     However, the ``b`` prefix is applied to indicate the boolean data type and to make it different
 *     from other potential ``TRUE`` macros defined in external sw modules that might use a
 *     completely different macro value.
 * 
 *     The value 0xFF is chosen to be compatible with the ``BOOL`` enumerator data type
 *     commonly used in many Danfoss projects where the boolean value true is also defined
 *     with a numerical value 0xFF. Using the same value allows simple conversions between
 *     the two representations.
 */
#define bTRUE   0xFFu
#endif

#ifndef bFALSE
/** 
 * Macro defining the boolean value "false".
 * 
 * .. note::
 *     The macro name intentionally deviates from the Danfoss naming convention requiring the
 *     use of the ``_D`` suffix to improve the readability and shorten the code lines since
 *     this macro is going to be commonly used in many source files.
 *     However, the ``b`` prefix is applied to indicate the boolean data type and to make it different
 *     from other potential ``FALSE`` macros defined in external sw modules that might use a
 *     completely different macro value.
 */
#define bFALSE  0x00u
#endif

/*--------------------------------------------------------------------------------------------------
 * PUBLIC TYPE DEFINITIONS
 *--------------------------------------------------------------------------------------------------*/
/** 
 * The Boolean data type represented as a small unsigned integer number (usually 8-bit).
 * 
 * .. note::
 *     ``unsigned char`` is used as a base for the boolean type instead of an ``enum`` ``typedef``,
 *     which is typically used in Danfoss valve applications for its simplicity and guaranteed
 *     memory efficiency. According to the C standard, ``enum`` shall be capable of holding ``int``
 *     values, but an actual ``int`` size is compiler-specific and wasteful for boolean values.
 *     Certain compilers optimize the ``enum`` size according to the highest value used, but some
 *     compilers do not so the ``unsigned char`` was used instead to avoid potential ambiguity and
 *     to allow operations requiring an unsigned type (e.g., bit-wise operations or operations
 *     with other unsigned variables) without conversion to unsigned data type first (required
 *     by MISRA).
 * 
 *     The Boolean type and values are also defined separately for the component's purposes because
 *     the definition of boolean values is not aligned in all Danfoss valve applications, e.g. they
 *     use at least the following three different names: ``enFALSE`` / ``enTRUE``, ``eFALSE`` / ``eTRUE``,
 *     ``FALSE`` / ``TRUE``, where the last definitions can be in conflict (redefinition) with the
 *     boolean value definitions in external libraries in case they are using the same names for the
 *     boolean values (e.g. SYS TEC COP stack). The definitions in this file allow the components to
 *     always use the same boolean type definitions without any potential ambiguity or issues relating to missing
 *     or duplicate definitions when relying on the definitions provided by the application using the
 *     component.
 */
typedef unsigned char   BOOL8;

/*--------------------------------------------------------------------------------------------------
 * PUBLIC FUNCTION DECLARATIONS
 *--------------------------------------------------------------------------------------------------*/
/*--------------------------------------------------------------------------------------------------
 * PUBLIC CONSTANT DECLARATIONS
 *--------------------------------------------------------------------------------------------------*/
/*--------------------------------------------------------------------------------------------------
 * PUBLIC VARIABLE DECLARATIONS
 *--------------------------------------------------------------------------------------------------*/


#endif /* #ifndef BASE_DATA_TYPES_H */
