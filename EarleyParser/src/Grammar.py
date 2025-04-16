class Grammar:
    def __init__(self, rules_list=[],
                 nt_number=0,
                 alph_size=0,
                 grammar_rules_number=0,
                 old_start_terminal="S",
                 end_terminal="#",
                 terminals="",
                 non_terminals=""):
        self.rules = dict()
        self.nt_number = nt_number
        self.alph_size = alph_size
        self.grammar_rules_number = grammar_rules_number
        self.old_start_terminal = old_start_terminal.replace("\n", "")
        self.end_terminal = end_terminal
        self.terminals = terminals + "#"
        self.non_terminals = non_terminals + "$"
        for N in self.non_terminals:
            self.rules[N] = []
        for inp_rule in rules_list:
            rule = inp_rule.replace(" ", "").replace("\n", "").split("->")
            rule.append("")
            if len(rule) == 3:
                rule.pop()
            if (len(rule) == 0) or (len(rule) >= 3) or (not (rule[0] in self.non_terminals)):
                raise Exception("incorrect input of grammar rule")
            for ch in rule[1]:
                if (not (ch in self.terminals)) and (not (ch in self.non_terminals)):
                    raise Exception("incorrect input of grammar rule")

            self.rules[rule[0]].append(rule[1] + self.end_terminal)

    def input_grammar(self):
        self.nt_number, self.alph_size, self.grammar_rules_number = map(int, input().split())
        self.non_terminals = input() + "$"
        for N in self.non_terminals:
            self.rules[N] = []
        self.terminals = input() + "#"
        for i in range(self.grammar_rules_number):
            rule = input().replace(" ", "").split("->")
            rule.append("")
            if len(rule) == 3:
                rule.pop()
            if (len(rule) == 0) or (len(rule) >= 3) or (not (rule[0] in self.non_terminals)):
                raise Exception("incorrect input of grammar rule")
            for ch in rule[1]:
                if (not (ch in self.terminals)) and (not (ch in self.non_terminals)):
                    raise Exception("incorrect input of grammar rule")

            self.rules[rule[0]].append(rule[1] + self.end_terminal)
        self.old_start_terminal = input()

    def output_grammar(self):
        print(self.grammar_rules_number)
        for elem in self.rules.keys():
            print(elem, "->", self.rules[elem], sep='')
