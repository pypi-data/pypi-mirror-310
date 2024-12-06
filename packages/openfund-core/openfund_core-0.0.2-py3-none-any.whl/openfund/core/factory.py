from __future__ import annotations

import logging

from pathlib import Path
from typing import TYPE_CHECKING
from poetry.factory import Factory as BaseFactory
from openfund.core.pyopenfund import Openfund

if TYPE_CHECKING:
    from poetry.poetry import Poetry


logger = logging.getLogger(__name__)


class Factory(BaseFactory):
    def __init__(self) -> None:
        super().__init__()

    def create_poetry(
        self,
        cwd: Path | None = None,
        with_groups: bool = True,
    ) -> Poetry:
        poetry = super().create_poetry(cwd=cwd, with_groups=with_groups)
        return poetry

    def create_openfund(
        self,
        cwd: Path | None = None,
        with_groups: bool = True,
    ) -> Openfund:

        poetry = self.create_poetry(cwd=cwd, with_groups=with_groups)

        return Openfund(poetry)
