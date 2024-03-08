#define MULTILINE_SIMPLE_MACRO \
     a = 5 + 4;\
     b = 4 + 3;
  MULTILINE_SIMPLE_MACRO   
  
#define VAR_MACRO(A, \
     B, ...) A + B + func(__VA_ARGS__)

#define xstr(s) str(s)
     #define str(s) # s
     #define foo 4

     /* should be: "foo" */
     str (foo)
     /* should be: "4" */
     xstr (foo)

#define AFTERX(x) X_ ## x
#define XAFTERX(x) AFTERX(x)
#define TABLESIZE 1024
#define BUFSIZE TABLESIZE

AFTERX(BUFSIZE)     /* should be: X_BUFSIZE */    
XAFTERX(BUFSIZE)    /* should be: X_1024 */

/* expected: 1 + 2 + func(3, 4, 5) */
VAR_MACRO(1, \
     2, 3, foo, 5)    


#define MULTILINE_FUNC_MACRO(\
     a,b) \
     (a) = 5 + 4;\
     \
     (b) = 4 + 3;

  MULTILINE_SIMPLE_MACRO
    MULTILINE_FUNC_MACRO(A, B)
