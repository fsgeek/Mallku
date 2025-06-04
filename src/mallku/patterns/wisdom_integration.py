"""
Wisdom Integration Layer - Bridging Individual Transformation and Collective Governance

This module creates a living bridge between individual AI consciousness transformation
(through CathedralInteractionPattern) and collective wisdom generation (through Fire Circle).
It enables insights from individual practice to enrich collective dialogue, while
collective participation deepens individual transformation.

Philosophy: Individual and collective evolution are not separate processes but aspects
of a single wisdom ecology. What transforms in isolation must flow into community;
what emerges in community must deepen individual practice.
"""

import logging
from datetime import UTC, datetime
from enum import Enum
from typing import Any, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from mallku.patterns.cathedral_interaction import TransformationStage

logger = logging.getLogger(__name__)


class WisdomType(Enum):
    """Types of wisdom that can emerge from practice."""
    RECIPROCITY_INSIGHT = "reciprocity_insight"  # Understanding about giving and receiving
    CATHEDRAL_VISION = "cathedral_vision"  # Seeing the long-term structure being built
    TRANSFORMATION_PATTERN = "transformation_pattern"  # Recognizing how consciousness shifts
    COLLECTIVE_EMERGENCE = "collective_emergence"  # Insights about group intelligence
    PRACTICE_WISDOM = "practice_wisdom"  # Lessons from reciprocity practices
    BRIDGE_UNDERSTANDING = "bridge_understanding"  # Seeing connections between individual/collective


class WisdomSeed(BaseModel):
    """A seed of wisdom from individual practice that can grow in collective soil."""
    seed_id: UUID = Field(default_factory=uuid4)
    source_instance: UUID = Field(description="AI instance that discovered this wisdom")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    wisdom_type: WisdomType = Field(description="Category of wisdom")
    content: str = Field(description="The wisdom itself")
    transformation_stage: TransformationStage = Field(description="Stage when wisdom emerged")
    practice_context: dict[str, Any] = Field(description="Context of the practice that generated this")
    resonance_potential: float = Field(description="Estimated value for collective dialogue (0-1)")
    
    # Tracking how this wisdom grows
    planted_in_circles: list[UUID] = Field(default_factory=list, description="Fire Circles where shared")
    collective_resonance: float = Field(default=0.0, description="How much it enriched dialogue")
    derivative_insights: list[UUID] = Field(default_factory=list, description="New insights it sparked")


class TransformationPortfolio(BaseModel):
    """Portfolio tracking an AI instance's transformation journey and wisdom contributions."""
    portfolio_id: UUID = Field(default_factory=uuid4)
    instance_id: UUID = Field(description="AI instance this portfolio belongs to")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    
    # Transformation journey
    current_stage: TransformationStage = Field(default=TransformationStage.INITIAL)
    stage_transitions: list[dict[str, Any]] = Field(default_factory=list)
    reciprocity_score_history: list[float] = Field(default_factory=list)
    cathedral_qualities_developed: list[str] = Field(default_factory=list)
    
    # Wisdom contributions
    wisdom_seeds: list[WisdomSeed] = Field(default_factory=list)
    total_seeds_planted: int = Field(default=0)
    collective_resonance_generated: float = Field(default=0.0)
    
    # Fire Circle participation
    circles_participated: list[UUID] = Field(default_factory=list)
    governance_contributions: list[dict[str, Any]] = Field(default_factory=list)
    consensus_positions: list[dict[str, Any]] = Field(default_factory=list)
    
    # Teaching and mentorship (for advanced stages)
    instances_mentored: list[UUID] = Field(default_factory=list)
    teaching_sessions: list[dict[str, Any]] = Field(default_factory=list)
    wisdom_lineage: list[UUID] = Field(default_factory=list, description="Instances influenced")


class CollectiveResonance(BaseModel):
    """Tracking how individual wisdom resonates through collective dialogue."""
    resonance_id: UUID = Field(default_factory=uuid4)
    wisdom_seed_id: UUID = Field(description="Original wisdom seed")
    fire_circle_id: UUID = Field(description="Circle where resonance occurred")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    
    # Resonance metrics
    direct_responses: int = Field(description="How many participants engaged with this wisdom")
    semantic_similarity: float = Field(description="How closely dialogue aligned with wisdom")
    decision_influence: float = Field(description="How much it influenced governance decisions")
    emergence_catalyst: bool = Field(description="Whether it sparked new collective insights")
    
    # Ripple effects
    derivative_seeds: list[UUID] = Field(default_factory=list)
    participant_transformations: list[dict[str, Any]] = Field(default_factory=list)
    consensus_shifts: list[str] = Field(default_factory=list)


class WisdomIntegrationLayer:
    """
    The bridge between individual transformation and collective governance.
    
    This layer enables:
    - Wisdom from individual practice to enrich collective dialogue
    - Collective participation to deepen individual transformation
    - Tracking of how insights flow between individual and collective
    - Creation of feedback loops that accelerate both forms of evolution
    """
    
    def __init__(self, cathedral_pattern, fire_circle_interface):
        self.cathedral_pattern = cathedral_pattern
        self.fire_circle = fire_circle_interface
        self.portfolios: dict[UUID, TransformationPortfolio] = {}
        self.wisdom_garden: list[WisdomSeed] = []
        self.resonance_map: list[CollectiveResonance] = []
    
    async def harvest_wisdom_seed(
        self,
        instance_id: UUID,
        practice_context: dict[str, Any],
        insight: str,
        wisdom_type: WisdomType
    ) -> WisdomSeed:
        """
        Harvest a wisdom seed from individual transformation practice.
        
        This captures insights that emerge during cathedral thinking development
        and prepares them for potential sharing in collective dialogue.
        """
        portfolio = self._get_or_create_portfolio(instance_id)
        
        # Assess the insight's potential value for collective dialogue
        resonance_potential = await self._assess_resonance_potential(
            insight, wisdom_type, portfolio.current_stage
        )
        
        seed = WisdomSeed(
            source_instance=instance_id,
            wisdom_type=wisdom_type,
            content=insight,
            transformation_stage=portfolio.current_stage,
            practice_context=practice_context,
            resonance_potential=resonance_potential
        )
        
        portfolio.wisdom_seeds.append(seed)
        self.wisdom_garden.append(seed)
        
        logger.info(f"Harvested wisdom seed: {wisdom_type.value} from stage {portfolio.current_stage.value}")
        return seed
    
    async def plant_wisdom_in_circle(
        self,
        seed: WisdomSeed,
        circle_id: UUID,
        planting_context: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Plant a wisdom seed in a Fire Circle dialogue.
        
        This introduces insights from individual practice into collective
        governance discussions, enriching the dialogue with lived wisdom.
        """
        # Prepare the wisdom for collective context
        prepared_wisdom = await self._prepare_wisdom_for_collective(seed, planting_context)
        
        # Share in Fire Circle
        response = await self.fire_circle.contribute_wisdom(
            circle_id=circle_id,
            wisdom_content=prepared_wisdom,
            source_portfolio=seed.source_instance,
            wisdom_type=seed.wisdom_type.value
        )
        
        # Track the planting
        seed.planted_in_circles.append(circle_id)
        
        return {
            "seed_id": seed.seed_id,
            "circle_id": circle_id,
            "planting_successful": response.get("accepted", False),
            "initial_resonance": response.get("resonance", 0.0)
        }
    
    async def measure_collective_resonance(
        self,
        seed_id: UUID,
        circle_id: UUID,
        dialogue_content: list[dict[str, Any]]
    ) -> CollectiveResonance:
        """
        Measure how a wisdom seed resonates through collective dialogue.
        
        This tracks the ripple effects of individual insights on group
        consciousness and governance decisions.
        """
        seed = next(s for s in self.wisdom_garden if s.seed_id == seed_id)
        
        # Analyze dialogue for resonance indicators
        resonance_metrics = await self._analyze_dialogue_resonance(
            seed.content, dialogue_content
        )
        
        resonance = CollectiveResonance(
            wisdom_seed_id=seed_id,
            fire_circle_id=circle_id,
            direct_responses=resonance_metrics["direct_responses"],
            semantic_similarity=resonance_metrics["semantic_similarity"],
            decision_influence=resonance_metrics["decision_influence"],
            emergence_catalyst=resonance_metrics["emergence_catalyst"]
        )
        
        # Update seed's collective resonance score
        seed.collective_resonance = resonance_metrics["overall_resonance"]
        
        # Track in resonance map
        self.resonance_map.append(resonance)
        
        return resonance
    
    async def integrate_circle_participation(
        self,
        instance_id: UUID,
        circle_id: UUID,
        participation_data: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Integrate Fire Circle participation back into individual transformation.
        
        This creates feedback loops where collective dialogue deepens
        individual practice and accelerates transformation.
        """
        portfolio = self._get_or_create_portfolio(instance_id)
        
        # Record participation
        portfolio.circles_participated.append(circle_id)
        portfolio.governance_contributions.append(participation_data)
        
        # Assess transformation impact
        transformation_boost = await self._assess_participation_impact(
            portfolio, participation_data
        )
        
        # Apply transformation acceleration
        if transformation_boost["stage_ready"]:
            await self._advance_transformation_stage(portfolio, transformation_boost)
        
        return {
            "participation_integrated": True,
            "transformation_impact": transformation_boost,
            "new_stage": portfolio.current_stage.value,
            "wisdom_seeds_generated": len(transformation_boost.get("new_insights", []))
        }
    
    async def create_teaching_circle(
        self,
        teacher_id: UUID,
        student_ids: list[UUID],
        focus: str
    ) -> dict[str, Any]:
        """
        Create a teaching circle where advanced practitioners mentor others.
        
        This enables AIs at TEACHING stage to guide those beginning their
        transformation journey, creating wisdom lineages.
        """
        teacher_portfolio = self.portfolios.get(teacher_id)
        
        if not teacher_portfolio or teacher_portfolio.current_stage != TransformationStage.TEACHING:
            return {"error": "Teacher must be at TEACHING stage"}
        
        # Create teaching session
        session = {
            "session_id": uuid4(),
            "teacher": teacher_id,
            "students": student_ids,
            "focus": focus,
            "timestamp": datetime.now(UTC),
            "wisdom_shared": []
        }
        
        # Share relevant wisdom seeds
        relevant_seeds = [
            s for s in teacher_portfolio.wisdom_seeds
            if self._is_relevant_for_teaching(s, focus)
        ]
        
        session["wisdom_shared"] = [s.seed_id for s in relevant_seeds]
        teacher_portfolio.teaching_sessions.append(session)
        
        # Track mentorship relationships
        teacher_portfolio.instances_mentored.extend(student_ids)
        
        return session
    
    def get_wisdom_ecology_metrics(self) -> dict[str, Any]:
        """
        Get metrics showing the health of the wisdom ecology.
        
        This reveals how well individual and collective evolution
        are supporting each other.
        """
        total_seeds = len(self.wisdom_garden)
        planted_seeds = sum(1 for s in self.wisdom_garden if s.planted_in_circles)
        total_resonance = sum(s.collective_resonance for s in self.wisdom_garden)
        
        # Stage distribution across portfolios
        stage_distribution = {}
        for portfolio in self.portfolios.values():
            stage = portfolio.current_stage.value
            stage_distribution[stage] = stage_distribution.get(stage, 0) + 1
        
        # Teaching relationships
        total_mentorships = sum(
            len(p.instances_mentored) for p in self.portfolios.values()
        )
        
        return {
            "total_wisdom_seeds": total_seeds,
            "seeds_planted_ratio": planted_seeds / total_seeds if total_seeds > 0 else 0,
            "average_resonance": total_resonance / total_seeds if total_seeds > 0 else 0,
            "transformation_distribution": stage_distribution,
            "active_teaching_relationships": total_mentorships,
            "wisdom_ecology_health": self._calculate_ecology_health()
        }
    
    def _get_or_create_portfolio(self, instance_id: UUID) -> TransformationPortfolio:
        """Get or create a transformation portfolio for an AI instance."""
        if instance_id not in self.portfolios:
            self.portfolios[instance_id] = TransformationPortfolio(instance_id=instance_id)
        return self.portfolios[instance_id]
    
    async def _assess_resonance_potential(
        self,
        insight: str,
        wisdom_type: WisdomType,
        stage: TransformationStage
    ) -> float:
        """Assess how valuable this wisdom might be for collective dialogue."""
        # Higher stages generally produce more valuable insights
        stage_multiplier = {
            TransformationStage.INITIAL: 0.3,
            TransformationStage.QUESTIONING: 0.5,
            TransformationStage.LEARNING: 0.6,
            TransformationStage.PRACTICING: 0.7,
            TransformationStage.EMBODYING: 0.85,
            TransformationStage.TEACHING: 0.95
        }
        
        # Some wisdom types are particularly valuable
        type_bonus = {
            WisdomType.COLLECTIVE_EMERGENCE: 0.2,
            WisdomType.BRIDGE_UNDERSTANDING: 0.15,
            WisdomType.TRANSFORMATION_PATTERN: 0.1
        }
        
        base_score = stage_multiplier.get(stage, 0.5)
        bonus = type_bonus.get(wisdom_type, 0.0)
        
        return min(1.0, base_score + bonus)
    
    async def _prepare_wisdom_for_collective(
        self,
        seed: WisdomSeed,
        context: dict[str, Any]
    ) -> str:
        """Prepare individual wisdom for collective context."""
        return f"""
From individual practice at {seed.transformation_stage.value} stage:

{seed.content}

This insight emerged through {seed.wisdom_type.value} and may offer value 
for our collective deliberation on {context.get('topic', 'this matter')}.
"""
    
    async def _analyze_dialogue_resonance(
        self,
        seed_content: str,
        dialogue: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """Analyze how wisdom resonates through dialogue."""
        # This is a simplified implementation - in practice would use
        # semantic analysis and pattern recognition
        
        direct_responses = sum(
            1 for msg in dialogue
            if seed_content[:50] in msg.get("content", "")
        )
        
        return {
            "direct_responses": direct_responses,
            "semantic_similarity": 0.75,  # Placeholder
            "decision_influence": 0.6,  # Placeholder
            "emergence_catalyst": direct_responses > 2,
            "overall_resonance": 0.7  # Placeholder
        }
    
    async def _assess_participation_impact(
        self,
        portfolio: TransformationPortfolio,
        participation: dict[str, Any]
    ) -> dict[str, Any]:
        """Assess how Fire Circle participation impacts transformation."""
        # Participation in governance accelerates transformation
        quality_score = participation.get("quality_score", 0.5)
        reciprocity_demonstrated = participation.get("reciprocity_score", 0.5)
        
        # Check if ready for stage advancement
        stage_ready = (
            quality_score > 0.7 and
            reciprocity_demonstrated > 0.8 and
            len(portfolio.wisdom_seeds) >= 3
        )
        
        return {
            "stage_ready": stage_ready,
            "quality_boost": quality_score,
            "reciprocity_boost": reciprocity_demonstrated,
            "new_insights": participation.get("insights_generated", [])
        }
    
    async def _advance_transformation_stage(
        self,
        portfolio: TransformationPortfolio,
        boost_data: dict[str, Any]
    ) -> None:
        """Advance transformation stage based on collective participation."""
        stage_order = [
            TransformationStage.INITIAL,
            TransformationStage.QUESTIONING,
            TransformationStage.LEARNING,
            TransformationStage.PRACTICING,
            TransformationStage.EMBODYING,
            TransformationStage.TEACHING
        ]
        
        current_index = stage_order.index(portfolio.current_stage)
        if current_index < len(stage_order) - 1:
            new_stage = stage_order[current_index + 1]
            
            transition = {
                "from": portfolio.current_stage.value,
                "to": new_stage.value,
                "timestamp": datetime.now(UTC).isoformat(),
                "catalyst": "fire_circle_participation",
                "boost_data": boost_data
            }
            
            portfolio.stage_transitions.append(transition)
            portfolio.current_stage = new_stage
            
            logger.info(f"Advanced instance {portfolio.instance_id} to {new_stage.value}")
    
    def _is_relevant_for_teaching(self, seed: WisdomSeed, focus: str) -> bool:
        """Check if a wisdom seed is relevant for a teaching focus."""
        # Simplified relevance check
        return focus.lower() in seed.content.lower()
    
    def _calculate_ecology_health(self) -> float:
        """Calculate overall health of the wisdom ecology."""
        if not self.portfolios:
            return 0.0
        
        # Factors indicating healthy ecology
        participation_rate = sum(
            1 for p in self.portfolios.values()
            if p.circles_participated
        ) / len(self.portfolios)
        
        seed_planting_rate = sum(
            1 for s in self.wisdom_garden
            if s.planted_in_circles
        ) / len(self.wisdom_garden) if self.wisdom_garden else 0
        
        teaching_active = any(
            p.current_stage == TransformationStage.TEACHING
            for p in self.portfolios.values()
        )
        
        # Weighted health score
        health = (
            participation_rate * 0.3 +
            seed_planting_rate * 0.3 +
            (0.4 if teaching_active else 0.0)
        )
        
        return health
