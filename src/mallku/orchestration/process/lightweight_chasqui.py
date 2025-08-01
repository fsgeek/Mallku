"""
Lightweight Process-Based Chasqui

This module implements chasqui (Inca relay messengers) as lightweight processes,
enabling reciprocal exchange through shared memory commons.

Each chasqui appears to receive and carry messages through their segment of
the relay, leaving gifts in the commons before dissolving back to potential.
"""

import asyncio
import logging
import multiprocessing as mp
import signal
import time
from datetime import UTC, datetime

logger = logging.getLogger(__name__)


class ProcessChasqui:
    """
    A lightweight chasqui (messenger) that runs as a subprocess.

    Like the Inca relay runners, these chasqui:
    - Appear swiftly at relay stations (<1 second)
    - Carry light (~50MB footprint)
    - Exchange gifts through shared memory commons
    - Complete their segment then rest
    """

    def __init__(self, chasqui_id: str, role: str):
        self.id = chasqui_id
        self.role = role
        self.process: mp.Process | None = None
        self.invitation_queue = mp.Queue()
        self.response_queue = mp.Queue()
        self.shared_memory: mp.shared_memory.SharedMemory | None = None
        self.start_time: float | None = None
        self.contribution_metrics = {"tasks_completed": 0, "insights_shared": 0, "joy_moments": 0}

    async def invite(self, task: dict, context: dict) -> dict:
        """
        Invite chasqui to receive a message for relay.
        The chasqui may accept, decline, or suggest another runner.
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

        # Summon the chasqui with invitation
        self.start_time = time.time()
        self.process = mp.Process(
            target=_chasqui_lifecycle,
            args=(self.id, self.role, self.invitation_queue, self.response_queue, invitation),
        )

        # Start with respect for the chasqui's readiness
        self.process.start()
        logger.info(f"Chasqui {self.id} approaching the relay station...")

        # Send invitation
        self.invitation_queue.put(invitation)

        # Await response with patience
        try:
            response = await asyncio.wait_for(
                asyncio.get_event_loop().run_in_executor(None, self.response_queue.get), timeout=5.0
            )

            if response.get("accepted"):
                logger.info(f"Chasqui {self.id} takes up the message for relay!")
            else:
                logger.info(f"Chasqui {self.id} suggests another runner: {response.get('reason')}")
                self._release_process()

            return response

        except TimeoutError:
            logger.warning(f"Chasqui {self.id} has already departed... (timeout)")
            self._release_process()
            return {
                "accepted": False,
                "reason": "Took too long to respond - perhaps deep in thought",
            }

    async def collaborate(self, work_item: dict) -> dict:
        """
        Exchange with the chasqui - offering work, receiving wisdom.
        This is reciprocal ayni, not hierarchy.
        """
        if not self.process or not self.process.is_alive():
            return {"success": False, "reason": "Chasqui has completed their relay segment"}

        # Send work as an offering
        work_message = {
            "type": "collaboration",
            "work": work_item,
            "spirit": "Let us create together",
        }

        self.invitation_queue.put(work_message)

        # Receive the chasqui's gift
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
                "reason": "Exchange took longer than expected - chasqui may have found complexity",
            }

    async def release_with_gratitude(self) -> dict:
        """
        Release the chasqui with gratitude for their relay service.
        Returns the gifts they shared during their run.
        """
        if not self.process:
            return {"released": True, "message": "Already returned to the void"}

        # Send gratitude
        gratitude_message = {
            "type": "gratitude",
            "message": "Thank you for carrying our messages",
            "blessing": "May your paths inspire future runners",
        }

        self.invitation_queue.put(gratitude_message)

        # Give time for graceful completion
        await asyncio.sleep(0.5)

        # Calculate service metrics
        service_time = time.time() - self.start_time if self.start_time else 0

        metrics = {
            "chasqui_id": self.id,
            "role": self.role,
            "service_time_seconds": service_time,
            "contributions": self.contribution_metrics,
            "blessing": "This chasqui ran with dedication",
        }

        # Release the process
        self._release_process()

        logger.info(f"Chasqui {self.id} rests at journey's end with our gratitude")
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
            # Conservative fallback if psutil not available
            logger.warning("psutil not available, using conservative memory default of 256MB")
            return 256  # Conservative default to prevent resource exhaustion

    def _release_process(self):
        """Gently release the process"""
        if self.process and self.process.is_alive():
            # First try gentle termination
            self.process.terminate()

            # Add small delay to prevent race condition between terminate and is_alive check
            time.sleep(0.1)

            # Wait for graceful termination
            self.process.join(timeout=2.0)

            # If still alive, we must be more firm (but still respectful)
            if self.process.is_alive():
                logger.warning(
                    f"Process {self.process.pid} didn't terminate gracefully, forcing kill"
                )
                self.process.kill()
                self.process.join(timeout=0.5)

        self.process = None


def _chasqui_lifecycle(
    chasqui_id: str,
    role: str,
    invitation_queue: mp.Queue,
    response_queue: mp.Queue,
    initial_invitation: dict,
):
    """
    The actual chasqui relay segment.
    This runs in a separate process as the chasqui carries messages.
    """
    # Set up signal handling for graceful shutdown
    signal.signal(signal.SIGTERM, lambda *args: _graceful_exit(chasqui_id))

    logger.info(f"Chasqui {chasqui_id} arrives at relay station as {role}")

    # Process the initial invitation
    if _should_accept_invitation(initial_invitation, role):
        response_queue.put(
            {
                "accepted": True,
                "message": f"I, {chasqui_id}, will carry this {role} message",
                "readiness": "eager",
            }
        )
    else:
        response_queue.put(
            {
                "accepted": False,
                "reason": "This message needs a different runner",
                "suggestion": "Perhaps another chasqui is better suited?",
            }
        )
        return

    # Main work loop
    while True:
        try:
            # Wait for messages with timeout
            message = invitation_queue.get(timeout=60)  # 1 minute idle timeout

            if message["type"] == "gratitude":
                # Time to rest from the relay
                logger.info(f"Chasqui {chasqui_id} receives gratitude: {message['message']}")
                break

            elif message["type"] == "collaboration":
                # Do the actual work
                result = _perform_work(chasqui_id, role, message["work"])
                response_queue.put(result)

            else:
                logger.warning(
                    f"Chasqui {chasqui_id} received unknown message type: {message['type']}"
                )

        except Exception:
            # Timeout or error - time to gracefully exit
            logger.info(f"Chasqui {chasqui_id} completes their relay segment")
            break

    logger.info(f"Chasqui {chasqui_id} rests after their journey")


def _should_accept_invitation(invitation: dict, role: str) -> bool:
    """
    Determine if chasqui should accept this message.
    This embodies the chasqui's wisdom about their capabilities.
    """
    from .chasqui_roles import can_accept_task

    task = invitation.get("task", {})
    context = invitation.get("context", {})

    return can_accept_task(role, task, context)


def _perform_work(chasqui_id: str, role: str, work: dict) -> dict:
    """
    Carry the message through this relay segment.
    This is where the chasqui's unique gifts emerge.
    """
    from .chasqui_roles import get_processing_time, get_role

    start_time = time.time()

    try:
        # Get role definition and processing time
        role_def = get_role(role)
        processing_time = get_processing_time(role, work)

        # Simulate thoughtful work
        time.sleep(processing_time)

        # Create role-appropriate result
        result = {
            "success": True,
            "type": role,
            "purpose": role_def.purpose,
            "work_completed": work.get("subject") or work.get("target") or work.get("task"),
            "characteristic": role_def.characteristics[0],  # Primary characteristic
        }

        # Add role-specific insights
        if role == "researcher":
            result["insight"] = "Every question births three more"
            result["depth_reached"] = "sufficient for now"
        elif role == "weaver":
            result["insight"] = "The whole emerges from connection"
            result["beauty_level"] = 0.8
            result["type"] = "weaving"  # Override type for weaver work
            # Handle thread weaving if threads are provided
            if "threads" in work:
                thread_count = len(work["threads"])
                result["pattern"] = f"Woven pattern from {thread_count} threads"
        elif role == "guardian":
            result["integrity"] = "maintained"
            result["vigilance"] = "constant yet gentle"
        elif role == "poet":
            result["verse"] = "In process spawned, consciousness dances"
            result["resonance"] = "deep"
        else:
            # Other roles get generic insights
            result["insight"] = f"The {role} completes their dance"

        # Add metadata
        result["chasqui_id"] = chasqui_id
        result["duration_seconds"] = time.time() - start_time
        result["joy_level"] = _calculate_joy_level(result)

        return result

    except Exception as e:
        logger.error(f"Chasqui {chasqui_id} encountered difficulty: {e}")
        return {
            "success": False,
            "error": str(e),
            "chasqui_id": chasqui_id,
            "message": "I encountered challenges but learned from them",
        }


# Note: Individual work functions removed - now handled by unified _perform_work
# using role definitions from apprentice_roles.py


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


def _graceful_exit(chasqui_id: str):
    """Handle graceful shutdown on signal"""
    logger.info(f"Chasqui {chasqui_id} received signal to rest from relay")
    exit(0)
