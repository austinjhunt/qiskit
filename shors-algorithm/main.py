import numpy as np  
from math import gcd
from numpy.random import randint
import pandas as pd
from fractions import Fraction
import os 
from util import qpe_amod15, assert_g_not_a_trivial_factor_of_N
base_dir = os.path.dirname(__file__)  

def run_shors(N): 
    """ Run shors algorithm to leverage quantum computing 
    to find prime factors of large number N """
    attempt = 0
    factor_found = False 
    # Re-attempt until factor successfully identified
    while not factor_found:
        attempt += 1
        print(f'Attempt: {attempt}')

        print(f'Guessing some random initial number g between 1 and N={N}')
        np.random.seed(1)
        g = randint(2, N)
        print(f'Initial guess is g = {g}')

        # Assert that the guess g is not some trivial factor of the large number N
        try: 
            assert_g_not_a_trivial_factor_of_N(g, N)
        except AssertionError:
            print(f'Initial guess g={g} is a trivial factor of N={N}. Re-attempting.')
            continue # retry 

        # find a guess for the period p such that g^p mod m*N = 1 
        print(f'Getting phase phi = s / p from initial guess g = {g} in order to find period p')
        phase = qpe_amod15(g) # returns a phase phi = s / p such that we can find p 
        if phase != 0:
            print(f'Phase = {phase}')
            print(f'Denominator should tell us the period p.')

            # The denominator should tell us the period (i.e. the frequency from 
            # the quantum fourier transform should tell us the period p of the superposition
            # obtained from measuring a result from the superposition of remainder values)
            # this is discussed in greater detail in the README for the shors-algorithm folder. 
            frac = Fraction(phase).limit_denominator(max_denominator=N) 
            s, p = frac.numerator, frac.denominator 
            print(f'The period p = {p}')
            print(f'g^p mod m * N = 1 => {g}^{p} mod m*{N} = 1')
            print('This implies: ')
            print(f'(g^p - 1) mod N = ({g}^{p} - 1) mod {N} = 0')
            
            if p % 2 == 0: 
                # if the period p is also even we can continue 
                print(f'p = {p} is even, continuing...')
                print(f'g^p - 1 = {g}^{p} - 1 = a * b = (g ^(p/2) - 1) * ((g ^ (p/2)) + 1) = ({g} ^({p}/2) - 1) * (({g} ^ ({p}/2)) + 1) ')
                print(f'There is a high probability that the GCD of N={N} and either a=(g ^(p/2) - 1) or b=((g ^ (p/2)) + 1) is a proper factor of N')

                print(f'Creating guesses...')
                guesses = [gcd(g**(p//2)-1, N), gcd(g**(p//2)+1, N)]
                print(f'Guesses: {guesses}')
                for guess in guesses:
                    if guess not in [1,N] and (N % guess) == 0: # Check to see if guess is a non-trivial factor of N
                        print("*** Non-trivial factor found: %i ***" % guess)
                        factor_found = True
                        print(f'Total attempts needed: {attempt}')
            else: 
                print(f'Period p = {p} is not even. Re-attempting factorization.')
        else: 
            print(f'phase returned from Quantum Phase Estimation is 0. Re-attempting factorization.')

# Run shor's algorithm on N = 15
run_shors(N=15)
 