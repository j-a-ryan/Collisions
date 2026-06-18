from sympy import solve, symbols, sqrt, Eq

import config
from model.util import calculate_m_2, minkowski_dot


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

    def define_equations(self, Xi1, Xi2, qHT2):

        eq1 = Eq(
            self.p1_dot_q / (self.Q2 + qHT2) + sqrt((self.p1_dot_q / (self.Q2 + qHT2)) ** 2 - (self.m2_2 / (self.Q2 + qHT2))),
            Xi1,
        )
        eq2 = Eq(
            self.p2_dot_q / (self.Q2 + qHT2) + sqrt((self.p2_dot_q / (self.Q2 + qHT2)) ** 2 - (self.m2_2 / (self.Q2 + qHT2))),
            Xi2,
        )
        eq3 = Eq(
            ((self.Q2 + qHT2) * Xi1 * Xi2) + self.m1_2 * self.m2_2 / ((self.Q2 + qHT2) * Xi1 * Xi2),
            self.twice_p1_dot_p2,
        )
        return [eq1, eq2, eq3]

    def solve_for_exp_2yT(self, Xi1_value, Xi2_value, qHT2_value):
        print("Xi1 " + str(Xi1_value))
        print("Xi2 " + str(Xi2_value))
        print("qHT2 " + str(qHT2_value))
        sum_in_denominators = self.Q2 + qHT2_value
        top_inner_denominator = Xi2_value * sum_in_denominators
        numerator = Xi1_value + self.m2_2 / top_inner_denominator
        bottom_inner_denominator = Xi1_value * sum_in_denominators
        denominator = Xi2_value + self.m1_2 / bottom_inner_denominator
        exp_2yT = numerator / denominator
        return exp_2yT

    def find_exp_2yT(self):

        exp_2yT = None

        # Define the unknowns as symbols. Make a tuple of them just for aesthetics below
        Xi1, Xi2, qHT2 = symbols("Xi1 Xi2 qHT2")
        symbols_tuple = (Xi1, Xi2, qHT2)

        # Define the equations
        equations = self.define_equations(Xi1, Xi2, qHT2)

        # Get the solution(s) and use the zeroth one in the set.
        solutions = solve(equations, symbols_tuple, dict=True)  # Returns list of solutions as dictionaries.
        if solutions:
            soln0 = solutions[0]
            Xi1_value = soln0[Xi1]
            Xi2_value = soln0[Xi2]
            qHT2_value = soln0[qHT2]
            exp_2yT = self.solve_for_exp_2yT(Xi1_value, Xi2_value, qHT2_value)
        print("Found exp_2yT: " + str(exp_2yT))
        boost_default_set_message = None
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
