import time

from typing import Tuple
from torch import Tensor
from torch.utils.data import DataLoader


class DataLoaderWrapper:
    """DataLoader wrapper used especially during the Knowledge Distillation (KD) training."""

    def __init__(self, loader: DataLoader) -> None:
        """Ctor.

        Args:
            loader (DataLoader): Data loader to wrap.
        """
        self._loader = loader
        self._cached = None
        self._time = -1.0

    def __iter__(self):
        for batch in self._loader:
            self._cached = batch
            self._time = time.time()
            yield batch

        self._cached = None

    def __len__(self):
        return len(self._loader)

    def cached_batch(self) -> Tuple[Tensor, Tensor]:
        """Returns last batch generated by Data loader.

        Returns:
            Tuple[Tensor, Tensor]: Last batch generated by Data loader.
        """
        return self._cached

    def timestamp(self) -> float:
        """Returns last generated batch's timestamp.

        Returns:
            float: Last generated batch's timestamp.
        """
        return self._time
