from math import factorial as fact
from decimal import *
import time
import timeit
import math
from multiprocessing import Pool

def read_pi(file):
	with open(file) as f:
		return f.read().replace("\n", "").replace(" ", "")


def get_correct_decimals(pi_est):
	pi_est_str = str(pi_est)[2:]
	real_pi = read_pi("pidigits.txt")

	correct_decimals = 0
	for est, real in zip(pi_est_str, real_pi):
		if est != real:
			break
		correct_decimals += 1
	return correct_decimals

def chudnovsky_sum(k):
	num = Decimal((-1)**k*fact(6*k)*(545140134*k+13591409))
	den = Decimal(fact(3*k)*fact(k)**3*(640320)**Decimal(3*k+1.5))
	return num/den

def chudnovsky(q):
	"""Calculate pi using chudnovsky algorithm
	for q iterations."""
	s = 0
	for i in range(q+1):
		s += chudnovsky_sum(i)
	pi = 1/(12*s)
	return pi

def atan(x_and_terms):
	x = x_and_terms[0]
	terms = x_and_terms[1]

	s = 0
	for term in range(terms):
		num = (-1)**term*x**(2*term+1)
		den = 2*term+1
		s += num/den
	return s

def machin(q):
	"""Calculate pi using machin inverse method
	using q iterations for each calculation of 
	inverse tangens"""
	x_s = [(1/Decimal(49), q), (1/Decimal(57),q),
			(1/Decimal(239),q), (1/Decimal(110443),q)]
	with Pool(None) as p:
		pi_terms = p.map(atan, x_s)
		pi_est = 4*(12*pi_terms[0] + 32*pi_terms[1] - 5*pi_terms[2] +12*pi_terms[3])
		return pi_est

getcontext().prec = 10000

# Calculate digits of pi with machin method
t1 = time.time()
pi_guess = machin(3000)
t2 = time.time()
print(f"Calculating {get_correct_decimals(pi_guess)} digits of pi with machin took {round(t2-t1, 4)} seconds")

# Calculates digits of pi with chudnovsky
# t1 = time.time()
# pi_guess = chudnovsky(76)
# t2 = time.time()
# print(f"Calculating {get_correct_decimals(pi_guess)} digits of pi with chudnovsky took {round(t2-t1, 4)} seconds")

# Calculate digits of pi with 
