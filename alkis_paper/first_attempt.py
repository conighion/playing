import numpy as np
from scipy import optimize
from scipy.interpolate import UnivariateSpline
import matplotlib.pyplot as plt
from typing import Optional

_n_points_in_grid = 100
_x_grid = np.linspace(1 / _n_points_in_grid, 1, num=_n_points_in_grid - 1, endpoint=False)
_beta = 2  # this is the rho/kappa ratio


# define u functions
def u_fun_1(vec: np.ndarray) -> np.ndarray:
    return np.abs(2*vec - 1)


def u_fun_2(vec: np.ndarray) -> np.ndarray:
    return 1/4-2*vec**2*(1-vec)**2


def u_fun_3(vec: np.ndarray) -> np.ndarray:
    tmp = [np.max([1-2*x, 1/2, 2*x-1]) for x in vec]
    return np.array(tmp)


# Define g functions
def g_fun_1(vec: np.ndarray) -> np.ndarray:
    return np.log(vec / (1 - vec)) * (2 * vec - 1)


# Functions options
g_fun = g_fun_1
u_fun = u_fun_3


# Initialize parameters
g_vec = g_fun(_x_grid)
g_vec_d = np.gradient(g_fun(_x_grid), 1/_n_points_in_grid)
u_vec = u_fun(_x_grid)
x_vec = _x_grid


def lambda_fun(v_vec: np.ndarray, return_arg_max: Optional[bool] = False) -> np.ndarray:

    v_vec_d = np.gradient(v_vec, 1 / _n_points_in_grid)

    def lambda_fun_i(row_i_index: int) -> np.ndarray:
        v_i = v_vec[row_i_index]
        x_i = _x_grid[row_i_index]
        u_i = u_vec[row_i_index]
        g_i = g_vec[row_i_index]
        gd_i = g_vec_d[row_i_index]
        vd_i = v_vec_d[row_i_index]

        row_i = v_vec - v_i - vd_i * (x_vec - x_i) - _beta * (v_i - u_i) * (g_fun(x_vec) - g_i - gd_i * (x_vec - x_i))

        if return_arg_max:
            ret_val = _x_grid[np.argmax(np.delete(row_i, row_i_index))]
        else:
            ret_val = np.max(np.delete(row_i, row_i_index))
        return ret_val

    lambda_vec = [lambda_fun_i(i) for i in range(len(v_vec))]

    return lambda_vec


def lambda_fun_norm(v_vec: np.ndarray) -> float:
    return np.linalg.norm(lambda_fun(v_vec))


# solve
initial_guess = u_fun(_x_grid)
initial_guess = _x_grid**2
v_sol = optimize.root(lambda_fun, initial_guess)  # , method='krylov'

# # minimization
# initial_guess = u_fun(_x_grid)
# v_sol = optimize.minimize(lambda_fun_norm, x0=initial_guess)


# plot
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.scatter(_x_grid, u_fun(_x_grid), s=10, c='b', marker="s", label='first')
ax1.scatter(_x_grid, v_sol.x, s=10, c='r', marker="o", label='second')
ax1.scatter(_x_grid, _x_grid, s=10, c='b', marker="_", label='second')
# ax1.get_legend().remove()
plt.legend(loc='upper left')
plt.show()

spl = UnivariateSpline(_x_grid, v_sol.x)
lambda_fun(v_sol.x, return_arg_max=True)
plt.plot(_x_grid, _x_grid[lambda_fun(u_fun(_x_grid), return_arg_max=True)], 'o', color='black')
plt.show()
