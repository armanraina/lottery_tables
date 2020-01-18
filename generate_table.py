import numpy as np
import pandas as pd
import math
from rounding import *


def X(X_1, X_2, sigma, r):
    return ((X_2 ** sigma - (1 - r) * (X_1 ** sigma)) / r) ** (1 / sigma)


def Y(Y_1, Y_2, Y_3, sigma, ratio, l):
    return (Y_2 ** sigma + l * (Y_3 ** sigma - Y_1 ** sigma) / ratio) ** (1 / sigma)


def generate_table_series_1(X_1, X_2, sigmas, ratios):
    table = np.empty((len(sigmas), len(ratios)))
    for j, sigma in enumerate(sigmas):
        for i, r in enumerate(ratios):
            table[j, i] = X(X_1, X_2, sigma, r)
    return table


def generate_table_series_2(Z_1, sigmas, ratios):
    table = np.empty((len(sigmas), len(ratios)))
    for j, sigma in enumerate(sigmas):
        for i, r in enumerate(ratios):
            table[j, i] = X(0, Z_1, sigma, r)
    return table


def generate_table_series_3(Y_1, Y_2, sigmas, pi_ps):
    table = np.empty((len(pi_ps), len(sigmas)))
    for j, sigma in enumerate(sigmas):
        for i, pi_p in enumerate(pi_ps):
            table[i, j] = X(Y_1, Y_2, sigma, pi_p)
    return table


def generate_tables_series_4(Y_1, Y_2, Y_3, sigmas, ratios, ls):
    table = np.empty((len(ls), len(sigmas), len(ratios)))
    for i, l in enumerate(ls):
        for j, sigma in enumerate(sigmas):
            for k, ratio in enumerate(ratios):
                table[i, j, k] = Y(Y_1, Y_2, Y_3, sigma, ratio, l)
    return table


sigmas = np.arange(0.3, 1.5, 0.1)
ratios = np.linspace(0.3, 0.94, num=9)
pi_ps = np.linspace(0.15, 0.78, num=10)  # 0.08
ls = np.linspace(0.25, 5, num=20)

X_1 = 80
X_2 = 100
Z_1 = 300
Y_1 = 20
Y_2 = 100
W_1 = 80
W_2 = 10
W_3 = 100

pd.set_option('display.max_columns', None)

table_1 = generate_table_series_1(X_1, X_2, sigmas, ratios)
df_1 = pd.DataFrame(table_1, columns=ratios, index=sigmas)

maxes = list(table_1[0])
mins = list(table_1[-1])

mins = [roundup(maxes[0], 100)] + mins
maxes = maxes + [rounddown(mins[-1], 5)]

result_1 = [getroundedmidpoint(lo, hi) for lo, hi in zip(maxes, mins)]

print('table 1')
df_result_1 = pd.DataFrame(reversed(result_1[:-1]), index = reversed(ratios))
df_result_1.to_csv(r'table_1.csv')
print(df_result_1)
####

table_2 = generate_table_series_2(Z_1, sigmas, ratios)
df_2 = pd.DataFrame(table_2, columns=ratios, index=sigmas)

# print(df_2)
result_2 = np.empty(np.shape(table_2))

for i in range(1, len(table_2)):
    for j in range(len(table_2[0])):
        result_2[i, j] = getroundedmidpoint(table_2[i, j], table_2[i - 1, j])

result_2[0] = np.array([roundup(x, 100) for x in list(table_2[0])])

df_result_2 = pd.DataFrame(result_2, columns=ratios, index=sigmas)
df_result_2.to_csv(r'table_2.csv')
print(df_result_2)
####

table_3 = generate_table_series_3(Y_1, Y_2, sigmas, pi_ps)
df_3 = pd.DataFrame(table_3, columns=sigmas, index=pi_ps)

# print(df_3)
result_3 = np.empty(np.shape(table_3))

for i in range(1, len(table_3)):
    for j in range(len(table_3[0])):
        result_3[i, j] = getroundedmidpoint(table_3[i, j], table_3[i - 1, j])

result_3[0] = np.array([roundup(x, 100) for x in list(table_3[0])])

df_result_3 = pd.DataFrame(result_3, columns=sigmas, index=pi_ps)

print('table 3')
df_result_3.to_csv(r'table_3.csv')
print(df_result_3)

#### 

ratio_view = 0
table_4 = generate_tables_series_4(W_1, W_2, W_3, sigmas, ratios, ls)
df_4 = pd.DataFrame(table_4[:, :, ratio_view], columns=sigmas, index=ls)
result_4 = np.empty(np.shape(table_4))

# print(df_4)

for i in range(1, len(ls)):
    for j in range(len(sigmas)):
        for k in range(len(ratios)):
            result_4[i, j, k] = getroundedmidpoint(table_4[i - 1, j, k], table_4[i, j, k])

for k in range(len(ratios)):
    result_4[0, :, k] = np.array([rounddown(x, 1) for x in list(table_4[0, :, k])])

for k in range(len(ratios)):
    df_result_4 = pd.DataFrame(result_4[:, :, k], columns=sigmas, index=ls)
    print(f'table 4 with ratio = {ratios[k]:.2f}')
    df_result_4.to_csv(f'table_4_{ratios[k]*100:.0f}.csv')
    print(df_result_4)


