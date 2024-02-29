#define xstr(s) str(s)
     #define str(s) # s
     #define foo 4

     str (foo)
     xstr (foo)

#define AFTERX(x) X_ ## x
#define XAFTERX(x) AFTERX(x)
#define TABLESIZE 1024
#define BUFSIZE TABLESIZE

AFTERX(BUFSIZE)
XAFTERX(BUFSIZE)