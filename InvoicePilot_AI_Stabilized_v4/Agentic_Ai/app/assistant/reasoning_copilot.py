"""
Enterprise AI Reasoning Copilot.

Answers natural language questions about a processed invoice, and
remembers each conversation so follow-up questions can build on
what was already discussed.
"""

from app.agent.execution_store import execution_store
from app.assistant.chat_history_store import chat_history_store

from app.reasoning.context_builder import ContextBuilder
from app.reasoning.prompt_builder import PromptBuilder
from app.reasoning.guardrails import Guardrails
from app.reasoning.response_formatter import ResponseFormatter

from app.schemas.chat import ChatResponse

from app.services.llm.llm_service import LLMService


class ReasoningCopilot:
    """
    Enterprise AI Copilot.
    """

    def __init__(
        self,
        llm_service: LLMService,
    ):

        self.llm = llm_service

        self.execution_store = execution_store

        self.chat_history = chat_history_store

        self.context_builder = ContextBuilder()

        self.prompt_builder = PromptBuilder()

        self.guardrails = Guardrails()

        self.formatter = ResponseFormatter()

    # ---------------------------------------------------------

    def chat(
        self,
        execution_id: str,
        question: str,
    ) -> ChatResponse:
        """
        Answer a question about a processed invoice, using the
        conversation's prior turns (if any) as extra context.
        """

        # ---------------------------------------------
        # Guardrails
        # ---------------------------------------------

        allowed, message = self.guardrails.validate(
            question
        )

        if not allowed:

            return self.formatter.format(

                answer=message,

                execution_id=execution_id,

                provider="Guardrails",

                confidence=1.0,

            )

        # ---------------------------------------------
        # Retrieve execution — prefer the live in-memory
        # context, but fall back to the persisted snapshot
        # (e.g. after a server restart) before giving up, so
        # older invoices stay answerable.
        # ---------------------------------------------

        context = self.execution_store.get(
            execution_id
        )

        invoice_context = None

        if context is not None:

            invoice_context = self.context_builder.build(
                context
            )

        else:

            invoice_context = self.execution_store.get_snapshot(
                execution_id
            )

        if invoice_context is None:

            return self.formatter.format(

                answer=(
                    "I couldn't find that invoice "
                    "execution."
                ),

                execution_id=execution_id,

                provider="System",

                confidence=1.0,

            )

        # ---------------------------------------------
        # Load prior conversation turns for this
        # execution, so follow-up questions have
        # something to refer back to.
        # ---------------------------------------------

        history = self.chat_history.recent(execution_id)

        # ---------------------------------------------
        # Build Prompt
        # ---------------------------------------------

        prompt = self.prompt_builder.build(

            invoice_context,

            question,

            history=history,

        )

        # ---------------------------------------------
        # Ask LLM
        # ---------------------------------------------

        answer, provider, model = self.llm.chat(
            prompt
        )

        # ---------------------------------------------
        # Save this turn (question + answer) so it can
        # inform future questions in this conversation.
        # ---------------------------------------------

        self.chat_history.append(
            execution_id, "user", question
        )

        self.chat_history.append(
            execution_id, "assistant", answer
        )

        # ---------------------------------------------
        # Format Response
        # ---------------------------------------------

        return self.formatter.format(

            answer=answer,

            execution_id=execution_id,

            provider=provider,

            confidence=1.0,

        )

    # ---------------------------------------------------------
    # Conversation history access (used by the /chat history
    # endpoints so the frontend can restore a conversation on
    # reload instead of losing it).
    # ---------------------------------------------------------

    def get_history(self, execution_id: str) -> list[dict]:

        return self.chat_history.get(execution_id)

    def clear_history(self, execution_id: str) -> None:

        self.chat_history.clear(execution_id)
