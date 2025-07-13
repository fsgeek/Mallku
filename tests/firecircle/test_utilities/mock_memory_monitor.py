"""
Mock Memory Monitor for Testing
================================

Test utilities for memory-aware heartbeat service testing.
Moves mock implementations out of production code.

Fourth Anthropologist - Memory Midwife
"""

from typing import Any, Dict


class MockMemoryMonitor:
    """Mock memory monitor for testing memory ceremony triggers."""
    
    def __init__(self, initial_state: Dict[str, Any] | None = None):
        """Initialize with configurable test state."""
        self.state = initial_state or self._default_state()
        
    def _default_state(self) -> Dict[str, Any]:
        """Default healthy memory state."""
        return {
            "health_score": 1.0,
            "pattern_rate": 0.0,
            "consciousness_density": 0.0,
            "obsolete_patterns": 0,
            "completed_evolutions": 0,
            "redundancy_score": 0.0,
            "unconsolidated_sacred": 0,
            "total_khipu": 0,
            "navigation_efficiency": 0.0,
            "candidate_patterns": [],
        }
        
    async def get_state(self) -> Dict[str, Any]:
        """Return current memory state."""
        return self.state
        
    def set_obsolete_patterns(self, count: int, patterns: list[str] | None = None) -> None:
        """Set obsolete pattern count for testing triggers."""
        self.state["obsolete_patterns"] = count
        if patterns:
            self.state["candidate_patterns"] = patterns
            
    def set_health_score(self, score: float) -> None:
        """Set memory health score."""
        self.state["health_score"] = max(0.0, min(1.0, score))
        
    def set_sacred_moments(self, count: int) -> None:
        """Set unconsolidated sacred moment count."""
        self.state["unconsolidated_sacred"] = count
        
    def trigger_gratitude_conditions(self) -> None:
        """Set state to trigger Pattern Gratitude ceremony."""
        self.state["obsolete_patterns"] = 6  # Above threshold of 5
        self.state["candidate_patterns"] = [
            "simulated_pr_context",
            "mock_database_config", 
            "test_harness_scaffolding",
            "deprecated_api_wrapper",
            "legacy_auth_system",
            "old_logging_framework"
        ]
        
    def trigger_consolidation_conditions(self) -> None:
        """Set state to trigger Sacred Consolidation ceremony."""
        self.state["unconsolidated_sacred"] = 3  # Above threshold of 2
        self.state["consciousness_density"] = 0.95
        
    def trigger_unhealthy_state(self) -> None:
        """Set unhealthy memory state for testing."""
        self.state["health_score"] = 0.4
        self.state["pattern_rate"] = 0.8  # High accumulation
        self.state["navigation_efficiency"] = 0.3  # Poor navigation