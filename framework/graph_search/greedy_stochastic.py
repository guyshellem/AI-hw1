from .graph_problem_interface import *
from .best_first_search import BestFirstSearch
from typing import Optional
import numpy as np


class GreedyStochastic(BestFirstSearch):
    def __init__(self, heuristic_function_type: HeuristicFunctionType,
                 T_init: float = 1.0, N: int = 5, T_scale_factor: float = 0.95):
        # GreedyStochastic is a graph search algorithm. Hence, we use close set.
        super(GreedyStochastic, self).__init__(use_close=True)
        self.heuristic_function_type = heuristic_function_type
        self.T = T_init
        self.N = N
        self.T_scale_factor = T_scale_factor
        self.solver_name = 'GreedyStochastic (h={heuristic_name})'.format(
            heuristic_name=heuristic_function_type.heuristic_name)

    def _init_solver(self, problem: GraphProblem):
        super(GreedyStochastic, self)._init_solver(problem)
        self.heuristic_function = self.heuristic_function_type(problem)

    def _open_successor_node(self, problem: GraphProblem, successor_node: SearchNode):
        """
        DONE: implement this method!
        """
        if not (self.open.has_state(successor_node.state) or self.close.has_state(successor_node.state)):
            self.open.push_node(successor_node)

        #raise NotImplemented()  # DONE: remove!

    def _calc_node_expanding_priority(self, search_node: SearchNode) -> float:
        """
        DONE: implement this method!
        Remember: `GreedyStochastic` is greedy.
        """
        return self.heuristic_function.estimate(search_node.state)
        #raise NotImplemented()  # DONE: remove!

    def _extract_next_search_node_to_expand(self) -> Optional[SearchNode]:
        """
        Extracts the next node to expand from the open queue,
         using the stochastic method to choose out of the N
         best items from open.
        DONE: implement this method!
        Use `np.random.choice(...)` whenever you need to randomly choose
         an item from an array of items given a probabilities array `p`.
        You can read the documentation of `np.random.choice(...)` and
         see usage examples by searching it in Google.
        Notice: You might want to pop min(N, len(open) items from the
                `open` priority queue, and then choose an item out
                of these popped items. The other items have to be
                pushed again into that queue.
        """

        if len(self.open) == 0:
            return None
        options_to_expand = []
        list_size = min(len(self.open), self.N)
        for i in range(list_size):
            options_to_expand += [self.open.pop_next_node()]
            if i == 0 and self._calc_node_expanding_priority(options_to_expand[0]) == 0:
                return options_to_expand[0]
        x_vec = map(self._calc_node_expanding_priority, options_to_expand)
        alpha = min(x_vec)
        sum_of_prob = sum(list(map(lambda x: (x / alpha) ** (-1 / self.T), x_vec)))
        p = np.array(list(map(lambda x: ((x / alpha) ** (-1 / self.T)) / sum_of_prob, x_vec)))

        index_to_expand = np.random.choice(list_size, 1, p)[0]
        for i in filter(lambda x: x != index_to_expand, list(range(list_size))):
            self.open.push_node(options_to_expand[i])
        self.T /= self.T_scale_factor
        return options_to_expand[index_to_expand]
        # raise NotImplemented()  # DONE: remove!
