
#define bla 0 /* This is a comment:
    #define NONEXISTENT_MACRO_A 5
    everything should be ignored. */

#if 0
#define MACRO_A 5
#endif

#if 0
#else 2
#endif


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