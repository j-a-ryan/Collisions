from sympy import solve, symbols, sqrt, Eq
import numpy as np
from scipy.optimize import fsolve

import config
from model.util import calculate_m_2, minkowski_dot


class SquareRootOfNegativeNumber(ValueError):
    def __init__(self):
        super().__init__("Square root of a negative number. Calculation failed.")


class SecondStepTransformationEquationSystem:

    def __init__(self, V_prime, Y_prime, q_prime):
        # print("V' " + str(V_prime))
        # print("Y' " + str(Y_prime))
        # print("q' " + str(q_prime))
        self.Q2 = minkowski_dot(q_prime, q_prime)
        self.m1_2 = calculate_m_2(V_prime)
        self.m2_2 = calculate_m_2(Y_prime)
        self.p1_dot_q = minkowski_dot(V_prime, q_prime)

        self.p2_dot_q = minkowski_dot(Y_prime, q_prime)
        # print(f"p2_dot_q {self.p2_dot_q}")
        self.twice_p1_dot_p2 = 2 * minkowski_dot(V_prime, Y_prime)

    def solve_for_exp_2yT(self, Xi1_value, Xi2_value, qHT2_value):
        # print("Xi1 " + str(Xi1_value))
        # print("Xi2 " + str(Xi2_value))
        # print("qHT2 " + str(qHT2_value))
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
            boost_default_set_message = "Exception solving system of equations"
            # print(error)

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
        xi1_expr = equations[0].lhs
        xi2_expr = equations[1].lhs

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
        # return final_solutions
