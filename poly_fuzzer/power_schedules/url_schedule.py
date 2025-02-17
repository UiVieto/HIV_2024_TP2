import random

from poly_fuzzer.power_schedules.abstract_power_schedule import AbstractPowerSchedule
from poly_fuzzer.common.abstract_seed import AbstractSeed


class URLPowerSchedule(AbstractPowerSchedule):
    def __init__(self) -> None:
        """Constructor"""
        self.path_frequency: set = set()

    def _assign_energy(self, seeds: list[AbstractSeed]) -> list[AbstractSeed]:
        """Assigns seed energy, assigns 1 if already chosen."""
        for seed in seeds:
            if seed not in self.path_frequency:
                seed.energy = len(self.path_frequency) + 1  # Add 1 to avoid 0 energy
            else:
                seed.energy = 1
        
        return seeds

    def _normalized_energy(self, seeds: list[AbstractSeed]) -> list[float]:
        """Normalize energy"""
        energy = [seed.energy for seed in seeds]
        sum_energy = sum(energy)  # Add up all values in energy
        assert sum_energy != 0, "Energy should be greater than zero."
        norm_energy = [nrg / sum_energy for nrg in energy]
        
        return norm_energy

    def choose(self, seeds: list[AbstractSeed]) -> AbstractSeed:
        """Choose weighted by normalized energy."""
        seeds = self._assign_energy(seeds)
        normalized_energy = self._normalized_energy(seeds)
        seed = random.choices(seeds, weights=normalized_energy)[0]
        self.path_frequency.add(seed)
       
        return seed
