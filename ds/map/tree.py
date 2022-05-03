from .node import Node


class Tree:
    def __init__(self):
        self._unique_nodes_weight: dict[int, (Node, int)] = {}
        self.root: Node = None

    @property
    def unique_nodes_weight(self):
        return self._unique_nodes_weight

    def get_from_nodes_table(self, identifier):
        if self._unique_nodes_weight in identifier:
            return self._unique_nodes_weight[identifier]

    def create_node(self,  data, parent=None):
        node = Node(data)
        return node if self.add_node(node, parent) else None

    def contains(self, data):
        return hash(data) in self._unique_nodes_weight

    def add_node(self, node, parent: Node = None):
        assert isinstance(
            node, Node), f"First parameter must be object of {Node}"

        if parent is None and self.root is None:
            return self._set_root(node)
        assert isinstance(
            self.root, Node) and parent is not None, f"A parent node was not passed and the tree already has a root"

        parent.add_successor(node)
        node_parent_distance = len(node.trace_up()) - 1
        if node.identifier in self._unique_nodes_weight:
            if node_parent_distance < self._unique_nodes_weight[node.identifier][1]:
                self._unique_nodes_weight.update(
                    {node.identifier: (node, node_parent_distance)})
            else:
                parent.remove_successor(node)
                return False
        else:
            self._unique_nodes_weight.update(
                {node.identifier: (node, node_parent_distance)})
        return True

    def _set_root(self, node):
        self.clear()
        node.predecessor = None
        self.root = node
        self._unique_nodes_weight.update({node.identifier: (node, 0)})

    def clear(self):
        self._unique_nodes_weight = {}
        self.root = None

    def dfs(self, value):
        return self.root.dfs(value)

    def dfst(self, value):
        return self.root.dfst(value)

    def bfs(self, value):
        return self.root.bfs(value)

    def bfst(self, value):
        return self.root.bfst(value)

    def breadth_filter(self, filter_func):
        return self.root.breadth_filter(filter_func)

    def depth_filter(self, filter_func):
        return self.root.depth_filter(filter_func)
