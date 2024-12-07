"""Configuration models for LLMling."""

from __future__ import annotations

from collections.abc import Sequence as TypingSequence  # noqa: TC003
import os  # noqa: TC003
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from llmling.core.typedefs import ProcessingStep  # noqa: TC001
from llmling.processors.base import ProcessorConfig  # noqa: TC001


ContextType = Literal["path", "text", "cli", "source", "callable", "image"]


class GlobalSettings(BaseModel):
    """Global settings that apply to all components."""

    timeout: int = 30
    """Maximum time in seconds to wait for operations"""

    max_retries: int = 3
    """Maximum number of retries for failed operations"""

    temperature: float = 0.7
    """Default sampling temperature for LLM completions"""

    model_config = ConfigDict(frozen=True)


class LLMProviderConfig(BaseModel):
    """LLM provider configuration."""

    name: str
    """Display name of the provider for UI/logging purposes"""

    model: str
    """Model identifier in format 'provider/model' (e.g. 'openai/gpt-4-1106-preview')"""

    provider: Literal["litellm", "llm"] | str = "litellm"  # noqa: PYI051
    """Provider type - which implementation to use"""

    temperature: float | None = None
    """Sampling temperature between 0 and 1 (higher means more random)"""

    max_tokens: int | None = None
    """Maximum number of tokens to generate"""

    top_p: float | None = None
    """Nucleus sampling parameter between 0 and 1"""

    tools: dict[str, dict[str, Any]] | list[str] | None = None
    """Available tools for function calling. Can be list of names or dict with settings"""

    tool_choice: Literal["none", "auto"] | str | None = None  # noqa: PYI051
    """How to handle tool selection - 'none', 'auto' or specific tool name"""

    max_image_size: int | None = None
    """Maximum image size in pixels for vision models"""

    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Provider-specific configuration options",
    )
    """Additional provider-specific configuration options and settings"""
    model_config = ConfigDict(frozen=True)

    @field_validator("tools", mode="before")
    @classmethod
    def convert_tools(cls, v: Any) -> dict[str, dict[str, Any]] | None:
        """Convert tool references to dictionary format."""
        if isinstance(v, list):
            return {tool: {} for tool in v}
        return v

    @model_validator(mode="after")
    def validate_model_format(self) -> LLMProviderConfig:
        """Validate that model follows provider/name format."""
        if "/" not in self.model:
            msg = f"Model {self.model} must be in format 'provider/model'"
            raise ValueError(msg)
        return self


class TaskSettings(BaseModel):
    """Settings for a task."""

    temperature: float | None = None
    """Temperature for this specific task, overrides provider default"""

    max_tokens: int | None = None
    """Maximum tokens to generate in the response"""

    top_p: float | None = None
    """Nucleus sampling parameter between 0 and 1"""

    tools: list[str] | None = None
    """Names of tools allowed for this task"""

    tool_choice: Literal["none", "auto"] | str | None = None  # noqa: PYI051
    """How to handle tool selection - 'none', 'auto' or specific tool name"""

    model_config = ConfigDict(frozen=True)


class BaseContext(BaseModel):
    """Base class for all context types."""

    context_type: ContextType = Field(...)
    description: str = ""
    processors: list[ProcessingStep] = Field(
        default_factory=list
    )  # Optional with empty default
    model_config = ConfigDict(frozen=True)


class PathContext(BaseContext):
    """Context loaded from a file or URL."""

    context_type: Literal["path"] = "path"
    path: str | os.PathLike[str]

    @model_validator(mode="after")
    def validate_path(self) -> PathContext:
        """Validate that the path is not empty."""
        if not self.path:
            msg = "Path cannot be empty"
            raise ValueError(msg)
        return self


class TextContext(BaseContext):
    """Raw text context."""

    context_type: Literal["text"] = "text"
    content: str

    @model_validator(mode="after")
    def validate_content(self) -> TextContext:
        """Validate that the content is not empty."""
        if not self.content:
            msg = "Content cannot be empty"
            raise ValueError(msg)
        return self


class CLIContext(BaseContext):
    """Context from CLI command execution."""

    context_type: Literal["cli"] = "cli"
    command: str | TypingSequence[str]
    shell: bool = False
    cwd: str | None = None
    timeout: float | None = None

    @model_validator(mode="after")
    def validate_command(self) -> CLIContext:
        """Validate command configuration."""
        if not self.command:
            msg = "Command cannot be empty"
            raise ValueError(msg)
        if (
            isinstance(self.command, list | tuple)
            and not self.shell
            and not all(isinstance(part, str) for part in self.command)
        ):
            msg = "When shell=False, all command parts must be strings"
            raise ValueError(msg)
        return self


class SourceContext(BaseContext):
    """Context from Python source code."""

    context_type: Literal["source"] = "source"
    import_path: str
    recursive: bool = False
    include_tests: bool = False

    @model_validator(mode="after")
    def validate_import_path(self) -> SourceContext:
        """Validate that the import path is properly formatted."""
        if not all(part.isidentifier() for part in self.import_path.split(".")):
            msg = f"Invalid import path: {self.import_path}"
            raise ValueError(msg)
        return self


class CallableContext(BaseContext):
    """Context from executing a Python callable."""

    context_type: Literal["callable"] = "callable"
    import_path: str
    keyword_args: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_import_path(self) -> CallableContext:
        """Validate that the import path is properly formatted."""
        if not all(part.isidentifier() for part in self.import_path.split(".")):
            msg = f"Invalid import path: {self.import_path}"
            raise ValueError(msg)
        return self


class ImageContext(BaseContext):
    """Context for image input."""

    context_type: Literal["image"] = "image"
    path: str  # Local path or URL
    alt_text: str | None = None

    model_config = ConfigDict(frozen=True)

    @model_validator(mode="before")
    @classmethod
    def validate_path(cls, data: dict[str, Any]) -> dict[str, Any]:
        """Validate that path is not empty."""
        if isinstance(data, dict) and not data.get("path"):
            msg = "Path cannot be empty for image context"
            raise ValueError(msg)
        return data


Context = (
    PathContext
    | TextContext
    | CLIContext
    | SourceContext
    | CallableContext
    | ImageContext
)


class TaskTemplate(BaseModel):
    """Template for a task."""

    provider: str
    """Provider or provider group name to use for this task"""

    context: str
    """Context or context group name for task input"""

    settings: TaskSettings | None = None
    """Optional task-specific settings that override provider defaults"""

    inherit_tools: bool | None = None
    """Whether to inherit tools configured for the provider"""

    tools: list[str] | None = None
    """Additional tools to make available for this task"""

    tool_choice: Literal["none", "auto"] | str | None = None  # noqa: PYI051
    """How to handle tool selection for this task"""

    model_config = ConfigDict(frozen=True)


class ToolConfig(BaseModel):
    """Configuration for a tool."""

    import_path: str
    """Import path to the tool implementation (e.g. 'mymodule.tools.MyTool')"""

    name: str | None = None
    """Optional override for the tool's display name"""

    description: str | None = None
    """Optional override for the tool's description"""

    model_config = ConfigDict(frozen=True)


class Config(BaseModel):
    """Root configuration model."""

    version: str = "1.0"
    global_settings: GlobalSettings = Field(default_factory=GlobalSettings)
    context_processors: dict[str, ProcessorConfig] = Field(default_factory=dict)
    llm_providers: dict[str, LLMProviderConfig]  # Required: at least one provider needed
    provider_groups: dict[str, list[str]] = Field(default_factory=dict)
    contexts: dict[str, Context]  # Required: at least one context needed
    context_groups: dict[str, list[str]] = Field(default_factory=dict)
    task_templates: dict[str, TaskTemplate]  # Required: at least one template needed
    tools: dict[str, ToolConfig] = Field(default_factory=dict)

    model_config = ConfigDict(
        frozen=True,
        arbitrary_types_allowed=True,
    )

    @model_validator(mode="after")
    def validate_references(self) -> Config:
        """Validate all references between components."""
        # Only validate if the optional components are present
        if self.provider_groups:
            self._validate_provider_groups()
        if self.context_groups:
            self._validate_context_groups()
        if self.context_processors:
            self._validate_processor_references()
        self._validate_task_templates()
        return self

    def _validate_provider_groups(self) -> None:
        """Validate provider references in groups."""
        for group, providers in self.provider_groups.items():
            for provider in providers:
                if provider not in self.llm_providers:
                    msg = f"Provider {provider} referenced in group {group} not found"
                    raise ValueError(msg)

    def _validate_context_groups(self) -> None:
        """Validate context references in groups."""
        for group, contexts in self.context_groups.items():
            for context in contexts:
                if context not in self.contexts:
                    msg = f"Context {context} referenced in group {group} not found"
                    raise ValueError(msg)

    def _validate_processor_references(self) -> None:
        """Validate processor references in contexts."""
        for context in self.contexts.values():
            for processor in context.processors:
                if processor.name not in self.context_processors:
                    msg = f"Processor {processor.name!r} not found"
                    raise ValueError(msg)

    def _validate_task_templates(self) -> None:
        """Validate task template references."""
        for name, template in self.task_templates.items():
            # Validate provider reference
            if (
                template.provider not in self.llm_providers
                and template.provider not in self.provider_groups
            ):
                msg = f"Provider {template.provider} referenced in task {name} not found"
                raise ValueError(msg)

            # Validate context reference
            if (
                template.context not in self.contexts
                and template.context not in self.context_groups
            ):
                msg = f"Context {template.context} referenced in task {name} not found"
                raise ValueError(msg)

    def model_dump_yaml(self) -> str:
        """Dump configuration to YAML string."""
        import yamling

        return yamling.dump_yaml(self.model_dump(exclude_none=True))


if __name__ == "__main__":
    from pydantic import ValidationError

    from llmling.config.loading import load_config

    try:
        config = load_config("src/llmling/resources/test.yml")  # type: ignore[has-type]
        print(config)
    except ValidationError as e:
        print(e)
