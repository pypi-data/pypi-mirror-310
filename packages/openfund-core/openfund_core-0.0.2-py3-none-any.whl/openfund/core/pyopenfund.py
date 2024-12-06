from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any

from poetry.core.pyproject.toml import PyProjectTOML


if TYPE_CHECKING:
    from poetry.core.packages.project_package import ProjectPackage
    from poetry.poetry import Poetry
    from openfund.core.factory import Factory


class Openfund:
    def __init__(self, poetry: Openfund) -> None:
        self._poetry: Poetry = poetry

    @property
    def poetry(self) -> Poetry:
        from pathlib import Path

        if self._poetry is not None:
            return self._poetry

        project_path = Path.cwd()

        self._poetry = Factory().create_poetry(
            cwd=project_path,
        )

        return self._poetry
