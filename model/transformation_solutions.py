from typing import Optional

import numpy as np
from scipy.optimize import fsolve, root_scalar
from sympy import Eq, solve, sqrt, symbols

import config
from model.util import calculate_m_2, minkowski_dot


class SquareRootOfNegativeNumber(ValueError):
    def __init__(self):
        super().__init__("Square root of a negative number. Calculation failed.")


class SecondStepTransformationEquationSystem:

    def __init__(self, V_prime, Y_prime, q_prime):
        print("V' " + str(V_prime))
        print("Y' " + str(Y_prime))
        print("q' " + str(q_prime))
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

    def define_equations(self, Xi1, Xi2, qHT2):

        eq1 = Eq(self.p1_dot_q / (self.Q2 + qHT2) + sqrt((self.p1_dot_q / (self.Q2 + qHT2)) ** 2 - (self.m1_2 / (self.Q2 + qHT2))), Xi1)
        eq2 = Eq(self.p2_dot_q / (self.Q2 + qHT2) + sqrt((self.p2_dot_q / (self.Q2 + qHT2)) ** 2 - (self.m2_2 / (self.Q2 + qHT2))), Xi2)
        eq3 = Eq(((self.Q2 + qHT2) * Xi1 * Xi2) + self.m1_2 * self.m2_2 / ((self.Q2 + qHT2) * Xi1 * Xi2), self.twice_p1_dot_p2)
        return [eq1, eq2, eq3]

    def find_exp_2yT(self):

        # Define the unknowns as symbols. Make a tuple of them just for aesthetics below
        Xi1, Xi2, qHT2 = symbols("Xi1 Xi2 qHT2")
        symbols_tuple = (Xi1, Xi2, qHT2)

        # Define the equations
        equations = self.define_equations(Xi1, Xi2, qHT2)

        # Get the solution(s) and use the zeroth one in the set.
        solutions = solve(equations, symbols_tuple, dict=True)  # Returns list of solutions as dictionaries.

        exp_2yT = None
        if solutions:
            soln0 = solutions[0]
            Xi1_value = soln0[Xi1]
            Xi2_value = soln0[Xi2]
            qHT2_value = soln0[qHT2]
            exp_2yT = self.solve_for_exp_2yT(Xi1_value, Xi2_value, qHT2_value)
        # print("Found exp_2yT: " + str(exp_2yT))
        boost_default_set_message = None
        if exp_2yT is not None:
            if exp_2yT > config.boost_A_max:
                boost_default_set_message = (
                    f"Boost parameter A calculated to be {exp_2yT}: too high.\nDefault maximum value {config.boost_A_max} used instead."
                )
                exp_2yT = config.boost_A_max
                # print("Setting exp_2yT to config.boost_A_max")

        else:
            exp_2yT = 1
            boost_default_set_message = f"Set of equations could not be solved. A boost parameter A\nvalue of {exp_2yT} was used instead."
        return exp_2yT, boost_default_set_message

    def check_square_root_error(self, denom, raise_error=True):
        if (self.p1_dot_q / denom) ** 2 - (self.m1_2 / denom) < 0 or (self.p2_dot_q / denom) ** 2 - (self.m2_2 / denom) < 0:
            if raise_error:
                raise SquareRootOfNegativeNumber()
            else:
                return True

    def find_exp_2yT_numerical(self):

        # this function will be passed into SciPy fsolve. It uses a guess for qHT2 to
        # guess at Xi1 and Xi2 using their respective equations and then substitutes for
        # their variables in the transcendental equation for qHT2.
        def residual(self, qHT2_guess):
            qHT2 = qHT2_guess[0]
            denom = self.Q2 + qHT2
            self.check_square_root_error(denom, True)
            # Calculate Xi1 and Xi2 directly from eq1 and eq2
            Xi1_guessed = (self.p1_dot_q / denom) + np.sqrt((self.p1_dot_q / denom) ** 2 - (self.m1_2 / denom))
            Xi2_guessed = (self.p2_dot_q / denom) + np.sqrt((self.p2_dot_q / denom) ** 2 - (self.m2_2 / denom))

            # Create eq3 as LHS - RHS = 0
            lhs = (denom * Xi1_guessed * Xi2_guessed) + (self.m1_2 * self.m2_2) / (denom * Xi1_guessed * Xi2_guessed)
            rhs = self.twice_p1_dot_p2
            return lhs - rhs

        initial_guess = [self.Q2]  # Q2 should be in the ballpark. [1.0] Alternatively use 1.0

        exp_2yT = None
        denom_with_soln = None
        qHT2_solns = None
        boost_default_set_message = None
        try:
            qHT2_solns = fsolve(residual, initial_guess)
        except Exception as error:
            boost_default_set_message = f"Exception solving system of equations {error}"

        if qHT2_solns:
            qHT2_soln = qHT2_solns[0]
            denom_with_soln = self.Q2 + qHT2_soln  # Re-calculate the Xi1 and Xi2 values using the qHT2_sol solution

            if not self.check_square_root_error(denom_with_soln, False):
                Xi1_soln = (self.p1_dot_q / denom_with_soln) + np.sqrt(
                    (self.p1_dot_q / denom_with_soln) ** 2 - (self.m1_2 / denom_with_soln)
                )
                Xi2_soln = (self.p2_dot_q / denom_with_soln) + np.sqrt(
                    (self.p2_dot_q / denom_with_soln) ** 2 - (self.m2_2 / denom_with_soln)
                )

                exp_2yT = self.solve_for_exp_2yT(Xi1_soln, Xi2_soln, qHT2_soln)

        if exp_2yT is not None:
            if exp_2yT > config.boost_A_max:
                boost_default_set_message = (
                    f"Boost parameter A calculated to be {exp_2yT}: too high.\nDefault maximum value {config.boost_A_max} used instead."
                )
                exp_2yT = config.boost_A_max
                print("Setting exp_2yT to config.boost_A_max")
        else:
            exp_2yT = 1
            boost_default_set_message = f"Set of equations could not be solved. A boost parameter A\nvalue of {exp_2yT} was used instead."

        return exp_2yT, boost_default_set_message

    def find_exp_2yT_symbolic(self):
        Xi1, Xi2, qHT2 = symbols("Xi1 Xi2 qHT2")

        # Get the algebraic expressions for Xi1 and Xi2 directly from your equations
        equations = self.define_equations(Xi1, Xi2, qHT2)
        # sympy's stubs can't express that solve()/Eq results carry .lhs; sympy's typing is
        # inherently dynamic here.
        xi1_expr = equations[0].lhs  # type: ignore[attr-defined]
        xi2_expr = equations[1].lhs  # type: ignore[attr-defined]

        # Substitute them directly into equation 3
        eq3_substituted = equations[2].subs({Xi1: xi1_expr, Xi2: xi2_expr})

        # Solve ONLY for qHT2 (much easier for SymPy's solver)
        qHT2_solutions = solve(eq3_substituted, qHT2)
        qHT2_soln = None
        Xi1_soln = None
        Xi2_soln = None
        # Back-substitute qHT2 to get Xi1 and Xi2 values
        if qHT2_solutions:
            qHT2_soln = qHT2_solutions[0]
            Xi1_soln = xi1_expr.subs(qHT2, qHT2_soln)
            Xi2_soln = xi2_expr.subs(qHT2, qHT2_soln)

        exp_2yT = None
        boost_default_set_message = None
        exp_2yT = self.solve_for_exp_2yT(Xi1_soln, Xi2_soln, qHT2_soln)
        if exp_2yT is not None:
            if exp_2yT > config.boost_A_max:
                boost_default_set_message = (
                    f"Boost parameter A calculated to be {exp_2yT}: too high.\nDefault maximum value {config.boost_A_max} used instead."
                )
                exp_2yT = config.boost_A_max
                print("Setting exp_2yT to config.boost_A_max")
        else:
            exp_2yT = 1
            boost_default_set_message = f"Set of equations could not be solved. A boost parameter A\nvalue of {exp_2yT} was used instead."
        print(f"Got exp_2yT {exp_2yT}")
        return exp_2yT, boost_default_set_message

    def find_exp_2yT_numerical_2(self):
        """Numerically solve for qHT2 and then exp_2yT using the system of equations."""

        def residual(qHT2):
            """Residual of the third equation after substituting Xi1 and Xi2."""
            if np.isnan(qHT2) or np.isinf(qHT2):
                return np.nan

            denom = self.Q2 + qHT2
            if not self.check_square_root_error(denom, True):
                return np.nan

            # Xi1 and Xi2 from eq1 and eq2
            arg1 = (self.p1_dot_q / denom) ** 2 - (self.m1_2 / denom)
            arg2 = (self.p2_dot_q / denom) ** 2 - (self.m2_2 / denom)

            if arg1 < 0 or arg2 < 0:
                return np.nan  # would give imaginary Xi -> invalid

            Xi1 = (self.p1_dot_q / denom) + np.sqrt(arg1)
            Xi2 = (self.p2_dot_q / denom) + np.sqrt(arg2)

            # Third equation: LHS - RHS
            prod_xi = Xi1 * Xi2
            lhs = denom * prod_xi + (self.m1_2 * self.m2_2) / (denom * prod_xi)
            return lhs - self.twice_p1_dot_p2

        # ------------------------------------------------------------------
        exp_2yT = None
        boost_default_set_message = None
        qHT2_soln = None

        # Try Brentq (very reliable for 1D) with sensible brackets
        try:
            # Reasonable physical brackets — adjust based on your domain knowledge
            bracket = [0.0, max(10 * self.Q2, 100.0)]  # or tune as needed

            sol = root_scalar(residual, bracket=bracket, method="brentq", xtol=1e-10, rtol=1e-10, maxiter=100)

            if sol.converged:
                qHT2_soln = sol.root
        except Exception:
            pass  # Fall through to next strategies

        # Fallback 1: Try with a different bracket / initial guess
        if qHT2_soln is None:
            try:
                sol = root_scalar(residual, x0=self.Q2, method="secant", maxiter=50)
                if sol.converged:
                    qHT2_soln = sol.root
            except Exception:
                pass

        # Fallback 2: fsolve (original) as last resort
        if qHT2_soln is None:
            try:
                from scipy.optimize import fsolve

                qHT2_solns = fsolve(residual, [self.Q2])
                candidate = qHT2_solns[0]
                if np.isfinite(candidate) and abs(residual(candidate)) < 1e-6:
                    qHT2_soln = candidate
            except Exception:
                pass

        # ------------------------------------------------------------------
        if qHT2_soln is not None:
            denom = self.Q2 + qHT2_soln

            if self.check_square_root_error(denom, False):
                arg1 = (self.p1_dot_q / denom) ** 2 - (self.m1_2 / denom)
                arg2 = (self.p2_dot_q / denom) ** 2 - (self.m2_2 / denom)

                if arg1 >= 0 and arg2 >= 0:
                    Xi1 = (self.p1_dot_q / denom) + np.sqrt(arg1)
                    Xi2 = (self.p2_dot_q / denom) + np.sqrt(arg2)

                    # Assume this method exists on self
                    exp_2yT = self.solve_for_exp_2yT(Xi1, Xi2, qHT2_soln)

        # Final validation and clamping
        if exp_2yT is not None:
            if exp_2yT > config.boost_A_max:
                boost_default_set_message = (
                    f"Boost parameter A calculated to be {exp_2yT:.4f}: too high.\n"
                    f"Default maximum value {config.boost_A_max} used instead."
                )
                exp_2yT = config.boost_A_max
            elif exp_2yT <= 0:  # usually unphysical
                exp_2yT = 1.0
                boost_default_set_message = "Invalid (non-positive) boost value computed; using default 1.0"
        else:
            exp_2yT = 1.0
            boost_default_set_message = "Set of equations could not be solved. " f"Default boost parameter A = {exp_2yT} was used instead."

        return exp_2yT, boost_default_set_message

        def solve_for_exp_2yT(self, Xi1: float, Xi2: float, qHT2: float) -> float:
            """Compute exp(2yT) from the solved variables."""
            sum_den = self.Q2 + qHT2
            if abs(sum_den) < 1e-12:
                return 1.0  # fallback

            num = Xi1 - self.m2_2 / (Xi2 * sum_den)
            den = Xi2 - self.m1_2 / (Xi1 * sum_den)
            if abs(den) < 1e-12:
                return 1.0
            return num / den

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
            print("Result:")
            print(f"Xi1 {Xi1}")
            print(f"Xi2 {Xi2}")
            print(f"exp_2yT {exp_2yT}")
        else:
            exp_2yT = 1.0
            boost_default_set_message = f"Equations could not be solved (fsolve message: {msg}). " f"Default value {exp_2yT} used."
            return exp_2yT, boost_default_set_message

        # Apply physical bounds
        boost_default_set_message = None
        if exp_2yT > config.boost_A_max:
            boost_default_set_message = (
                f"Boost parameter A calculated to be {exp_2yT:.4f}: too high.\n" f"Default maximum value {config.boost_A_max} used instead."
            )
            exp_2yT = config.boost_A_max

        return exp_2yT, boost_default_set_message
