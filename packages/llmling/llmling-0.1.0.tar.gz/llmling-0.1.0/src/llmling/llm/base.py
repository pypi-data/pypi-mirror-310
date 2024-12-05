"""Base classes and types for LLM integration."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from llmling.core import exceptions
from llmling.core.log import get_logger


if TYPE_CHECKING:
    from collections.abc import AsyncIterator


logger = get_logger(__name__)


class LLMConfig(BaseModel):
    """Configuration for LLM providers."""

    # Core identification
    model: str
    provider_name: str  # Key used for provider lookup
    display_name: str = ""  # Human-readable name

    # LLM parameters
    temperature: float = 0.7
    max_tokens: int | None = None
    top_p: float | None = None
    timeout: int = 30
    streaming: bool = False
    tools: list[dict[str, Any]] | None = None
    tool_choice: Literal["none", "auto"] | str | None = None  # noqa: PYI051

    # LiteLLM settings
    api_base: str | None = None
    api_key: str | None = None
    num_retries: int | None = None
    request_timeout: float | None = None
    metadata: dict[str, Any] | None = None
    mock_response: str | None = None
    cache: bool | None = None
    cache_key: str | None = None
    fallbacks: list[str] | None = None
    context_window_fallbacks: list[str] | None = None
    bearer_token: str | None = None
    model_list: list[str] | None = None
    drop_params: bool = False
    add_function_to_prompt: bool = False
    force_timeout: float | None = None
    proxy_url: str | None = None
    api_version: str | None = None
    use_queue: bool = False

    model_config = ConfigDict(frozen=True)


MessageRole = Literal["system", "user", "assistant", "tool"]
"""Valid message roles for chat completion."""


class ToolCall(BaseModel):
    """A tool call request from the LLM."""

    id: str  # Required by OpenAI
    name: str
    parameters: dict[str, Any]

    model_config = ConfigDict(frozen=True)


class Message(BaseModel):
    """A chat message."""

    role: MessageRole
    content: str
    name: str | None = None  # For tool messages
    tool_calls: list[ToolCall] | None = None  # For assistant messages
    tool_call_id: str | None = None  # For tool response messages

    model_config = ConfigDict(frozen=True)


class CompletionResult(BaseModel):
    """Result from an LLM completion."""

    content: str
    model: str
    finish_reason: str | None = None
    tool_calls: list[ToolCall] | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(frozen=True)


class LLMProvider(ABC):
    """Base class for LLM providers."""

    def __init__(self, config: LLMConfig) -> None:
        """Initialize the provider.

        Args:
            config: Provider configuration
        """
        self.config = config

    @abstractmethod
    async def complete(
        self,
        messages: list[Message],
        **kwargs: Any,
    ) -> CompletionResult:
        """Generate a completion for the messages.

        Args:
            messages: List of messages for chat completion
            **kwargs: Additional provider-specific parameters

        Returns:
            Completion result

        Raises:
            LLMError: If completion fails
        """

    @abstractmethod
    async def complete_stream(
        self,
        messages: list[Message],
        **kwargs: Any,
    ) -> AsyncIterator[CompletionResult]:
        """Generate a streaming completion for the messages.

        Args:
            messages: List of messages for chat completion
            **kwargs: Additional provider-specific parameters

        Yields:
            Streamed completion results

        Raises:
            LLMError: If completion fails
        """
        yield NotImplemented  # pragma: no cover

    async def validate_response(self, result: CompletionResult) -> None:
        """Validate completion result.

        Args:
            result: Completion result to validate

        Raises:
            LLMError: If validation fails
        """
        if not result.content and not result.tool_calls:
            msg = "Empty response from LLM"
            raise exceptions.LLMError(msg)
