from scipy.optimize import fsolve
import numpy as np
import pandas as pd


def weight(p, delta, gamma):
	return (delta*(p**gamma))/(delta*(p**gamma)+((1-p)**gamma))


def equations(par, *args):
	delta, gamma = par
	p, q, pi_p, pi_q = args

	def w(p):
		return weight(p, delta, gamma)
	return w(p) - pi_p, w(q)-pi_q


def get_delta_gamma(pi_ratios, pi_ps, p):
	deltas = np.empty((len(pi_ratios), len(pi_ps)))
	gammas = np.empty((len(pi_ratios), len(pi_ps)))
	for i, pi_ratio in enumerate(pi_ratios):
		for j, pi_p in enumerate(pi_ps):
				pi_q = pi_p*pi_ratio
				data = (p, 1-p, pi_p, pi_q)
				delta, gamma = fsolve(equations, (1, 1), args=data)
				deltas[i, j] = delta
				gammas[i, j] = gamma
	return deltas, gammas


def get_pi_ratios_pi_ps(deltas, gammas, p):
	pi_ratios = np.empty(deltas.shape)
	pi_ps = np.empty(deltas.shape)
	for i, j in np.ndindex(deltas.shape):
		pi_ps[i, j] = weight(p, deltas[i, j], gammas[i, j])
		pi_ratios[i, j] = weight(1-p, deltas[i, j], gammas[i, j])/pi_ps[i, j]
	return pi_ratios, pi_ps


pd.set_option('display.max_columns', None)


ratios = np.linspace(0.3, 0.94, num=9)
pi_ps = np.linspace(0.15, 0.78, num=10)  # 0.08

deltas, gammas = get_delta_gamma(ratios, pi_ps, 0.6)

df_delta = pd.DataFrame(deltas, index=ratios, columns=pi_ps)
df_gamma = pd.DataFrame(gammas, index=ratios, columns=pi_ps)

print('deltas and gammas for new pi-ratios and pi(p) with p=0.6')
print(df_delta)
print(df_gamma)

old_ratios = np.linspace(0.1, 0.8, num=8)
old_pi_ps = np.linspace(0.2, 0.8, num=11)

old_deltas, old_gammas = get_delta_gamma(old_ratios, old_pi_ps, 0.75)

required_ratios, required_pi_ps = get_pi_ratios_pi_ps(old_deltas, old_gammas, 0.6)
df_ratios = pd.DataFrame(required_ratios, index=old_ratios, columns=old_pi_ps)
df_pi_ps = pd.DataFrame(required_pi_ps, index=old_ratios, columns=old_pi_ps)

print('ratios and pi(p)s for p=0.6 required to obtain the same delta/gamma as old ratio pi(p) for p=0.75')

print(df_ratios)
print(df_pi_ps)


