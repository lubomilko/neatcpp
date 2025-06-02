"HI THERE" // outputs "HI THERE", because concatenation occurs before normal expansion
HI_THERE // outputs HI_THERE, because the tokens originating from parameters ("HE" and "LLO") are expanded first
"HI THERE" // outputs "HI THERE", because this evaluates to CAT(a,b)

/* outputs
"p = "foo\n";" */
"p = "foo\n";"
/* outputs
"\n" */
"\n"

// outputs "foo"
"foo"
// outputs "4"
"4"

  a = 5 + 4;
  b = 4 + 3;
    (A) = 5 + 4;

    (B) = 4 + 3;

X_BUFSIZE     /* should be: X_BUFSIZE */
X_1024    /* should be: X_1024 */

/* expected:
1 + 2 + func(3, 4, 5) */
1 + 2 + func(3, 4, 5)


/* Expected:
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1*/
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1

IGN_MACRO_OBJ
IGN_MACRO_FUNC(bana, na)

5 + 101u * 100u    /* Expected: 5 + 101u * 100u */

5 + 12u * 10u    /* Expected: 5 + 12u * 10u */

5 + 3u    /* Expected: 5 + 3u */

5    /* Expected: 5 */

5 - -2    /* Expected: 5 - -2 */

7 /* Expected: 7 */

11 /* Expected: 11 */

0 /* Expected: 0 */

1 /* Expected: 1 */
