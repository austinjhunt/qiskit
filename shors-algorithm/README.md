# Shor's Algorithm 

## Overview

In short, Shor's Algorithm  offers a method of efficiently factoring large psuedoprime integers into their prime factors using quantum computing. The implications of this algorithm are drastic considering the security of modern public key infrastructure (PKI) relies on the hardness of that factorization. PKI is used all over the place, whether in digital signatures for verifying the integrity of transmitted messages, in setting up websites with SSL certificates for encrypted connections, in authenticating members of a Windows domain network against Active Directory with Active Directory Certificate Services (AD CS), and a lot more. If the prime factorization on which PKI relies for security guarantees is cracked, there goes most of our online security - that's why Shor's Algorithm is worth studying. 

## Number Theory 
The approach taken to finding the prime factors of large integers in classical computing essentially just comes down to iteratively guessing factors and continuing as long as the guesses are wrong. 

With Shor's algorithm, we're also guessing, but the approach is a bit different. Given a similar large integer *N*, we first guess some random integer *g* that likely does not share any factors with *N*, and then we use quantum computing to essentially transform that bad guess *g* into a new integer that probably *does* share a factor with *N*. Note that this transformation of bad guesses into good guesses takes a very long time on a normal computer, but runs very quickly on quantum computers. 

With Shor's algorithm, we aren't interested necessarily in directly guessing the factors of the large number *N*. Thanks to Euclid's algorithm for finding common factors, we can guess integers that simply share factors with N. If we used Euclid's algorithm to find a common factor *f1* between a guessed integer *g* and the large number *N*, then it's game over (in a good way), since you can just divide N by that common factor *f1* to get the *other factor* *f2*; those two factors are all you need to break the encryption. However, it's *very* unlikely that your randomly guessed number *g* will actually share a factor with *N* considering the *N*s used for modern encryption are massive numbers.

This is where that bad-guess-to-good-guess transformation comes into play. The transformation is based on a simple fact in mathematics. For any two integers *a* and *b* that *do not share a factor* (e.g. our bad guess *g* and the large integer *N*), some power *p* of *a* will certainly produce some multiple *m* of *b* plus 1. 

$$a^p = m * b + 1$$


Shor's algorithm solves the problem of *period finding*.