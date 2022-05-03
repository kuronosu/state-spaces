from re import sub
from ds import Tree, Node
from .base import BaseState


class JarsState(BaseState):
    def __init__(self, j4, j3, throw=False):
        super().__init__()
        self._j4 = j4
        self._j3 = j3
        if throw and not self.is_valid:
            raise ValueError(f"Invalid state: ({j4}, {j3})")

    def __eq__(self, o: object):
        return isinstance(o, JarsState) and o._j4 == self._j4 and o._j3 == self._j3

    def __hash__(self):
        return hash((self._j4, self._j3))

    def __str__(self):
        return f"State(A: {self._j4}, B: {self._j3})"

    @classmethod
    def validate(cls, state):
        return isinstance(state, cls) and state._j4 >= 0 and state._j4 <= 4 and state._j3 >= 0 and state._j3 <= 3

    @property
    def is_objective(self):
        return self.is_valid and self._j4 == 2

    def apply_rule1(self):
        """llenar la jarra de 4l"""
        if self._j4 < 4:
            a = 4
            b = self._j3
            return JarsState(a, b)

    def apply_rule2(self):
        """llenar la jarra de 3l"""
        if self._j3 < 3:
            a = self._j4
            b = 3
            return JarsState(a, b)

    def apply_rule3(self):
        """vaciar la jarra de 4l"""
        if self._j4 > 0:
            a = 0
            b = self._j3
            return JarsState(a, b)

    def apply_rule4(self):
        """vaciar la jarra de 3l"""
        if self._j3 > 0:
            a = self._j4
            b = 0
            return JarsState(a, b)

    def apply_rule5(self):
        """llenar la jarra de 4l con la de 3l"""
        if self._j4 < 4 and self._j4+self._j3 >= 4:
            b = self._j3 - 4 + self._j4
            a = 4
            return JarsState(a, b)

    def apply_rule6(self):
        """llenar la jarra de 3l con la de 4l"""
        if self._j3 < 3 and self._j4+self._j3 >= 3:
            a = self._j4 - 3 + self._j3
            b = 3
            return JarsState(a, b)

    def apply_rule7(self):
        """vaciar el contenido de la jarra de 4l en la de 3l"""
        if self._j4 > 0 and self._j4+self._j3 <= 3:
            b = self._j4 + self._j3
            a = 0
            return JarsState(a, b)

    def apply_rule8(self):
        """vaciar el contenido de la jarra de 3l en la de 4l"""
        if self._j3 > 0 and self._j4 + self._j3 <= 4:
            a = self._j4 + self._j3
            b = 0
            return JarsState(a, b)

    @classmethod
    def _generate_state_tree(cls, tree: Tree, node=None):
        if node is None:
            node = tree.root
        for state in cls.generate_next_states(node.data):
            if state and state.is_valid:
                sub_node = tree.create_node(state, node)
                if sub_node:
                    cls._generate_state_tree(tree, sub_node)
        return tree

    @classmethod
    def generate_states_tree(cls):
        tree = Tree()
        tree.create_node(JarsState(0, 0))
        return cls._generate_state_tree(tree)
