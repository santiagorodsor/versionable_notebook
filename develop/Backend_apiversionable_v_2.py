
#Upper line left intentionally in blank, but this line sadly appears in versionable_file

import math
def add(a,b):
    return a + b

def power(x,y):
    return math.pow(x,y)

def sqrt_cool(x,precision=0.0001):
    guess = x/2.0 if x !=1 else 1.0
    make_guess = lambda guess_,x: .5*(guess_ + x/guess_)

    last = guess
    new_guess = make_guess(last,x)
    while (abs(new_guess-last) > precision):
        last = new_guess
        new_guess = make_guess(last,x)
    return new_guess