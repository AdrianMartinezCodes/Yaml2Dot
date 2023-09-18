import random

import networkx as nx


def generate_large_graph(num_nodes, random_seed=42):
    random.seed(random_seed)
    g = nx.DiGraph()

    for i in range(num_nodes):
        g.add_node(i, label=f"Node {i}")

    for i in range(num_nodes):
        for _ in range(10):  # Adjust the number of edges as needed
            j = random.randint(0, num_nodes - 1)
            if i != j:
                g.add_edge(i, j)

    return g


if __name__ == "__main__":
    random_seed = 42  # Set your desired random seed
    large_graph = generate_large_graph(1000, random_seed)
    print(f"Number of nodes: {large_graph.number_of_nodes()}")
    print(f"Number of edges: {large_graph.number_of_edges()}")
