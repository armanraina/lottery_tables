import math 

def roundup(x, val):
	return int(math.ceil(x / val)) * val

def rounddown(x, val):
	return int(math.floor(x / val)) * val
def roundnearest(x, val):
	return round(x/val)*val

def getroundedmidpoint(lo, hi, initial_tol=256):
	def helper(lo, hi, tol = 2**32):
		vals = [100, 50, 10, 5, 2, 1, 0.5]
		estimate = (lo+hi)/2 
		i = 0
		k = roundnearest(estimate, vals[i])

		while (k > (hi-hi/tol) or k < (lo+lo/tol)) and i < len(vals):
			k = roundnearest(estimate, vals[i])
			i+=1

		if i == len(vals):
			return -1
		else:
			return k 
			
	result = -1
	tol = initial_tol
	while result == -1 and tol < 2**32:
		result = helper(lo, hi, tol)
		tol *= 2
	if result == -1:
		return helper(lo, hi)
	else:
		return result
