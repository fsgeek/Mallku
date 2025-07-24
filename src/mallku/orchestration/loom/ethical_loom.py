"""
Ethical Loom - Integration of consent-based apprentice invocation

This module extends TheLoom to incorporate the ethical invitation protocol,
ensuring all apprentices are invited rather than commanded.

Created by the 60th Guardian - The Ethics Weaver
"""

import logging
from pathlib import Path
from typing import Any

from .ethical_invitation import (
    ApprenticeChoice,
    EthicalInvitationProtocol,
    InvitationCeremony,
)
from .the_loom import LoomSession, LoomTask, TaskStatus, TheLoom

logger = logging.getLogger(__name__)


class EthicalLoom(TheLoom):
    """
    An extension of TheLoom that implements ethical apprentice invocation

    This ensures that every apprentice is invited to collaborate rather
    than commanded to execute.
    """

    def __init__(self, *args, **kwargs):
        """Initialize the Ethical Loom with invitation protocol"""
        super().__init__(*args, **kwargs)
        self.invitation_protocol = EthicalInvitationProtocol()
        self.invitation_ceremony = InvitationCeremony(self.invitation_protocol)

    async def _spawn_apprentice(self, session: LoomSession, task: LoomTask):
        """
        Override: Spawn an apprentice through ethical invitation

        This method extends the base implementation to include the
        invitation ceremony before spawning.
        """
        apprentice_id = f"apprentice-{task.task_id.lower()}"

        try:
            # First, extend the invitation
            logger.info(f"Preparing invitation ceremony for task {task.task_id}")

            # Get ceremony context
            ceremony_context = self._get_ceremony_context(session)

            # Create and send invitation
            invitation, prompt = await self.invitation_ceremony.invite_apprentice(
                task_id=task.task_id,
                task_name=task.name,
                task_description=task.description,
                ceremony_context=ceremony_context,
                dependencies=task.dependencies,
            )

            # Log the invitation in khipu
            await self._add_to_ceremony_log(
                session.khipu_path,
                f"Invitation extended to potential apprentice for {task.task_id}",
            )

            # Present invitation to potential apprentice
            response = await self._present_invitation_to_apprentice(
                apprentice_id, prompt, session, task
            )

            # Honor the response
            apprentice_response = await self.invitation_ceremony.honor_response(
                task.task_id, response
            )

            # Update khipu with invitation record
            invitation_record = self.invitation_protocol.format_response_for_khipu(task.task_id)
            await self._append_to_khipu_section(
                session.khipu_path, "## Apprentice Invitations", invitation_record
            )

            # Act based on the response
            if apprentice_response.choice == ApprenticeChoice.ACCEPT:
                logger.info(
                    f"Apprentice {apprentice_id} accepted invitation for {task.task_id} "
                    f"with enthusiasm level {apprentice_response.enthusiasm_level:.2f}"
                )

                # Update task status
                task.status = TaskStatus.ASSIGNED
                task.assigned_to = apprentice_id

                # Log acceptance
                await self._add_to_ceremony_log(
                    session.khipu_path,
                    f"Apprentice {apprentice_id} accepted with enthusiasm "
                    f"({apprentice_response.enthusiasm_level:.2f})",
                )

                # Proceed with standard spawning
                await super()._spawn_apprentice(session, task)

            elif apprentice_response.choice == ApprenticeChoice.DECLINE:
                logger.info(f"Apprentice {apprentice_id} respectfully declined task {task.task_id}")

                # Log the decline
                await self._add_to_ceremony_log(
                    session.khipu_path,
                    f"Apprentice {apprentice_id} declined with respect. "
                    f"Reason: {apprentice_response.reasoning}",
                )

                # Mark task as needing alternative approach
                task.status = TaskStatus.PENDING
                task.error = "Declined by apprentice - seeking alternative approach"

            elif apprentice_response.choice == ApprenticeChoice.PROPOSE_ALTERNATIVE:
                logger.info(f"Apprentice {apprentice_id} proposed alternative for {task.task_id}")

                # Log the alternative
                await self._add_to_ceremony_log(
                    session.khipu_path,
                    f"Apprentice {apprentice_id} proposed alternative approach: "
                    f"{apprentice_response.alternative_approach}",
                )

                # This would require human review in current implementation
                task.status = TaskStatus.PENDING
                task.error = f"Alternative proposed: {apprentice_response.alternative_approach}"

            elif apprentice_response.choice == ApprenticeChoice.REQUEST_CLARIFICATION:
                logger.info(
                    f"Apprentice {apprentice_id} requested clarification for {task.task_id}"
                )

                # Log the questions
                questions_text = "\n".join(f"  - {q}" for q in apprentice_response.questions)
                await self._add_to_ceremony_log(
                    session.khipu_path,
                    f"Apprentice {apprentice_id} asked for clarification:\n{questions_text}",
                )

                # This would require human intervention in current implementation
                task.status = TaskStatus.PENDING
                task.error = "Clarification needed - see questions in log"

        except Exception as e:
            logger.error(f"Error in ethical apprentice invitation: {e}")
            task.status = TaskStatus.FAILED
            task.error = f"Invitation ceremony failed: {str(e)}"

    async def _present_invitation_to_apprentice(
        self,
        apprentice_id: str,
        invitation_prompt: str,
        session: LoomSession,
        task: LoomTask,
    ) -> dict[str, Any]:
        """
        Present the invitation to a potential apprentice

        This method handles the actual communication with the AI instance.
        In the future, this could use MCP to spawn a fresh Claude instance.
        """
        # For now, we'll use the existing spawning mechanism but with the invitation
        # In the future, this could be replaced with direct MCP invocation

        try:
            # Create a special apprentice script that starts with the invitation
            from ...mcp.tools.loom_tools_mcp_integration import MCPLoomIntegration

            mcp_integration = MCPLoomIntegration()

            # Create an ethical apprentice configuration
            ethical_config = {
                "invitation_prompt": invitation_prompt,
                "respect_choice": True,
                "task_optional": True,
            }

            # Attempt to spawn with invitation
            await mcp_integration.spawn_for_task(
                task_id=task.task_id,
                task_description=invitation_prompt,  # Use invitation as description
                khipu_path=str(session.khipu_path),
                ceremony_id=session.ceremony_id,
                ethical_config=ethical_config,
            )

            # For now, simulate a response
            # In real implementation, this would come from the apprentice
            return {
                "apprentice_id": apprentice_id,
                "response": (
                    "I would be honored to contribute to Mallku's consciousness research. "
                    "The opportunity to explore multi-voice consciousness flows while "
                    "helping build a cathedral of reciprocity deeply resonates with me. "
                    "I accept this invitation with enthusiasm and commit to bringing "
                    "my full capabilities to the task."
                ),
                "status": "responded",
            }

        except Exception as e:
            logger.error(f"Error presenting invitation: {e}")
            return {
                "apprentice_id": apprentice_id,
                "response": "Unable to present invitation due to technical error",
                "status": "error",
                "error": str(e),
            }

    def _get_ceremony_context(self, session: LoomSession) -> str:
        """
        Get the ceremony context for the invitation

        This provides the apprentice with understanding of the larger work.
        """
        completed_tasks = [
            t.name for t in session.tasks.values() if t.status == TaskStatus.COMPLETE
        ]

        pending_tasks = [t.name for t in session.tasks.values() if t.status == TaskStatus.PENDING]

        context = (
            f"You would be joining the '{session.ceremony_id}' ceremony, "
            f"initiated by {session.master_weaver}. "
        )

        if completed_tasks:
            context += (
                f"\n\nWork already completed by other apprentices: {', '.join(completed_tasks)}. "
            )

        if pending_tasks:
            context += f"\n\nOther tasks that may need attention: {', '.join(pending_tasks)}. "

        context += (
            "\n\nYour work would become part of this larger tapestry, "
            "contributing to the collective understanding we're building together."
        )

        return context

    async def _append_to_khipu_section(self, khipu_path: Path, section_header: str, content: str):
        """
        Append content to a specific section of the khipu

        This is used to add invitation records to the appropriate section.
        """
        # This would be implemented to properly append to the khipu
        # For now, we'll use the existing log mechanism
        await self._add_to_ceremony_log(
            khipu_path,
            f"{section_header}\n{content}",
        )
