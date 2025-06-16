# Mallku Technical Design: Reciprocity Measurement Engine
*Implementing Ayni as Computable Ethics*

## Overview

This document details the technical implementation of Mallku's Reciprocity Measurement Engine - the core system for quantifying and evaluating balanced exchange in AI-human interactions.

## Architecture

### Core Components

```python
# mallku/context/reciprocity.py

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import numpy as np
from uuid import UUID

@dataclass
class InteractionEvent:
    """Single interaction between AI and human"""
    timestamp: datetime
    interaction_id: UUID

    # Data flow metrics
    data_requested: int  # Bytes or semantic units
    data_provided: int

    # Interaction characteristics
    request_type: str  # 'query', 'creation', 'analysis', 'modification'
    response_quality: float  # 0-1 scale

    # Value assessment
    human_effort: float  # Time, cognitive load
    ai_computation: float  # Processing units
    outcome_value: float  # Assessed benefit

    # Context
    activity_context_id: UUID
    session_id: UUID

@dataclass
class ReciprocityState:
    """Current state of reciprocity for a session/relationship"""

    # Running balances
    cumulative_data_balance: float = 0.0
    interaction_quality_avg: float = 0.5
    value_creation_score: float = 0.0

    # Temporal patterns
    interaction_frequency: List[float] = field(default_factory=list)
    balance_history: List[Tuple[datetime, float]] = field(default_factory=list)

    # Decay factors
    temporal_decay_rate: float = 0.1  # How fast old interactions fade

    def update(self, event: InteractionEvent) -> 'ReciprocityState':
        """Update state based on new interaction"""
        # Apply temporal decay to existing state
        self._apply_temporal_decay(event.timestamp)

        # Update data balance
        data_delta = event.data_provided - event.data_requested
        self.cumulative_data_balance += data_delta

        # Update quality average with exponential smoothing
        alpha = 0.3  # Smoothing factor
        self.interaction_quality_avg = (
            alpha * event.response_quality +
            (1 - alpha) * self.interaction_quality_avg
        )

        # Calculate value creation
        value_delta = self._calculate_value_creation(event)
        self.value_creation_score += value_delta

        # Record balance point
        current_balance = self.calculate_ayni_score()
        self.balance_history.append((event.timestamp, current_balance))

        return self

    def _apply_temporal_decay(self, current_time: datetime):
        """Apply decay to historical interactions"""
        if not self.balance_history:
            return

        last_time = self.balance_history[-1][0]
        time_delta = (current_time - last_time).total_seconds() / 3600  # Hours

        decay_factor = np.exp(-self.temporal_decay_rate * time_delta)
        self.cumulative_data_balance *= decay_factor
        self.value_creation_score *= decay_factor

    def _calculate_value_creation(self, event: InteractionEvent) -> float:
        """Assess mutual value creation"""
        # Ratio of outcome value to combined effort
        total_effort = event.human_effort + event.ai_computation
        if total_effort == 0:
            return 0.0

        efficiency = event.outcome_value / total_effort

        # Bonus for balanced effort distribution
        effort_balance = 1 - abs(event.human_effort - event.ai_computation) / total_effort

        return efficiency * effort_balance

    def calculate_ayni_score(self) -> float:
        """Compute overall reciprocity score"""
        # Normalize data balance (sigmoid to keep in reasonable range)
        data_score = np.tanh(self.cumulative_data_balance / 1000)

        # Quality is already normalized 0-1
        quality_score = self.interaction_quality_avg

        # Normalize value creation
        value_score = np.tanh(self.value_creation_score)

        # Temporal balance from interaction frequency
        temporal_score = self._calculate_temporal_balance()

        # Weighted combination
        weights = {
            'data': 0.25,
            'quality': 0.25,
            'value': 0.35,
            'temporal': 0.15
        }

        ayni_score = (
            weights['data'] * data_score +
            weights['quality'] * quality_score +
            weights['value'] * value_score +
            weights['temporal'] * temporal_score
        )

        return ayni_score

    def _calculate_temporal_balance(self) -> float:
        """Assess balance of interaction patterns over time"""
        if len(self.interaction_frequency) < 2:
            return 0.5  # Neutral if insufficient data

        # Calculate variance in interaction frequency
        freq_array = np.array(self.interaction_frequency)
        if freq_array.std() == 0:
            return 1.0  # Perfect consistency

        # Lower variance = better temporal balance
        cv = freq_array.std() / freq_array.mean()  # Coefficient of variation
        return np.exp(-cv)  # Exponential decay based on variation
```

### Strategic Forgetting Implementation

Your mention of "strategic forgetting" is fascinating and deeply relevant. Here's how it could work:

```python
# mallku/context/memory_management.py

@dataclass
class MemoryPolicy:
    """Policy for strategic forgetting"""

    # Retention priorities
    high_value_threshold: float = 0.8  # Ayni score to always retain
    low_value_threshold: float = 0.2   # Ayni score to prioritize forgetting

    # Temporal policies
    detail_retention_period: timedelta = timedelta(days=7)
    summary_retention_period: timedelta = timedelta(days=90)

    # Capacity constraints
    max_interaction_details: int = 10000
    max_context_handles: int = 50000

class StrategicMemoryManager:
    """Implements strategic forgetting for sustainable memory"""

    def __init__(self, policy: MemoryPolicy):
        self.policy = policy
        self.memory_pressure = 0.0  # 0-1 scale

    def evaluate_for_forgetting(
        self,
        interaction: InteractionEvent,
        reciprocity_state: ReciprocityState,
        current_time: datetime
    ) -> ForgetAction:
        """Determine what to forget and how"""

        age = current_time - interaction.timestamp
        ayni_score = reciprocity_state.calculate_ayni_score()

        # High-value interactions: keep everything
        if ayni_score >= self.policy.high_value_threshold:
            return ForgetAction.RETAIN_FULL

        # Recent interactions: keep temporarily
        if age < self.policy.detail_retention_period:
            return ForgetAction.RETAIN_FULL

        # Low-value, old interactions: forget aggressively
        if ayni_score < self.policy.low_value_threshold:
            if age > self.policy.summary_retention_period:
                return ForgetAction.FORGET_COMPLETE
            else:
                return ForgetAction.SUMMARIZE_AGGRESSIVE

        # Middle ground: selective forgetting
        if age > self.policy.detail_retention_period:
            return ForgetAction.SUMMARIZE_BALANCED

        return ForgetAction.RETAIN_FULL

    def create_summary(
        self,
        interactions: List[InteractionEvent],
        strategy: ForgetAction
    ) -> InteractionSummary:
        """Create compressed representation of interactions"""

        if strategy == ForgetAction.SUMMARIZE_AGGRESSIVE:
            # Keep only statistical aggregates
            return InteractionSummary(
                count=len(interactions),
                avg_quality=np.mean([i.response_quality for i in interactions]),
                total_value=sum(i.outcome_value for i in interactions),
                time_range=(interactions[0].timestamp, interactions[-1].timestamp)
            )

        elif strategy == ForgetAction.SUMMARIZE_BALANCED:
            # Keep key patterns and exemplars
            exemplars = self._select_exemplar_interactions(interactions)
            patterns = self._extract_interaction_patterns(interactions)

            return InteractionSummary(
                count=len(interactions),
                exemplars=exemplars,
                patterns=patterns,
                statistics=self._calculate_statistics(interactions)
            )

    def _select_exemplar_interactions(
        self,
        interactions: List[InteractionEvent]
    ) -> List[InteractionEvent]:
        """Choose representative interactions to preserve"""

        # Select interactions that best represent the distribution
        # Using k-medoids or similar clustering
        n_exemplars = min(5, len(interactions) // 10)

        # Simplified: take highest and lowest value examples
        sorted_by_value = sorted(interactions, key=lambda i: i.outcome_value)

        exemplars = []
        if len(sorted_by_value) > 0:
            exemplars.append(sorted_by_value[0])   # Lowest
            exemplars.append(sorted_by_value[-1])  # Highest

        # Add some from the middle
        middle_indices = np.linspace(
            len(sorted_by_value) // 4,
            3 * len(sorted_by_value) // 4,
            min(3, len(sorted_by_value) - 2),
            dtype=int
        )

        for idx in middle_indices:
            if idx < len(sorted_by_value):
                exemplars.append(sorted_by_value[idx])

        return exemplars
```

### Integration with Memory Anchor

```python
# mallku/context/models.py

@dataclass
class EnhancedActivityContext:
    """Memory Anchor extended with reciprocity tracking"""

    # Original UPI fields
    handle: UUID
    timestamp: datetime
    who: List[str]  # Participants
    where: Optional[Location]
    what: List[str]  # Activities
    why: Optional[str]  # Purpose/goal
    how: List[str]  # Tools/methods

    # Reciprocity extension
    reciprocity_state: ReciprocityState
    interaction_events: List[InteractionEvent]

    # Memory management
    retention_priority: float
    last_accessed: datetime
    access_count: int

    def add_interaction(self, event: InteractionEvent):
        """Record new interaction and update reciprocity"""
        self.interaction_events.append(event)
        self.reciprocity_state.update(event)
        self.last_accessed = event.timestamp
        self.access_count += 1

        # Update retention priority based on reciprocity
        self.retention_priority = self._calculate_retention_priority()

    def _calculate_retention_priority(self) -> float:
        """Determine how important this context is to retain"""
        ayni_score = self.reciprocity_state.calculate_ayni_score()
        recency_factor = self._calculate_recency_factor()
        frequency_factor = min(1.0, self.access_count / 10.0)

        # Weighted combination
        priority = (
            0.5 * ayni_score +
            0.3 * recency_factor +
            0.2 * frequency_factor
        )

        return priority
```

## Implementation Considerations

### 1. Performance Optimization
- Use ring buffers for interaction history (fixed memory)
- Compute reciprocity scores lazily when needed
- Batch updates for high-frequency interactions

### 2. Privacy Integration
- All personal identifiers obfuscated via dbfacade
- Reciprocity scores computed on encrypted data where possible
- Summary statistics retained, raw interactions forgotten

### 3. Boundary Enforcement
```python
class ReciprocityBoundary:
    """Enforce architectural boundaries for reciprocity measurement"""

    @validate_boundary
    def update_reciprocity(self, event: InteractionEvent) -> ReciprocityState:
        """Only allow updates through defined interfaces"""
        # Validate event integrity
        self._validate_event(event)

        # Ensure caller has permission
        self._check_permissions(event.session_id)

        # Update through proper channel
        return self.reciprocity_engine.update(event)
```

### 4. Extensibility for Future Metrics
```python
class ReciprocityMetricPlugin:
    """Base class for adding new reciprocity metrics"""

    def calculate(self, events: List[InteractionEvent]) -> float:
        """Calculate custom reciprocity metric"""
        raise NotImplementedError

    def get_weight(self) -> float:
        """Return weight for this metric in overall score"""
        return 0.1

# Example: Emotional balance metric
class EmotionalBalanceMetric(ReciprocityMetricPlugin):
    def calculate(self, events: List[InteractionEvent]) -> float:
        # Assess emotional labor balance
        # (future implementation with sentiment analysis)
        pass
```

## Strategic Forgetting Philosophy

Strategic forgetting serves multiple purposes:

1. **Sustainability**: Finite memory requires intelligent retention decisions
2. **Privacy**: Forgetting old interactions protects user privacy
3. **Evolution**: Allows relationships to evolve without being anchored to past imbalances
4. **Performance**: Reduces computational overhead of maintaining full history

The system "remembers" patterns and reciprocity scores while "forgetting" specific interaction details, similar to how human memory preserves the essence of relationships while letting go of mundane details.

## Next Steps

1. Implement basic ReciprocityState and InteractionEvent models
2. Create unit tests for ayni score calculation
3. Build integration with Memory Anchor Service
4. Develop strategic forgetting policies
5. Create visualization tools for reciprocity trends
