
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

#define HE HI
#define LLO _THERE
#define HELLO "HI THERE"
#define CAT(a,b) a##b
#define XCAT(a,b) CAT(a,b)
#define CALL(fn) fn(HE,LLO)

CAT(HE, LLO) // outputs "HI THERE", because concatenation occurs before normal expansion
XCAT(HE, LLO) // outputs HI_THERE, because the tokens originating from parameters ("HE" and "LLO") are expanded first
CALL(CAT) // outputs "HI THERE", because this evaluates to CAT(a,b)


#define str(s) #s

/* outputs
"p = "foo\n";" */
str(p = "foo\n";)
/* outputs
"\n" */
str(\n)


#define xstr(s) str(s)
    #define str(s) #s
    #define foo 4

// outputs "foo"
str (foo)
// outputs "4" 
xstr (foo)

#define AFTERX(x) X_ ## x
#define XAFTERX(x) AFTERX(x)
#define TABLESIZE 1024
#define BUFSIZE TABLESIZE

#define MULTILINE_SIMPLE_MACRO \
     a = 5 + 4;\
     b = 4 + 3;

#define MULTILINE_FUNC_MACRO(\
     a,b) \
     (a) = 5 + 4;\
     \
     (b) = 4 + 3;

#define VARIADIC_MACRO(A, \
     B, ...) A + B + func(__VA_ARGS__)

  MULTILINE_SIMPLE_MACRO
    MULTILINE_FUNC_MACRO(A, B)

AFTERX(BUFSIZE)     /* should be: X_BUFSIZE */    
XAFTERX(BUFSIZE)    /* should be: X_1024 */

/* expected:
1 + 2 + func(3, 4, 5) */
VARIADIC_MACRO(1, \
     2, 3, foo, 5)


/* Expected: 
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1*/
REP(1, 5, 1)


#define IGN_MACRO_OBJ    7 + 5
#define IGN_MACRO_FUNC(A, B)   A ## B !

IGN_MACRO_OBJ
IGN_MACRO_FUNC(bana, na)


#define A   101u

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

B(5)    /* Expected: 5 + 101u * 100u */

#undef A

#define A   12u

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

B(5)    /* Expected: 5 + 12u * 10u */

#undef A

#define A   3u

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

B(5)    /* Expected: 5 + 3u */

#undef A

#define A   0u

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

B(5)    /* Expected: 5 */

#undef A

#define A   -2

#if A > 1
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

B(5)    /* Expected: 5 - -2 */

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