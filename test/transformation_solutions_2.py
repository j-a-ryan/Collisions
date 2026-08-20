import numpy as np
from scipy.optimize import least_squares, minimize

from model.util import calculate_m_2, minkowski_dot

"""
Key Improvements

Multiple initial guesses + hybrid optimization (least_squares + minimize) for better convergence.
Strict physical constraints: Penalizes invalid regions where square-root discriminants are negative or s ≤ 0.
Better diagnostics and fallback logic.
Safer _compute_exp_2yT_safe with guards against division by zero or unphysical values.
Cleaner class structure and more informative messages.

"""


class TransformationEquationSystem:
    def __init__(self, V_prime, Y_prime, q_prime):
        self.V = np.asarray(V_prime, dtype=float)
        self.Y = np.asarray(Y_prime, dtype=float)
        self.q = np.asarray(q_prime, dtype=float)

        self.Q2 = minkowski_dot(self.q, self.q)
        self.m1_2 = calculate_m_2(self.V)
        self.m2_2 = calculate_m_2(self.Y)
        self.p1_dot_q = minkowski_dot(self.V, self.q)
        self.p2_dot_q = minkowski_dot(self.Y, self.q)
        self.twice_p1_dot_p2 = 2 * minkowski_dot(self.V, self.Y)

    def _residuals(self, x):
        """Residual vector [r1, r2, r3]. Returns large values in unphysical regions."""
        Xi1, Xi2, qHT2 = x
        s = self.Q2 + qHT2
        if s <= 1e-8:
            return [1e8, 1e8, 1e8]

        # Residual 1
        term1 = self.p1_dot_q / s
        disc1 = term1**2 - self.m1_2 / s
        if disc1 < -1e-6:
            return [1e8, 1e8, 1e8]
        sqrt1 = np.sqrt(max(0.0, disc1))
        r1 = term1 + sqrt1 - Xi1

        # Residual 2
        term2 = self.p2_dot_q / s
        disc2 = term2**2 - self.m2_2 / s
        if disc2 < -1e-6:
            return [1e8, 1e8, 1e8]
        sqrt2 = np.sqrt(max(0.0, disc2))
        r2 = term2 + sqrt2 - Xi2

        # Residual 3
        prod = Xi1 * Xi2
        if prod < 1e-12:
            return [1e8, 1e8, 1e8]
        r3 = (s * prod) + (self.m1_2 * self.m2_2) / (s * prod) - self.twice_p1_dot_p2

        return [r1, r2, r3]

    def _objective(self, x):
        """Scalar objective for minimize fallback."""
        res = np.array(self._residuals(x))
        penalty = 0.0
        if self.Q2 + x[2] <= 1e-8 or x[0] <= 0 or x[1] <= 0:
            penalty = 1e8
        return np.sum(res**2) + penalty

    def find_exp_2yT_numerical(self, initial_guess: np.ndarray | None) -> tuple[float, str | None]:
        """
        Robust solver for exp(2yT).
        Returns (exp_2yT, message)
        """
        if initial_guess is None:
            initial_guess = np.array([1.5, 1.5, max(1.0, -self.Q2 + 5.0)])

        best_cost = np.inf
        best_x = None

        # Try several starting points
        guesses = [
            initial_guess,
            np.array([2.0, 2.0, max(1.0, -self.Q2 + 10.0)]),
            np.array([1.0, 3.0, max(1.0, -self.Q2 + 3.0)]),
            np.array([3.0, 1.0, max(1.0, -self.Q2 + 8.0)]),
            np.array([1.8, 1.2, max(1.0, -self.Q2 + 4.0)]),
        ]

        for guess in guesses:
            # Primary: least_squares (great for residual systems)
            bounds = ([0.1, 0.1, -self.Q2 + 1e-6], [100.0, 100.0, 1e6])
            res_ls = least_squares(self._residuals, guess, bounds=bounds, ftol=1e-14, xtol=1e-14, gtol=1e-14, max_nfev=5000)
            if res_ls.cost < best_cost:
                best_cost = res_ls.cost
                best_x = res_ls.x.copy()

            # Fallback optimization
            res_min = minimize(self._objective, guess, bounds=[(0.1, None), (0.1, None), (-self.Q2 + 1e-6, None)], tol=1e-14)
            if res_min.fun < best_cost:
                best_cost = res_min.fun
                best_x = res_min.x.copy()

        if best_cost < 1e-6 and best_x is not None:
            Xi1, Xi2, qHT2 = best_x
            exp_2yT = self._compute_exp_2yT_safe(Xi1, Xi2, qHT2)
            message = None
        else:
            exp_2yT = 1.0
            message = f"No physically valid solution found (best residual cost: {best_cost:.2e}). Using default 1.0."
            return exp_2yT, message

        # Apply physical bounds on the boost parameter
        if exp_2yT > 10.0:
            message = f"Boost too large ({exp_2yT:.4f}) → capped at 10.0"
            exp_2yT = 10.0
        elif exp_2yT < 0.05:
            message = f"Boost too small ({exp_2yT:.4f}) → set to 1.0"
            exp_2yT = 1.0

        return exp_2yT, message

    def _compute_exp_2yT_safe(self, Xi1: float, Xi2: float, qHT2: float) -> float:
        """Safeguarded version of your original analytic formula."""
        s = self.Q2 + qHT2
        if s <= 0 or Xi1 <= 0 or Xi2 <= 0:
            return 1.0

        num = Xi1 - self.m2_2 / (Xi2 * s)
        den = Xi2 - self.m1_2 / (Xi1 * s)

        if abs(den) < 1e-10:
            return 1.0
        ratio = num / den
        return max(0.01, ratio)  # avoid unphysical negative values


# V_prime = np.array([5, 0, 1, 2])
# Y_prime = np.array([5, 0, -1, -2])
# q_prime = np.array([3, 1, 0, 0])
# system_of_equations = TransformationEquationSystem(V_prime, Y_prime, q_prime)
# exp_2yT, failure_message = system_of_equations.find_exp_2yT_numerical()
# print(failure_message)
# print(f"result {exp_2yT}")

# V_prime = np.array([np.float64(4.86664), np.float64(-3.14190), 0, np.float64(-5.27377)])
# Y_prime = np.array([8, 6, 6, 1])
# q_prime = np.array([8, 3, 4, 5])
# system_of_equations = TransformationEquationSystem(V_prime, Y_prime, q_prime)
# exp_2yT, failure_message = system_of_equations.find_exp_2yT_numerical()
# print(failure_message)
# print(f"result {exp_2yT}")
