/***************************************************************************************************
 * ..
 *  Copyright (c) 2024 Danfoss
 *
 *  File name:     interpolation.h
 *  Module:        interpolation
 *  Author:        Martin Madliak
 *
 *  Description:
 * 
 * This component provides the interpolation functions listed below for any numerical data type
 * specified by the developer:
 *
 * * Linear interpolation between two points.
 * * Linear interpolation of a non-equidistant data set.
 * * Linear interpolation of a data set with equidistant coordinates.
 * 
 * The functions are provided in the form of function-definition macros with arguments specifying the
 * required data types. Referencing macros from this component in the target project enables the definition
 * of any function from the list above with custom data types needed in the project.
 ****************************************************************************************************/

#ifndef INTERPOLATION_H
#define INTERPOLATION_H

/*--------------------------------------------------------------------------------------------------
 * INCLUDED FILES
 *--------------------------------------------------------------------------------------------------*/
#include "base_data_types.h"
#include "util_type.h"

/*--------------------------------------------------------------------------------------------------
 * COMPILER DIRECTIVES
 *--------------------------------------------------------------------------------------------------*/
/*--------------------------------------------------------------------------------------------------
 * PUBLIC MACRO CONSTANTS AND FUNCTION-LIKE MACROS
 *--------------------------------------------------------------------------------------------------*/
/**
 * A macro to calculate an absolute delta value from two numbers and also to identify the sign of the experession.
 * 
 * Args:
 *     A: First input variable to calculate the absolute delta value.
 *     B: Second input variable to calculate the absolute delta value.
 *     ABS: Output variable holding absolute value calculated from A and B inpud variables.
 *     U8SIGN: Output variable to hold the sign of the expression A - B, e.g. value 1 representing
 *         the negative sign and value 0 representing the positive sign. The variable representing
 *         a U8SIGN parameter needs to be set to 0 before it will be used to identify the expression sign.
 * 
 * Returns:
 *     void
 */
#define intrpl_ABS_DELTA(A, B, ABS, U8SIGN)\
    if(((A) - (B)) < 0)\
    {\
        (U8SIGN) ^= 1u;\
        (ABS) = (B) - (A);\
    }\
    else\
    {\
        (ABS) = (A) - (B);\
    }

/**
 * A function-like macro to declare the function to perform a linear interpolation from two known points.
 * 
 * Args:
 *     STRG_CLS: Storage class specifier for the declared function. Typically ``extern`` or ``static``.
 *     DATA_T: Data type of input values to be processed by the function, e.g., ``SIGNED16``, ``FLOAT32``, etc.
 *         The output interpolated value of the declared function will have the same data type.
 * 
 * Returns:
 *     void
 * 
 * The example below illustrates the macro reference with the ``SIGNED16`` data types::
 * 
 *     intrpl_DECLARE_FUNC_INTERPOLATION_LINEAR(extern, SIGNED16)
 * 
 * The macro reference generates the following function declaration::
 * 
 *     extern SIGNED16 intrpl_s16InterpolationLinear( SIGNED16 s16X0, SIGNED16 s16Y0, SIGNED16 s16X1,
 *         SIGNED16 s16Y1, SIGNED16 s16Xi, BOOL8 bExtrapolate, BOOL8 bRound);
 * 
 * .. seealso::
 *     See the :c:macro:`intrpl_DEFINE_FUNC_INTERPOLATION_LINEAR` for the description of the defined function.
 */
#define intrpl_DECLARE_FUNC_INTERPOLATION_LINEAR(STRG_CLS, DATA_T)\
    utltype_REF_MACRO_EXP_ARGS(intrpl_DIRECT_DECLARE_FUNC_INTERPOLATION_LINEAR,\
        STRG_CLS, DATA_T, utltype_PRFX_LC(DATA_T))

/** An internal macro directly performing the function declaration using the specified data type and type prefix.
 *  This macro is referenced by the interface macro :c:macro:`intrpl_DECLARE_FUNC_INTERPOLATION_LINEAR`. */
#define intrpl_DIRECT_DECLARE_FUNC_INTERPOLATION_LINEAR(STRG_CLS, DATA_T, PREF_T)\
    STRG_CLS DATA_T intrpl_ ## PREF_T ## InterpolationLinear(\
        DATA_T PREF_T ## X0,\
        DATA_T PREF_T ## Y0,\
        DATA_T PREF_T ## X1,\
        DATA_T PREF_T ## Y1,\
        DATA_T PREF_T ## Xi,\
        BOOL8 bExtrapolate,\
        BOOL8 bRound);

/**
 * A function-like macro to define the function to perform a linear interpolation from two known points.
 * 
 * Args:
 *     STRG_CLS: Storage class specifier for the defined function. Typically left empty or ``static``.
 *     DATA_T: Data type of input values to be processed by the function, e.g., ``SIGNED16``, ``FLOAT32``, etc.
 *         The output interpolated value of the defined function will have the same data type.
 * 
 * Returns:
 *     void
 * 
 * The example below illustrates the macro reference with the ``SIGNED16`` data types::
 * 
 *     intrpl_DEFINE_FUNC_INTERPOLATION_LINEAR(, SIGNED16)
 * 
 * The sample macro reference generates the following function definition:
 * 
 * .. c:function::
 *     SIGNED16 intrpl_s16InterpolationLinear(SIGNED16 s16X0, SIGNED16 s16Y0, SIGNED16 s16X1, SIGNED16 s16Y1, \
 *         SIGNED16 s16Xi, BOOL8 bExtrapolate, BOOL8 bRound)
 * 
 *     A function returning the interpolated value representing the y-axis point from the known x-axis point
 *     given as an input.
 * 
 *     .. note::
 *         The function also supports extrapolation, i.e. finding the y-axis coordinate based on extending a known \
 *         sequence of the values. Extrapolation can be enabled by setting up the parameter ``bExtrapolate`` to \
 *         :c:macro:`bTRUE` value.
 * 
 *     :param SIGNED16 s16X0: X0 coordinate.
 *     :param SIGNED16 s16Y0: Y0 coordinate.
 *     :param SIGNED16 s16X1: X1 coordinate.
 *     :param SIGNED16 s16Y1: Y1 coordinate.
 *     :param SIGNED16 s16Xi: Input x-axis coordinate to find the y-axis coordinate pair with interpolation.
 *     :param BOOL8 bExtrapolate: Parameter to enable/disable extrapolation (bTRUE - enabled, otherwise disabled).
 *     :param BOOL8 bRound: Parameter to enable/disable rounding to the closest higher integer value
 *         (bTRUE - enabled, otherwise disabled). Rounding shall be disabled for floating point data types,
 *         e.g. ``FLOAT32`` or ``DOUBLE64``.
 *     :returns: (SIGNED16) Interpolated y-axis coordinate that corresponds to the x-axis coordinate given as an input.
 */
#define intrpl_DEFINE_FUNC_INTERPOLATION_LINEAR(STRG_CLS, DATA_T)\
    utltype_REF_MACRO_EXP_ARGS(intrpl_DIRECT_DEFINE_FUNC_INTERPOLATION_LINEAR,\
        STRG_CLS, DATA_T, utltype_MULTIPL_TYPE(DATA_T), utltype_PRFX_LC(DATA_T),\
        utltype_REF_MACRO_EXP_ARGS(utltype_PRFX_LC, utltype_MULTIPL_TYPE(DATA_T)))

/** An internal macro directly performing the function definition using the specified data type and type prefix.
 *  This macro is referenced by the interface macro :c:macro:`intrpl_DEFINE_FUNC_INTERPOLATION_LINEAR`. */
#define intrpl_DIRECT_DEFINE_FUNC_INTERPOLATION_LINEAR(STRG_CLS, DATA_T, DATA_MULT_T, PREF_T, PREF_MULT_T)\
    STRG_CLS DATA_T intrpl_ ## PREF_T ## InterpolationLinear(\
        DATA_T PREF_T ## X0,\
        DATA_T PREF_T ## Y0,\
        DATA_T PREF_T ## X1,\
        DATA_T PREF_T ## Y1,\
        DATA_T PREF_T ## Xi,\
        BOOL8 bExtrapolate,\
        BOOL8 bRound)\
    {\
        DATA_MULT_T PREF_MULT_T ## Yo = (DATA_MULT_T)0;\
        DATA_MULT_T PREF_MULT_T ## DeltaY1Y0;\
        DATA_MULT_T PREF_MULT_T ## DeltaXiX0;\
        DATA_MULT_T PREF_MULT_T ## DeltaX1X0;\
        UNSIGNED8 u8Sign = 0u;\
        \
        if( (bExtrapolate == bFALSE) &&\
            (((PREF_T ## X0 < PREF_T ## X1) && (PREF_T ## Xi <= PREF_T ## X0)) ||\
            ((PREF_T ## X0 > PREF_T ## X1) && (PREF_T ## Xi >= PREF_T ## X0))) )\
        {\
            PREF_MULT_T ## Yo = (DATA_MULT_T)PREF_T ## Y0;\
        }\
        else if( (bExtrapolate == bFALSE) &&\
            (((PREF_T ## X0 < PREF_T ## X1) && (PREF_T ## Xi >= PREF_T ## X1)) ||\
            ((PREF_T ## X0 > PREF_T ## X1) && (PREF_T ## Xi <= PREF_T ## X1))) )\
        {\
            PREF_MULT_T ## Yo = (DATA_MULT_T)PREF_T ## Y1;\
        }\
        else\
        {\
            /* Calculate absolute values from deltas and determine the final sign of the expression. */\
            intrpl_ABS_DELTA(PREF_T ## Y1, PREF_T ## Y0, PREF_MULT_T ## DeltaY1Y0, u8Sign);\
            intrpl_ABS_DELTA(PREF_T ## Xi, PREF_T ## X0, PREF_MULT_T ## DeltaXiX0, u8Sign);\
            intrpl_ABS_DELTA(PREF_T ## X1, PREF_T ## X0, PREF_MULT_T ## DeltaX1X0, u8Sign);\
            \
            if(PREF_MULT_T ## DeltaX1X0 != (DATA_MULT_T)0)\
            {\
                if(bRound == bTRUE)\
                {\
                    /* Calculate part of the interpolation expression with rounding to the closest value: */\
                    /* (((Y1 - Y0) * (Xi - X0)) + ((X1 - X0) / 2)) / (X1 - X0)). */\
                    PREF_MULT_T ## Yo = ((PREF_MULT_T ## DeltaY1Y0 * PREF_MULT_T ## DeltaXiX0) +\
                        (PREF_MULT_T ## DeltaX1X0 / (DATA_MULT_T)2)) /\
                            PREF_MULT_T ## DeltaX1X0;\
                }\
                else\
                {\
                    /* Calculate part of the interpolation expression: ((Y1 - Y0) * (Xi - X0)) / (X1 - X0). */\
                    PREF_MULT_T ## Yo = (PREF_MULT_T ## DeltaY1Y0 * PREF_MULT_T ## DeltaXiX0) /\
                        PREF_MULT_T ## DeltaX1X0;\
                }\
                \
                /* Calculate interpolated coordinate. */\
                PREF_MULT_T ## Yo = ((u8Sign & 0x01u) == 1u) ?\
                    ((DATA_MULT_T)PREF_T ## Y0 - PREF_MULT_T ## Yo) :\
                    ((DATA_MULT_T)PREF_T ## Y0 + PREF_MULT_T ## Yo);\
            }\
        }\
        \
        return (DATA_T)PREF_MULT_T ## Yo;\
    }

/**
 * A function-like macro to declare the function to perform a linear interpolation of a data set with non-equidistant
 * x-axis coordinates, i.e. the distances between x coordinates are variable.
 * 
 * Args:
 *     STRG_CLS: Storage class specifier for the declared function. Typically ``extern`` or ``static``.
 *     DATA_T: Data type of input values to be processed by the function, e.g., ``SIGNED16``, ``FLOAT32``, etc.
 *         The output interpolated value of the declared function will have the same data type.
 * 
 * Returns:
 *     void
 * 
 * The example below illustrates the macro reference with the ``SIGNED16`` data types::
 * 
 *     intrpl_DECLARE_FUNC_DATA_SET_INTERPOLATION_LINEAR(extern, SIGNED16)
 * 
 * The macro reference generates the following function declaration::
 * 
 *     extern SIGNED16 intrpl_s16DataSetInterpolationLinear( SIGNED16 s16PointsX[], SIGNED16 s16PointsY[],
 *         UNSIGNED16 u16PointsNum, SIGNED16 s16Xi, BOOL8 bExtrapolate, BOOL8 bRound);
 * 
 * .. seealso::
 *     See the :c:macro:`intrpl_DEFINE_FUNC_DATA_SET_INTERPOLATION_LINEAR` for the description of the defined function.
 */
#define intrpl_DECLARE_FUNC_DATA_SET_INTERPOLATION_LINEAR(STRG_CLS, DATA_T)\
    utltype_REF_MACRO_EXP_ARGS(intrpl_DIRECT_DECLARE_FUNC_DATA_SET_INTERPOLATION_LINEAR,\
        STRG_CLS, DATA_T, utltype_PRFX_LC(DATA_T))

/** An internal macro directly performing the function declaration using the specified data type and type prefix.
 *  This macro is referenced by the interface macro :c:macro:`intrpl_DECLARE_FUNC_DATA_SET_INTERPOLATION_LINEAR`. */
#define intrpl_DIRECT_DECLARE_FUNC_DATA_SET_INTERPOLATION_LINEAR(STRG_CLS, DATA_T, PREF_T)\
    STRG_CLS DATA_T intrpl_ ## PREF_T ## DataSetInterpolationLinear(\
        DATA_T a ## PREF_T ## PointsX[],\
        DATA_T a ## PREF_T ## PointsY[],\
        UNSIGNED16 u16PointsNum,\
        DATA_T PREF_T ## Xi,\
        BOOL8 bExtrapolate,\
        BOOL8 bRound);

/**
 * A function-like macro to define the function to perform a linear interpolation of a data set with non-equidistant
 * x-axis coordinates, i.e. the distances between x coordinates are variable.
 * 
 * Args:
 *     STRG_CLS: Storage class specifier for the defined function. Typically left empty or ``static``.
 *     DATA_T: Data type of input values to be processed by the function, e.g., ``SIGNED16``, ``FLOAT32``, etc.
 *         The output interpolated value of the defined function will have the same data type.
 *     LIN_INTRPL_2PNT_FUNC: Name of the function to be used for the calculating linear interpolation
 *         between two points. The interpolation function must be defined separately and it must have the following
 *         form with the ``DATA_T`` data type matching the data type specified for the function,
 *         where the interpolation function is used::
 * 
 *             <DATA_T> <IntrplFuncName>(...)
 * 
 *         .. note::
 *             The expected interpolation function format matches the interpolation function defined by the
 *             :c:macro:`intrpl_DEFINE_FUNC_INTERPOLATION_LINEAR` macro and it is highly recommended to use this macro
 *             to define the required interpolation function and provide the name of the defined function as a
 *             parameter to this macro.
 * 
 * Returns:
 *     void
 * 
 * The example below illustrates the macro reference with the ``SIGNED16`` data types::
 * 
 *     intrpl_DEFINE_FUNC_DATA_SET_INTERPOLATION_LINEAR(, SIGNED16, intrpl_s16InterpolationLinear)
 * 
 * The sample macro reference generates the following function definition:
 * 
 * .. c:function::
 *     SIGNED16 intrpl_s16DataSetInterpolationLinear(SIGNED16 s16PointsX[], SIGNED16 s16PointsY[], \
 *         UNSIGNED16 u16PointsNum, SIGNED16 s16Xi, BOOL8 bExtrapolate, BOOL8 bRound)
 * 
 *     A function returning the interpolated value representing the y-axis point from the known x-axis point given
 *     as an input.
 * 
 *     :param SIGNED16 s16PointsX[]: Array with x-axis coordinates.
 *     :param SIGNED16 s16PointsY[]: Array with y-axis coordinates.
 *     :param UNSIGNED16 u16PointsNum: Number of the elements in arrays.
 *     :param SIGNED16 s16Xi: Input x-axis coordinate to find the y-axis coordinate pair with interpolation.
 *     :param BOOL8 bExtrapolate: Parameter to enable/disable extrapolation (bTRUE - enabled, otherwise disabled).
 *     :param BOOL8 bRound: Parameter to enable/disable rounding to the closest higher integer value
 *         (bTRUE - enabled, otherwise disabled). Rounding shall be disabled for floating point data types,
 *         e.g. ``FLOAT32`` or ``DOUBLE64``.
 *     :returns: (SIGNED16) Interpolated y-axis coordinate that corresponds to the x-axis coordinate given as an input.
 */
#define intrpl_DEFINE_FUNC_DATA_SET_INTERPOLATION_LINEAR(STRG_CLS, DATA_T, LIN_INTRPL_2PNT_FUNC)\
    utltype_REF_MACRO_EXP_ARGS(intrpl_DIRECT_DEFINE_FUNC_DATA_SET_INTERPOLATION_LINEAR,\
        STRG_CLS, DATA_T, utltype_PRFX_LC(DATA_T), LIN_INTRPL_2PNT_FUNC)

/** An internal macro directly performing the function definition using the specified data type and type prefix.
 *  This macro is referenced by the interface macro :c:macro:`intrpl_DEFINE_FUNC_DATA_SET_INTERPOLATION_LINEAR`. */
#define intrpl_DIRECT_DEFINE_FUNC_DATA_SET_INTERPOLATION_LINEAR(STRG_CLS, DATA_T, PREF_T, LIN_INTRPL_2PNT_FUNC)\
    STRG_CLS DATA_T intrpl_ ## PREF_T ## DataSetInterpolationLinear(\
        DATA_T a ## PREF_T ## PointsX[],\
        DATA_T a ## PREF_T ## PointsY[],\
        UNSIGNED16 u16PointsNum,\
        DATA_T PREF_T ## Xi,\
        BOOL8 bExtrapolate,\
        BOOL8 bRound)\
    {\
        DATA_T PREF_T ## Yo = (DATA_T)0;\
        UNSIGNED16 u16High = u16PointsNum - 1u;\
        UNSIGNED16 u16Low = 0u;\
        UNSIGNED16 u16Mid;\
        BOOL8 bIsAsc;\
        \
        if( (a ## PREF_T ## PointsX != NULL) && (a ## PREF_T ## PointsY != NULL) && (u16PointsNum > 1u) )\
        {\
            bIsAsc = (a ## PREF_T ## PointsX[0u] <= a ## PREF_T ## PointsX[u16High]) ? bTRUE : bFALSE;\
            \
            /* Find the X0 coordinate for Xi using a binary search algorithm. */\
            while((u16High - u16Low) > 1u)\
            {\
                u16Mid = (u16High + u16Low) >> 1u;\
                \
                if( ((bIsAsc == bTRUE) && (a ## PREF_T ## PointsX[u16Mid] > PREF_T ## Xi)) ||\
                    ((bIsAsc == bFALSE) && (a ## PREF_T ## PointsX[u16Mid] < PREF_T ## Xi)) )\
                {\
                    u16High = u16Mid;\
                }\
                else\
                {\
                    u16Low = u16Mid;\
                }\
            }\
            \
            /* Perform linear interpolation. */\
            PREF_T ## Yo = LIN_INTRPL_2PNT_FUNC(\
                a ## PREF_T ## PointsX[u16Low],\
                a ## PREF_T ## PointsY[u16Low],\
                a ## PREF_T ## PointsX[u16Low + 1u],\
                a ## PREF_T ## PointsY[u16Low + 1u],\
                PREF_T ## Xi,\
                bExtrapolate,\
                bRound);\
        }\
        \
        return PREF_T ## Yo;\
    }

/**
 * A function-like macro to declare the function to perform linear interpolation of a data set with equidistant
 * x-axis coordinates, i.e. the x coordinates are equally spaced from each other.
 * 
 * Args:
 *     STRG_CLS: Storage class specifier for the declared function. Typically ``extern`` or ``static``.
 *     DATA_T: Data type of input values to be processed by the function, e.g., ``SIGNED16``, ``FLOAT32``, etc.
 *         The output interpolated value of the declared function will have the same data type.
 * 
 * Returns:
 *     void
 * 
 * The example below illustrates the macro reference with the ``SIGNED16`` data types::
 * 
 *     intrpl_DECLARE_FUNC_DATA_SET_EQDIST_INTERPOLATION_LINEAR(extern, SIGNED16)
 * 
 * The macro reference generates the following function declaration::
 * 
 *     extern SIGNED16 intrpl_s16DataSetEqdistInterpolationLinear(SIGNED16 s16X0, SIGNED16 s16X_AbsStep,
 *         BOOL8 bX_Ascending, SIGNED16 s16PointsY[], UNSIGNED16 u16PointsNum, SIGNED16 s16Xi, BOOL8 bExtrapolate,
 *         BOOL8 bRound);
 * 
 * .. seealso::
 *     See the :c:macro:`intrpl_DEFINE_FUNC_DATA_SET_EQDIST_INTERPOLATION_LINEAR` for the description of the defined
 *     function.
 */
#define intrpl_DECLARE_FUNC_DATA_SET_EQDIST_INTERPOLATION_LINEAR(STRG_CLS, DATA_T)\
    utltype_REF_MACRO_EXP_ARGS(intrpl_DIRECT_DECLARE_FUNC_DATA_SET_EQDIST_INTERPOLATION_LINEAR,\
        STRG_CLS, DATA_T, utltype_PRFX_LC(DATA_T))

/** An internal macro directly performing the function declaration using the specified data type and type prefix.
 *  This macro is referenced by the interface macro
 *  :c:macro:`intrpl_DECLARE_FUNC_DATA_SET_EQDIST_INTERPOLATION_LINEAR`. */
#define intrpl_DIRECT_DECLARE_FUNC_DATA_SET_EQDIST_INTERPOLATION_LINEAR(STRG_CLS, DATA_T, PREF_T)\
    STRG_CLS DATA_T intrpl_ ## PREF_T ## DataSetEqdistInterpolationLinear(\
        DATA_T PREF_T ## X0,\
        DATA_T PREF_T ## X_AbsStep,\
        BOOL8 bX_Ascending,\
        DATA_T a ## PREF_T ## PointsY[],\
        UNSIGNED16 u16PointsNum,\
        DATA_T PREF_T ## Xi,\
        BOOL8 bExtrapolate,\
        BOOL8 bRound);

/**
 * A function-like macro to define the function to perform linear interpolation of a data set with equidistant
 * x-axis coordinates, i.e. the x coordinates are equally spaced from each other.
 * 
 * Args:
 *     STRG_CLS: Storage class specifier for the defined function. Typically left empty or ``static``.
 *     DATA_T: Data type of input values to be processed by the function, e.g., ``SIGNED16``, ``FLOAT32``, etc.
 *         The output interpolated value of the defined function will have the same data type.
 *     LIN_INTRPL_2PNT_FUNC: Name of the function to be used for the calculating linear interpolation
 *         between two points. The interpolation function must be defined separately and it must have the following
 *         form with the ``DATA_T`` data type matching the data type specified for the function,
 *         where the interpolation function is used::
 * 
 *             <DATA_T> <IntrplFuncName>(...)
 * 
 *         .. note::
 *             The expected interpolation function format matches the interpolation function defined by the
 *             :c:macro:`intrpl_DEFINE_FUNC_INTERPOLATION_LINEAR` macro and it is highly recommended to use this macro
 *             to define the required interpolation function and provide the name of the defined function as a
 *             parameter to this macro.
 * 
 * Returns:
 *     void
 * 
 * The example below illustrates the macro reference with the ``SIGNED16`` data types::
 * 
 *     intrpl_DEFINE_FUNC_DATA_SET_EQDIST_INTERPOLATION_LINEAR(, SIGNED16, intrpl_s16InterpolationLinear)
 * 
 * The sample macro reference generates the following function definition:
 * 
 * .. c:function::
 *     SIGNED16 intrpl_s16DataSetEqdistInterpolationLinear( SIGNED16 s16X0, SIGNED16 s16X_AbsStep, \
 *         BOOL8 bX_Ascending, SIGNED16 s16PointsY[], UNSIGNED16 u16PointsNum, SIGNED16 s16Xi, BOOL8 bExtrapolate, \
 *         BOOL8 bRound)
 * 
 *     A function returning the interpolated value representing the y-axis point from the known x-axis point given
 *     as an input.
 * 
 *     :param SIGNED16 s16X0: X0 coordinate.
 *     :param SIGNED16 s16X_AbsStep: Step between two points.
 *     :param BOOL8 bX_Ascending: Ascending flag (bTRUE - ascending, bFALSE - descending).
 *     :param SIGNED16 s16PointsY[]: Array with y-axis coordinates.
 *     :param UNSIGNED16 u16PointsNum: Number of the elements in arrays.
 *     :param SIGNED16 s16Xi: Input x-axis coordinate to find the y-axis coordinate pair with interpolation.
 *     :param BOOL8 bExtrapolate: Parameter to enable/disable extrapolation (bTRUE - enabled, otherwise disabled).
 *     :param BOOL8 bRound: Parameter to enable/disable rounding to the closest higher integer value
 *         (bTRUE - enabled, otherwise disabled). Rounding shall be disabled for floating point data types,
 *         e.g. ``FLOAT32`` or ``DOUBLE64``.
 *     :returns: (SIGNED16) Interpolated y-axis coordinate that corresponds to the x-axis coordinate given as an input.
 */
#define intrpl_DEFINE_FUNC_DATA_SET_EQDIST_INTERPOLATION_LINEAR(STRG_CLS, DATA_T, LIN_INTRPL_2PNT_FUNC)\
    utltype_REF_MACRO_EXP_ARGS(intrpl_DIRECT_DEFINE_FUNC_DATA_SET_EQDIST_INTERPOLATION_LINEAR,\
        STRG_CLS, DATA_T, utltype_PRFX_LC(DATA_T), LIN_INTRPL_2PNT_FUNC)

/** An internal macro directly performing the function definition using the specified data type and type prefix.
 *  This macro is referenced by the interface macro
 *  :c:macro:`intrpl_DEFINE_FUNC_DATA_SET_EQDIST_INTERPOLATION_LINEAR`. */
#define intrpl_DIRECT_DEFINE_FUNC_DATA_SET_EQDIST_INTERPOLATION_LINEAR(STRG_CLS, DATA_T, PREF_T, LIN_INTRPL_2PNT_FUNC)\
    STRG_CLS DATA_T intrpl_ ## PREF_T ## DataSetEqdistInterpolationLinear(\
        DATA_T PREF_T ## X0,\
        DATA_T PREF_T ## X_AbsStep,\
        BOOL8 bX_Ascending,\
        DATA_T a ## PREF_T ## PointsY[],\
        UNSIGNED16 u16PointsNum,\
        DATA_T PREF_T ## Xi,\
        BOOL8 bExtrapolate,\
        BOOL8 bRound)\
    {\
        DATA_T PREF_T ## Yo = (DATA_T)0;\
        DATA_T PREF_T ## Xj;\
        DATA_T PREF_T ## Xj_Next;\
        UNSIGNED16 u16Idx_Xj;\
        UNSIGNED16 u16DeltaXiX0;\
        UNSIGNED8 u8Sign = 0u;\
        \
        if( (a ## PREF_T ## PointsY != NULL) && (u16PointsNum > 1u) )\
        {\
            /* Calculate index of the Xj. */\
            if( ((bX_Ascending == bTRUE) && (PREF_T ## Xi > PREF_T ## X0)) ||\
                ((bX_Ascending == bFALSE) && (PREF_T ## Xi < PREF_T ## X0)) )\
            {\
                intrpl_ABS_DELTA(PREF_T ## Xi, PREF_T ## X0, u16DeltaXiX0, u8Sign);\
                u16Idx_Xj = u16DeltaXiX0 / (UNSIGNED16)PREF_T ## X_AbsStep;\
                \
                if(u16Idx_Xj >= (u16PointsNum - 1u))\
                {\
                    u16Idx_Xj = u16PointsNum - 2u;\
                }\
            }\
            else\
            {\
                u16Idx_Xj = 0u;\
            }\
            \
            /* Calculate Xj and Xj + 1 depending on coordinate characteristic. */\
            if(bX_Ascending == bTRUE)\
            {\
                PREF_T ## Xj = PREF_T ## X0 + ((DATA_T)u16Idx_Xj * PREF_T ## X_AbsStep);\
                PREF_T ## Xj_Next = PREF_T ## Xj + PREF_T ## X_AbsStep;\
            }\
            else\
            {\
                PREF_T ## Xj = PREF_T ## X0 - ((DATA_T)u16Idx_Xj * PREF_T ## X_AbsStep);\
                PREF_T ## Xj_Next = PREF_T ## Xj - PREF_T ## X_AbsStep;\
            }\
            \
            /* Perform linear interpolation in [Xj; Xj + 1] range. */\
            PREF_T ## Yo = LIN_INTRPL_2PNT_FUNC(\
                PREF_T ## Xj,\
                a ## PREF_T ## PointsY[u16Idx_Xj],\
                PREF_T ## Xj_Next,\
                a ## PREF_T ## PointsY[u16Idx_Xj + 1u],\
                PREF_T ## Xi,\
                bExtrapolate,\
                bRound);\
        }\
        \
        return PREF_T ## Yo;\
    }

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


#endif /* #ifndef INTERPOLATION_H */
