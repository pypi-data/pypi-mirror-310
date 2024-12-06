from typing import Any

from pydantic import Field

from emp_agents.models.protocol import SkillSet

from .base import AgentBase


class SkillsAgent(AgentBase):
    skills: list[type[SkillSet]] = Field(default_factory=list)

    def model_post_init(self, __context: Any):
        super().model_post_init(__context)

        for skill in self.skills:
            for tool in skill._tools:
                self._add_tool(tool)
