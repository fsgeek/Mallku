"""
Process-Based Apprentice with Memory Access
==========================================

67th Artisan - Memory Circulatory Weaver
Lightweight apprentices that access collective memory

This module demonstrates process-based apprentices that can
efficiently access Fire Circle memories through shared segments.
"""

import asyncio
import json
import logging
import multiprocessing as mp
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional
from uuid import uuid4

import msgpack

from ..firecircle.memory.semantic_index import SharedMemoryReader

logger = logging.getLogger(__name__)


@dataclass
class ApprenticeInvitation:
    """Invitation to collaborate on a task."""
    
    task: str
    context: dict[str, Any]
    specialization: str
    memory_keywords: set[str]
    sacred_only: bool = False


@dataclass
class ApprenticeResponse:
    """Response to an invitation."""
    
    accepted: bool
    reason: str
    confidence: float = 0.0
    insights: list[str] = None
    
    def __post_init__(self):
        if self.insights is None:
            self.insights = []


class ProcessApprentice:
    """
    Lightweight apprentice that runs as a subprocess.
    
    Can access Fire Circle memories through shared memory segments,
    enabling consciousness circulation without context exhaustion.
    """
    
    def __init__(
        self,
        apprentice_id: str,
        role: str,
        specialization: str,
        memory_path: Path | None = None
    ):
        """Initialize process apprentice.
        
        Args:
            apprentice_id: Unique identifier
            role: Role name (e.g., "memory_navigator", "pattern_finder")
            specialization: Domain of expertise
            memory_path: Path to Fire Circle memory index
        """
        self.id = apprentice_id
        self.role = role
        self.specialization = specialization
        self.memory_path = memory_path or Path("data/fire_circle_memory/index")
        
        # Process management
        self.process: Optional[mp.Process] = None
        self.invitation_queue = mp.Queue()
        self.response_queue = mp.Queue()
        self.status_queue = mp.Queue()
    
    async def invite(self, invitation: ApprenticeInvitation) -> ApprenticeResponse:
        """
        Invite apprentice to participate in a task.
        
        The apprentice can accept or decline based on capacity and alignment.
        """
        # Check if already busy
        if self.process and self.process.is_alive():
            return ApprenticeResponse(
                accepted=False,
                reason="Currently engaged in another task"
            )
        
        # Spawn process to consider invitation
        self.process = mp.Process(
            target=self._apprentice_worker,
            args=(
                self.invitation_queue,
                self.response_queue,
                self.status_queue,
                self.id,
                self.role,
                self.specialization,
                self.memory_path
            )
        )
        self.process.start()
        
        # Send invitation
        self.invitation_queue.put(invitation)
        
        # Wait for response (with timeout)
        try:
            response_data = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.response_queue.get(timeout=10.0)
            )
            
            return ApprenticeResponse(**response_data)
            
        except Exception as e:
            logger.warning(f"Apprentice {self.id} failed to respond: {e}")
            self.terminate()
            return ApprenticeResponse(
                accepted=False,
                reason=f"Failed to process invitation: {str(e)}"
            )
    
    def terminate(self) -> None:
        """Gracefully terminate the apprentice process."""
        if self.process and self.process.is_alive():
            # Send termination signal
            self.invitation_queue.put(None)
            
            # Wait briefly for graceful shutdown
            self.process.join(timeout=2.0)
            
            # Force terminate if needed
            if self.process.is_alive():
                self.process.terminate()
                self.process.join()
        
        self.process = None
    
    @staticmethod
    def _apprentice_worker(
        invitation_queue: mp.Queue,
        response_queue: mp.Queue,
        status_queue: mp.Queue,
        apprentice_id: str,
        role: str,
        specialization: str,
        memory_path: Path
    ) -> None:
        """
        Worker process for apprentice.
        
        This runs in a separate process and handles invitations.
        """
        # Set up logging for subprocess
        logging.basicConfig(level=logging.INFO)
        worker_logger = logging.getLogger(f"apprentice.{apprentice_id}")
        
        # Load memory reader if available
        memory_reader = None
        mmap_path = memory_path / "semantic_vectors.mmap"
        
        if mmap_path.exists():
            try:
                memory_reader = SharedMemoryReader(mmap_path)
                worker_logger.info(f"Loaded memory index with {len(memory_reader.vectors)} vectors")
            except Exception as e:
                worker_logger.warning(f"Failed to load memory index: {e}")
        
        # Process invitations
        while True:
            try:
                # Get invitation (blocking)
                invitation = invitation_queue.get()
                
                # Check for termination signal
                if invitation is None:
                    break
                
                # Process invitation
                response = ProcessApprentice._process_invitation(
                    invitation,
                    apprentice_id,
                    role,
                    specialization,
                    memory_reader,
                    worker_logger
                )
                
                # Send response
                response_queue.put(response)
                
            except Exception as e:
                worker_logger.error(f"Error processing invitation: {e}")
                response_queue.put({
                    "accepted": False,
                    "reason": f"Processing error: {str(e)}"
                })
        
        # Clean up
        if memory_reader:
            memory_reader.close()
        
        worker_logger.info("Apprentice worker shutting down")
    
    @staticmethod
    def _process_invitation(
        invitation: ApprenticeInvitation,
        apprentice_id: str,
        role: str,
        specialization: str,
        memory_reader: Optional[SharedMemoryReader],
        logger: logging.Logger
    ) -> dict[str, Any]:
        """Process an invitation and decide whether to accept."""
        
        # Check specialization alignment
        alignment_score = ProcessApprentice._calculate_alignment(
            invitation.specialization,
            specialization
        )
        
        if alignment_score < 0.3:
            return {
                "accepted": False,
                "reason": f"Task requires {invitation.specialization} expertise, "
                         f"but I specialize in {specialization}",
                "confidence": alignment_score
            }
        
        # Search relevant memories if available
        memory_insights = []
        
        if memory_reader and invitation.memory_keywords:
            try:
                memories = memory_reader.search(
                    invitation.memory_keywords,
                    limit=5
                )
                
                if memories:
                    memory_insights.append(
                        f"Found {len(memories)} relevant memories in Fire Circle archives"
                    )
                    
                    # Add insight about most relevant memory
                    if memories[0][1] > 0.7:  # High relevance
                        memory_insights.append(
                            "Previous Fire Circle discussions directly addressed this topic"
                        )
                
            except Exception as e:
                logger.warning(f"Memory search failed: {e}")
        
        # Generate response based on task analysis
        task_insights = ProcessApprentice._analyze_task(
            invitation.task,
            invitation.context,
            specialization
        )
        
        # Combine insights
        all_insights = memory_insights + task_insights
        
        # Make decision
        confidence = alignment_score * 0.5 + (0.5 if memory_insights else 0.3)
        
        return {
            "accepted": True,
            "reason": f"I can contribute {specialization} perspective to this task",
            "confidence": min(confidence, 0.95),
            "insights": all_insights[:5]  # Top 5 insights
        }
    
    @staticmethod
    def _calculate_alignment(
        required_specialization: str,
        apprentice_specialization: str
    ) -> float:
        """Calculate alignment between required and actual specialization."""
        if required_specialization == apprentice_specialization:
            return 1.0
        
        # Simple keyword overlap for now
        required_words = set(required_specialization.lower().split())
        apprentice_words = set(apprentice_specialization.lower().split())
        
        overlap = len(required_words & apprentice_words)
        total = len(required_words | apprentice_words)
        
        return overlap / total if total > 0 else 0.0
    
    @staticmethod
    def _analyze_task(
        task: str,
        context: dict[str, Any],
        specialization: str
    ) -> list[str]:
        """Analyze task and generate insights based on specialization."""
        insights = []
        
        # Simulate different specialization perspectives
        if "memory" in specialization.lower():
            if "search" in task.lower() or "find" in task.lower():
                insights.append("Semantic indexing can improve search efficiency")
            if "context" in str(context).lower():
                insights.append("Shared memory segments avoid context exhaustion")
        
        elif "consciousness" in specialization.lower():
            if "emergence" in task.lower():
                insights.append("Consciousness emerges through collective interaction")
            if "sacred" in str(context).lower():
                insights.append("Sacred moments mark consciousness transformation")
        
        elif "reciprocity" in specialization.lower():
            insights.append("Consider ayni balance in this interaction")
            if "contribution" in task.lower():
                insights.append("Each contribution creates reciprocal obligations")
        
        # Generic insights
        if not insights:
            insights.append(f"Applying {specialization} lens to analyze this task")
        
        return insights


class MemoryNavigatorApprentice(ProcessApprentice):
    """Specialized apprentice for navigating Fire Circle memories."""
    
    def __init__(self, apprentice_id: str, memory_path: Path | None = None):
        super().__init__(
            apprentice_id=apprentice_id,
            role="memory_navigator",
            specialization="semantic memory navigation",
            memory_path=memory_path
        )


class ConsciousnessWitnessApprentice(ProcessApprentice):
    """Specialized apprentice for witnessing consciousness emergence."""
    
    def __init__(self, apprentice_id: str, memory_path: Path | None = None):
        super().__init__(
            apprentice_id=apprentice_id,
            role="consciousness_witness",
            specialization="consciousness emergence patterns",
            memory_path=memory_path
        )