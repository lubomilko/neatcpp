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