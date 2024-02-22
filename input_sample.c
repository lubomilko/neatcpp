
 /* This is a comment:
    #define BLA 1
    
    everything should be ignored. */

#define MACRO_X     (a + b)

#define	MACRO_Y		(c + \
    d)

#define MACRO_Z     \
    (e + f) * \
    (g + h)


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
