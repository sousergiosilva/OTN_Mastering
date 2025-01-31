from jmetal.core.problem import IntegerProblem
from jmetal.core.solution import IntegerSolution
from Problem import Evaluation


class OTNProblem(IntegerProblem):
    def __init__(self, network, number_of_variables):
        super(OTNProblem, self).__init__()
        self.number_of_objectives = 2
        self.number_of_constraints = 0
        self.number_of_variables = number_of_variables

        self.obj_directions = [self.MINIMIZE, self.MINIMIZE]
        self.obj_labels = ['InterfacesQuantities', 'TIRF']

        self.lower_bound = number_of_variables * [0]
        self.upper_bound = number_of_variables * [8]

        self.network = network

    def evaluate(self, solution: IntegerSolution) -> IntegerSolution:
        EvaluationResult = Evaluation.evaluateNetwork(self.network, solution.variables)
        solution.objectives[0] = EvaluationResult[0]
        solution.objectives[1] = EvaluationResult[1]
        # solution.objectives[0] = solution.variables[0]
        # solution.objectives[1] = h * g

        return solution

    def get_name(self):
        return 'OTNProblem'
