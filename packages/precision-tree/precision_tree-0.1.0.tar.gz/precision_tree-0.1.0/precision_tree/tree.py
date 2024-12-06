from graphviz import Digraph
from .nodes import Node, DecisionNode, ChanceNode, PayoffNode


class TreeWrapper:
    def __init__(self, tree: DecisionNode):
        #self._validate_tree(tree)
        self.tree = tree


    def _validate_tree(self, tree):
        if not isinstance(tree, DecisionNode):
            raise TypeError("The root of the tree must be a DecisionNode instance")

        self._validate_nodes(tree)


    def _validate_nodes(self, tree):
        if tree is None:
            return

        for (child, _, _) in tree.branches:
            if not isinstance(child, Node):
                raise TypeError("All children of the tree must be Node instances")

            self._validate_nodes(child)


    def get_optimal_path(self) -> tuple:
        return self._get_optimal_path(self.tree)


    def _get_optimal_path(self, node):
        optimal_nodes = {node.name}
        optimal_edges = set()

        if isinstance(node, DecisionNode) and node.best_branch:
            for branch_label, child, _ in node.branches:
                if branch_label == node.best_branch:
                    optimal_edges.add((node.name, child.name))
                    child_nodes, child_edges = self._get_optimal_path(child)
                    optimal_nodes.update(child_nodes)
                    optimal_edges.update(child_edges)

        elif isinstance(node, ChanceNode):
            for _, child, probability in node.branches:
                if probability > 0:
                    optimal_edges.add((node.name, child.name))
                    child_nodes, child_edges = self._get_optimal_path(child)
                    optimal_nodes.update(child_nodes)
                    optimal_edges.update(child_edges)

        return optimal_nodes, optimal_edges


    def show(self, title: str ="Decision Tree"):
        optimal_nodes, optimal_edges = self.get_optimal_path()
        graph = self._visualize_tree(node=self.tree, optimal_nodes=optimal_nodes, optimal_edges=optimal_edges)
        graph.render(title, view=True)


    def _visualize_tree(self, node,
                       graph=None,
                       parent=None,
                       edge_label="",
                       optimal_nodes=None,
                       optimal_edges=None
                    ):
        if graph is None:
            graph = Digraph()
            graph.attr(rankdir="LR")

        label = f"{node.name}"
        if node.value is not None:
            label += f"\nValue: {node.value:.2f}"

        shape = node.type.value
        color = "red" if optimal_nodes and node.name in optimal_nodes else "black"
        graph.node(node.name, label, shape=shape, color=color, fontcolor=color)

        if parent:
            edge_color = "red" if optimal_edges and (parent, node.name) in optimal_edges else "black"
            graph.edge(parent, node.name, label=edge_label, color=edge_color)

        for branch_label, child, probability in node.branches:
            edge_label = branch_label
            if probability is not None:
                edge_label += f" (P: {probability:.2f})"
            self._visualize_tree(
                child,
                graph,
                node.name,
                edge_label,
                optimal_nodes=optimal_nodes,
                optimal_edges=optimal_edges,
            )

        return graph
