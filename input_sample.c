
#define bla 0 /* This is a comment:
    #define NONEXISTENT_MACRO_A 5
    everything should be ignored. */

#if 0
#define MACRO_A 5
#endif

#if 0
#else 2
#endif


/* Macro constant representing the value of pi using a 32 bit floating point data type. */
#define f32PI   3.1415926f



/**
 * Function-like macro to set one bit in an array to value 1.
 * 
 * Args:
 *     BitSize: Array data type bit length. Only exact values ``8``, ``16``, ``32`` or ``64`` are allowed.
 *     Array: ``UNSIGNED8/16/32/64`` array in which the bit should be set.
 *     BitIdx: Index of a bit to set (0 = LSB).
 */
#define bit_op_ARR_SET_BIT(BitSize, Array, BitIdx) \
    (Array[(BitIdx) / (BitSize)] |= \
    ((UNSIGNED ## BitSize)1u << \
    ((UNSIGNED ## BitSize)(BitIdx) % (UNSIGNED ## BitSize)(BitSize))))


#define xstr(s) str(s)
     #define str(s) # s
     #define foo 4

     str (foo)
     xstr (foo)


/* another comment
#define NONEXISTENT_MACRO_B 10
*/
#define MACRO_X     (a + b)

#define	MACRO_Y		(c + \
    d)\

#define MACRO_Z     \
	/* some formula */\
    (e + f) * \
    (g + h)

/* another comment
#define NONEXISTENT_MACRO_C 15 */

#if A == 1
    #define MACRO_A 1
    #if B = 1
        #define MACRO_B 2
    #endif
#else
    #define MACRO_A 0
#endif


#define MACRO_TEST_1( X , Y )   X + Y

MACRO_TEST_1( (C,D), E );

bla;