"""
Methods and Utilities for Project Euler Problems
"""

__all__ = [
    "memoize", "timer", "primes", "prime", "is_prime", "GCD", "LCM",
    "DivisorSigma", "FactorInteger", "PrimeQ", "PrimePi", "pack", "fst", "snd", 
    "Seq", "tco"
]

__version__ = '0.3.0'

from .euler import memoize, timer, primes, prime, is_prime, GCD, LCM, \
                   DivisorSigma, FactorInteger, pack, fst, snd, PrimeQ, PrimePi

from .tco import tco

from . import Seq
