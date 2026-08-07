"""
Enterprise Skill Registry.
"""

from typing import Dict

from app.skills.base import BaseSkill


class SkillRegistry:

    def __init__(self):

        self._skills: Dict[str, BaseSkill] = {}

    # ---------------------------------------------

    def register(
        self,
        skill: BaseSkill,
    ) -> None:
        """
        Register a skill.
        """

        self._skills[skill.name] = skill

    # ---------------------------------------------

    def get(
        self,
        name: str,
    ) -> BaseSkill:
        """
        Retrieve a skill.
        """

        if name not in self._skills:

            raise KeyError(
                f"Skill '{name}' is not registered."
            )

        return self._skills[name]

    # ---------------------------------------------

    def exists(
        self,
        name: str,
    ) -> bool:

        return name in self._skills

    # ---------------------------------------------

    def list_skills(
        self,
    ) -> list[str]:

        return list(self._skills.keys())