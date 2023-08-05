from pathlib import Path
from typing import Any, Optional, Type, TypeVar, Union

import pandas as pd

from ...basic.navaid import Navaids

# https://github.com/python/mypy/issues/2511
T = TypeVar("T", bound="NMNavaids")


class NMNavaids(Navaids):
    name: str = "nm_navaids"
    filename: Optional[Path] = None
    priority: int = 1

    @property
    def available(self) -> bool:
        if self.filename is None:
            return False
        nnpt_file = next(self.filename.glob("AIRAC_*.nnpt"), None)
        return nnpt_file is not None

    @property
    def data(self) -> pd.DataFrame:
        if self._data is not None:
            return self._data

        msg = f"No AIRAC_*.nnpt file found in {self.filename}"
        raise RuntimeError(msg)

    @classmethod
    def from_file(
        cls: Type[T], filename: Union[Path, str], **kwargs: Any
    ) -> Optional[T]:

        if filename == "":
            return cls(None)

        cls.filename = Path(filename)
        nnpt_file = next(cls.filename.glob("AIRAC_*.nnpt"), None)

        if nnpt_file is None:
            return cls(None)

        instance = cls(
            pd.read_csv(
                nnpt_file,
                sep=";",
                names=["name", "type", "latitude", "longitude", "description"],
                skiprows=1,
            )
        )
        return instance
