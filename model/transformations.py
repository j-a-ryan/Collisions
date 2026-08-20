from typing import Optional

import numpy as np
from scipy.optimize import fsolve

import config


def calculate_m_2(vector):  # return minkowski_dot(vector, vector)
    return minkowski_dot(vector, vector)


def minkowski_dot(vector_1, vector_2):
    return vector_1[0] * vector_2[0] - vector_1[1] * vector_2[1] - vector_1[2] * vector_2[2] - vector_1[3] * vector_2[3]


class TransformationEquationSystem:

    def __init__(self, V_prime, Y_prime, q_prime):

        self.Q2 = minkowski_dot(q_prime, q_prime)
        self.m1_2 = calculate_m_2(V_prime)
        self.m2_2 = calculate_m_2(Y_prime)
        self.p1_dot_q = minkowski_dot(V_prime, q_prime)
        self.p2_dot_q = minkowski_dot(Y_prime, q_prime)
        self.twice_p1_dot_p2 = 2 * minkowski_dot(V_prime, Y_prime)

    def solve_for_exp_2yT(self, Xi1_value, Xi2_value, qHT2_value):
        sum_in_denominators = self.Q2 + qHT2_value
        top_inner_denominator = Xi2_value * sum_in_denominators
        numerator = Xi1_value - self.m2_2 / top_inner_denominator
        bottom_inner_denominator = Xi1_value * sum_in_denominators
        denominator = Xi2_value - self.m1_2 / bottom_inner_denominator
        exp_2yT = numerator / denominator
        return exp_2yT

    def _residuals(self, x: np.ndarray, qHT2_guess: float) -> np.ndarray:
        """Residual function for fsolve: f(Xi1, Xi2, qHT2) = 0."""
        Xi1, Xi2, qHT2 = x
        s = self.Q2 + qHT2

        # eq1 residual
        term1 = self.p1_dot_q / s
        sqrt_term1 = np.sqrt(np.maximum(0.0, term1**2 - self.m1_2 / s))  # avoid NaN
        r1 = term1 + sqrt_term1 - Xi1

        # eq2 residual
        term2 = self.p2_dot_q / s
        sqrt_term2 = np.sqrt(np.maximum(0.0, term2**2 - self.m2_2 / s))
        r2 = term2 + sqrt_term2 - Xi2

        # eq3 residual
        r3 = (s * Xi1 * Xi2) + (self.m1_2 * self.m2_2) / (s * Xi1 * Xi2) - self.twice_p1_dot_p2

        return np.array([r1, r2, r3])

    def find_exp_2yT_numerical_3(self, initial_guess: Optional[np.ndarray] = None) -> tuple[float, Optional[str]]:
        """
        Numerically solve for exp(2yT).
        Returns (exp_2yT, warning_message)
        """
        if initial_guess is None:
            initial_guess = np.array([1.0, 1.0, 0.0])  # reasonable starting point

        # Solve the system
        sol, info, ier, msg = fsolve(
            self._residuals, initial_guess, args=(initial_guess[2],), full_output=True, xtol=1e-10  # not really used but kept for signature
        )

        if ier == 1:  # successful convergence
            Xi1, Xi2, qHT2 = sol
            exp_2yT = self.solve_for_exp_2yT(Xi1, Xi2, qHT2)
        else:
            exp_2yT = 1.0
            boost_default_set_message = f"Equations could not be solved (fsolve message: {msg}). " f"Default value {exp_2yT} used."
            return exp_2yT, boost_default_set_message

        # Apply physical bounds
        boost_default_set_message = None
        if exp_2yT > 10:
            boost_default_set_message = (
                f"Boost parameter A calculated to be {exp_2yT:.4f}: too high.\n" f"Default maximum value {config.boost_A_max} used instead."
            )
            exp_2yT = 10

        return exp_2yT, boost_default_set_message
