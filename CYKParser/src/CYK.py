from .Grammar import Grammar, Rule


class CYK:
    def __init__(self, grammar: Grammar | None = None):
        self.grammar = grammar or Grammar()

    def fit(self, grammar: Grammar) -> "CYK":
        self.grammar = grammar
        self.grammar.to_normal_form()
        return self

    def __init_dp(self, word: str, tg_rules: list[Rule], dp: dict) -> None:
        for i in range(len(word)):
            letter = word[i]
            for rule in tg_rules:
                if letter == rule.right[0]:
                    dp[rule.left][i][i + 1] = True

    def __calc_dp(self, word: str, tg_rules: list[Rule], dp: dict) -> None:
        for substr_len in range(2, len(word) + 1):
            for left in range(len(word) - substr_len + 1):
                right = left + substr_len
                for rule in tg_rules:
                    for mid in range(left + 1, right):
                        dp[rule.left][left][right] = dp[rule.left][left][right] or (
                                dp[rule.right[0]][left][mid] and dp[rule.right[1]][mid][right])

    def predict(self, word: str) -> bool:
        n = len(word)
        dp = dict()
        for nt in self.grammar.non_terminals:
            dp[nt] = [[False for _ in range(n + 1)] for _ in range(n + 1)]
        if word == "":
            return self.grammar.is_start_terminal_eps_gen
        terminal_gen_rules = []
        non_terminal_gen_rules = []
        for rule in self.grammar.rules_list:
            if len(rule.right) == 0:
                continue
            if len(rule.right) == 1:
                terminal_gen_rules.append(rule)
            else:
                non_terminal_gen_rules.append(rule)
        self.__init_dp(word, terminal_gen_rules, dp)
        self.__calc_dp(word, non_terminal_gen_rules, dp)
        return dp[self.grammar.start_terminal][0][n]
