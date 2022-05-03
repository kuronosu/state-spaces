from inspect import isfunction


def value_eq_func(data):
    def inner(value):
        return data == value
    return inner


class Node:
    def __init__(self, data):
        self._identifier = hash(data)
        self._predecessor = None
        self._successors: dict[int, Node] = {}
        self.data = data

    @property
    def identifier(self): return self._identifier

    @property
    def predecessor(self): return self._predecessor

    @predecessor.setter
    def predecessor(self, value):
        assert isinstance(
            value, Node) or value == None, f"{value} must be a Node instance or None"
        self._predecessor = value

    @property
    def successors(self):
        return list(self._successors.values())

    def __str__(self) -> str:
        return f"Node({self.identifier}, {self.data})"

    def __repr__(self) -> str:
        return str(self)

    def remove_successor(self, node):
        if node.identifier in self._successors:
            self._successors[node.identifier].predecessor = None
            return self._successors.pop(node.identifier)

    def add_successor(self, new_node):
        assert isinstance(
            new_node, Node), f"{new_node} must be a Node instance"
        new_node.predecessor = self
        self._successors[new_node.identifier] = new_node

    def trace_up(self):
        el = self
        _trace = []
        while el != None:
            _trace.append(el)
            el = el.predecessor
        return _trace

    def str_trace(self):
        return f"[{' => '.join(map(str, reversed(self.trace_up())))}]"

    def values_trace(self):
        return [el.data for el in self.trace_up()]

    # Metodos de busqueda por profundidad
    def dfst(self, value_or_func):
        func = value_or_func
        if not isfunction(value_or_func):
            func = value_eq_func(value_or_func)
        return self._depth_first_search(func)

    def dfs(self, value_or_func):
        return self.dfst(value_or_func)[0]

    def _depth_first_search(self, func, visited: list = []):
        visited.append(self)
        if func(self.data):
            return self, visited
        for child in self.successors:
            res = child._depth_first_search(func, visited)
            if res[0] != None:
                return res
        return None, visited

    # Metodos de busqueda por anchura
    def bfs(self, value_or_func):
        return self.bfst(value_or_func)[0]

    def bfst(self, value_or_func):
        func = value_or_func
        if not isfunction(value_or_func):
            func = value_eq_func(value_or_func)
        return self._breadth_first_search(func)

    def _breadth_first_search(self, func):
        queue = [self]
        visited = []
        while len(queue) > 0:
            visited.append(queue[0])
            if func(queue[0].data):
                return queue[0], visited
            el = queue.pop(0)
            queue.extend(el.successors)
        return None, visited

    # Metodos de filtrado
    def breadth_filter(self, filter_func):
        queue = [self]
        results = []
        while len(queue) > 0:
            if filter_func(queue[0].data):
                results.append(queue[0])
            el = queue.pop(0)
            queue.extend(el.successors)
        return results

    def _depth_filter(self, filter_func, results: list = []):
        if filter_func(self.data):
            results.append(self)
        for child in self.successors:
            child._depth_filter(filter_func, results)
        return results

    def depth_filter(self, filter_func):
        return self._depth_filter(filter_func)
