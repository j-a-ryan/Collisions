import unittest
import numpy as np
from model.transformation_solutions import SecondStepTransformationEquationSystem


class TestTransformationSolutions(unittest.TestCase):

    def test_case_1(self):
        V_prime = np.array([5, 0, 1, 2])
        Y_prime = np.array([5, 0, -1, -2])
        q_prime = np.array([3, 1, 0, 0])
        system_of_equations = SecondStepTransformationEquationSystem(V_prime, Y_prime, q_prime)
        result, failure_message = system_of_equations.find_exp_2yT_numerical_3()
        self.assertIsNone(failure_message)
        expected_result = 1
        self.assertAlmostEqual(result, expected_result)

    def test_case_1_proportion_float(self):  # 4/5 proportion of test 1, causing floating point nums
        V_prime = np.array([5, 0, 1, 2]) * 4 / 5
        Y_prime = np.array([5, 0, -1, -2]) * 4 / 5
        q_prime = np.array([3, 1, 0, 0]) * 4 / 5
        system_of_equations = SecondStepTransformationEquationSystem(V_prime, Y_prime, q_prime)
        result, failure_message = system_of_equations.find_exp_2yT()
        self.assertIsNone(failure_message)
        expected_result = 1
        self.assertAlmostEqual(result, expected_result)


# V_prime = np.array([5, 0, 1, 2])
# Y_prime = np.array([5, 0, -1, -2])
# q_prime = np.array([3, 1, 0, 0])
# system_of_equations = TransformationEquationSystem(V_prime, Y_prime, q_prime)
# exp_2yT, failure_message = system_of_equations.find_exp_2yT_numerical_3()
# print(failure_message)
# print(f"result {exp_2yT}")

# V_prime = np.array([np.float64(4.86664), np.float64(-3.14190), 0, np.float64(-5.27377)])
# Y_prime = np.array([8, 6, 6, 1])
# q_prime = np.array([8, 3, 4, 5])
# system_of_equations = TransformationEquationSystem(V_prime, Y_prime, q_prime)
# exp_2yT, failure_message = system_of_equations.find_exp_2yT_numerical_3()
# print(failure_message)
# print(f"result {exp_2yT}")

