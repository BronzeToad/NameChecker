import json
import os

from typing import Dict, List, Optional, Union

from src.utils.config_helper import ConfigHelper, EnvType
from src.domain_checker import DomainChecker
from src.github_checker import GitHubChecker


# =============================================================================================== #


class NameChecker:
    def __init__(
        self,
        env_type: EnvType,
        names: Optional[List[str]] = None,
        batch_size: Optional[int] = None,
        batch_retries: Optional[int] = None,
        batch_limit: Optional[int] = None,
        domain_max_retries: Optional[int] = None,
        domain_endings: Optional[List[str]] = None,
    ) -> None:
        self.env_type = env_type
        self.names = names
        self.batch_size = batch_size
        self.batch_retries = batch_retries
        self.batch_limit = batch_limit
        self.domain_max_retries = domain_max_retries
        self.domain_endings = domain_endings
        self.__post_init__()

    def __post_init__(self) -> None:
        """Post initialization to set class properties."""
        self.cfg = ConfigHelper(self.env_type)
        self.seeds = self.get_seeds()
        self.names = self.force_list(self.names) or self.get_names()
        self.batch_size = self.batch_size or self.cfg.batch_size
        self.batch_retries = self.batch_retries or self.cfg.batch_retries
        self.batch_limit = self.batch_limit
        self.batches = self.create_batches()

    @staticmethod
    def force_list(string_or_list: Union[str, List[str], None]) -> List[str]:
        """Force a string or list of strings to a list of strings."""
        if string_or_list is None:
            return []
        elif isinstance(string_or_list, str):
            return [string_or_list]
        else:
            return [str(item) for item in string_or_list]

    def get_seeds(self) -> List[Dict]:
        """Get the list of seeds from the seeds file."""
        filepath = os.path.join(self.cfg.config_dir, self.cfg.seeds_filename)
        with open(filepath, "r") as f:
            return json.load(f)

    def get_seed_items(self, seed_position: int) -> List[str]:
        """Get the list of seed items for a given seed position."""
        for seed in self.seeds:
            if seed["seedPosition"] == seed_position:
                return seed["seedItems"]
        return []

    def get_names(self) -> List[str]:
        """Generate the list of names to check."""
        seed_positions = sorted([seed["seedPosition"] for seed in self.seeds])

        def _combine_items(pos_index: int) -> List[str]:
            """Recursively combine seed items to generate names."""
            if pos_index == len(seed_positions) - 1:
                return self.get_seed_items(seed_positions[pos_index])
            current_items = self.get_seed_items(seed_positions[pos_index])
            next_items = _combine_items(pos_index + 1)
            combined = [
                c_item + n_item for c_item in current_items for n_item in next_items
            ]
            return combined

        return _combine_items(0)

    def create_batches(self) -> List[List[str]]:
        """Create batches of names to check."""
        if self.names is None:
            return []
        batches = []
        batch_size = self.batch_size or 1
        for i in range(0, len(self.names), batch_size):
            batches.append(self.names[i: i + batch_size])

        if self.batch_limit is not None and len(batches) > self.batch_limit > 0:
            return batches[: self.batch_limit]
        else:
            return batches

    def process_batch(self, batch: List[str]) -> List[Dict[str, bool]]:
        """Process a batch of names."""
        print(f"Processing batch: {batch} of {len(self.batches)}...")
        domain_checker = DomainChecker(
            host_names=batch,
            config_helper=self.cfg,
            max_retries=self.domain_max_retries,
            endings=self.domain_endings,
        )
        github_checker = GitHubChecker(usernames=batch, config_helper=self.cfg)

        results = self.aggregate_results(
            domain_checker.check(), github_checker.check())
        return results

    # def check(self) -> None:
    #     total_available = 0
    #     total_processed = 0
    #
    #     for i, batch in enumerate(self.batches):
    #         print(f"\nProcessing batch {i + 1} of {len(self.batches)}...")
    #         print(f"Batch items: {batch}")
    #         json_results, calc_results = self.check_batch(batch)
    #
    #         batch_available = 0
    #         for item in calc_results:
    #             if item['domain'] is True:
    #                 batch_available += 1
    #
    #         total_available += batch_available
    #         total_processed += len(batch)
    #
    #         self.save_results(json_results)
    #
    #         batch_percent = 100 * batch_available // len(batch)
    #         total_percent = 100.0 * total_available / total_processed
    #
    #         print(f"Batch: {batch_available} of "
    #               f"{len(batch)} available ({batch_percent}%).")
    #         print(f"Total: {total_available} of "
    #               f"{total_processed} available ({total_percent:.1f}%).")

    def aggregate_results(self, *results) -> List[Dict[str, bool]]:
        """Aggregate the results from multiple checkers."""
        aggregated_results = []
        for result in results:
            aggregated_results.extend(result)
        return aggregated_results

    def save_results(self, results: List[Dict[str, bool]]) -> None:
        """Save the results to the results file."""
        # FIXME: this doesn't feel like it will work properly

        filepath = os.path.join(self.cfg.output_dir, self.cfg.results_filename)
        try:
            with open(filepath, "r") as f:
                existing_data = json.load(f)
        except FileNotFoundError:
            existing_data = []

        for item in results:
            for existing_item in existing_data:
                if item["name"] == existing_item["name"]:
                    existing_item.update(item)
                    break
            else:
                existing_data.append(item)

        with open(filepath, "w") as f:
            json.dump(existing_data, f, indent=4)

    def run(self) -> None:
        all_results = []
        for batch in self.batches:
            batch_results = self.process_batch(batch)
            all_results.extend(batch_results)
            # TODO: save batch results
        # TODO: save all results
