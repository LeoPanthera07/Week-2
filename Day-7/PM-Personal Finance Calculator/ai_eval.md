## Prompt
"Generate a Python type conversion matrix showing what happens when you convert between int, float, str, bool, list, and tuple — include edge cases and potential errors"

## Critical Evaluation

The AI-generated type conversion matrix was largely accurate for standard,
commonly used conversions such as int-to-float, float-to-int, bool-to-int,
and str-to-float. These are well-documented behaviors and the AI handled
them correctly, including noting that int(3.99) truncates rather than rounds.

However, the AI fell short on several important edge cases. It did not flag
that list(42) and tuple(42) raise a TypeError because integers are not
iterable — a critical distinction when teaching type conversion. Similarly,
int(float('inf')) raises an OverflowError that went unmentioned. The most
misleading omission was bool("False") returning True — since any non-empty
string is truthy in Python, this counterintuitive behavior trips up beginners
and deserved explicit highlighting.

Additionally, the AI did not mention that int(-3.99) truncates toward zero
giving -3, not -4, which differs from floor division behavior.

Overall, the AI is a useful starting reference but should never be trusted
without verification. Testing every conversion revealed gaps that could cause
real bugs in production code if accepted blindly.
