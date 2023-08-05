# Copyright (C) 2022 b5327157
# SPDX-License-Identifier: LGPL-3.0-or-later

from __future__ import annotations

import pathlib

from abc import abstractmethod
from dataclasses import dataclass
from typing import Iterable, Optional, Protocol, Sequence, TypeVar

from no_vtf.pipeline import Pipeline
from no_vtf.texture import Texture

_TextureTypeVar = TypeVar("_TextureTypeVar", bound=Texture)


class PipelineRunner(Protocol):
    @abstractmethod
    def __call__(
        self, pipeline: Pipeline[_TextureTypeVar], tasks: Sequence[Task]
    ) -> Iterable[Result]:
        ...


@dataclass(frozen=True, kw_only=True)
class Task:
    input_file: pathlib.Path
    output_directory: pathlib.Path


@dataclass(frozen=True, kw_only=True)
class Result:
    task: Task
    exception: Optional[Exception]
