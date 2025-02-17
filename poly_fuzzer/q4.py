from urllib.parse import urlparse
from html.parser import HTMLParser

import cgi_decode

from poly_fuzzer.fuzzers.url_fuzzer import test_mutation_fuzzer, URL_PARSE_SEEDS, HTML_PARSER_SEEDS, URL_PARSE_BUDGET, HTML_PARSER_BUDGET
from poly_fuzzer.fuzzers.cgi_fuzzer import SEEDS as CGI_SEEDS
from poly_fuzzer.fuzzers.cgi_fuzzer import BUDGET as CGI_BUDGET
from poly_fuzzer.power_schedules.url_schedule import URLPowerSchedule
from poly_fuzzer.common.abstract_executor import AbstractExecutor

N_RUNS: int = 10


if __name__ == '__main__':
    max_cgi_coverage: int = 0
    max_url_coverage: int = 0
    max_html_coverage: int = 0

    for _ in range(N_RUNS):
        executor = AbstractExecutor(cgi_decode.cgi_decode)
        power = URLPowerSchedule()
        coverage = test_mutation_fuzzer(executor, CGI_SEEDS, CGI_BUDGET, power)['coverage'][-1]
        max_cgi_coverage = max(max_cgi_coverage, coverage)

        executor = AbstractExecutor(urlparse)
        coverage = test_mutation_fuzzer(executor, URL_PARSE_SEEDS, URL_PARSE_BUDGET)['coverage'][-1]
        max_url_coverage = max(max_url_coverage, coverage)

        executor = AbstractExecutor(HTMLParser().feed)
        power = URLPowerSchedule()
        coverage = test_mutation_fuzzer(executor, HTML_PARSER_SEEDS, HTML_PARSER_BUDGET, power)['coverage'][-1]
        max_html_coverage = max(max_html_coverage, coverage)

    print("Couverture maximale cgi_decode:", max_cgi_coverage)
    print("Couverture maximale urlparse:", max_url_coverage)
    print("Couverture maximale HTMLParser.feed:", max_html_coverage)
