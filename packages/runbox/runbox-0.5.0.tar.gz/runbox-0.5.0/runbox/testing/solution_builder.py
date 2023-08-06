from __future__ import annotations

from typing import Protocol

from runbox import DockerExecutor, Mount
from runbox.models import DockerProfile, Limits


class SolutionBuilder(Protocol):

    def with_profile(self, profile: DockerProfile) -> SolutionBuilder:
        ...

    def with_limits(self, limits: Limits) -> SolutionBuilder:
        ...

    async def build(self, executor: DockerExecutor) -> Mount:
        ...
