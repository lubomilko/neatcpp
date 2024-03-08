/***************************************************************************************************
 * ..
 *  Copyright (c) 2023 Danfoss
 *
 *  File name:     util_type.h
 *  Module:        type utilities (core)
 *  Author:        Lubomir Milko
 *
 *  Description:
 *
 * A data type utility component providing helper macros and other constructs usable for the
 * creation of a code supporting multiple data types.
 ****************************************************************************************************/

#ifndef UTIL_TYPE_H
#define UTIL_TYPE_H

/*--------------------------------------------------------------------------------------------------
 * INCLUDED FILES
 *--------------------------------------------------------------------------------------------------*/
/*--------------------------------------------------------------------------------------------------
 * COMPILER DIRECTIVES
 *--------------------------------------------------------------------------------------------------*/
/*--------------------------------------------------------------------------------------------------
 * PUBLIC MACRO CONSTANTS AND FUNCTION-LIKE MACROS
 *--------------------------------------------------------------------------------------------------*/
/* --- Macros defining lowercase prefixes indicating the base data type used to define an object. */
#define utltype_PRFX_LC_SIGNED8_D                           s8
#define utltype_PRFX_LC_SIGNED16_D                          s16
#define utltype_PRFX_LC_SIGNED32_D                          s32
#define utltype_PRFX_LC_SIGNED64_D                          s64
#define utltype_PRFX_LC_UNSIGNED8_D                         u8
#define utltype_PRFX_LC_UNSIGNED16_D                        u16
#define utltype_PRFX_LC_UNSIGNED32_D                        u32
#define utltype_PRFX_LC_UNSIGNED64_D                        u64
#define utltype_PRFX_LC_FLOAT32_D                           f32
#define utltype_PRFX_LC_FLOAT64_D                           f64
#define utltype_PRFX_LC_FLOAT96_D                           f96
#define utltype_PRFX_LC_FLOAT128_D                          f128
#define utltype_PRFX_LC_DOUBLE32_D                          d32
#define utltype_PRFX_LC_DOUBLE64_D                          d64
#define utltype_PRFX_LC_DOUBLE96_D                          d96
#define utltype_PRFX_LC_DOUBLE128_D                         d128
#define utltype_PRFX_LC_CHAR_D                              c
#define utltype_PRFX_LC_BOOL8_D                             b
/* --- */

/* --- Macros defining uppercase prefixes indicating the base data type used to define an object. */
#define utltype_PRFX_UC_SIGNED8_D                           S8
#define utltype_PRFX_UC_SIGNED16_D                          S16
#define utltype_PRFX_UC_SIGNED32_D                          S32
#define utltype_PRFX_UC_SIGNED64_D                          S64
#define utltype_PRFX_UC_UNSIGNED8_D                         U8
#define utltype_PRFX_UC_UNSIGNED16_D                        U16
#define utltype_PRFX_UC_UNSIGNED32_D                        U32
#define utltype_PRFX_UC_UNSIGNED64_D                        U64
#define utltype_PRFX_UC_FLOAT32_D                           F32
#define utltype_PRFX_UC_FLOAT64_D                           F64
#define utltype_PRFX_UC_FLOAT96_D                           F96
#define utltype_PRFX_UC_FLOAT128_D                          F128
#define utltype_PRFX_UC_DOUBLE32_D                          D32
#define utltype_PRFX_UC_DOUBLE64_D                          D64
#define utltype_PRFX_UC_DOUBLE96_D                          D96
#define utltype_PRFX_UC_DOUBLE128_D                         D128
#define utltype_PRFX_UC_CHAR_D                              C
#define utltype_PRFX_UC_BOOL8_D                             B
/* --- */

/**
 * Function-like macro returning a lowercase prefix for the specified base data type.
 * 
 * Example:
 * 
 * .. code-block:: c
 * 
 *     utltype_PRFX_LC(UNSIGNED16)
 * 
 * Expands to:
 * 
 * .. code-block:: c
 * 
 *     u16
 * 
 * Args:
 *     TYPE_NAME: Base data type name, e.g. ``UNSIGNED8``, ``SIGNED32``, etc.
 * 
 * Returns:
 *     Raw source code string (not ``char*`` data type) representing a lowercase prefix to be used
 *     in the names of objects defined using the specified base data type, e.g. ``u8``, ``s32``, etc.
 */
#define utltype_PRFX_LC(TYPE_NAME)                          utltype_PRFX_LC_ ## TYPE_NAME ## _D

/**
 * Function-like macro returning an uppercase prefix for the specified base data type.
 * 
 * Example:
 * 
 * .. code-block:: c
 * 
 *     utltype_PRFX_UC(UNSIGNED16)
 * 
 * Expands to:
 * 
 * .. code-block:: c
 * 
 *     U16
 * 
 * Args:
 *     TYPE_NAME: Base data type name, e.g. ``UNSIGNED8``, ``SIGNED32``, etc.
 * 
 * Returns:
 *     Raw source code string (not ``char*`` data type) representing an uppercase prefix to be used
 *     in the names of objects defined using the specified base data type, e.g. ``U8``, ``S32``, etc.
 */
#define utltype_PRFX_UC(TYPE_NAME)                          utltype_PRFX_UC_ ## TYPE_NAME ## _D

/**
 * Function-like macro usable for referencing another specified function-like macro that will be
 * supplied with the specified arguments that themselves are expanded before being used as arguments.
 * 
 * This macro is primarily meant to be used together with macros :c:macro:`utltype_PRFX_LC` and
 * :c:macro:`utltype_PRFX_UC` to generate data type prefixes corresponding to the provided base
 * data types.
 * 
 * An example below shows a function performing a square operation defined using a macro that
 * allows to specify the data type for the function input value and also for the result of the
 * square operation. The data type prefixes corresponding to the used data types are also a part
 * of the macro defining the function. The :c:macro:`utltype_REF_MACRO_EXP_ARGS` is used to
 * internally expand the required data type prefixes for the internal macro
 * ``EXPLICIT_DEFINE_FUNC_GET_SQR``.
 * 
 * The square function is defined using the following macros (notice the usage of
 * :c:macro:`utltype_REF_MACRO_EXP_ARGS` and :c:macro:`utltype_PRFX_LC`):
 * 
 * .. code-block:: c
 * 
 *     #define DEFINE_FUNC_GET_SQR(IN_TYPE, OUT_TYPE) \
 *         utltype_REF_MACRO_EXP_ARGS(EXPLICIT_DEFINE_FUNC_GET_SQR, \
 *             IN_TYPE, utltype_PRFX_LC(IN_TYPE), OUT_TYPE,  utltype_PRFX_LC(OUT_TYPE))
 * 
 *     #define EXPLICIT_DEFINE_FUNC_GET_SQR(IN_TYPE, IN_TYPE_PRFX, OUT_TYPE, OUT_TYPE_PRFX)\
 *         OUT_TYPE OUT_TYPE_PRFX ## GetSqr(IN_TYPE IN_TYPE_PRFX ## Input)\
 *         {\
 *             return (OUT_TYPE)IN_TYPE_PRFX ## Input * (OUT_TYPE)IN_TYPE_PRFX ## Input;\
 *         }
 * 
 * The square function using ``UNSIGNED16`` data type for the input and ``UNSIGNED32`` for the
 * output can then be defined by the following macro reference:
 * 
 *  .. code-block:: c
 * 
 *      DEFINE_FUNC_GET_SQR(UNSIGNED16, UNSIGNED32)
 * 
 * The macro reference above expands to the following function definition:
 * 
 * .. code-block:: c
 * 
 *     UNSIGNED32 u32GetSqr(UNSIGNED16 u16Input)
 *     {
 *         return (UNSIGNED32)u16Input * (UNSIGNED32)u16Input;
 *     }
 * 
 * Args:
 *     REF_MACRO_NAME: Name of the macro to be referenced with the provided arguments that are
 *         first expanded before being used in a macro reference.
 *     ...: Variable number of arguments used as arguments in a ``REF_MACRO_NAME`` macro reference.
 * 
 * Returns:
 *     No specific return. Return value depends on the macro referenced using the ``REF_MACRO_NAME``
 *     argument.
 */
#define utltype_REF_MACRO_EXP_ARGS(REF_MACRO_NAME, ...)     REF_MACRO_NAME(__VA_ARGS__)

/* --- Macros defining multiplication data types. */
#define utltype_MULTIPL_TYPE_SIGNED8_D                      SIGNED16
#define utltype_MULTIPL_TYPE_SIGNED16_D                     SIGNED32
#define utltype_MULTIPL_TYPE_SIGNED32_D                     SIGNED64
#define utltype_MULTIPL_TYPE_UNSIGNED8_D                    UNSIGNED16
#define utltype_MULTIPL_TYPE_UNSIGNED16_D                   UNSIGNED32
#define utltype_MULTIPL_TYPE_UNSIGNED32_D                   UNSIGNED64
#define utltype_MULTIPL_TYPE_FLOAT32_D                      FLOAT32
#define utltype_MULTIPL_TYPE_DOUBLE64_D                     DOUBLE64
/* --- */

/**
 * Function-like macro returning the data type recommended for storing the output of the multiplication operation
 * of two variables with the specified input data type.
 * 
 * Example:
 * 
 * .. code-block:: c
 * 
 *     utltype_MULTIPL_TYPE(UNSIGNED16)
 * 
 * Expands to:
 * 
 * .. code-block:: c
 * 
 *     UNSIGNED32
 * 
 * Args:
 *     TYPE_NAME: Base data type name, e.g. ``UNSIGNED8``, ``SIGNED32``, etc.
 * 
 * Returns:
 *     Recommended output data type of the multiplication using two variables with the specified input data type, e.g.
 *     the result of the multiplication of 2 ``SIGNED16`` variables needs ``SIGNED32`` variable to avoid overflow.
 */
#define utltype_MULTIPL_TYPE(TYPE_NAME)                     utltype_MULTIPL_TYPE_ ## TYPE_NAME ## _D

/*--------------------------------------------------------------------------------------------------
 * PUBLIC TYPE DEFINITIONS
 *--------------------------------------------------------------------------------------------------*/
/*--------------------------------------------------------------------------------------------------
 * PUBLIC FUNCTION DECLARATIONS
 *--------------------------------------------------------------------------------------------------*/
/*--------------------------------------------------------------------------------------------------
 * PUBLIC CONSTANT DECLARATIONS
 *--------------------------------------------------------------------------------------------------*/
/*--------------------------------------------------------------------------------------------------
 * PUBLIC VARIABLE DECLARATIONS
 *--------------------------------------------------------------------------------------------------*/


#endif /* #ifndef UTIL_TYPE_H */
