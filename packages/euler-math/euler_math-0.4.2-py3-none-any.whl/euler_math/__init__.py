"""
Methods and Utilities for Project Euler Problems
"""
import importlib.metadata


__all__ = [
    "memoize", "timer", "primes", "prime", "is_prime", "GCD", "LCM",
    "DivisorSigma", "FactorInteger", "PrimeQ", "PrimePi", "pack", "fst", "snd", 
    "Seq", "tco"
]


__version__ = importlib.metadata.version("euler_math")


from .euler import memoize, timer, primes, prime, is_prime, GCD, LCM, \
                   DivisorSigma, FactorInteger, PrimeQ, PrimePi


from .tco import tco


from .Seq import pack, fst, snd


from . import Seq

