#define REP0(X)
#define REP1(X) X
#define REP2(X) REP1(X) X
#define REP3(X) REP2(X) X
#define REP4(X) REP3(X) X
#define REP5(X) REP4(X) X
#define REP6(X) REP5(X) X
#define REP7(X) REP6(X) X
#define REP8(X) REP7(X) X
#define REP9(X) REP8(X) X
#define REP10(X) REP9(X) X

#define REP(TENS,ONES,X) \
  REP##TENS(REP10(X)) REP##ONES(X)
  
  
#define A   7u

#if A > 1u
    #if A > 100
        #define B(X)  X + A * 100u
    #elif A > 10
        #define B(X)  X + A * 10u
    #else
        #define B(X)  X + A
    #endif
#elif A == 0u
    #define B(X)  X
#else
    #define B(X)  X - A
#endif

B(5)    /* Expected: 5 + 7u */



/* Expected: 
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1*/
REP(1, 5, 1)


#define MACRO_A 7
#define MACRO_B 11

#ifdef MACRO_A
    #if (MACRO_A + 5) > 10 && defined MACRO_B
        #define MACRO_C  MACRO_A
    #elif defined MACRO_B
        #define MACRO_C  MACRO_B
    #else
        #define MACRO_C  0
    #endif
#elif defined(MACRO_B)
    #define MACRO_C  1
#endif

MACRO_C /* Expected: 7 */

#undef MACRO_A
#undef MACRO_B

#define MACRO_A 5
#define MACRO_B 11

#ifdef MACRO_A
    #if (MACRO_A + 5) > 10 && defined MACRO_B
        #define MACRO_C  MACRO_A
    #elif defined MACRO_B
        #define MACRO_C  MACRO_B
    #else
        #define MACRO_C  0
    #endif
#elif defined(MACRO_B)
    #define MACRO_C  1
#endif

MACRO_C /* Expected: 11 */

#undef MACRO_A
#undef MACRO_B

#define MACRO_A 5

#ifdef MACRO_A
    #if (MACRO_A + 5) > 10 && defined MACRO_B
        #define MACRO_C  MACRO_A
    #elif defined MACRO_B
        #define MACRO_C  MACRO_B
    #else
        #define MACRO_C  0
    #endif
#elif defined(MACRO_B)
    #define MACRO_C  1
#endif

MACRO_C /* Expected: 0 */


#undef MACRO_A

#define MACRO_B 11

#ifdef MACRO_A
    #if (MACRO_A + 5) > 10 && defined MACRO_B
        #define MACRO_C  MACRO_A
    #elif defined MACRO_B
        #define MACRO_C  MACRO_B
    #else
        #define MACRO_C  0
    #endif
#elif defined(MACRO_B)
    #define MACRO_C  1
#endif

MACRO_C /* Expected: 1 */