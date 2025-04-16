import unittest
import random
from abc import ABC
from pathlib import Path

from src.Grammar import Grammar
from src.CYK import CYK


class Parser(ABC):
    def _parse_grammar(self, number) -> Grammar:
        with open(self.path / self.filename.format(number)) as file:
            nt_number, alph_size, grammar_rules_number = map(int, file.readline().replace("\n", "").split(" "))
            non_terminals = file.readline().replace("\n", "")
            rules_list = []
            terminals = file.readline().replace("\n", "")
            for i in range(grammar_rules_number):
                rules_list.append(file.readline().replace("\n", ""))
            start_terminal = file.readline().replace("\n", "")
            return Grammar(rules_list, nt_number, alph_size, grammar_rules_number, start_terminal,
                           terminals, non_terminals)


class TestAppropriateGrammars(unittest.TestCase, Parser):
    def setUp(self):
        self.path = Path(__file__).parent / "cases"
        self.filename = "correct_grammar_{}.txt"

    def test_one(self):
        grammar = self._parse_grammar(1)
        parser = CYK()
        parser.fit(grammar)
        self.assertTrue(parser.predict('bbbacccb'))
        self.assertFalse(parser.predict('bbbaccca'))

    def test_two(self):
        grammar = self._parse_grammar(2)
        parser = CYK()
        parser.fit(grammar)
        self.assertTrue(parser.predict('ccbccbca'))
        self.assertFalse(parser.predict('ccbccbcb'))

    def test_three(self):
        grammar = self._parse_grammar(3)
        parser = CYK()
        parser.fit(grammar)
        self.assertTrue(parser.predict('bccaba'))
        self.assertFalse(parser.predict('bccabb'))

    def test_four(self):
        grammar = self._parse_grammar(4)
        parser = CYK()
        parser.fit(grammar)
        self.assertTrue(parser.predict('aabb'))
        self.assertFalse(parser.predict('baba'))

    def test_five(self):
        grammar = self._parse_grammar(5)
        parser = CYK()
        parser.fit(grammar)
        self.assertTrue(parser.predict('()()((()))(())'))
        self.assertFalse(parser.predict('()()()(()))'))

    def test_six(self):
        grammar = self._parse_grammar(6)
        parser = CYK()
        parser.fit(grammar)
        for i in range(5):
            num_a = random.randint(0, 10)
            s_list = list("a" * num_a + "b" * num_a * 2)
            for j in range(5):
                random.shuffle(s_list)
                shuffled_s = ''.join(s_list)
                self.assertTrue(parser.predict(shuffled_s), shuffled_s + '\n')
            for j in range(5):
                another_list = list("a" * random.randint(0, 25) + "b" * random.randint(0, 25))
                random.shuffle(another_list)
                shuffled_s = ''.join(another_list)
                if shuffled_s.count("a") * 2 == shuffled_s.count("b"):
                    self.assertTrue(
                        parser.predict(shuffled_s), shuffled_s + '\n')
                else:
                    self.assertFalse(
                        parser.predict(shuffled_s), shuffled_s + '\n')

    def test_seven(self):
        grammar = self._parse_grammar(7)
        parser = CYK()
        parser.fit(grammar)
        for i in range(10):
            num_a = random.randint(0, 50)
            stroke = "a" * num_a + "b" * num_a
            self.assertTrue(parser.predict(stroke))
            for j in range(10):
                num_a = random.randint(0, 50)
                another_list = list("a" * num_a + "b" * (50 - num_a))
                random.shuffle(another_list)
                shuffled_s = ''.join(another_list)
                if not ('b' in shuffled_s[:25]) and not ('a' in shuffled_s[25:]):
                    self.assertTrue(
                        parser.predict(shuffled_s), shuffled_s + '\n')
                else:
                    self.assertFalse(
                        parser.predict(shuffled_s), shuffled_s + '\n')

    def test_eight(self):
        grammar = self._parse_grammar(8)
        parser = CYK()
        parser.fit(grammar)
        self.assertTrue(parser.predict("abcdeedcba"))
        self.assertTrue(parser.predict("abcdedcba"))
        for i in range(10):
            for j in range(10):
                num_a = random.randint(0, 10)
                num_b = random.randint(0, 10)
                num_c = random.randint(0, 10)
                num_d = random.randint(0, 10)
                num_e = random.randint(0, 10)
                another_list = list("a" * num_a + "b" * num_b + "c" * num_c + "d" * num_d + "e" * num_e)
                random.shuffle(another_list)
                shuffled_s = ''.join(another_list)
                if shuffled_s == shuffled_s[::-1]:
                    self.assertTrue(
                        parser.predict(shuffled_s), shuffled_s + '\n')
                else:
                    self.assertFalse(
                        parser.predict(shuffled_s), shuffled_s + '\n')


class TestInappropriateGrammars(unittest.TestCase, Parser):
    def setUp(self):
        self.path = Path(__file__).parent / "cases"
        self.filename = "incorrect_grammar_{}.txt"

    def test_one(self):
        with self.assertRaises(Exception):
            self._parse_grammar(1)

    def test_two(self):
        with self.assertRaises(Exception):
            self._parse_grammar(2)

    def test_three(self):
        with self.assertRaises(Exception):
            self._parse_grammar(3)


if __name__ == '__main__':
    unittest.main()
