from urllib.parse import urlparse
from html.parser import HTMLParser
from typing import TypedDict

import matplotlib.pyplot as plt
import numpy as np

from poly_fuzzer.fuzzers.mutation_fuzzer import MutationFuzzer
from poly_fuzzer.common.abstract_executor import AbstractExecutor
from poly_fuzzer.common.abstract_seed import AbstractSeed
from poly_fuzzer.power_schedules.url_schedule import URLPowerSchedule
from poly_fuzzer.power_schedules.abstract_power_schedule import AbstractPowerSchedule
from poly_fuzzer.common.abstract_grammar import AbstractGrammar

FuzzingOutput = TypedDict("FuzzingOutput", {
    "coverage": list[int],
    "inputs": list,
    "execution_times": list,
    "exceptions": int
})

URL_PARSE_BUDGET: int = 200
NUMBER_RUNS: int = 10
URL_PARSE_SEEDS: list[AbstractSeed] = [
    AbstractSeed('https://www.google.com/search?q=allo'), 
    AbstractSeed('https://www.github.com'), 
    AbstractSeed('http://localhost:8080'),
    AbstractSeed('https://www.youtube.com/watch?v=u6QfIXgjwGQ'),
    AbstractSeed('https://moodle.polymtl.ca/course/view.php?id=994')
]
MAX_SEEDS: int = 5


def test_mutation_fuzzer(
        executor: AbstractExecutor,
        seeds: list[AbstractSeed],
        budget: int,
        power_schedule: AbstractPowerSchedule | None=None,
        grammar: AbstractGrammar | None=None,
        n_seeds: int | None=None) -> FuzzingOutput:
    
    if grammar is None:
        assert len(seeds) != 0, "Error: No seed provided."
        fuzzing_seeds = seeds

    else:
        assert n_seeds is not None, "Error: Number of seeds to generate not provided."
        fuzzing_seeds = [AbstractSeed(grammar.generate_input()) for _ in range(n_seeds)]

    mutation_fuzzer = MutationFuzzer(executor, fuzzing_seeds, power_schedule)
    
    return mutation_fuzzer.run_fuzzer(budget)


def test_mutation_fuzzer_no_power_no_grammar(test_module):
    executor = AbstractExecutor(test_module)
    mutation_fuzzer = MutationFuzzer(executor, URL_PARSE_SEEDS)

    output = mutation_fuzzer.run_fuzzer(budget=URL_PARSE_BUDGET)

    return output

def test_mutation_fuzzer_with_power_no_grammar(test_module):
    executor = AbstractExecutor(test_module)
    power = URLPowerSchedule()
    seeds = URL_PARSE_SEEDS
    mutation_fuzzer = MutationFuzzer(executor, seeds, power)

    output = mutation_fuzzer.run_fuzzer(budget=URL_PARSE_BUDGET)

    return output

def test_mutation_fuzzer_with_power_with_grammar(test_module):
    gram = {
        "<start>": ["<url>"],
        "<url>": ["<www><content><domain>"],
        "<www>": ["www."],
        "<domain>": [".ca", ".com", ".org", ".net", ".edu", ".us", ".to"],
        "<content>": ["<letter>"] * 40,
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

    output = mutation_fuzzer.run_fuzzer(budget=URL_PARSE_BUDGET)

    return output


if __name__ == '__main__':
    coverages_no_power_no_grammar = []
    coverages_with_power_no_grammar = []
    coverages_with_power_with_grammar = []

    for i in range(NUMBER_RUNS):
        coverage = np.array(test_mutation_fuzzer_no_power_no_grammar(urlparse)['coverage'])
        coverages_no_power_no_grammar.append(coverage)

        coverage = np.array(test_mutation_fuzzer_with_power_no_grammar(urlparse)['coverage'])
        coverages_with_power_no_grammar.append(coverage)

        coverage = np.array(test_mutation_fuzzer_with_power_with_grammar(urlparse)['coverage'])
        coverages_with_power_with_grammar.append(coverage)

    avg_coverage_no_power_no_grammar = np.average(coverages_no_power_no_grammar, axis=0)
    print("Couverture moyenne pour aucun power schedule et grammaire:", avg_coverage_no_power_no_grammar[-1])

    plt.plot(range(1, BUDGET+1), avg_coverage_no_power_no_grammar)

    plt.title("Figure 4. Couverture moyenne pour le fuzzing de mutation\nsans power schedule ou grammaire")
    plt.xlabel("Nombre de valeurs d'entrées générées")
    plt.ylabel("Nombre de lignes couvertes")
    plt.grid(True, "both", "both")

    plt.show()

    avg_coverage_with_power_no_grammar = np.average(coverages_with_power_no_grammar, axis=0)
    print("Couverture moyenne avec power schedule et sans grammaire:", avg_coverage_with_power_no_grammar[-1])

    plt.plot(range(1, URL_PARSE_BUDGET+1), avg_coverage_with_power_no_grammar)

    plt.title("Figure 5. Couverture moyenne pour le fuzzing de mutation\navec power schedule et sans grammaire")
    plt.xlabel("Nombre de valeurs d'entrées générées")
    plt.ylabel("Nombre de lignes couvertes")
    plt.grid(True, "both", "both")

    plt.show()

    avg_coverage_with_power_with_grammar = np.average(coverages_with_power_with_grammar, axis=0)
    print("Couverture moyenne avec power schedule et grammaire:", avg_coverage_with_power_with_grammar[-1])

    plt.plot(range(1, URL_PARSE_BUDGET+1), avg_coverage_with_power_with_grammar)

    plt.title("Figure 6. Couverture moyenne pour le fuzzing de mutation\navec power schedule et grammaire")
    plt.xlabel("Nombre de valeurs d'entrées générées")
    plt.ylabel("Nombre de lignes couvertes")
    plt.grid(True, "both", "both")

    plt.show()
