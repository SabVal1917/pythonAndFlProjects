import argparse
from src.CYK import CYK
from src.Grammar import Grammar


def parse_input_file(filename):
    with open(filename) as file:
        nt_number, alph_size, grammar_rules_number = map(int, file.readline().split(" "))
        non_terminals = file.readline()
        rules_list = []
        terminals = file.readline()
        for i in range(grammar_rules_number):
            rules_list.append(file.readline())
        old_start_terminal = file.readline()
        CYKALgo = CYK().fit(
            Grammar(rules_list, nt_number, alph_size, grammar_rules_number, old_start_terminal,
                    terminals, non_terminals))
        number_of_words = int(file.readline())
        with open("output.txt", "w") as output_file:
            for i in range(number_of_words):
                output_file.write("YES\n" if CYKALgo.predict(file.readline().replace('\n', '')) else "NO\n")


def input_stdin():
    CFGrammar = Grammar()
    CFGrammar.input_grammar()
    CYKALgo = CYK().fit(CFGrammar)
    number_of_words = int(input())
    for i in range(number_of_words):
        print("YES" if CYKALgo.predict(input()) else "NO")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Earley Parser')
    parser.add_argument('-f', '--file', help='Имя файла для чтения тестов', default=None)
    args = parser.parse_args()
    if args.file:
        parse_input_file(args.file)
    else:
        input_stdin()
