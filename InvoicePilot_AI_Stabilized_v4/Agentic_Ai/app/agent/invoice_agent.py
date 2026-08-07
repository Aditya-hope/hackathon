"""
Enterprise Invoice Agent.

Main orchestrator for the invoice workflow.
"""
import time

from app.agent.execution_store import execution_store
from app.agent.context import AgentContext
from app.agent.state import AgentState
from app.agent.planner import Planner
from app.core import logger
from app.skills.registry import SkillRegistry


class InvoiceAgent:
    """
    Main workflow orchestrator.
    """

    def __init__(
        self,
        planner: Planner,
        registry: SkillRegistry,
    ):

        self.planner = planner
        self.registry = registry

    # ---------------------------------------------------------

    def process(
        self,
        context: AgentContext,
    ) -> AgentContext:
        logger.info("Invoice Agent started.")

        try:
            context.set_state(
                AgentState.PLANNING
            )

            plan = self.planner.create_plan(
                context
            )

            context.add_event(
                skill="planner",
                message="Execution plan created.",
            )

            for step in plan:

                skill_name = step.skill

                logger.info(
                    f"Executing {skill_name}"
                )

                skill = self.registry.get(
                    skill_name
                )

                context.set_current_skill(
                    skill_name
                )

                attempts = 0

                step_started_at = time.perf_counter()

                while True:

                    try:

                        context = skill.execute(
                            context
                        )

                        break

                    except Exception as e:

                        attempts += 1

                        logger.warning(
                            f"{skill_name} failed "
                            f"(attempt {attempts}/{step.retry}): {e}"
                        )

                        if attempts >= step.retry:

                            if step.required:
                                raise

                            context.add_warning(
                                f"{skill_name} failed and was skipped: {e}"
                            )

                            context.add_event(
                                skill=skill_name,
                                message=str(e),
                                status="SKIPPED",
                            )

                            break

                # Record how long this skill took so the UI can show a
                # per-stage processing time breakdown (e.g. Groq LLM,
                # Duplicate Engine, Policy Engine).
                context.add_skill_timing(
                    skill_name,
                    round(time.perf_counter() - step_started_at, 4),
                )

                if (
                    skill_name == "validate_invoice"
                    and not context.is_valid
                ):

                    logger.warning(
                        "Validation failed. Stopping workflow."
                    )

                    break

            if context.is_valid:

                context.set_state(
                    AgentState.COMPLETED
                )

                context.mark_completed()

                context.add_event(
                    skill="invoice_agent",
                    message="Workflow completed successfully.",
                )

            # Save execution for AI Copilot

            execution_store.save(
                context
            )

            logger.info(
                f"Execution {context.metadata.execution_id} stored."
            )

            logger.info(
                "Invoice Agent finished."
            )

            return context

        except Exception as e:

            logger.exception(
                "Invoice Agent failed."
            )

            context.mark_failed()

            context.add_error(
                str(e)
            )

            context.add_event(
                skill="invoice_agent",
                message=str(e),
                status="FAILED",
            )

            # Save failed execution

            execution_store.save(
                context
            )

            return context
