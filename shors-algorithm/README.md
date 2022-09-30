# Shor's Algorithm 

## Overview

In short, Shor's Algorithm  offers a method of efficiently factoring large psuedoprime integers into their prime factors using quantum computing. The implications of this algorithm are drastic considering the security of modern public key infrastructure (PKI) relies on the hardness of that factorization. PKI is used all over the place, whether in digital signatures for verifying the integrity of transmitted messages, in setting up websites with SSL certificates for encrypted connections, in authenticating members of a Windows domain network against Active Directory with Active Directory Certificate Services (AD CS), and a lot more. If the prime factorization on which PKI relies for security guarantees is cracked, there goes most of our online security - that's why Shor's Algorithm is worth studying. 

## Number Theory 
The approach taken to finding the prime factors of large integers in classical computing essentially just comes down to iteratively guessing factors and continuing as long as the guesses are wrong. 

With Shor's algorithm, we're also guessing, but the approach is a bit different. Given a similar large integer *N*, we first guess some random integer *g* that likely does not share any factors with *N*, and then we use quantum computing to essentially transform that bad guess *g* into a new integer that probably *does* share a factor with *N*. Note that this transformation of bad guesses into good guesses takes a very long time on a normal computer, but runs very quickly on quantum computers. 

With Shor's algorithm, we aren't interested necessarily in directly guessing the factors of the large number *N*. Thanks to Euclid's algorithm for finding common factors, we can guess integers that simply share factors with N. If we used Euclid's algorithm to find a common factor *f1* between a guessed integer *g* and the large number *N*, then it's game over (in a good way), since you can just divide N by that common factor *f1* to get the *other factor* *f2*; those two factors are all you need to break the encryption. However, it's *very* unlikely that your randomly guessed number *g* will actually share a factor with *N* considering the *N*s used for modern encryption are massive numbers.

This is where that bad-guess-to-good-guess transformation comes into play. The transformation is based on a simple fact in mathematics. For any two integers *a* and *b* that *do not share a factor* (e.g. our bad guess *g* and the large integer *N*), some power *p* of *a* will certainly produce some multiple *m* of *b* plus 1. 

$$a^p = m * b + 1$$

So to put this into context with our (likely bad) guess *g* and large number *N*, we can be certain that: 

$$g^p = m * N + 1$$

Now, the fun mathy part comes from subtracting the 1 from both sides to get 

$$g^p - 1 = m * N$$

Factoring the left side a bit further gives us:

$$(g^{p/2} + 1)*(g^{p/2} - 1) = m * N$$

Those two factors on the left are exactly the "good" guesses that Shor's algorithm provides from the initial bad guess *g*. In short, 
$$g \implies g^{p/2} \plusmn 1 = m * N$$
describes the transformation. 

Now, since the right side is not just *N*, but *m * N*, the two factors on the left (let's call them *a* and *b* from left to right) may be *multiples* of factors of N rather than factors of N directly. 

### 3 Problems 
There are 3 problems with the equation 
$$(g^{p/2} + 1)*(g^{p/2} - 1) = a * b = m * N$$
 
that necessitate the use of quantum computing for the implementation of this algorithm. 

First, one of the guesses (*a* or *b*) might itself be a factor of *N*. If that's the case, the other guess is a factor of *m*. If that is the case, neither guess is helpful. 

Second, what if the power *p* is odd? Then *p/2* is not a whole number and our original guess *g* raised to the power of *p/2* is likely not whole either. We're working with integers exclusively with this factorization goal, so that's not good. 

NOTE: based on experimental results, 37.5% percent of the time, a random guess *g* transformed into $g \implies g^{p/2} \plusmn 1$ will **not** lead to an odd *p* nor will it lead to *a*
 or *b* being a factor of *N*. Which means, 37.5% of the time, $g^{p/2} \plusmn 1$ will lead to a factor of N that breaks the decryption. 

Third, we need to find *p*. That is, we need to know how many times to multiply our guess *g* by itself to get a multiple *m* of *N* plus 1. This takes a ton of time on classical computers.  



## The Algorithm
To find the power *p* such that 
$$  g^{p/2} \plusmn 1 = m * N$$
we need to set up a quantum computer that takes in an integer *x* as input, raises our initial bad guess *g* to the power of *x*, and keeps track of both *x* and the value of $g^x$. The computer should then use the value of $g^x$ and calculate how much bigger than a multiple (*m*) of $N$ it is, i.e. 
$$r = (g^x) \text{ mod } (m * N) $$
Remember that we want the remainder to be 1 (from the equation above $g^p = m * N + 1$).

Obviously the above approach can be handled with a classical computer assuming we're trying one value of the input *x* at a time. However, with a quantum computer, we can provide a superposition of many values of *x* as the input to the quantum algorithm, and the computation will run simultaneously on all of those values. This computation would result first in the superposition of all corresponding values of $g^x$ for each *x* in the input superposition. Then, the next step should take *that* superposition of all $g^x$ and compute the superposition of all corresponding *remainders* $r$ where each $r_i$ is 
$$r_i = (g^x)_i \text{ mod } (m * N) $$

With this, we can also leverage [quantum interference](https://qiskit.org/documentation/qc_intro.html?highlight=interference#interference) to get all of our "non-p" answers (i.e. results that are not the *p* we are looking for) to destructively interfere with each other, i.e., to cancel each other out so we are only left with one possible answer: *p*. 

### Period Finding
Here we introduce the concept of period finding, which is ultimately the problem that Shor's algorithm solves. 
Assume you know $p$ such that 
$$g^p = m*N + 1$$
where the 1 is the remainder $r$. Great. Now, assume you guess a random $p$, e.g. $p = 29$. Chances are, with that random guess, you'll get a value of $r$ that isn't equal to 1, e.g. $r=3$. So, 
$$g^{29} = m * N + 3$$
What can we do with this? Well, if you take that same random guess 29, and instead raise $g$ to the power of that guess *plus* $p$ (which is still unknown), you get the same remainder on the right: 
$$g^{29 + p} = m * N + 3$$
In fact, if you add *any multiple of p* to that random guess for *p*, you get the same remainder $r$: 
$$g^{29 + [p, 2p, 3p, .... xp]} = m * N + 3$$

In short, that power $p$ that we are looking for to improve our initial bad guess $g$ has a "repeating" property such that if we take some power $x$ of $g$ and simply add or subtract some multiple of $p$ to that power (as above), the amount more than $m * N$ (i.e. the remainder $r$) stays the same.

Let's take a step back. Before, we looked at passing a superposition of all possible possible powers $p$ (we referred to them as $x$) into the quantum computer running Shor's algorithm. If we were to go ahead and measure the result from the remainder computation run on that superposition, that measurement would give us one possible value for the remainder, $r$, e.g. $r=3$. 

With quantum computing, if the result measured (e.g. if $r=3$) could have been produced from multiple states within the input superposition of states (the superposition of $x$ values), then we can only be left with the superposition of just the states that could have resulted in that measurement. So if we measure the remainder computation output and get $r = 3$, then we're left with only all of the possible powers of $p$ that could have resulted in $r = 3$. 

Combining that with the "repeating property" of $p$ discussed previously, each of those elements $x_i$ in the left-over superposition of possible powers of $p$ (that could have resulted in $r=3$) must be exactly $p$ apart from each other. Let's refer to that left-over superposition as $S$. Since a superposition can be represented as a wave function that shows probabilities of the individual states in that superposition, we can express this differently. The period of the wave function representing that leftover superposition must be $p$, which means the frequency of that wave function must be $\frac{1}{p}$. If you can find the frequency of that wave function, you can find $p$. 

### Fourier Transforms
The Fourier Transform is by far the best tool for finding frequencies. There happens to be a **quantum-specific version** of the Fourier Transform that you can apply to the superposition $S$ (from before) which repeats with a frequency of $f = \frac{1}{p}$. When applied, this will cause all of the frequencies that are not actually present to destructively interfere with each other, and thus cancel each other out to leave only one possible frequency for the superposition $S$ having a value of $\frac{1}{p}$. 

When you pass in a number $c$ to a Quantum Fourier Transform, you get back a superposition of other numbers, where each of those numbers is weighted such that when graphed they produce a wave function with a frequency of the number $c$. The higher the value of the input $c$, the higher the frequency of the output wave function (superposition). 

In our case, we want to pass in a superposition of numbers $S$. When you pass a superposition of numbers to a Quantum Fourier Transform you get back a **superposition of superpositions**. Since, again, superpositions can be expressed as wave functions, we can then take each wave function within the superposition of wave functions and add them together which will produce one wave function that captures destructive interference between the individual wave functions as low values, or dips in the wave. Those dips represent the canceling out of low probability states in the input superposition. 

Extending this idea to our specific context, if your input superposition $S$ consists of superpositions that are spread apart by some amount $p$ (our desired value), then the Fourier Transform will output one possible result of $\frac{1}{p}$ with everything else destructively interfering and canceling out as desired.

### Finally!
Once the frequency $f = \frac{1}{p}$ is obtained from the Quantum Fourier Transform of the superposition of superpositions $S$, we can find $p$ as easily as

$$\frac{1}{\frac{1}{p}} = p$$

And now, referring back to the 3 problems from before, as long as $p$ is even, and as long as $g^{\frac{p}{2}} \plusmn 1$ is *not* directly a multiple of $N$, then $g^{\frac{p}{2}} \plusmn 1$ shares factors with $N$. If that's the case, we can use Euclid's algorithm to *find* those factors $a$ and $b$ which are ultimately the factors providing the security for public key infrastructure. 

# Implementation in Qiskit
The Qiskit implementation of Shor's algorithm can be found in this folder's [main.py](main.py). The implementation is documented in more detail in the [official Qiskit documentation](https://qiskit.org/textbook/ch-algorithms/shor.html).

## Subproblems
As discussed in the above outline of the theory underlying Shor's algorithm, we'll need to address a few subproblems to implement the algorithm in Qiskit.

### Period Finding
First, we'll need to solve the **period finding problem**, i.e., we need to find the power $p$ such that our guess $g$ raised to the power $p$ gives a multiple $m$ of the large number $N$ plus 1, or 
$$ g^p = m * N + 1$$
 
With the periodic function 
$$f(x) = g^x \text{ mod } N$$
$g$ is less than $N$ and the two have no common factors (i.e. $g$ is a "bad guess" as described previously). The *period* $p$ is the smallest non-zero integer such that 
$$g^p = m * N + 1 \implies g^p \text{ mod } N = 1$$

### A quick note on [Quantum Phase Estimation](https://qiskit.org/textbook/ch-algorithms/quantum-phase-estimation.html)
First, since quantum phase estimation is defined on a unitary operator $\hat{U}$, let's define a unitary operator. As documented [here](http://vergil.chemistry.gatech.edu/notes/quantrev/node17.html), a unitary operator $\hat{U}$ is "some operator that preserves the **lengths** and **angles** between vectors and can be thought of as a type of rotation operator in abstract vector space." Or, in shorter mathematical terms, a unitary operator U is an operator whose inverse is equal to its adjoint: $\hat{U}^{-1} = \hat{U}^{\dagger}$. Matrix inversion is discussed in more detail [here](https://www.mathsisfun.com/algebra/matrix-inverse.html) and matrix adjoints (AKA conjugate transposes of matrices) are discussed in more detail [here](https://en.wikipedia.org/wiki/Conjugate_transpose).
 

As documented at the link above, quantum phase estimation is "one of the most important subroutines in quantum computing." Used by many different quantum algorithms (like Shor's), its objective is as follows: Given a unitary operator $U$ the algorithm estimates $\theta$ in $U| \psi\rangle = e^{2 \pi i \theta }| \psi\rangle$, where $| \psi \rangle$ is an eigenvector and $e^{2 \pi i \theta }$ is the corresponding eigenvalue of that eigenvector. In short, we're estimating eigenvalues of a unitary operator. Since $U$ is unitary, all of its eigenvalues have a norm (length) of 1. 

So, Shor's solution to the **period finding problem** was to use quantum phase estimation on the unitary operator: 
$$U| y \rangle = | gy \text{ mod } N \rangle$$

If we start with our register in the state $|1 \rangle$, each successive application of $U$ multiplies the current state of our register by $a \text{ (mod } N)$. After $r$ applications of that multiplication, the register arrives back at the original state $|1 \rangle$. For example, if our initial guess $g$ is 3 and $N$ is 35, and $p$ is the period we are trying to find:
$$U|1\rangle = | 3 \rangle$$
$$U^2|1\rangle = | 9 \rangle$$
$$U^3|1\rangle = | 27 \rangle$$
$$ ... $$
$$U^{(p - 1)}|1\rangle = | 12 \rangle$$
$$U^p|1\rangle = | 1 \rangle$$

The above cycle indicates that a superposition of states *in that cycle* ($|u_o\rangle$) would be an eigenstate of $U$. Or, mathematically speaking, 
$$|u_o\rangle = \frac{1}{\sqrt{p}} \sum_{k=0}^{p-1} | g^k \text{ mod } N$$
where p is the period of the superposition we're interested in finding. 

Note that if we refer back to our definition of the quantum phase estimation equation, we are currently using an eigenvalue of 1 (i.e., $e^{2 \pi i \theta } = 1$) for this eigenstate (the superposition of states in the cycle), meaning the phase is the same for each basis state. 

Let's generalize this to capture an eigenstate where the phase is *different* for each basis state. Specifically, we can focus on the case where the phase of the $k$th state is proportional to $k$. 

$$|u_1\rangle = \frac{1}{\sqrt{p}} \sum_{k=0}^{p-1} e^{-\frac{2 \pi i k}{p}} | g^k \text { mod } N$$

When expressed this way, the estimated eigenvalue

$$ U|u_1 \rangle = e^{\frac{2 \pi i }{p}}|u_1 \rangle$$
contains the period $p$ which we're looking for. The presence of $p$ in the quantum phase estimation ensures that the phase differences between the $p$ different basis states are equal. To further generalize, we can multiply the phase difference by some integer $s$:

$$|u_s\rangle = \frac{1}{\sqrt{p}} \sum_{k=0}^{p-1} e^{-\frac{2 \pi i s k}{p}} | g^k \text { mod } N$$
$$ U|u_s \rangle = e^{\frac{2 \pi i s }{p}}|u_s \rangle$$

This gives a unique eigenstate for each integer value of $s$ where $0 \leq s \leq p - 1$. Keeping in mind that $p$ is the period we're looking for such that our guess $g$ raised to $p$ gives a multiple $m$ of $N$ plus 1, or $g^p = m*N + 1$. 

If we take the summation of those eigenstates, the different phases cancel out all computational basis states except $| 1\rangle$ as expressed below:
$$\frac{1}{\sqrt{p}}\sum_{s=0}^{p-1} |u_s \rangle = |1 \rangle$$

This is similar to the previously discussed step of getting the "left-over" superposition $S$ from the measurement of some single remainder value $r$, e.g., $r=3$, such that $S$ includes only the states that could have produced $r$ as the measurement result. That basis state $|1 \rangle$ is a superposition of eigenstates so doing quantum phase estimation on $U$ using the basis state $| 1 \rangle$ will measure a phase 
$$\phi = \frac{s}{p}$$
where again, $s$ is some random integer between 0 and $p - 1$. This corresponds to the previously discussed step of obtaining the frequency of a superposition of superpositions $S$ via a Quantum Fourier Transform, which produces our $f = \frac{1}{p}$ such that we can easily find the period $p$. After this point, we can use the [continued fractions algorithm](https://en.wikipedia.org/wiki/Continued_fraction) on $\phi$ to find the period $p$.  

### Quantum Fourier Transform (QFT)
We also need to apply the quantum fourier transform to our "superposition of superpositions" as described in the above section such that we can find a frequency ($\frac{1}{p}$) of our superposition obtained from measuring the initial remainder computation. 