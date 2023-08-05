# Copyright (C) 2022 b5327157
# SPDX-License-Identifier: LGPL-3.0-or-later

from typing import Iterable, Optional, Sequence, TypeVar

from no_vtf.pipeline import Pipeline
from no_vtf.pipeline_runner import PipelineRunner, Result, Task
from no_vtf.texture import Texture

_TextureTypeVar = TypeVar("_TextureTypeVar", bound=Texture)


class SequentialRunner(PipelineRunner):
    def __call__(
        self, pipeline: Pipeline[_TextureTypeVar], tasks: Sequence[Task]
    ) -> Iterable[Result]:
        for task in tasks:
            yield self.process(pipeline, task)

    @staticmethod
    def process(pipeline: Pipeline[_TextureTypeVar], task: Task) -> Result:
        exception: Optional[Exception] = None
        try:
            pipeline(task.input_file, task.output_directory)
        except Exception as e:
            exception = e

        return Result(task=task, exception=exception)
