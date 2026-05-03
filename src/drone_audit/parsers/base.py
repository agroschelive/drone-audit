from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

import pandas as pd


@dataclass(frozen=True)
class ParsedData:
    """Container for parser output normalized for the pipeline."""

    dataframe: pd.DataFrame
    warnings: list[str]
    source_type: str


class Parser(Protocol):
    source_type: str

    def parse(self, path: str | Path) -> ParsedData:
        ...
