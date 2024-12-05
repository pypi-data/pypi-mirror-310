from __future__ import annotations

import pytest

from llmling.tools.base import DynamicTool, ToolRegistry
from llmling.tools.exceptions import ToolError


EXAMPLE_IMPORT = "llmling.testing.tools.example_tool"
FAILING_IMPORT = "llmling.testing.tools.failing_tool"
ANALYZE_IMPORT = "llmling.testing.tools.analyze_ast"


# Test fixtures
@pytest.fixture
def registry() -> ToolRegistry:
    """Create a fresh tool registry."""
    return ToolRegistry()


async def test_tool_registration_and_execution():
    """Test basic tool registration and execution flow."""
    registry = ToolRegistry()

    # Register a simple tool
    registry.register_path(import_path=EXAMPLE_IMPORT, name="test_tool")

    # Verify tool is registered
    assert "test_tool" in registry.list_tools()

    # Execute tool and verify result
    result = await registry.execute("test_tool", text="hello", repeat=2)
    assert result == "hellohello"


async def test_tool_registry_errors():
    """Test error handling in tool registry."""
    registry = ToolRegistry()

    # Test executing non-existent tool
    with pytest.raises(ToolError):
        await registry.execute("non_existent_tool")

    # Test duplicate registration
    registry.register_path(EXAMPLE_IMPORT, "test_tool")
    with pytest.raises(ToolError):
        registry.register_path(EXAMPLE_IMPORT, "test_tool")


async def test_tool_execution_with_invalid_params():
    """Test tool execution with invalid parameters."""
    registry = ToolRegistry()
    registry.register_path(EXAMPLE_IMPORT, "test_tool")

    # Test with missing required parameter and parameter with wrong type
    with pytest.raises(ValueError, match="Error executing"):  # noqa: PT012
        await registry.execute("test_tool")
        await registry.execute("test_tool", text=None)


async def test_failing_tool():
    """Test handling of a tool that raises an exception."""
    registry = ToolRegistry()
    registry.register_path(FAILING_IMPORT, "failing_tool")

    with pytest.raises(ValueError, match="failing"):
        await registry.execute("failing_tool", text="any input")


# Test DynamicTool
class TestDynamicTool:
    def test_init(self) -> None:
        """Test tool initialization."""
        tool = DynamicTool(import_path=EXAMPLE_IMPORT, name="name", description="desc")
        assert tool.name == "name"
        assert tool.description == "desc"
        assert tool.import_path == EXAMPLE_IMPORT

    def test_default_name(self) -> None:
        """Test default name from import path."""
        tool = DynamicTool(EXAMPLE_IMPORT)
        assert tool.name == "example_tool"

    def test_default_description(self) -> None:
        """Test default description from docstring."""
        tool = DynamicTool(EXAMPLE_IMPORT)
        assert "repeats text" in tool.description.lower()

    def test_schema_generation(self) -> None:
        """Test schema generation from function signature."""
        tool = DynamicTool(EXAMPLE_IMPORT)
        schema = tool.get_schema()

        assert schema.type == "function"
        assert schema.function["name"] == "example_tool"
        assert "text" in schema.function["parameters"]["properties"]
        assert "repeat" in schema.function["parameters"]["properties"]
        assert schema.function["parameters"]["required"] == ["text"]

    @pytest.mark.asyncio
    async def test_execution(self) -> None:
        """Test tool execution."""
        tool = DynamicTool(EXAMPLE_IMPORT)
        result = await tool.execute(text="test", repeat=2)
        assert result == "testtest"

    @pytest.mark.asyncio
    async def test_execution_failure(self) -> None:
        """Test tool execution failure."""
        tool = DynamicTool(FAILING_IMPORT)
        with pytest.raises(Exception, match="test"):
            await tool.execute(text="test")


# Test ToolRegistry
class TestToolRegistry:
    def test_register_path(self, registry: ToolRegistry) -> None:
        """Test registering a tool by import path."""
        registry.register_path(EXAMPLE_IMPORT, name="custom_tool")
        assert "custom_tool" in registry.list_tools()

    def test_register_duplicate(self, registry: ToolRegistry) -> None:
        """Test registering duplicate tool names."""
        registry.register_path(EXAMPLE_IMPORT, name="tool1")
        with pytest.raises(ToolError):
            registry.register_path(EXAMPLE_IMPORT, name="tool1")

    def test_get_nonexistent(self, registry: ToolRegistry) -> None:
        """Test getting non-existent tool."""
        with pytest.raises(ToolError):
            registry.get_tool("nonexistent")

    def test_list_tools(self, registry: ToolRegistry) -> None:
        """Test listing registered tools."""
        registry.register_path(EXAMPLE_IMPORT, name="tool1")
        registry.register_path(ANALYZE_IMPORT, name="tool2")
        tools = registry.list_tools()
        assert len(tools) == 2  # noqa: PLR2004
        assert "tool1" in tools
        assert "tool2" in tools

    @pytest.mark.asyncio
    async def test_execute(self, registry: ToolRegistry) -> None:
        """Test executing a registered tool."""
        registry.register_path(EXAMPLE_IMPORT)
        result = await registry.execute("example_tool", text="test", repeat=3)
        assert result == "testtesttest"

    @pytest.mark.asyncio
    async def test_execute_with_validation(self, registry: ToolRegistry) -> None:
        """Test tool execution with invalid parameters."""
        registry.register_path(ANALYZE_IMPORT)

        # Valid Python code
        code = "class Test: pass\ndef func(): pass"
        result = await registry.execute("analyze_ast", code=code)
        assert result["classes"] == 1
        assert result["functions"] == 1

        # Invalid Python code
        with pytest.raises(Exception, match="invalid syntax"):
            await registry.execute("analyze_ast", code="invalid python")

    def test_schema_generation(self, registry: ToolRegistry) -> None:
        """Test schema generation for registered tools."""
        registry.register_path(ANALYZE_IMPORT, description="desc")
        schema = registry.get_schema("analyze_ast")

        assert schema.type == "function"
        assert "code" in schema.function["parameters"]["properties"]
        assert schema.function["parameters"]["required"] == ["code"]
        assert schema.function["description"] == "desc"


# Integration tests
@pytest.mark.asyncio
async def test_tool_integration() -> None:
    """Test full tool workflow."""
    # Setup
    registry = ToolRegistry()
    registry.register_path(ANALYZE_IMPORT, name="analyze", description="Analyze AST")

    # Get schema
    schema = registry.get_schema("analyze")
    assert schema.type == "function"

    # Execute tool
    code = """
class TestClass:
    def method1(self):
        pass
    def method2(self):
        pass
    """
    result = await registry.execute("analyze", code=code)
    assert result["classes"] == code.count("class ")
    assert result["functions"] == code.count("def ")


if __name__ == "__main__":
    pytest.main(["-vv"])
