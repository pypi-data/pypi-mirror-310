from abc import ABC, abstractmethod
from .enums import NodeShape


class Node(ABC):
    def __init__(self,
                 name: str,
                 type: NodeShape =NodeShape.NONE,
                 value: float =None,
                 cost: float =0,
                 years: int=None
                ):
        self.name = name
        self.value = value
        self.cost = cost
        self.years = years
        self.type = type

        self.branches = []  # (child, label, probability)

    def add_branch(self, label: str, child, probability: float =None):
        self.branches.append((label, child, probability))

    @abstractmethod
    def calculate_value(self):
        pass


class PayoffNode(Node):
    def __init__(self, name, value):
        super().__init__(name=name, value=value, type=NodeShape.TRIANGLE)

    def calculate_value(self):
        return self.value


class ChanceNode(Node):
    def __init__(self, name, cost, years):
        super().__init__(name=name, cost=cost, years=years, type=NodeShape.CIRCLE)

    def calculate_value(self):
        expected_value = -self.cost
        for _, child, probability in self.branches:
            multiplier = self.years if self.years else 1
            expected_value += (probability * child.calculate_value() * multiplier)
        self.value = expected_value
        return expected_value


class DecisionNode(Node):
    def __init__(self, name, value=None):
        super().__init__(name=name, value=value, type=NodeShape.BOX)
        self.best_branch = None

    def calculate_value(self):
        best_value = float('-inf')
        self.best_branch = None

        for branch_label, child, _ in self.branches:
            branch_value = child.calculate_value()
            if branch_value > best_value:
                best_value = branch_value
                self.best_branch = branch_label
        self.value = best_value
        return best_value
