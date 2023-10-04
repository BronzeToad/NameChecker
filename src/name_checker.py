from typing import List, Optional

import src.utilities as Utils
from src.enum_factory import EnvType, SeedPosition


# =========================================================================== #

class NameChecker:

    def __init__(
        self,
        env_type: EnvType,
        names: Optional[List[str]] = None,
        batch_size: Optional[int] = None,
        batch_retries: Optional[int] = None,
        batch_limit: Optional[int] = None
    ):
        self.env_type = env_type
        self.names = names
        self.batch_size = batch_size
        self.batch_retries = batch_retries
        self.batch_limit = batch_limit
        self.__post_init__()


    def __post_init__(self):
        self.names = Utils.force_list(self.names) or self.get_names()
        self.names = self.apply_limit()
        self.batch_size = self.batch_size or self.get_batch_size()
        self.max_retries = self.max_retries or self.get_max_retries()

        self.batches = self.create_batches()

        self.results_filepath = Utils.get_results_filepath(self.env_type)


    def get_names(self) -> List[str]:
        names = []

        for start in self.get_name_seeds(SeedPosition.START):
            for end in self.get_name_seeds(SeedPosition.END):
                if start != end:
                    names.append(start + end)

        return names


    def create_batches(self) -> List[List[str]]:
        batches = []
        for i in range(0, len(self.names), self.batch_size):
            batches.append(self.names[i:i + self.batch_size])

        if self.batch_limit is not None and len(batches) > self.batch_limit > 0:
            return batches[:self.batch_limit]
        else:
            return batches


# =========================================================================== #

if __name__ == '__main__':
    tst_limit = None

    tst_a = list('abcdefg')
    tst_b = list('hijklmnop')
    tst_c = list('qrstuvwxyz')

    tst_batches = [tst_a, tst_b, tst_c]

    def apply_limit(batches, limit):
        if limit is not None:
            return batches[:limit]
        else:
            return batches

    print('Batches before limit:')
    for i, batch in enumerate(tst_batches):
        print(i, batch)

    print('\nBatches after limit:')
    tst_batches = apply_limit(tst_batches, tst_limit)
    for i, batch in enumerate(tst_batches):
        print(i, batch)
