#define str(s) #s

/* outputs "p = "foo\n";" */
str(p = "foo\n";)
/* outputs "\n" */
str(\n)

#define HE HI
#define LLO _THERE
#define HELLO "HI THERE"
#define CAT(a,b) a      ##    b
#define XCAT(a,b) CAT(a,b)
#define CALL(fn) fn(HE,LLO)

CAT(HE, LLO) // outputs "HI THERE", because concatenation occurs before normal expansion
XCAT(HE, LLO) // outputs HI_THERE, because the tokens originating from parameters ("HE" and "LLO") are expanded first
CALL(CAT) // outputs "HI THERE", because this evaluates to CAT(a,b)
