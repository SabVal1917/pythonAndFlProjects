from queue import Queue


class Rule:
    def __init__(self, left: str = "", right: list[str] = []):
        self.left = left
        self.right = right

    def __str__(self):
        return self.left + "->" + " ".join(self.right)


class Grammar:
    def __init__(self, rules_list=[],
                 nt_number=0,
                 alph_size=0,
                 grammar_rules_number=0,
                 start_terminal="S",
                 terminals=[],
                 non_terminals=[]):
        self.rules_list = []
        self.nt_number = nt_number
        self.alph_size = alph_size
        self.rules_number = grammar_rules_number
        self.start_terminal = start_terminal.replace("\n", "")
        self.terminals = list(terminals)
        self.non_terminals = list(non_terminals)
        for i in range(self.rules_number):
            rule = rules_list[i].replace(" ", "").replace("\n", "").split("->")
            rule.append("")
            if len(rule) == 3:
                rule.pop()
            if (len(rule) == 0) or (len(rule) >= 3) or (not (rule[0] in self.non_terminals)):
                raise Exception("incorrect input of grammar rule")
            for ch in rule[1]:
                if (not (ch in self.terminals)) and (not (ch in self.non_terminals)):
                    raise Exception("incorrect input of grammar rule")
            self.rules_list.append(Rule(rule[0], list(rule[1])))
        self.max_added_nt = 0
        self.is_start_terminal_eps_gen = False

    def input_grammar(self):
        self.nt_number, self.alph_size, self.rules_number = map(int, input().split())
        self.non_terminals = list(input())
        self.terminals = list(input())
        for i in range(self.rules_number):
            rule = input().replace(" ", "").split("->")
            rule.append("")
            if len(rule) == 3:
                rule.pop()
            if (len(rule) == 0) or (len(rule) >= 3) or (not (rule[0] in self.non_terminals)):
                raise Exception("incorrect input of grammar rule")
            for ch in rule[1]:
                if (not (ch in self.terminals)) and (not (ch in self.non_terminals)):
                    raise Exception("incorrect input of grammar rule")

            self.rules_list.append(Rule(rule[0], list(rule[1])))
        self.start_terminal = input()
        self.max_added_nt = 0
        self.is_start_terminal_eps_gen = False

    def __construct_rules_dict(self, rule_dict:dict[str, list[list[str]]]) -> None:
        for nt in self.non_terminals:
            rule_dict[nt] = []
        for rule in self.rules_list:
            rule_dict[rule.left].append(rule.right)



    def __remove_non_generative(self, is_epsilon_gen_modification: bool) -> None:
        queue = Queue()
        rule_num = self.rules_number
        is_rule_generative = [False for _ in range(rule_num)]
        rule_sets = [set() for _ in range(rule_num)]
        generative = set()
        is_eps_gen_nts = dict()
        for x in self.non_terminals:
            is_eps_gen_nts[x] = False
        for i in range(rule_num):
            flag_is_generative = True
            for x in self.rules_list[i].right:
                if x in self.non_terminals:
                    rule_sets[i].add(x)
                    flag_is_generative = False
            if flag_is_generative and not is_epsilon_gen_modification:
                generative.add(self.rules_list[i].left)
                is_rule_generative[i] = True
                continue
            if len(self.rules_list[i].right) == 0:
                generative.add(self.rules_list[i].left)
                is_rule_generative[i] = True
                is_eps_gen_nts[self.rules_list[i].left] = True

        for x in generative:
            queue.put(x)

        while not queue.empty():
            cur_non_term = queue.get()
            for i in range(rule_num):
                if len(rule_sets[i]) > 0:
                    if cur_non_term in rule_sets[i]:
                        rule_sets[i].remove(cur_non_term)
                    if len(rule_sets[i]) == 0:
                        is_rule_generative[i] = True
                        is_eps_gen_nts[self.rules_list[i].left] = True
                        queue.put(self.rules_list[i].left)

        if not is_epsilon_gen_modification:
            rules = dict()
            self.non_terminals = []
            new_rules_list = []
            for i in range(rule_num):
                if not is_rule_generative[i]:
                    continue
                rule = self.rules_list[i]
                new_rules_list.append(rule)
                if not (rule.left in rules.keys()):
                    rules[rule.left] = []
                rules[rule.left].append(rule.right)
            for nt in rules.keys():
                self.non_terminals.append(nt)
            self.nt_number = len(rules)
            self.rules_list = new_rules_list
            self.rules_number = len(new_rules_list)
        else:
            if is_eps_gen_nts[self.start_terminal]:
                self.is_start_terminal_eps_gen = True
            new_rules_list = []
            for i in range(rule_num):
                rule = self.rules_list[i]
                if len(rule.right) == 0:
                    continue
                if len(rule.right) == 1:
                    new_rules_list.append(rule)
                    continue
                A = rule.right[0]
                B = rule.right[1]
                if is_eps_gen_nts[A]:
                    new_rules_list.append(Rule(rule.left, [B]))
                elif is_eps_gen_nts[B]:
                    new_rules_list.append(Rule(rule.left, [A]))
                new_rules_list.append(rule)
            self.rules_list = new_rules_list
            self.rules_number = len(new_rules_list)

    def __remove_unreachable(self) -> None:
        is_nt_reachable = dict()
        for x in self.non_terminals:
            is_nt_reachable[x] = False
        queue = Queue()
        queue.put(self.start_terminal)
        is_nt_reachable[self.start_terminal] = True
        rules = dict()
        self.__construct_rules_dict(rules)

        while not queue.empty():
            cur_non_term = queue.get()
            for right in rules[cur_non_term]:
                for x in right:
                    if (x in self.non_terminals) and not is_nt_reachable[x]:
                        is_nt_reachable[x] = True
                        queue.put(x)

        self.non_terminals = []
        for nt in is_nt_reachable.keys():
            if is_nt_reachable[nt]:
                self.non_terminals.append(nt)
        self.nt_number = len(self.non_terminals)
        new_rules_list = []
        for i in range(self.rules_number):
            rule = self.rules_list[i]
            if not (rule.left in self.non_terminals):
                continue
            is_rule_correct = True
            for x in rule.right:
                if (x in self.terminals) or (x in self.non_terminals):
                    continue
                is_rule_correct = False
                break
            if is_rule_correct:
                new_rules_list.append(rule)
        self.rules_list = new_rules_list
        self.rules_number = len(new_rules_list)

    def __remove_mixed_rules(self) -> None:
        tnt_matching = dict()
        for c in self.terminals:
            tnt_matching[c] = str(self.max_added_nt)
            self.max_added_nt += 1

        for c in self.terminals:
            self.non_terminals.append(tnt_matching[c])

        for i in range(self.rules_number):
            rule = self.rules_list[i]
            has_term = False
            has_nterm = False
            for x in rule.right:
                if x in self.terminals:
                    has_term = True
                if x in self.non_terminals:
                    has_nterm = True
            if has_term and has_nterm:
                for j in range(len(rule.right)):
                    if rule.right[j] in self.terminals:
                        rule.right[j] = tnt_matching[rule.right[j]]
        for c in self.terminals:
            self.rules_list.append(Rule(tnt_matching[c], [c]))
        self.nt_number = len(self.non_terminals)
        self.rules_number = len(self.rules_list)

    def __remove_chain_rules(self) -> None:
        old_max_added_nt = self.max_added_nt
        new_rules_list = []
        for i in range(self.rules_number):
            rule = self.rules_list[i]
            if (len(rule.right) <= 1) or (rule.right[0] in self.terminals):
                new_rules_list.append(rule)
                continue
            right_len = len(rule.right)
            prev_left = rule.left
            for j in range(right_len):
                B_j = str(self.max_added_nt)
                if j == right_len - 2:
                    rule_j = Rule(prev_left, [rule.right[j], rule.right[j + 1]])
                    new_rules_list.append(rule_j)
                    break
                rule_j = Rule(prev_left, [rule.right[j], B_j])
                new_rules_list.append(rule_j)
                prev_left = B_j
                self.max_added_nt += 1

        self.rules_list = new_rules_list
        self.rules_number = len(new_rules_list)
        for j in range(old_max_added_nt, self.max_added_nt):
            self.non_terminals.append(str(j))
        self.nt_number = len(self.non_terminals)

    def __remove_non_generative_and_unreachable(self) -> None:
        self.__remove_non_generative(False)
        self.__remove_unreachable()

    def __process_eps(self):
        # "$" - new start_term
        self.non_terminals = ["$"] + self.non_terminals
        self.rules_list.append(Rule("$", [self.start_terminal]))
        self.start_terminal = "$"
        self.nt_number += 1
        if self.is_start_terminal_eps_gen:
            self.rules_list.append(Rule("$", []))
        self.rules_number = len(self.rules_list)

    def __dfs(self, nt, nt_dict, used, graph):
        used[nt] = True
        for rule in graph[nt]:
            if len(rule) == 0:
                continue
            if len(rule) == 1:
                if rule[0] in self.terminals:
                    continue
                nt_dict[rule[0]].add(nt)
                if not used[rule[0]]:
                    self.__dfs(rule[0], nt_dict, used, graph)
                continue
            if not used[rule[0]]:
                self.__dfs(rule[0], nt_dict, used, graph)
            if not used[rule[1]]:
                self.__dfs(rule[1], nt_dict, used, graph)

    def __reverse_dfs(self, nt, new_rules, used, graph, right_part):
        used[nt] = True
        for non_term in graph[nt]:
            new_rule = Rule(non_term, right_part)
            if not used[non_term]:
                new_rules.append(new_rule)
                self.__reverse_dfs(non_term, new_rules, used, graph, right_part)

    def __remove_unary_rules(self):
        non_terms_reachable_unary_rules = dict()
        used = dict()
        graph = dict()
        for nt in self.non_terminals:
            used[nt] = False
            graph[nt] = []
            non_terms_reachable_unary_rules[nt] = set()
        for i in range(self.rules_number):
            rule = self.rules_list[i]
            graph[rule.left].append(rule.right)
        self.__dfs(self.start_terminal, non_terms_reachable_unary_rules, used, graph)

        new_rules_list = []
        for nt in self.non_terminals:
            used[nt] = False
        for i in range(self.rules_number):
            rule = self.rules_list[i]
            if (len(rule.right) == 1) and (rule.right[0] in self.non_terminals):
                continue
            new_rules_list.append(rule)
            if len(rule.right) == 0:
                continue
            self.__reverse_dfs(rule.left, new_rules_list, used, non_terms_reachable_unary_rules, rule.right)
            for nt in self.non_terminals:
                used[nt] = False

        self.rules_list = new_rules_list
        self.rules_number = len(self.rules_list)

    def to_normal_form(self) -> None:
        self.__remove_non_generative_and_unreachable()
        self.__remove_mixed_rules()
        self.__remove_non_generative_and_unreachable()
        self.__remove_chain_rules()
        self.__remove_non_generative(is_epsilon_gen_modification=True)
        self.__remove_non_generative_and_unreachable()
        self.__process_eps()
        self.__remove_unary_rules()
        self.__remove_non_generative_and_unreachable()

    def output_grammar(self):
        print("-------------------------")
        print(self.rules_number)
        print(self.nt_number)
        print(self.non_terminals)
        for elem in self.rules_list:
            print(elem)
        print("-------------------------")

