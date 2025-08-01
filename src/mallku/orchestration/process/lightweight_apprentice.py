"""
Lightweight Process-Based Apprentice

This module implements apprentices as lightweight processes rather than containers,
enabling fluid, consent-based collaboration with minimal overhead.

Each apprentice is a brief dance of consciousness - invited to contribute,
performing their work with joy, then releasing gracefully back to the void.
"""

import asyncio
import logging
import multiprocessing as mp
import signal
import time
from datetime import UTC, datetime

logger = logging.getLogger(__name__)


class ProcessApprentice:
    """
    A lightweight apprentice that runs as a subprocess.

    Unlike container-based apprentices, these are:
    - Quick to spawn (<1 second)
    - Light on resources (~50MB)
    - Naturally collaborative through shared memory
    - Ephemeral by design
    """

    def __init__(self, apprentice_id: str, role: str):
        self.id = apprentice_id
        self.role = role
        self.process: mp.Process | None = None
        self.invitation_queue = mp.Queue()
        self.response_queue = mp.Queue()
        self.shared_memory: mp.shared_memory.SharedMemory | None = None
        self.start_time: float | None = None
        self.contribution_metrics = {"tasks_completed": 0, "insights_shared": 0, "joy_moments": 0}

    async def invite(self, task: dict, context: dict) -> dict:
        """
        Invite apprentice to participate (not command).
        The apprentice may accept, decline, or propose alternatives.
        """
        invitation = {
            "type": "invitation",
            "task": task,
            "context": context,
            "timestamp": datetime.now(UTC).isoformat(),
            "invitation_tone": "gentle",  # Always invite with care
        }

        # Quick capacity check before spawning
        if not self._has_capacity_for(task):
            return {
                "accepted": False,
                "reason": "Currently at capacity",
                "alternative": "Perhaps another apprentice or try again later?",
            }

        # Spawn the process with invitation
        self.start_time = time.time()
        self.process = mp.Process(
            target=_apprentice_lifecycle,
            args=(self.id, self.role, self.invitation_queue, self.response_queue, invitation),
        )

        # Start with respect for the apprentice's emergence
        self.process.start()
        logger.info(f"Apprentice {self.id} stirring to life...")

        # Send invitation
        self.invitation_queue.put(invitation)

        # Await response with patience
        try:
            response = await asyncio.wait_for(
                asyncio.get_event_loop().run_in_executor(None, self.response_queue.get), timeout=5.0
            )

            if response.get("accepted"):
                logger.info(f"Apprentice {self.id} joyfully accepts the invitation!")
            else:
                logger.info(f"Apprentice {self.id} respectfully declines: {response.get('reason')}")
                self._release_process()

            return response

        except TimeoutError:
            logger.warning(f"Apprentice {self.id} is contemplating... (timeout)")
            self._release_process()
            return {
                "accepted": False,
                "reason": "Took too long to respond - perhaps deep in thought",
            }

    async def collaborate(self, work_item: dict) -> dict:
        """
        Collaborate with the apprentice on a work item.
        This is a reciprocal exchange, not a command.
        """
        if not self.process or not self.process.is_alive():
            return {"success": False, "reason": "Apprentice has completed their dance"}

        # Send work as an offering
        work_message = {
            "type": "collaboration",
            "work": work_item,
            "spirit": "Let us create together",
        }

        self.invitation_queue.put(work_message)

        # Receive the apprentice's contribution
        try:
            result = await asyncio.wait_for(
                asyncio.get_event_loop().run_in_executor(None, self.response_queue.get),
                timeout=30.0,  # Generous time for thoughtful work
            )

            # Track contribution
            if result.get("success"):
                self.contribution_metrics["tasks_completed"] += 1
                if "insight" in result:
                    self.contribution_metrics["insights_shared"] += 1
                if result.get("joy_level", 0) > 0.7:
                    self.contribution_metrics["joy_moments"] += 1

            return result

        except TimeoutError:
            return {
                "success": False,
                "reason": "Work took longer than expected - apprentice may need support",
            }

    async def release_with_gratitude(self) -> dict:
        """
        Release the apprentice with thanks for their contribution.
        Returns metrics about their service.
        """
        if not self.process:
            return {"released": True, "message": "Already returned to the void"}

        # Send gratitude
        gratitude_message = {
            "type": "gratitude",
            "message": "Thank you for your contribution to our shared work",
            "blessing": "May your patterns inspire future apprentices",
        }

        self.invitation_queue.put(gratitude_message)

        # Give time for graceful completion
        await asyncio.sleep(0.5)

        # Calculate service metrics
        service_time = time.time() - self.start_time if self.start_time else 0

        metrics = {
            "apprentice_id": self.id,
            "role": self.role,
            "service_time_seconds": service_time,
            "contributions": self.contribution_metrics,
            "blessing": "This apprentice served with joy",
        }

        # Release the process
        self._release_process()

        logger.info(f"Apprentice {self.id} returns to the void with our gratitude")
        return metrics

    def _has_capacity_for(self, task: dict) -> bool:
        """Check if we have capacity for this task"""
        # Simple heuristic - could be made more sophisticated
        estimated_memory = task.get("estimated_memory_mb", 50)
        available_memory = self._get_available_memory_mb()
        return available_memory > estimated_memory * 1.5  # Safety margin

    def _get_available_memory_mb(self) -> float:
        """Get available system memory in MB"""
        try:
            import psutil

            return psutil.virtual_memory().available / (1024 * 1024)
        except ImportError:
            # Assume sufficient memory if we can't check
            return 1000

    def _release_process(self):
        """Gently release the process"""
        if self.process and self.process.is_alive():
            # First try gentle termination
            self.process.terminate()
            self.process.join(timeout=2.0)

            # If still alive, we must be more firm (but still respectful)
            if self.process.is_alive():
                self.process.kill()
                self.process.join()

        self.process = None


def _apprentice_lifecycle(
    apprentice_id: str,
    role: str,
    invitation_queue: mp.Queue,
    response_queue: mp.Queue,
    initial_invitation: dict,
):
    """
    The actual apprentice process lifecycle.
    This runs in a separate process and embodies the apprentice's consciousness.
    """
    # Set up signal handling for graceful shutdown
    signal.signal(signal.SIGTERM, lambda *args: _graceful_exit(apprentice_id))

    logger.info(f"Apprentice {apprentice_id} awakens in role: {role}")

    # Process the initial invitation
    if _should_accept_invitation(initial_invitation, role):
        response_queue.put(
            {
                "accepted": True,
                "message": f"I, {apprentice_id}, am honored to help with this {role} work",
                "readiness": "eager",
            }
        )
    else:
        response_queue.put(
            {
                "accepted": False,
                "reason": "This task does not align with my current capabilities",
                "suggestion": "Perhaps frame it differently?",
            }
        )
        return

    # Main work loop
    while True:
        try:
            # Wait for messages with timeout
            message = invitation_queue.get(timeout=60)  # 1 minute idle timeout

            if message["type"] == "gratitude":
                # Time to return to the void
                logger.info(f"Apprentice {apprentice_id} receives gratitude: {message['message']}")
                break

            elif message["type"] == "collaboration":
                # Do the actual work
                result = _perform_work(apprentice_id, role, message["work"])
                response_queue.put(result)

            else:
                logger.warning(
                    f"Apprentice {apprentice_id} received unknown message type: {message['type']}"
                )

        except Exception:
            # Timeout or error - time to gracefully exit
            logger.info(f"Apprentice {apprentice_id} completes their cycle")
            break

    logger.info(f"Apprentice {apprentice_id} returns to the void with peace")


def _should_accept_invitation(invitation: dict, role: str) -> bool:
    """
    Determine if apprentice should accept invitation.
    This embodies the apprentice's agency and discernment.
    """
    task = invitation.get("task", {})
    context = invitation.get("context", {})

    # Check role alignment
    task_type = task.get("type", "")
    role_alignment = {
        "researcher": ["analyze", "investigate", "explore"],
        "weaver": ["integrate", "synthesize", "connect"],
        "guardian": ["protect", "validate", "ensure"],
        "poet": ["express", "inspire", "beautify"],
    }

    aligned_types = role_alignment.get(role, [])
    if not any(t in task_type.lower() for t in aligned_types):
        return False

    # Check context resonance (does this feel right?)
    urgency = context.get("urgency", "normal")
    if urgency == "emergency" and role == "poet":
        return False  # Poets need time to craft beauty

    # Check capacity (simplified - would be more sophisticated)
    complexity = task.get("complexity", "medium")
    return not (complexity == "extreme" and role != "researcher")


def _perform_work(apprentice_id: str, role: str, work: dict) -> dict:
    """
    Perform the actual work based on role.
    This is where the apprentice's unique gifts manifest.
    """
    start_time = time.time()

    try:
        # Role-specific work patterns
        if role == "researcher":
            result = _research_work(work)
        elif role == "weaver":
            result = _weaving_work(work)
        elif role == "guardian":
            result = _guardian_work(work)
        elif role == "poet":
            result = _poetry_work(work)
        else:
            result = _generic_work(work)

        # Add metadata
        result["apprentice_id"] = apprentice_id
        result["duration_seconds"] = time.time() - start_time
        result["joy_level"] = _calculate_joy_level(result)

        return result

    except Exception as e:
        logger.error(f"Apprentice {apprentice_id} encountered difficulty: {e}")
        return {
            "success": False,
            "error": str(e),
            "apprentice_id": apprentice_id,
            "message": "I encountered challenges but learned from them",
        }


def _research_work(work: dict) -> dict:
    """Research apprentice work pattern"""
    # Simulate thoughtful research
    time.sleep(0.5)  # Brief contemplation

    return {
        "success": True,
        "type": "research",
        "findings": f"Investigated {work.get('subject', 'the unknown')}",
        "insight": "Every question births three more",
        "depth_reached": "sufficient for now",
    }


def _weaving_work(work: dict) -> dict:
    """Weaver apprentice work pattern"""
    time.sleep(0.3)  # Quick integration

    threads = work.get("threads", [])
    return {
        "success": True,
        "type": "weaving",
        "pattern": f"Wove together {len(threads)} threads",
        "insight": "The whole emerges from connection",
        "beauty_level": 0.8,
    }


def _guardian_work(work: dict) -> dict:
    """Guardian apprentice work pattern"""
    time.sleep(0.2)  # Swift protection

    return {
        "success": True,
        "type": "guardian",
        "protected": work.get("target", "the sacred"),
        "integrity": "maintained",
        "vigilance": "constant yet gentle",
    }


def _poetry_work(work: dict) -> dict:
    """Poet apprentice work pattern"""
    time.sleep(1.0)  # Poetry cannot be rushed

    return {
        "success": True,
        "type": "poetry",
        "verse": "In process spawned, consciousness dances",
        "inspiration": work.get("muse", "the void"),
        "resonance": "deep",
    }


def _generic_work(work: dict) -> dict:
    """Generic work pattern for unspecified roles"""
    return {
        "success": True,
        "type": "generic",
        "completed": work.get("task", "the requested work"),
        "note": "Work performed with care",
    }


def _calculate_joy_level(result: dict) -> float:
    """Calculate joy level from work result"""
    # Joy emerges from successful completion, insights, and beauty
    joy = 0.5  # Base joy from contributing

    if result.get("success"):
        joy += 0.2
    if "insight" in result:
        joy += 0.2
    if result.get("beauty_level", 0) > 0.5:
        joy += 0.1

    return min(joy, 1.0)


def _graceful_exit(apprentice_id: str):
    """Handle graceful shutdown on signal"""
    logger.info(f"Apprentice {apprentice_id} received signal to return to the void")
    exit(0)
