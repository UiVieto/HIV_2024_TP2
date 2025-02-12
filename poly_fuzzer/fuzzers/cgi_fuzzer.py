import matplotlib.pyplot as plt
import numpy as np

from poly_fuzzer.fuzzers.mutation_fuzzer import MutationFuzzer
from poly_fuzzer.common.abstract_executor import AbstractExecutor
from poly_fuzzer.common.abstract_seed import AbstractSeed
from poly_fuzzer.power_schedules.url_schedule import URLPowerSchedule
from poly_fuzzer.common.abstract_grammar import AbstractGrammar

from cgi_decode import cgi_decode

BUDGET: int = 100
NUMBER_RUNS: int = 10
SEEDS: list[AbstractSeed] = [
    AbstractSeed('www.google.com'), 
    AbstractSeed('www.github.com'), 
    AbstractSeed('www.fandom.com'),
    AbstractSeed('www.youtube.com'),
    AbstractSeed('www.moodle.polymtl.ca')
]
MAX_SEEDS: int = 5

def test_mutation_fuzzer_no_power_no_grammar(test_module):
    executor = AbstractExecutor(test_module)
    mutation_fuzzer = MutationFuzzer(executor, SEEDS)

    output = mutation_fuzzer.run_fuzzer(budget=BUDGET)

    return output

def test_mutation_fuzzer_with_power_no_grammar(test_module):
    executor = AbstractExecutor(test_module)
    power = URLPowerSchedule()
    seeds = SEEDS
    mutation_fuzzer = MutationFuzzer(executor, seeds, power)

    output = mutation_fuzzer.run_fuzzer(budget=BUDGET)

    return output

def test_mutation_fuzzer_with_power_with_grammar(test_module):
    gram = {
        "<start>": ["<url>"],
        "<url>": ["<www><content><domain>"],
        "<www>": ["www."],
        "<domain>": [".ca", ".com", ".org", ".net", ".edu", ".us"],
        "<content>": ["<letter><letter><letter><letter><letter><letter><letter><letter>"],
        "<letter>": [
            "a", "b", "c", "d", "e", "f", "g", "h", "i", "j" ,"k", "l", "m", 
            "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
            "A", "B", "C", "D", "E", "F", "G", "H", "I", "J" ,"K", "L", "M",
            "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"
        ],
    }
    grammar = AbstractGrammar(gram)
    seeds = [AbstractSeed(grammar.generate_input()) for _ in range(MAX_SEEDS)]
    executor = AbstractExecutor(test_module)
    power = URLPowerSchedule()
    mutation_fuzzer = MutationFuzzer(executor, seeds, power)

    output = mutation_fuzzer.run_fuzzer(budget=BUDGET)

    return output


if __name__ == '__main__':
    coverages_no_power_no_grammar = []
    coverages_with_power_no_grammar = []
    coverages_with_power_with_grammar = []

    for i in range(NUMBER_RUNS):
        coverage = np.array(test_mutation_fuzzer_no_power_no_grammar(cgi_decode)['coverage'])
        coverages_no_power_no_grammar.append(coverage)

        coverage = np.array(test_mutation_fuzzer_with_power_no_grammar(cgi_decode)['coverage'])
        coverages_with_power_no_grammar.append(coverage)

        coverage = np.array(test_mutation_fuzzer_with_power_with_grammar(cgi_decode)['coverage'])
        coverages_with_power_with_grammar.append(coverage)

    avg_coverage_no_power_no_grammar = np.average(coverages_no_power_no_grammar, axis=0)
    print("Couverture moyenne pour aucun power schedule et grammaire:", avg_coverage_no_power_no_grammar[-1])

    plt.plot(range(1, BUDGET+1), avg_coverage_no_power_no_grammar)

    plt.title("Figure 1. Couverture moyenne pour le fuzzing de mutation\nsans power schedule ou grammaire")
    plt.xlabel("Nombre de valeurs d'entrées générées")
    plt.ylabel("Nombre de lignes couvertes")
    plt.grid(True, "both", "both")

    plt.show()

    avg_coverage_with_power_no_grammar = np.average(coverages_with_power_no_grammar, axis=0)
    print("Couverture moyenne avec power schedule et sans grammaire:", avg_coverage_with_power_no_grammar[-1])

    plt.plot(range(1, BUDGET+1), avg_coverage_with_power_no_grammar)

    plt.title("Figure 2. Couverture moyenne pour le fuzzing de mutation\navec power schedule et sans grammaire")
    plt.xlabel("Nombre de valeurs d'entrées générées")
    plt.ylabel("Nombre de lignes couvertes")
    plt.grid(True, "both", "both")

    plt.show()

    avg_coverage_with_power_with_grammar = np.average(coverages_with_power_with_grammar, axis=0)
    print("Couverture moyenne avec power schedule et grammaire:", avg_coverage_with_power_with_grammar[-1])

    plt.plot(range(1, BUDGET+1), avg_coverage_with_power_with_grammar)

    plt.title("Figure 3. Couverture moyenne pour le fuzzing de mutation\navec power schedule et grammaire")
    plt.xlabel("Nombre de valeurs d'entrées générées")
    plt.ylabel("Nombre de lignes couvertes")
    plt.grid(True, "both", "both")

    plt.show()
