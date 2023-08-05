# Copyright (C) 2022 b5327157
# SPDX-License-Identifier: LGPL-3.0-or-later

import functools
import multiprocessing
import signal

from dataclasses import dataclass
from typing import Iterable, Optional, Sequence, TypeVar

from no_vtf.pipeline import Pipeline
from no_vtf.pipeline_runner import PipelineRunner, Result, Task
from no_vtf.pipeline_runners.sequential_runner import SequentialRunner
from no_vtf.texture import Texture

_TextureTypeVar = TypeVar("_TextureTypeVar", bound=Texture)


@dataclass(frozen=True, kw_only=True)
class ParallelRunner(PipelineRunner):
    max_workers: Optional[int] = None

    def __call__(
        self, pipeline: Pipeline[_TextureTypeVar], tasks: Sequence[Task]
    ) -> Iterable[Result]:
        ignore_sigint = functools.partial(signal.signal, signal.SIGINT, signal.SIG_IGN)
        with multiprocessing.Pool(self.max_workers, initializer=ignore_sigint) as pool:
            process_with_pipeline = functools.partial(SequentialRunner.process, pipeline)
            for result in pool.imap_unordered(process_with_pipeline, tasks):
                yield result
