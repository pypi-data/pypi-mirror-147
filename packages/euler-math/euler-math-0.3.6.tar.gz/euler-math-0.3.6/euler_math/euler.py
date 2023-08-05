import numpy as np
import operator
from functools import reduce
from sys import setrecursionlimit
setrecursionlimit(4000)

# utility methods ------------------------------------


def memoize(f):

    class memodict(dict):
        __slots__ = ()

        def __missing__(self, key):
            self[key] = ret = f(key)
            return ret

    return memodict().__getitem__


def timer(f):
    from timeit import default_timer
    start = default_timer()
    result = f()
    end = default_timer()
    print('result:', result, '(%.2fs)' % (end - start))


def readlines(file):
    return open(file).read().splitlines()


def pack(function):
    return lambda p: function(*p)


fst = operator.itemgetter(0)
snd = operator.itemgetter(1)

# number theory methods ---------------------------------------

HAS_GMPY = False

try:
    import gmpy2
    HAS_GMPY = True
except ImportError as e:
    pass 

def mr(n, bases):   
    """Perform a Miller-Rabin strong pseudoprime test on n using a
    given list of bases/witnesses."""
    s = ((n - 1) & (1 - n)).bit_length() - 1
    d = n >> s
    for a in bases:
        if HAS_GMPY:
            p = gmpy2.powmod(a, d, n)
        else:
            p = pow(a, d, n)
        if p == 1 or p == n - 1 or a % n == 0:
            continue
        for _ in range(s):
            p = (p * p) % n
            if p == n - 1:
                break
        else:
            return False
    return True


def PrimeQ(n):
    """yields true if a prime number and yields false otherwise"""
    if n in [2, 3, 5]:
        return True
    if n < 2 or (n % 2) == 0 or (n % 3) == 0 or (n % 5) == 0:
        return False
    if n < 49:
        return True
    if (n %  7) == 0 or (n % 11) == 0 or (n % 13) == 0 or (n % 17) == 0 or \
       (n % 19) == 0 or (n % 23) == 0 or (n % 29) == 0 or (n % 31) == 0 or \
       (n % 37) == 0 or (n % 41) == 0 or (n % 43) == 0 or (n % 47) == 0:
        return False
    if n < 2809:
        return True
    if n <= 23001:
        if HAS_GMPY:
            return gmpy2.powmod(2, n, n) == 2 and n not in [7957, 8321, 13747, 18721, 19951]
        else:        
            return pow(2, n, n) == 2 and n not in [7957, 8321, 13747, 18721, 19951]
    
    # https://miller-rabin.appspot.com/
    
    if n < 341531:
        return mr(n, [9345883071009581737])
    if n < 885594169:
        return mr(n, [725270293939359937, 3569819667048198375])
    if n < 350269456337:
       return mr(n, [4230279247111683200, 14694767155120705706, 16641139526367750375])
    if n < 55245642489451:
       return mr(n, [2, 141889084524735, 1199124725622454117, 11096072698276303650])
    if n < 7999252175582851:
       return mr(n, [2, 4130806001517, 149795463772692060, 186635894390467037, 3967304179347715805])
    if n < 585226005592931977:
       return mr(n, [2, 123635709730000, 9233062284813009, 43835965440333360, 761179012939631437, 1263739024124850375])
    # valid for n < 2 ** 64
    return mr(n, [2, 325, 9375, 28178, 450775, 9780504, 1795265022])



# prime generator ---------------------------------------

# prime list cache
_primes = [2]


def _grow_primes():
    p0 = _primes[len(_primes) - 1] + 1
    b = np.ones(p0, dtype=bool)
    for di in _primes:
        i0 = p0 // di * di
        if i0 < p0:
            b[i0 + di - p0::di] = False
        else:
            b[i0 - p0::di] = False
    _primes.extend(np.where(b)[0] + p0)


def primes():
    i = 0
    while True:
        if i >= len(_primes):
            _grow_primes()
        yield _primes[i]
        i += 1


def prime(n):
    while n >= len(_primes):
        _grow_primes()
    return _primes[n]


def is_prime(n):
    if n < 2:
        return False
    ps = primes()
    p = next(ps)
    while p * p <= n:
        if n % p == 0:
            return False
        p = next(ps)
    return True


def PrimePi(n):
    """gives the number of primes less than or equal to n"""
    i = 0
    while prime(i) <= n:
        i += 1
    return i


def GCD(a, b):
    """https://reference.wolfram.com/language/ref/GCD.html"""
    while b:
        a, b = b, a % b
    return a


def LCM(a, b):
    """https://reference.wolfram.com/language/ref/LCM.html"""
    return a // GCD(a, b) * b


def FactorInteger(n):
    """https://reference.wolfram.com/language/ref/FactorInteger.html"""
    from itertools import groupby
    factors = []
    ps = primes()
    m = n
    p = next(ps)
    while p * p <= m:
        if m % p == 0:
            m //= p
            factors.append(p)
        else:
            p = next(ps)
    factors.append(m)
    return list((item, len(list(group)))
                for item, group in groupby(sorted(factors)))


def DivisorSigma(n):
    """https://reference.wolfram.com/language/ref/DivisorSigma.html"""
    import operator
    return reduce(operator.mul, [(x[1] + 1) for x in FactorInteger(n)], 1)