"""
Unit tests for app.agent.planner.Planner and
app.skills.registry.SkillRegistry.
"""

import pytest

from app.agent.context import AgentContext
from app.agent.planner import Planner
from app.skills.base import BaseSkill
from app.skills.registry import SkillRegistry


EXPECTED_PLAN_ORDER = [
    "extract_invoice",
    "vendor_lookup",
    "validate_invoice",
    "duplicate_detection",
    "policy_engine",
    "risk_assessment",
    "recommendation",
    "approval_queue",
    "audit_logger",
]


def test_planner_produces_the_expected_step_order():
    planner = Planner()

    # Planner.create_plan does not read from the context it's given -
    # the plan is static and domain-defined - so a placeholder is fine.
    plan = planner.create_plan(context=None)  # type: ignore[arg-type]

    assert [step.skill for step in plan] == EXPECTED_PLAN_ORDER


def test_planner_steps_are_required_by_default():
    planner = Planner()

    plan = planner.create_plan(context=None)  # type: ignore[arg-type]

    assert all(step.required for step in plan)


class _DummySkill(BaseSkill):
    name = "dummy_skill"

    def execute(self, context: AgentContext) -> AgentContext:
        return context


def test_skill_registry_register_and_get():
    registry = SkillRegistry()
    skill = _DummySkill()

    registry.register(skill)

    assert registry.exists("dummy_skill")
    assert registry.get("dummy_skill") is skill


def test_skill_registry_unknown_skill_raises_keyerror():
    registry = SkillRegistry()

    with pytest.raises(KeyError):
        registry.get("does_not_exist")


def test_every_planned_step_name_matches_a_registered_skill():
    """
    Guards against the exact class of bug the README documents as
    already having broken this codebase once: plan step names that
    don't match the names skills are registered under in
    app/bootstrap.py.
    """

    from app.skills import (
        ApprovalQueueSkill,
        AuditLoggerSkill,
        DuplicateDetectionSkill,
        ExtractInvoiceSkill,
        PolicyEngineSkill,
        RecommendationSkill,
        RiskAssessmentSkill,
        ValidateInvoiceSkill,
        VendorLookupSkill,
    )

    registered_names = {
        cls.name
        for cls in (
            ExtractInvoiceSkill,
            VendorLookupSkill,
            ValidateInvoiceSkill,
            DuplicateDetectionSkill,
            PolicyEngineSkill,
            RiskAssessmentSkill,
            RecommendationSkill,
            ApprovalQueueSkill,
            AuditLoggerSkill,
        )
    }

    planner = Planner()
    plan = planner.create_plan(context=None)  # type: ignore[arg-type]
    planned_names = {step.skill for step in plan}

    assert planned_names == registered_names
