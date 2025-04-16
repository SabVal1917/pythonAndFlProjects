from .Grammar import Grammar
from .Situation import Situation


class Earley:
    def __init__(self):
        self.grammar = Grammar()
        self.layers: list[dict[str, set]] = []
        self.predicted: set[str] = set()
        self.changes_flag = False

    def fit(self, g: Grammar) -> "Earley":
        self.grammar = g
        return self

    def __scan(self, letter: str, layer_index: int):
        if (len(self.layers[layer_index][letter]) == 0) or (letter == self.grammar.end_terminal):
            return
        for situation in self.layers[layer_index][letter]:
            self.layers[layer_index + 1][situation.right_part[situation.dot_index + 1]].add(
                Situation(situation.left_part, situation.right_part, situation.dot_index + 1, situation.left_index))

    def __predict(self, layer_index: int):
        for N in self.grammar.non_terminals:
            if (len(self.layers[layer_index][N]) == 0) or (N in self.predicted):
                continue
            for right_part in self.grammar.rules[N]:
                next_char = right_part[0]
                new_situation = Situation(N, right_part, 0, layer_index)
                prev_len = len(self.layers[layer_index][next_char])
                self.layers[layer_index][next_char].add(new_situation)
                if prev_len < len(self.layers[layer_index][next_char]):
                    self.changes_flag = True
            self.predicted.add(N)

    def __complete(self, layer_index: int):
        if len(self.layers[layer_index][self.grammar.end_terminal]) == 0:
            return
        completed_situations = set()
        new_situations = set()
        for end_situation in self.layers[layer_index][self.grammar.end_terminal]:
            if (end_situation in completed_situations) or (
                    (len(self.layers[end_situation.left_index][end_situation.left_part]) == 0)):
                continue
            for read_situation in self.layers[end_situation.left_index][end_situation.left_part]:
                new_situations.add(
                    Situation(read_situation.left_part, read_situation.right_part, read_situation.dot_index + 1,
                              read_situation.left_index)
                )
            completed_situations.add(end_situation)
        for compl_sit in completed_situations:
            self.layers[layer_index][self.grammar.end_terminal].discard(compl_sit)
        for new_sit in new_situations:
            if not (new_sit in self.layers[layer_index][new_sit.right_part[new_sit.dot_index]]):
                self.changes_flag = True
            self.layers[layer_index][new_sit.right_part[new_sit.dot_index]].add(new_sit)

    def predict(self, word: str) -> bool:
        for i in range(len(word) + 1):
            self.layers.append({})
            for y in self.grammar.non_terminals + self.grammar.terminals:
                self.layers[i][y] = set()
        self.layers[0][self.grammar.old_start_terminal].add(
            Situation("$", self.grammar.old_start_terminal + self.grammar.end_terminal, 0, 0))

        self.changes_flag = True
        while self.changes_flag:
            self.changes_flag = False
            self.__complete(0)
            self.__predict(0)

        for index, letter in enumerate(word):
            if not (letter in self.grammar.terminals):
                self.predicted.clear()
                self.layers.clear()
                self.changes_flag = False
                return False
            self.__scan(letter, index)
            self.changes_flag = True
            self.predicted.clear()
            while self.changes_flag:
                self.changes_flag = False
                self.__complete(index + 1)
                self.__predict(index + 1)

        result = Situation("$", self.grammar.old_start_terminal + "#", 1, 0) in self.layers[len(word)][
            self.grammar.end_terminal]
        self.predicted.clear()
        self.layers.clear()
        self.changes_flag = False
        return result
