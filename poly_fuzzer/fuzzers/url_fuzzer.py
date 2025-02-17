from urllib.parse import urlparse
from html.parser import HTMLParser
from typing import TypedDict
from random import randint

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
    "inputs": list[str],
    "execution_times": list[float],
    "exceptions": int
})

NUMBER_RUNS: int = 25
MAX_SEEDS: int = 10

URL_PARSE_BUDGET: int = 200
URL_PARSE_SEEDS: list[AbstractSeed] = [
    AbstractSeed('https://www.google.com/search?q=allo'), 
    AbstractSeed('https://www.github.com'), 
    AbstractSeed('http://localhost:8080'),
    AbstractSeed('https://www.youtube.com/watch?v=u6QfIXgjwGQ'),
    AbstractSeed('https://moodle.polymtl.ca/course/view.php?id=994')
]

HTML_PARSER_BUDGET: int = 500
HTML_PARSER_SEEDS: list[AbstractSeed] = [
    AbstractSeed('<html></html>'), 
    AbstractSeed('<html><div>LOG6305</div></html>'),
    AbstractSeed('<html><head><title>Titre</title></head></html>'),
    AbstractSeed('<html><head><title>Titre</title></head><body><p>Lien</p></body></html>'),
    AbstractSeed('<html><head><title>Titre</title></head><body><p>Lien</p><p>Lotto</p></body></html>')
]


def test_mutation_fuzzer(
        executor: AbstractExecutor,
        seeds: list[AbstractSeed],
        budget: int,
        power_schedule: AbstractPowerSchedule | None=None,
    ) -> FuzzingOutput:    
    assert len(seeds) > 0, "Error: No seed provided."
    
    return MutationFuzzer(executor, seeds, power_schedule).run_fuzzer(budget)

def test_url_parse():
    """Effectue des tests de fuzzing pour le module url_parse"""

    coverages_no_power_no_grammar = []
    coverages_with_power_no_grammar = []
    coverages_with_power_with_grammar = []

    grammar = AbstractGrammar({
        "<start>": ["<url>"],
        "<url>": ["https://www.<content><domain>/<param>?<letter>=<value>"],
        "<domain>": [".ca", ".com", ".org"],
        "<content>": ["<letter>"] * 10,
        "<letter>": [
            "a", "b", "c", "d", "e", "f", "g", "h", "i", "j" ,"k", "l", "m", 
            "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
            "A", "B", "C", "D", "E", "F", "G", "H", "I", "J" ,"K", "L", "M",
            "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"
        ],
        "<param>": ["search", "watch", "database"],
        "<value>": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    })
    seeds = lambda : [AbstractSeed(grammar.generate_input()) for _ in range(MAX_SEEDS)]

    for _ in range(NUMBER_RUNS):
        # Test sans power schedule ou grammaire
        output = test_mutation_fuzzer(AbstractExecutor(urlparse), URL_PARSE_SEEDS, URL_PARSE_BUDGET)
        coverage = output['coverage']
        coverages_no_power_no_grammar.append(coverage)

        # Test avec power schedule, sans grammaire
        output = test_mutation_fuzzer(AbstractExecutor(urlparse), URL_PARSE_SEEDS, URL_PARSE_BUDGET, URLPowerSchedule())
        coverage = output['coverage']
        coverages_with_power_no_grammar.append(coverage)

        # Test avec power schedule et grammaire
        output = test_mutation_fuzzer(AbstractExecutor(urlparse), seeds(), URL_PARSE_BUDGET, URLPowerSchedule())
        coverage = output['coverage']
        coverages_with_power_with_grammar.append(coverage)

    avg_coverage_no_power_no_grammar = np.average(coverages_no_power_no_grammar, axis=0)
    print("Couverture moyenne pour aucun power schedule et grammaire:", avg_coverage_no_power_no_grammar[-1])

    plt.plot(range(1, URL_PARSE_BUDGET+1), avg_coverage_no_power_no_grammar)

    plt.title("Figure 4. Couverture moyenne pour le fuzzing de mutation\n du url_parse sans power schedule ou grammaire")
    plt.xlabel("Nombre de valeurs d'entrées générées")
    plt.ylabel("Nombre de lignes couvertes")
    plt.grid(True, "both", "both")

    plt.show()

    avg_coverage_with_power_no_grammar = np.average(coverages_with_power_no_grammar, axis=0)
    print("Couverture moyenne avec power schedule et sans grammaire:", avg_coverage_with_power_no_grammar[-1])

    plt.plot(range(1, URL_PARSE_BUDGET+1), avg_coverage_with_power_no_grammar)

    plt.title("Figure 5. Couverture moyenne pour le fuzzing de mutation\n du url_parse avec power schedule et sans grammaire")
    plt.xlabel("Nombre de valeurs d'entrées générées")
    plt.ylabel("Nombre de lignes couvertes")
    plt.grid(True, "both", "both")

    plt.show()

    avg_coverage_with_power_with_grammar = np.average(coverages_with_power_with_grammar, axis=0)
    print("Couverture moyenne avec power schedule et grammaire:", avg_coverage_with_power_with_grammar[-1])

    plt.plot(range(1, URL_PARSE_BUDGET+1), avg_coverage_with_power_with_grammar)

    plt.title("Figure 6. Couverture moyenne pour le fuzzing de mutation\n du url_parse avec power schedule et grammaire")
    plt.xlabel("Nombre de valeurs d'entrées générées")
    plt.ylabel("Nombre de lignes couvertes")
    plt.grid(True, "both", "both")

    plt.show()

def test_html_parse():
    """Effectue des tests de fuzzing pour le module html_parse"""

    def generate_input() -> str:
        HTML_ELEMENT = ["<p>LOG6305</p>", "<li>Lien</li>", "<span>Hello World!</span>"]
        GRAMMAR = {
            "<html_content>": [
                ["<body>", "<content>", "</body>"],
                ["<head>", "</head>", "<body>", "<content>", "</body>"]
            ],
        }

        html_content = GRAMMAR["<html_content>"][randint(0, 1)]
        html = ""

        for element in html_content:
            if element == "<content>":
                html += HTML_ELEMENT[randint(0, len(HTML_ELEMENT) - 1)]
            else:
                html += element

        return html

    coverages_no_power_no_grammar = []
    coverages_with_power_no_grammar = []
    coverages_with_power_with_grammar = []

    seeds = lambda : [AbstractSeed(generate_input()) for _ in range(MAX_SEEDS)]

    for _ in range(NUMBER_RUNS):
        # Test sans power schedule ou grammaire
        output = test_mutation_fuzzer(AbstractExecutor(HTMLParser().feed), HTML_PARSER_SEEDS, HTML_PARSER_BUDGET)
        coverage = output['coverage']
        coverages_no_power_no_grammar.append(coverage)

        # Test avec power schedule, sans grammaire
        output = test_mutation_fuzzer(AbstractExecutor(HTMLParser().feed), HTML_PARSER_SEEDS, HTML_PARSER_BUDGET, URLPowerSchedule())
        coverage = output['coverage']
        coverages_with_power_no_grammar.append(coverage)

        # Test avec power schedule et grammaire
        output = test_mutation_fuzzer(AbstractExecutor(HTMLParser().feed), seeds(), HTML_PARSER_BUDGET, URLPowerSchedule())
        coverage = output['coverage']
        coverages_with_power_with_grammar.append(coverage)

    avg_coverage_no_power_no_grammar = np.average(coverages_no_power_no_grammar, axis=0)
    print("Couverture moyenne pour aucun power schedule et grammaire:", avg_coverage_no_power_no_grammar[-1])

    plt.plot(range(1, HTML_PARSER_BUDGET+1), avg_coverage_no_power_no_grammar)

    plt.title("Figure 7. Couverture moyenne pour le fuzzing de mutation\n du html_parse sans power schedule ou grammaire")
    plt.xlabel("Nombre de valeurs d'entrées générées")
    plt.ylabel("Nombre de lignes couvertes")
    plt.grid(True, "both", "both")

    plt.show()

    avg_coverage_with_power_no_grammar = np.average(coverages_with_power_no_grammar, axis=0)
    print("Couverture moyenne avec power schedule et sans grammaire:", avg_coverage_with_power_no_grammar[-1])

    plt.plot(range(1, HTML_PARSER_BUDGET+1), avg_coverage_with_power_no_grammar)

    plt.title("Figure 8. Couverture moyenne pour le fuzzing de mutation\n du html_parse avec power schedule et sans grammaire")
    plt.xlabel("Nombre de valeurs d'entrées générées")
    plt.ylabel("Nombre de lignes couvertes")
    plt.grid(True, "both", "both")

    plt.show()

    avg_coverage_with_power_with_grammar = np.average(coverages_with_power_with_grammar, axis=0)
    print("Couverture moyenne avec power schedule et grammaire:", avg_coverage_with_power_with_grammar[-1])

    plt.plot(range(1, HTML_PARSER_BUDGET+1), avg_coverage_with_power_with_grammar)

    plt.title("Figure 9. Couverture moyenne pour le fuzzing de mutation\n du html_parse avec power schedule et grammaire")
    plt.xlabel("Nombre de valeurs d'entrées générées")
    plt.ylabel("Nombre de lignes couvertes")
    plt.grid(True, "both", "both")

    plt.show()


if __name__ == '__main__':
    test_url_parse()
    test_html_parse()
