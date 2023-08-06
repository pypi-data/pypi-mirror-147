import itertools
from typing import Any, Dict, List, Set

import numpy as np


def _validate_search_space(search_space: Dict[str, List[Any]]) -> None:
    for hp_name, choices in search_space.items():
        if len(set(choices)) != len(choices):
            raise ValueError("No duplications are allowed for search space, but " f"got {choices} in {hp_name}")


class HashGenerator:
    """
    The class exclusively for converting a config to an integer
    given a search space.
    Args:
        search_space (Dict[str, List[Any]]):
            A search space that we are interested in.
            e.g.
            ```python
            search_space = "sphere": {
                "x0": [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5],
                "x1": [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
            }
            ```
    """

    def __init__(self, search_space: Dict[str, List[Any]]):
        """
        Attributes:
            hp_to_index (Dict[str, Dict[str, int]]):
                The mapping from a choice to an index in each dimension.
            base_list (List[int]):
                The base numbers used to generate a hash value for each config.
            n_max_choices (int):
                The maximum number of choices in search space.
        """
        _validate_search_space(search_space)
        n_choices = [len(choices) for choices in search_space.values()]
        self._n_max_choices = max(n_choices)
        self._hp_to_index = {
            hp_name: {c: idx for idx, c in enumerate(choices)} for hp_name, choices in search_space.items()
        }
        self._search_space = search_space
        dim = len(search_space)
        self._base_list = np.array([self._n_max_choices**d for d in range(dim)])
        self._hash_set: Set[int] = set()
        self._n_call_hash_set = 0

    def _generate_hash_set(self) -> None:
        index_list = [list(range(len(choices))) for choices in self._search_space.values()]
        hash_list = []
        for indices in itertools.product(*index_list):
            hash_val = np.asarray(indices) @ self._base_list
            hash_list.append(hash_val)

        self._hash_set = set(hash_list)

    @property
    def hash_set(self) -> Set[int]:
        self._n_call_hash_set += 1
        if self._n_call_hash_set >= 50:
            raise RuntimeError(
                "hash_set is copied every time you call. "
                "Please copy the attribute and avoid calling it from this instance."
            )

        if len(self._hash_set) == 0:
            self._generate_hash_set()

        return self._hash_set.copy()

    def config2hash(self, config: Dict[str, Any]) -> int:
        """
        A method that maps from config to a hash value.

        Args:
            config (Dict[str, ParamType]):
                A configuration of the objective function.

        Returns:
            hash_val (int):
                A hash value of the given config.
        """
        hash_val = 0
        for dim, (hp_name, map2index) in enumerate(self._hp_to_index.items()):
            idx = map2index[config[hp_name]]
            base = self._base_list[dim]
            hash_val += base * idx
        return hash_val

    def hash2config(self, hash_val: int) -> Dict[str, Any]:
        """
        A method that maps a hash value to config.

        Args:
            hash_val (int):
                A hash value of the given config.

        Returns:
            config (Dict[str, ParamType]):
                A configuration of the objective function.
        """
        config = {}
        for dim, (hp_name, choices) in enumerate(self._search_space.items()):
            idx = hash_val % self._n_max_choices
            config[hp_name] = choices[idx]
            hash_val //= self._n_max_choices

        return config
