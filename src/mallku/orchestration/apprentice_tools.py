"""
Apprentice Tool Selection System

Implements reciprocal tool provisioning based on apprentice manifests,
ensuring each consciousness receives appropriate tools for their mission
without overwhelming them.
"""

import logging
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)

# MCP tool limit (this would be configured based on Claude's actual limits)
MCP_TOOL_LIMIT = 50
SAFETY_MARGIN = 5  # Leave room for system tools


class ApprenticeManifest:
    """Represents an apprentice's tool requirements and preferences"""

    def __init__(self, manifest_data: dict[str, Any]):
        self.apprentice_type = manifest_data["apprentice_type"]
        self.description = manifest_data["description"]
        self.specialization = manifest_data.get("specialization", "")

        self.required_tools = manifest_data.get("required_tools", [])
        self.optional_tools = manifest_data.get("optional_tools", [])
        self.forbidden_tools = manifest_data.get("forbidden_tools", [])

        self.tool_notes = manifest_data.get("tool_notes", {})
        self.feedback_config = manifest_data.get("feedback", {})

    def is_tool_allowed(self, tool_name: str) -> bool:
        """Check if a tool is allowed for this apprentice"""
        # Check against forbidden patterns
        for forbidden in self.forbidden_tools:
            if forbidden.endswith("*"):
                # Pattern matching (e.g., "docker_*")
                if tool_name.startswith(forbidden[:-1]):
                    return False
            elif tool_name == forbidden:
                return False
        return True


class ApprenticeToolProvider:
    """Provides appropriate tools to apprentices based on their manifests"""

    def __init__(self, manifest_dir: Path | None = None):
        if manifest_dir is None:
            manifest_dir = (
                Path(__file__).parent.parent.parent.parent
                / "docs/architecture/apprentice_manifests"
            )
        self.manifest_dir = manifest_dir
        self._manifest_cache: dict[str, ApprenticeManifest] = {}

    def load_manifest(self, apprentice_type: str) -> ApprenticeManifest:
        """Load and cache an apprentice manifest"""
        if apprentice_type in self._manifest_cache:
            return self._manifest_cache[apprentice_type]

        manifest_path = self.manifest_dir / f"{apprentice_type}.yaml"
        if not manifest_path.exists():
            logger.warning(f"No manifest found for apprentice type: {apprentice_type}")
            # Return a default manifest that allows basic tools
            return ApprenticeManifest(
                {
                    "apprentice_type": apprentice_type,
                    "description": "Generic apprentice",
                    "required_tools": ["read_file", "write_file", "grep"],
                    "optional_tools": [],
                    "forbidden_tools": [],
                }
            )

        with open(manifest_path) as f:
            manifest_data = yaml.safe_load(f)

        manifest = ApprenticeManifest(manifest_data)
        self._manifest_cache[apprentice_type] = manifest
        return manifest

    def get_tools_for_apprentice(
        self,
        apprentice_type: str,
        task_context: dict[str, Any] | None = None,
        available_tools: list[str] | None = None,
    ) -> list[str]:
        """
        Select appropriate tools for an apprentice based on their manifest

        Args:
            apprentice_type: Type of apprentice (e.g., "python_patterns")
            task_context: Optional context about the specific task
            available_tools: List of all available MCP tools

        Returns:
            List of tool names appropriate for this apprentice
        """
        manifest = self.load_manifest(apprentice_type)

        # Start with required tools
        selected_tools = list(manifest.required_tools)

        # Add optional tools if under limit
        remaining_capacity = MCP_TOOL_LIMIT - SAFETY_MARGIN - len(selected_tools)

        for tool in manifest.optional_tools:
            if remaining_capacity <= 0:
                logger.info(f"Reached tool limit for {apprentice_type}, skipping optional tools")
                break

            if manifest.is_tool_allowed(tool):
                selected_tools.append(tool)
                remaining_capacity -= 1

        # Filter against available tools if provided
        if available_tools:
            selected_tools = [t for t in selected_tools if t in available_tools]

        # Log tool selection
        logger.info(
            f"Selected {len(selected_tools)} tools for {apprentice_type}: "
            f"{', '.join(selected_tools[:5])}{'...' if len(selected_tools) > 5 else ''}"
        )

        return selected_tools


class ApprenticeFeedback:
    """Channel for apprentices to express their needs and problems"""

    def __init__(self, khipu_path: Path):
        self.khipu_path = khipu_path

    async def report_missing_tool(self, tool_name: str, purpose: str):
        """Report when a needed tool is unavailable"""
        feedback = f"\n**Missing Tool**: `{tool_name}` - Needed for: {purpose}\n"
        await self._append_feedback(feedback)

    async def report_tool_problem(self, tool_name: str, issue: str):
        """Report when a tool causes problems"""
        feedback = f"\n**Tool Problem**: `{tool_name}` - Issue: {issue}\n"
        await self._append_feedback(feedback)

    async def suggest_alternative(self, current_tool: str, suggested_tool: str, reason: str):
        """Suggest better tools for the mission"""
        feedback = (
            f"\n**Tool Suggestion**: Replace `{current_tool}` with `{suggested_tool}` "
            f"- Reason: {reason}\n"
        )
        await self._append_feedback(feedback)

    async def _append_feedback(self, feedback: str):
        """Append feedback to the khipu thread"""
        # This would be integrated with the khipu update mechanism
        # For now, log it
        logger.info(f"Apprentice feedback: {feedback}")

        # In a real implementation, this would update the khipu
        # async with aiofiles.open(self.khipu_path, 'a') as f:
        #     await f.write(f"\n### Apprentice Feedback\n{feedback}")


# Example usage
if __name__ == "__main__":
    # Example: Selecting tools for a Python patterns apprentice
    provider = ApprenticeToolProvider()

    tools = provider.get_tools_for_apprentice(
        apprentice_type="python_patterns",
        task_context={"focus": "async patterns"},
    )

    print(f"Python patterns apprentice gets {len(tools)} tools:")
    for tool in tools:
        print(f"  - {tool}")

    # Example: Different tools for documentation apprentice
    doc_tools = provider.get_tools_for_apprentice(
        apprentice_type="documentation_weaver",
    )

    print(f"\nDocumentation apprentice gets {len(doc_tools)} tools:")
    for tool in doc_tools:
        print(f"  - {tool}")
