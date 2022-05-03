from states import JarsState


def is_objective_func(state): return state.is_objective


if __name__ == '__main__':
    tree = JarsState.generate_states_tree()

    # Busqueda por anchura
    node, route = tree.bfst(is_objective_func)
    print("Busqueda por anchura")
    print("Rama hasta el nodo objetivo: ", list(reversed(node.values_trace())))
    # print("Nodos visitados en la busqueda: ", [n.data for n in route], "\n")

    # Busqueda por anchura
    # node, route = tree.dfst(is_objective_func)
    # print("Busqueda por profundidad")
    # print("Rama hasta el nodo objetivo: ", list(reversed(node.values_trace())))
    # print("Nodos visitados en la busqueda: ", [n.data for n in route], "\n")

    # Filtrando por estados objetivo
    # print("Filtrado")
    # filtered_nodes = tree.depth_filter(is_objective_func)
    # filtered_nodes = tree.breadth_filter(is_objective_func)
    # for node in filtered_nodes:
    #     print(list(reversed(node.values_trace())))
