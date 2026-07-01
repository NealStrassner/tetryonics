"""
Number theory — Book 5 (Geometrics).

Tetryonics reads number theory off the equilateral grid: primes as differences of
consecutive squares (2n−1), twin primes at 6n±1, the digital-root cycle (base-9), and
the Fibonacci convergents to φ. These are exact integer constructions on the triangle.
"""

from __future__ import annotations

import math


def digital_root(n: int) -> int:
    """Digital root (repeated digit sum) = 1 + (n−1) mod 9 for n>0 (base-9 cycle)."""
    if n == 0:
        return 0
    return 1 + (abs(n) - 1) % 9


def is_prime(n: int) -> bool:
    """Primality test."""
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, math.isqrt(n) + 1, 2):
        if n % i == 0:
            return False
    return True


def primes_up_to(limit: int) -> list:
    """All primes ≤ limit (sieve)."""
    if limit < 2:
        return []
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, math.isqrt(limit) + 1):
        if sieve[i]:
            for j in range(i * i, limit + 1, i):
                sieve[j] = False
    return [i for i, p in enumerate(sieve) if p]


def is_twin_prime_form(n: int) -> bool:
    """Whether n has the 6k±1 form that all primes >3 take."""
    return n % 6 == 1 or n % 6 == 5


def mersenne(n: int) -> int:
    """The n-th Mersenne number  Mₙ = 2ⁿ − 1."""
    return 2 ** n - 1


def is_mersenne_prime(n: int) -> bool:
    """Whether 2ⁿ − 1 is prime (n itself must be prime)."""
    return is_prime(n) and is_prime(mersenne(n))


def goldbach_pair(even_n: int) -> tuple:
    """A pair of primes summing to an even number > 2 (Goldbach)."""
    if even_n <= 2 or even_n % 2:
        raise ValueError("need an even number > 2")
    for p in primes_up_to(even_n):
        if is_prime(even_n - p):
            return (p, even_n - p)
    return ()


def prime_as_square_difference(n: int) -> tuple:
    """Every odd number 2k−1 = k² − (k−1)²; returns (k, k−1) for odd n."""
    if n % 2 == 0:
        raise ValueError("only odd numbers are a difference of consecutive squares")
    k = (n + 1) // 2
    return (k, k - 1)


def fibonacci(n: int) -> int:
    """The n-th Fibonacci number (0-indexed: 0,1,1,2,3,5,…)."""
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def fibonacci_ratio(n: int) -> float:
    """F(n+1)/F(n) — converges to the golden ratio φ."""
    return fibonacci(n + 1) / fibonacci(n)


def is_perfect_number(n: int) -> bool:
    """Whether n equals the sum of its proper divisors (6, 28, 496, …)."""
    if n < 2:
        return False
    return sum(d for d in range(1, n) if n % d == 0) == n


def lucas(n: int) -> int:
    """The n-th Lucas number (2,1,3,4,7,11,…); ratio also converges to φ."""
    a, b = 2, 1
    for _ in range(n):
        a, b = b, a + b
    return a
